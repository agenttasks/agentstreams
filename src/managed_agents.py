"""Managed Agents API client for AgentStreams.

Wraps the Anthropic SDK's beta.agents, beta.environments, beta.sessions,
and beta.sessions.events namespaces into typed Python dataclasses with
convenience methods for the full agent lifecycle:

    Agent (create/update/archive/versions)
    → Environment (create/configure networking & packages)
    → Session (create/stream/interrupt/archive/delete)
    → Events (send user messages, handle custom tools, stream SSE)

Architecture follows the Anthropic Managed Agents design:
    - Brain: stateless harness (Claude + system prompt + tools)
    - Hands: cloud containers with bash, file ops, web access
    - Session: append-only event log for recovery and context

Beta header: managed-agents-2026-04-01 (set automatically by the SDK).

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import anthropic

# ── Enums ──────────────────────────────────────────────────────


class SessionStatus(Enum):
    """Session lifecycle status."""

    IDLE = "idle"
    RUNNING = "running"
    RESCHEDULING = "rescheduling"
    TERMINATED = "terminated"


class NetworkingMode(Enum):
    """Container networking mode."""

    UNRESTRICTED = "unrestricted"
    LIMITED = "limited"


class ToolPermission(Enum):
    """Tool permission policy."""

    ALWAYS_ALLOW = "always_allow"
    ALWAYS_ASK = "always_ask"


class StopReason(Enum):
    """Why the agent went idle."""

    END_TURN = "end_turn"
    MAX_TOKENS = "max_tokens"
    TOOL_CONFIRMATION = "tool_confirmation"
    CUSTOM_TOOL_USE = "custom_tool_use"
    INTERRUPT = "interrupt"


# ── Tool Configuration ────────────────────────────────────────


AGENT_TOOLS = (
    "bash",
    "read",
    "write",
    "edit",
    "glob",
    "grep",
    "web_fetch",
    "web_search",
)


@dataclass
class ToolConfig:
    """Per-tool enable/disable and permission override.

    Maps to the configs array inside agent_toolset_20260401.
    """

    name: str
    enabled: bool = True
    permission_policy: ToolPermission = ToolPermission.ALWAYS_ALLOW

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"name": self.name, "enabled": self.enabled}
        if self.permission_policy != ToolPermission.ALWAYS_ALLOW:
            result["permission_policy"] = {"type": self.permission_policy.value}
        return result


@dataclass
class CustomTool:
    """User-defined custom tool that the agent can invoke.

    Your application executes these tools and sends results back
    via user.custom_tool_result events.
    """

    name: str
    description: str
    input_schema: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "custom",
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }


@dataclass
class MCPServer:
    """Remote MCP server declaration for the agent."""

    name: str
    url: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "url", "name": self.name, "url": self.url}


@dataclass
class MCPToolset:
    """MCP toolset reference, linking an MCP server's tools to the agent."""

    mcp_server_name: str
    configs: list[ToolConfig] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "mcp_toolset",
            "mcp_server_name": self.mcp_server_name,
        }
        if self.configs:
            result["configs"] = [c.to_dict() for c in self.configs]
        return result


# ── Agent Definition ──────────────────────────────────────────


@dataclass
class AgentToolset:
    """Built-in agent toolset configuration.

    The agent_toolset_20260401 enables bash, file ops, web search, etc.
    Use configs to disable specific tools or override permissions.
    Use default_config to flip the default (e.g., all off, then enable specific).
    """

    configs: list[ToolConfig] = field(default_factory=list)
    default_enabled: bool | None = None
    default_permission: ToolPermission | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"type": "agent_toolset_20260401"}
        if self.configs:
            result["configs"] = [c.to_dict() for c in self.configs]
        if self.default_enabled is not None or self.default_permission is not None:
            default_config: dict[str, Any] = {}
            if self.default_enabled is not None:
                default_config["enabled"] = self.default_enabled
            if self.default_permission is not None:
                default_config["permission_policy"] = {
                    "type": self.default_permission.value,
                }
            result["default_config"] = default_config
        return result


@dataclass
class ManagedAgentConfig:
    """Full agent configuration for the Managed Agents API.

    Bundles model, system prompt, tools, MCP servers, and metadata.
    Create once, reference by ID across sessions.
    """

    name: str
    model: str = "claude-sonnet-4-6"
    system: str = ""
    description: str = ""
    toolset: AgentToolset = field(default_factory=AgentToolset)
    custom_tools: list[CustomTool] = field(default_factory=list)
    mcp_servers: list[MCPServer] = field(default_factory=list)
    mcp_toolsets: list[MCPToolset] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    fast_mode: bool = False

    def _build_tools(self) -> list[dict[str, Any]]:
        tools: list[dict[str, Any]] = [self.toolset.to_dict()]
        for ct in self.custom_tools:
            tools.append(ct.to_dict())
        for mt in self.mcp_toolsets:
            tools.append(mt.to_dict())
        return tools

    def _build_model(self) -> str | dict[str, str]:
        if self.fast_mode:
            return {"id": self.model, "speed": "fast"}
        return self.model

    def to_create_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {
            "name": self.name,
            "model": self._build_model(),
            "tools": self._build_tools(),
        }
        if self.system:
            params["system"] = self.system
        if self.description:
            params["description"] = self.description
        if self.mcp_servers:
            params["mcp_servers"] = [s.to_dict() for s in self.mcp_servers]
        if self.metadata:
            params["metadata"] = self.metadata
        return params


# ── Environment Configuration ─────────────────────────────────


@dataclass
class NetworkConfig:
    """Container networking configuration."""

    mode: NetworkingMode = NetworkingMode.UNRESTRICTED
    allowed_hosts: list[str] = field(default_factory=list)
    allow_mcp_servers: bool = False
    allow_package_managers: bool = False

    def to_dict(self) -> dict[str, Any]:
        if self.mode == NetworkingMode.UNRESTRICTED:
            return {"type": "unrestricted"}
        return {
            "type": "limited",
            "allowed_hosts": self.allowed_hosts,
            "allow_mcp_servers": self.allow_mcp_servers,
            "allow_package_managers": self.allow_package_managers,
        }


@dataclass
class Packages:
    """Pre-installed packages for the container.

    Supported managers: apt, cargo, gem, go, npm, pip.
    """

    apt: list[str] = field(default_factory=list)
    cargo: list[str] = field(default_factory=list)
    gem: list[str] = field(default_factory=list)
    go: list[str] = field(default_factory=list)
    npm: list[str] = field(default_factory=list)
    pip: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for mgr in ("apt", "cargo", "gem", "go", "npm", "pip"):
            pkgs = getattr(self, mgr)
            if pkgs:
                result[mgr] = pkgs
        return result


@dataclass
class EnvironmentConfig:
    """Environment (container template) configuration."""

    name: str
    networking: NetworkConfig = field(default_factory=NetworkConfig)
    packages: Packages = field(default_factory=Packages)
    metadata: dict[str, str] = field(default_factory=dict)

    def to_create_params(self) -> dict[str, Any]:
        config: dict[str, Any] = {
            "type": "cloud",
            "networking": self.networking.to_dict(),
        }
        pkgs = self.packages.to_dict()
        if pkgs:
            config["packages"] = pkgs
        params: dict[str, Any] = {"name": self.name, "config": config}
        if self.metadata:
            params["metadata"] = self.metadata
        return params


# ── Session Resources ─────────────────────────────────────────


@dataclass
class GitHubResource:
    """Mount a GitHub repository into the session container."""

    url: str
    authorization_token: str = ""
    branch: str = ""
    commit_sha: str = ""
    mount_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"type": "github_repository", "url": self.url}
        if self.authorization_token:
            result["authorization_token"] = self.authorization_token
        if self.branch:
            result["checkout"] = {"type": "branch", "name": self.branch}
        elif self.commit_sha:
            result["checkout"] = {"type": "commit", "sha": self.commit_sha}
        if self.mount_path:
            result["mount_path"] = self.mount_path
        return result


@dataclass
class FileResource:
    """Mount a file into the session container."""

    file_id: str
    mount_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"type": "file", "file_id": self.file_id}
        if self.mount_path:
            result["mount_path"] = self.mount_path
        return result


# ── Event Types ───────────────────────────────────────────────


@dataclass
class TextContent:
    """Text content block for messages."""

    text: str

    def to_dict(self) -> dict[str, str]:
        return {"type": "text", "text": self.text}


@dataclass
class UserMessage:
    """User message event to send to the agent."""

    content: list[TextContent]

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "user.message",
            "content": [c.to_dict() for c in self.content],
        }

    @classmethod
    def from_text(cls, text: str) -> UserMessage:
        return cls(content=[TextContent(text=text)])


@dataclass
class UserInterrupt:
    """Interrupt event to stop the agent mid-execution."""

    def to_dict(self) -> dict[str, str]:
        return {"type": "user.interrupt"}


@dataclass
class ToolConfirmation:
    """Approve or deny a tool call that requires permission."""

    tool_use_id: str
    result: str  # "allow" or "deny"
    deny_message: str = ""

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "type": "user.tool_confirmation",
            "tool_use_id": self.tool_use_id,
            "result": self.result,
        }
        if self.deny_message:
            d["deny_message"] = self.deny_message
        return d


@dataclass
class CustomToolResult:
    """Result of a custom tool execution, sent back to the agent."""

    custom_tool_use_id: str
    content: list[TextContent]
    is_error: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "user.custom_tool_result",
            "custom_tool_use_id": self.custom_tool_use_id,
            "content": [c.to_dict() for c in self.content],
            "is_error": self.is_error,
        }


# ── Parsed Event Wrappers ────────────────────────────────────


@dataclass
class AgentMessageEvent:
    """Parsed agent.message event."""

    id: str
    text: str
    raw: dict[str, Any]


@dataclass
class AgentToolUseEvent:
    """Parsed agent.tool_use event."""

    id: str
    name: str
    input: dict[str, Any]
    raw: dict[str, Any]


@dataclass
class AgentCustomToolUseEvent:
    """Parsed agent.custom_tool_use event — requires your response."""

    id: str
    name: str
    input: dict[str, Any]
    raw: dict[str, Any]


@dataclass
class SessionStatusEvent:
    """Parsed session status event (idle, running, rescheduled, terminated)."""

    status: SessionStatus
    stop_reason: str
    raw: dict[str, Any]


@dataclass
class SessionErrorEvent:
    """Parsed session.error event."""

    error_type: str
    message: str
    raw: dict[str, Any]


@dataclass
class SpanEvent:
    """Parsed span event for observability."""

    span_type: str
    raw: dict[str, Any]


@dataclass
class GenericEvent:
    """Fallback for unrecognized event types."""

    event_type: str
    raw: dict[str, Any]


# Union of all parsed event types
ManagedAgentEvent = (
    AgentMessageEvent
    | AgentToolUseEvent
    | AgentCustomToolUseEvent
    | SessionStatusEvent
    | SessionErrorEvent
    | SpanEvent
    | GenericEvent
)


def parse_event(raw: dict[str, Any]) -> ManagedAgentEvent:
    """Parse a raw SSE event dict into a typed wrapper."""
    event_type = raw.get("type", "")

    if event_type == "agent.message":
        text_parts = []
        for block in raw.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
        return AgentMessageEvent(
            id=raw.get("id", ""),
            text="".join(text_parts),
            raw=raw,
        )

    if event_type == "agent.tool_use":
        return AgentToolUseEvent(
            id=raw.get("id", ""),
            name=raw.get("name", ""),
            input=raw.get("input", {}),
            raw=raw,
        )

    if event_type == "agent.custom_tool_use":
        return AgentCustomToolUseEvent(
            id=raw.get("id", ""),
            name=raw.get("name", ""),
            input=raw.get("input", {}),
            raw=raw,
        )

    if event_type.startswith("session.status_"):
        status_str = event_type.removeprefix("session.status_")
        try:
            status = SessionStatus(status_str)
        except ValueError:
            status = SessionStatus.IDLE
        return SessionStatusEvent(
            status=status,
            stop_reason=raw.get("stop_reason", ""),
            raw=raw,
        )

    if event_type == "session.error":
        error = raw.get("error", {})
        return SessionErrorEvent(
            error_type=error.get("type", ""),
            message=error.get("message", ""),
            raw=raw,
        )

    if event_type.startswith("span."):
        return SpanEvent(span_type=event_type, raw=raw)

    return GenericEvent(event_type=event_type, raw=raw)


# ── Client ────────────────────────────────────────────────────


class ManagedAgentsClient:
    """High-level client for the Anthropic Managed Agents API.

    Wraps the SDK beta namespace with typed dataclasses and convenience
    methods for the full agent lifecycle. All methods use the
    managed-agents-2026-04-01 beta header automatically.

    Usage:
        client = ManagedAgentsClient()

        # Create reusable agent + environment
        agent_id = client.create_agent(ManagedAgentConfig(
            name="Coding Assistant",
            model="claude-sonnet-4-6",
            system="You are a helpful coding agent.",
        ))
        env_id = client.create_environment(EnvironmentConfig(
            name="python-dev",
            packages=Packages(pip=["pandas", "numpy"]),
        ))

        # Start a session and stream events
        session_id = client.create_session(agent_id, env_id)
        client.send_message(session_id, "Write a fibonacci script")
        for event in client.stream_events(session_id):
            if isinstance(event, AgentMessageEvent):
                print(event.text, end="")
            elif isinstance(event, SessionStatusEvent):
                if event.status == SessionStatus.IDLE:
                    break
    """

    def __init__(self, *, api_key: str = ""):
        key = api_key or os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
        if key:
            self._client = anthropic.Anthropic(api_key=key)
        else:
            self._client = anthropic.Anthropic()

    @property
    def sdk(self) -> anthropic.Anthropic:
        """Access the underlying Anthropic SDK client."""
        return self._client

    # ── Agents ─────────────────────────────────────────────

    def create_agent(self, config: ManagedAgentConfig) -> str:
        """Create a managed agent and return its ID."""
        params = config.to_create_params()
        result = self._client.beta.agents.create(**params)
        return result.id

    def retrieve_agent(self, agent_id: str) -> dict[str, Any]:
        """Retrieve agent details."""
        result = self._client.beta.agents.retrieve(agent_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def update_agent(
        self,
        agent_id: str,
        version: int,
        **updates: Any,
    ) -> dict[str, Any]:
        """Update an agent (creates a new version).

        Pass the current version for optimistic concurrency.
        Only include fields you want to change.
        """
        result = self._client.beta.agents.update(agent_id, version=version, **updates)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def archive_agent(self, agent_id: str) -> dict[str, Any]:
        """Archive an agent (read-only, no new sessions)."""
        result = self._client.beta.agents.archive(agent_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def list_agents(self, **kwargs: Any) -> list[dict[str, Any]]:
        """List all agents."""
        result = self._client.beta.agents.list(**kwargs)
        return [item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in result]

    def list_agent_versions(self, agent_id: str) -> list[dict[str, Any]]:
        """List all versions of an agent."""
        result = self._client.beta.agents.versions.list(agent_id)
        return [item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in result]

    # ── Environments ───────────────────────────────────────

    def create_environment(self, config: EnvironmentConfig) -> str:
        """Create a cloud environment and return its ID."""
        params = config.to_create_params()
        result = self._client.beta.environments.create(**params)
        return result.id

    def retrieve_environment(self, env_id: str) -> dict[str, Any]:
        """Retrieve environment details."""
        result = self._client.beta.environments.retrieve(env_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def update_environment(self, env_id: str, **updates: Any) -> dict[str, Any]:
        """Update an environment configuration."""
        result = self._client.beta.environments.update(env_id, **updates)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def archive_environment(self, env_id: str) -> dict[str, Any]:
        """Archive an environment (read-only, existing sessions continue)."""
        result = self._client.beta.environments.archive(env_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def delete_environment(self, env_id: str) -> dict[str, Any]:
        """Delete an environment (only if no sessions reference it)."""
        result = self._client.beta.environments.delete(env_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def list_environments(self, **kwargs: Any) -> list[dict[str, Any]]:
        """List all environments."""
        result = self._client.beta.environments.list(**kwargs)
        return [item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in result]

    # ── Sessions ───────────────────────────────────────────

    def create_session(
        self,
        agent_id: str,
        environment_id: str,
        *,
        title: str = "",
        agent_version: int | None = None,
        resources: list[GitHubResource | FileResource] | None = None,
        vault_ids: list[str] | None = None,
        metadata: dict[str, str] | None = None,
    ) -> str:
        """Create a session and return its ID.

        Pass agent_version to pin to a specific agent version.
        """
        agent_param: str | dict[str, Any]
        if agent_version is not None:
            agent_param = {
                "type": "agent",
                "id": agent_id,
                "version": agent_version,
            }
        else:
            agent_param = agent_id

        params: dict[str, Any] = {
            "agent": agent_param,
            "environment_id": environment_id,
        }
        if title:
            params["title"] = title
        if resources:
            params["resources"] = [r.to_dict() for r in resources]
        if vault_ids:
            params["vault_ids"] = vault_ids
        if metadata:
            params["metadata"] = metadata

        result = self._client.beta.sessions.create(**params)
        return result.id

    def retrieve_session(self, session_id: str) -> dict[str, Any]:
        """Retrieve session details including status and usage."""
        result = self._client.beta.sessions.retrieve(session_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def update_session(
        self,
        session_id: str,
        *,
        title: str = "",
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update session title and/or metadata."""
        params: dict[str, Any] = {}
        if title:
            params["title"] = title
        if metadata is not None:
            params["metadata"] = metadata
        result = self._client.beta.sessions.update(session_id, **params)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def archive_session(self, session_id: str) -> dict[str, Any]:
        """Archive a session (preserves history, blocks new events)."""
        result = self._client.beta.sessions.archive(session_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def delete_session(self, session_id: str) -> dict[str, Any]:
        """Permanently delete a session and its container."""
        result = self._client.beta.sessions.delete(session_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

    def list_sessions(self, **kwargs: Any) -> list[dict[str, Any]]:
        """List sessions with optional filtering."""
        result = self._client.beta.sessions.list(**kwargs)
        return [item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in result]

    # ── Events ─────────────────────────────────────────────

    def send_events(
        self,
        session_id: str,
        events: list[UserMessage | UserInterrupt | ToolConfirmation | CustomToolResult],
    ) -> None:
        """Send one or more user events to a session."""
        self._client.beta.sessions.events.send(
            session_id,
            events=[e.to_dict() for e in events],
        )

    def send_message(self, session_id: str, text: str) -> None:
        """Convenience: send a single text message to a session."""
        self.send_events(session_id, [UserMessage.from_text(text)])

    def send_interrupt(self, session_id: str) -> None:
        """Send an interrupt to stop the agent mid-execution."""
        self.send_events(session_id, [UserInterrupt()])

    def send_tool_confirmation(
        self,
        session_id: str,
        tool_use_id: str,
        *,
        allow: bool = True,
        deny_message: str = "",
    ) -> None:
        """Approve or deny a tool call that requires permission."""
        result = "allow" if allow else "deny"
        self.send_events(
            session_id,
            [ToolConfirmation(tool_use_id=tool_use_id, result=result, deny_message=deny_message)],
        )

    def send_custom_tool_result(
        self,
        session_id: str,
        tool_use_id: str,
        text: str,
        *,
        is_error: bool = False,
    ) -> None:
        """Send the result of a custom tool execution."""
        self.send_events(
            session_id,
            [
                CustomToolResult(
                    custom_tool_use_id=tool_use_id,
                    content=[TextContent(text=text)],
                    is_error=is_error,
                )
            ],
        )

    def list_events(
        self,
        session_id: str,
        *,
        limit: int | None = None,
        order: str = "asc",
    ) -> list[dict[str, Any]]:
        """List all events for a session."""
        params: dict[str, Any] = {"order": order}
        if limit is not None:
            params["limit"] = limit
        result = self._client.beta.sessions.events.list(session_id, **params)
        return [
            item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in result.data
        ]

    def stream_events(self, session_id: str) -> Iterator[ManagedAgentEvent]:
        """Open an SSE stream and yield parsed events.

        Usage:
            for event in client.stream_events(session_id):
                match event:
                    case AgentMessageEvent():
                        print(event.text, end="")
                    case AgentToolUseEvent():
                        print(f"[Using tool: {event.name}]")
                    case SessionStatusEvent(status=SessionStatus.IDLE):
                        break
        """
        with self._client.beta.sessions.events.stream(session_id) as stream:
            for raw_event in stream:
                raw = (
                    raw_event.model_dump() if hasattr(raw_event, "model_dump") else dict(raw_event)
                )
                yield parse_event(raw)

    # ── Custom Tool Loop ──────────────────────────────────

    def run_with_custom_tools(
        self,
        session_id: str,
        message: str,
        tool_handlers: dict[str, Any],
    ) -> list[ManagedAgentEvent]:
        """Send a message and handle custom tool calls until idle.

        tool_handlers maps tool names to callables:
            {"get_weather": lambda input: f"72°F in {input['location']}"}

        The loop:
        1. Send user message
        2. Stream events
        3. On agent.custom_tool_use: call handler, send result
        4. On session.status_idle: return collected events
        """
        self.send_message(session_id, message)
        collected: list[ManagedAgentEvent] = []

        while True:
            for event in self.stream_events(session_id):
                collected.append(event)

                if isinstance(event, AgentCustomToolUseEvent):
                    handler = tool_handlers.get(event.name)
                    if handler:
                        try:
                            result_text = str(handler(event.input))
                            self.send_custom_tool_result(session_id, event.id, result_text)
                        except Exception as exc:
                            self.send_custom_tool_result(
                                session_id,
                                event.id,
                                str(exc),
                                is_error=True,
                            )
                    else:
                        self.send_custom_tool_result(
                            session_id,
                            event.id,
                            f"Unknown tool: {event.name}",
                            is_error=True,
                        )

                elif isinstance(event, SessionStatusEvent):
                    if event.status == SessionStatus.IDLE:
                        return collected
                    if event.status == SessionStatus.TERMINATED:
                        return collected

        return collected  # unreachable but keeps type checker happy


# ── Factory Functions ─────────────────────────────────────────


def coding_agent(
    name: str = "Coding Assistant",
    model: str = "claude-sonnet-4-6",
    system: str = "You are a helpful coding assistant. Write clean, well-documented code.",
    *,
    disable_web: bool = False,
) -> ManagedAgentConfig:
    """Pre-configured coding agent with full toolset.

    Set disable_web=True to block web_fetch and web_search.
    """
    configs = []
    if disable_web:
        configs = [
            ToolConfig(name="web_fetch", enabled=False),
            ToolConfig(name="web_search", enabled=False),
        ]
    return ManagedAgentConfig(
        name=name,
        model=model,
        system=system,
        toolset=AgentToolset(configs=configs),
    )


def security_agent(
    name: str = "Security Auditor",
    model: str = "claude-opus-4-6",
) -> ManagedAgentConfig:
    """Pre-configured security audit agent (read-only tools)."""
    return ManagedAgentConfig(
        name=name,
        model=model,
        system=(
            "You are a security auditor. Scan for injection flaws, "
            "hard-coded secrets, unsafe eval/exec, prompt injection vectors, "
            "and dependency vulnerabilities. Do NOT modify any files. "
            "Report findings with severity and recommendation. "
            "End with verdict: PASS, NEEDS_REMEDIATION, or BLOCK."
        ),
        toolset=AgentToolset(
            default_enabled=False,
            configs=[
                ToolConfig(name="bash", enabled=True),
                ToolConfig(name="read", enabled=True),
                ToolConfig(name="glob", enabled=True),
                ToolConfig(name="grep", enabled=True),
            ],
        ),
    )


def data_analysis_env(
    name: str = "data-analysis",
    pip_packages: list[str] | None = None,
    npm_packages: list[str] | None = None,
) -> EnvironmentConfig:
    """Pre-configured environment with data science packages."""
    return EnvironmentConfig(
        name=name,
        packages=Packages(
            pip=pip_packages or ["pandas", "numpy", "scikit-learn", "matplotlib"],
            npm=npm_packages or [],
        ),
        networking=NetworkConfig(mode=NetworkingMode.UNRESTRICTED),
    )


def restricted_env(
    name: str = "restricted",
    allowed_hosts: list[str] | None = None,
) -> EnvironmentConfig:
    """Pre-configured environment with limited networking."""
    return EnvironmentConfig(
        name=name,
        networking=NetworkConfig(
            mode=NetworkingMode.LIMITED,
            allowed_hosts=allowed_hosts or [],
            allow_package_managers=True,
        ),
    )
