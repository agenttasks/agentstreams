"""Pydantic 2.0 data models for Claude Agent SDK and MCP SDK type tracking.

Pydantic 3.0-prepared: uses ConfigDict, model_validator, field_validator
(not deprecated class Config or @validator). All models use strict mode
where appropriate and frozen immutability for version-tracking types.

Tracks upstream SDK versions with semver constraints. Version bumps follow
conventional-commits + release-please:
  - feat(sdk): bump → minor version
  - fix(sdk): patch → patch version
  - feat(sdk)!: breaking → major version

Upstream dependencies tracked:
  - claude-code-sdk (anthropic-ai/claude-agent-sdk-python) >= 0.1.53
  - mcp (modelcontextprotocol/python-sdk) >= 1.26.0
  - anthropic (anthropic-sdk-python) >= 0.42.0

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum, StrEnum
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

# ── Semver ────────────────────────────────────────────────────

SEMVER_PATTERN = r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9.]+)?(?:\+[a-zA-Z0-9.]+)?$"
SemverStr = Annotated[str, StringConstraints(pattern=SEMVER_PATTERN)]


class SemverVersion(BaseModel):
    """Semantic version with comparison support.

    Pydantic 3.0 note: when Pydantic 3.0 ships, replace with
    `model_config = ConfigDict(frozen=True, strict=True)` and
    native __hash__ support.
    """

    model_config = ConfigDict(frozen=True)

    major: int = Field(ge=0)
    minor: int = Field(ge=0)
    patch: int = Field(ge=0)
    prerelease: str = ""
    build_metadata: str = ""

    @classmethod
    def parse(cls, version_str: str) -> SemverVersion:
        """Parse a semver string like '1.26.0' or '0.1.53-beta.1'."""
        match = re.match(
            r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+([a-zA-Z0-9.]+))?$",
            version_str.strip().lstrip("v"),
        )
        if not match:
            raise ValueError(f"Invalid semver: {version_str}")
        return cls(
            major=int(match.group(1)),
            minor=int(match.group(2)),
            patch=int(match.group(3)),
            prerelease=match.group(4) or "",
            build_metadata=match.group(5) or "",
        )

    def __str__(self) -> str:
        v = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            v += f"-{self.prerelease}"
        if self.build_metadata:
            v += f"+{self.build_metadata}"
        return v

    def bump_major(self) -> SemverVersion:
        return SemverVersion(major=self.major + 1, minor=0, patch=0)

    def bump_minor(self) -> SemverVersion:
        return SemverVersion(major=self.major, minor=self.minor + 1, patch=0)

    def bump_patch(self) -> SemverVersion:
        return SemverVersion(major=self.major, minor=self.minor, patch=self.patch + 1)

    def _tuple(self) -> tuple[int, int, int, str]:
        return (self.major, self.minor, self.patch, self.prerelease)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemverVersion):
            return NotImplemented
        return self._tuple() < other._tuple()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, SemverVersion):
            return NotImplemented
        return self._tuple() <= other._tuple()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, SemverVersion):
            return NotImplemented
        return self._tuple() > other._tuple()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, SemverVersion):
            return NotImplemented
        return self._tuple() >= other._tuple()

    def satisfies(self, constraint: str) -> bool:
        """Check if this version satisfies a pip-style constraint like '>=1.26.0'."""
        match = re.match(r"^([><=!~]+)\s*(.+)$", constraint.strip())
        if not match:
            return str(self) == constraint.strip()
        op, ver_str = match.group(1), match.group(2)
        other = SemverVersion.parse(ver_str)
        ops = {
            ">=": self >= other,
            "<=": self <= other,
            ">": self > other,
            "<": self < other,
            "==": self._tuple() == other._tuple(),
            "!=": self._tuple() != other._tuple(),
            "~=": self.major == other.major and self.minor >= other.minor,
        }
        return ops.get(op, False)


# ── Conventional Commits ──────────────────────────────────────


class ConventionalCommitType(StrEnum):
    """Conventional commit types mapped to semver bump rules."""

    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    PERF = "perf"
    TEST = "test"
    BUILD = "build"
    CI = "ci"
    CHORE = "chore"
    REVERT = "revert"


class SemverBump(StrEnum):
    """Semver bump level derived from conventional commit."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    NONE = "none"


class ConventionalCommit(BaseModel):
    """Parsed conventional commit message.

    Format: <type>[optional scope][!]: <description>

    The '!' indicates a breaking change (major bump).
    """

    model_config = ConfigDict(frozen=True)

    type: ConventionalCommitType
    scope: str = ""
    breaking: bool = False
    description: str
    body: str = ""
    footers: dict[str, str] = Field(default_factory=dict)

    @classmethod
    def parse(cls, message: str) -> ConventionalCommit:
        """Parse a conventional commit message string."""
        first_line = message.split("\n", 1)[0].strip()
        body = message.split("\n", 1)[1].strip() if "\n" in message else ""

        match = re.match(r"^(\w+)(?:\(([^)]*)\))?(!)?\s*:\s*(.+)$", first_line)
        if not match:
            raise ValueError(f"Not a conventional commit: {first_line}")

        commit_type = match.group(1).lower()
        scope = match.group(2) or ""
        breaking = match.group(3) == "!"
        description = match.group(4).strip()

        # Parse footers from body
        footers: dict[str, str] = {}
        if "BREAKING CHANGE:" in body or "BREAKING-CHANGE:" in body:
            breaking = True
        for line in body.split("\n"):
            footer_match = re.match(r"^([\w-]+)\s*:\s*(.+)$", line.strip())
            if footer_match:
                footers[footer_match.group(1)] = footer_match.group(2)

        return cls(
            type=ConventionalCommitType(commit_type),
            scope=scope,
            breaking=breaking,
            description=description,
            body=body,
            footers=footers,
        )

    @property
    def bump(self) -> SemverBump:
        """Determine the semver bump level for this commit."""
        if self.breaking:
            return SemverBump.MAJOR
        if self.type == ConventionalCommitType.FEAT:
            return SemverBump.MINOR
        if self.type == ConventionalCommitType.FIX:
            return SemverBump.PATCH
        if self.type == ConventionalCommitType.PERF:
            return SemverBump.PATCH
        if self.type == ConventionalCommitType.REVERT:
            return SemverBump.PATCH
        return SemverBump.NONE


# ── Upstream Dependency Tracking ──────────────────────────────


class UpstreamDependency(BaseModel):
    """Tracks an upstream SDK dependency with version constraint.

    When the upstream version changes beyond the constraint, a
    conventional commit is generated to bump the project version.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    package: str  # PyPI package name
    constraint: str  # pip constraint string, e.g. ">=0.42.0"
    current_version: SemverStr
    repo: str = ""  # GitHub repo, e.g. "anthropics/anthropic-sdk-python"
    changelog_url: str = ""

    def is_satisfied(self) -> bool:
        """Check if current version satisfies the constraint."""
        return SemverVersion.parse(self.current_version).satisfies(self.constraint)


# ── Claude Code CLI Models ────────────────────────────────────


class PermissionMode(StrEnum):
    """Claude Code permission mode for tool execution."""

    DEFAULT = "default"
    PLAN = "plan"
    BYPASS_PERMISSIONS = "bypassPermissions"


class OutputFormat(StrEnum):
    """Claude Code CLI output format."""

    TEXT = "text"
    JSON = "json"
    STREAM_JSON = "stream-json"


class ClaudeCodeExitCode(int, Enum):
    """Claude Code CLI exit codes."""

    SUCCESS = 0
    ERROR = 1
    SIGINT = 130


class ClaudeCodeConfig(BaseModel):
    """Claude Code CLI invocation configuration.

    Maps to: code.claude.com/docs/en/cli-reference.md
    """

    model_config = ConfigDict(frozen=True)

    prompt: str = ""
    output_format: OutputFormat = OutputFormat.TEXT
    system_prompt: str = ""
    append_system_prompt: str = ""
    allowed_tools: list[str] = Field(default_factory=list)
    disallowed_tools: list[str] = Field(default_factory=list)
    mcp_config: str = ""  # path to MCP JSON config
    permission_mode: PermissionMode = PermissionMode.DEFAULT
    max_turns: int = Field(default=0, ge=0)  # 0 = unlimited
    model: str = "claude-sonnet-4-6"
    resume: str = ""  # session ID to resume
    continue_session: bool = False
    verbose: bool = False
    input_format: Literal["text", "stream-json"] = "text"


# ── Environment Variables ─────────────────────────────────────


class ClaudeEnvVar(BaseModel):
    """Claude Code environment variable definition.

    Maps to: code.claude.com/docs/en/env-vars
    """

    model_config = ConfigDict(frozen=True)

    name: str
    default: str = ""
    description: str = ""
    type: Literal["string", "boolean", "number", "path"] = "string"
    required: bool = False


# Pre-defined environment variables from the docs
CLAUDE_ENV_VARS: list[ClaudeEnvVar] = [
    ClaudeEnvVar(
        name="CLAUDE_CODE_OAUTH_TOKEN",
        description="Auth token for Claude API",
        type="string",
        required=True,
    ),
    ClaudeEnvVar(
        name="API_TIMEOUT_MS",
        default="300000",
        description="Request timeout for Claude API",
        type="number",
    ),
    ClaudeEnvVar(
        name="CLAUDE_CODE_CERT_STORE",
        default="",
        description="Set to 'bundled' for enterprise proxy CAs",
        type="string",
    ),
    ClaudeEnvVar(
        name="OTEL_LOG_USER_PROMPTS",
        default="false",
        description="Include user prompts in OTEL trace spans",
        type="boolean",
    ),
    ClaudeEnvVar(
        name="OTEL_LOG_TOOL_DETAILS",
        default="false",
        description="Include tool call details in OTEL spans",
        type="boolean",
    ),
    ClaudeEnvVar(
        name="OTEL_LOG_TOOL_CONTENT",
        default="false",
        description="Include tool result content in OTEL spans",
        type="boolean",
    ),
    ClaudeEnvVar(
        name="DISABLE_NONESSENTIAL_TRAFFIC",
        default="0",
        description="Disable non-essential network requests",
        type="boolean",
    ),
    ClaudeEnvVar(
        name="CLAUDE_CODE_MAX_OUTPUT_TOKENS",
        default="16384",
        description="Max output tokens per response",
        type="number",
    ),
]


# ── Tools Reference ───────────────────────────────────────────


class ToolCategory(StrEnum):
    """Tool categories from Claude Code tools reference."""

    FILE_SYSTEM = "file_system"
    SEARCH = "search"
    EXECUTION = "execution"
    WEB = "web"
    MCP = "mcp"
    AGENT = "agent"
    NOTEBOOK = "notebook"


class ToolPermissionLevel(StrEnum):
    """Permission levels for tool execution."""

    ALLOW = "allow"
    ASK = "ask"
    DENY = "deny"


class ToolDefinition(BaseModel):
    """Claude Code tool definition.

    Maps to: code.claude.com/docs/en/tools-reference
    """

    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    category: ToolCategory
    parameters: dict[str, Any] = Field(default_factory=dict)
    default_permission: ToolPermissionLevel = ToolPermissionLevel.ASK
    requires_sandbox: bool = False


# Built-in tool registry
BUILTIN_TOOLS: list[ToolDefinition] = [
    ToolDefinition(
        name="Read",
        description="Read file contents",
        category=ToolCategory.FILE_SYSTEM,
        default_permission=ToolPermissionLevel.ALLOW,
    ),
    ToolDefinition(
        name="Write",
        description="Write content to a file",
        category=ToolCategory.FILE_SYSTEM,
    ),
    ToolDefinition(
        name="Edit",
        description="Make targeted edits to a file",
        category=ToolCategory.FILE_SYSTEM,
    ),
    ToolDefinition(
        name="Glob",
        description="Find files by pattern",
        category=ToolCategory.SEARCH,
        default_permission=ToolPermissionLevel.ALLOW,
    ),
    ToolDefinition(
        name="Grep",
        description="Search file contents with regex",
        category=ToolCategory.SEARCH,
        default_permission=ToolPermissionLevel.ALLOW,
    ),
    ToolDefinition(
        name="Bash",
        description="Execute shell commands",
        category=ToolCategory.EXECUTION,
        requires_sandbox=True,
    ),
    ToolDefinition(
        name="WebFetch",
        description="Fetch URL content",
        category=ToolCategory.WEB,
    ),
    ToolDefinition(
        name="WebSearch",
        description="Search the web",
        category=ToolCategory.WEB,
    ),
    ToolDefinition(
        name="Agent",
        description="Spawn a subagent for complex tasks",
        category=ToolCategory.AGENT,
    ),
    ToolDefinition(
        name="NotebookEdit",
        description="Edit Jupyter notebook cells",
        category=ToolCategory.NOTEBOOK,
    ),
    ToolDefinition(
        name="TodoWrite",
        description="Create and manage task lists",
        category=ToolCategory.FILE_SYSTEM,
        default_permission=ToolPermissionLevel.ALLOW,
    ),
]


# ── Hooks ─────────────────────────────────────────────────────


class HookEvent(StrEnum):
    """Hook event types from Claude Code hooks system.

    Maps to: code.claude.com/docs/en/hooks
    """

    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    NOTIFICATION = "Notification"
    SESSION_START = "SessionStart"
    SESSION_STOP = "SessionStop"
    USER_PROMPT_SUBMIT = "UserPromptSubmit"


class HookMatcherType(StrEnum):
    """Matcher types for hook tool filtering."""

    TOOL_NAME = "tool_name"


class HookMatcher(BaseModel):
    """Matcher for hook event filtering."""

    model_config = ConfigDict(frozen=True)

    type: HookMatcherType = HookMatcherType.TOOL_NAME
    tool_name: str = ""  # regex pattern for tool name matching


class HookDefinition(BaseModel):
    """A hook definition in .claude/settings.json.

    Hooks execute shell commands in response to events.
    """

    model_config = ConfigDict(frozen=True)

    event: HookEvent
    command: str
    matchers: list[HookMatcher] = Field(default_factory=list)
    timeout_ms: int = Field(default=30000, ge=1000, le=300000)


class HookSettings(BaseModel):
    """Hook configuration block in settings.json."""

    hooks: dict[str, list[HookDefinition]] = Field(default_factory=dict)


# ── Checkpointing ─────────────────────────────────────────────


class CheckpointData(BaseModel):
    """Session checkpoint for saving and restoring conversation state.

    Maps to: code.claude.com/docs/en/checkpointing
    """

    session_id: str
    conversation_id: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    summary: str = ""
    cost_usd: float = Field(default=0.0, ge=0.0)
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)


# ── Plugins ───────────────────────────────────────────────────


class PluginManifest(BaseModel):
    """Plugin manifest from .claude-plugin/plugin.json.

    Maps to: code.claude.com/docs/en/plugins-reference
    """

    model_config = ConfigDict(frozen=True)

    name: str
    version: SemverStr
    description: str
    author: dict[str, str] = Field(default_factory=dict)


class SkillFrontmatter(BaseModel):
    """SKILL.md frontmatter (YAML header).

    Universal format across Claude Code, Cursor, Gemini CLI, Codex CLI.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    user_invocable: bool = True
    argument_hint: str = ""


# ── Channels ──────────────────────────────────────────────────


class ChannelType(StrEnum):
    """Channel types for Claude Code communication.

    Maps to: code.claude.com/docs/en/channels-reference
    """

    STDIO = "stdio"
    HTTP = "http"
    WEBSOCKET = "websocket"


class ChannelConfig(BaseModel):
    """Channel configuration for Claude Code sessions."""

    model_config = ConfigDict(frozen=True)

    type: ChannelType = ChannelType.STDIO
    port: int = Field(default=0, ge=0, le=65535)
    host: str = "localhost"


# ── Claude Agent SDK Models ───────────────────────────────────
# Mirrors key types from claude-code-sdk (anthropic-ai/claude-agent-sdk-python)


class AgentSDKModel(StrEnum):
    """Claude model identifiers (hyphen format, no dots or date suffixes)."""

    OPUS_4_6 = "claude-opus-4-6"
    SONNET_4_6 = "claude-sonnet-4-6"
    HAIKU_4_5 = "claude-haiku-4-5"


class AgentSDKSessionConfig(BaseModel):
    """Session configuration for claude-code-sdk.

    Maps to the ClaudeCodeSDK options parameter.
    """

    model: str = AgentSDKModel.SONNET_4_6.value
    system_prompt: str = ""
    append_system_prompt: str = ""
    permission_mode: PermissionMode = PermissionMode.DEFAULT
    allowed_tools: list[str] = Field(default_factory=list)
    disallowed_tools: list[str] = Field(default_factory=list)
    max_turns: int = Field(default=0, ge=0)
    cwd: str = ""

    @field_validator("model")
    @classmethod
    def validate_model_format(cls, v: str) -> str:
        """Ensure model uses hyphen format per CLAUDE.md conventions."""
        if re.search(r"-\d{8}$", v) or ("." in v and not v.startswith("claude-")):
            raise ValueError(
                f"Model '{v}' must use hyphen format: "
                "claude-opus-4-6, claude-sonnet-4-6, claude-haiku-4-5"
            )
        return v


class AgentSDKMessageRole(StrEnum):
    """Message roles in Agent SDK conversation."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AgentSDKContentType(StrEnum):
    """Content block types in Agent SDK messages."""

    TEXT = "text"
    TOOL_USE = "tool_use"
    TOOL_RESULT = "tool_result"


class AgentSDKContentBlock(BaseModel):
    """Content block in an Agent SDK message."""

    type: AgentSDKContentType
    text: str = ""
    tool_use_id: str = ""
    tool_name: str = ""
    tool_input: dict[str, Any] = Field(default_factory=dict)


class AgentSDKMessage(BaseModel):
    """Message in Agent SDK conversation stream."""

    role: AgentSDKMessageRole
    content: list[AgentSDKContentBlock] = Field(default_factory=list)


class AgentSDKEvent(BaseModel):
    """Streaming event from Agent SDK.

    Event types mirror the claude-code-sdk Python package.
    """

    type: str
    session_id: str = ""
    message: AgentSDKMessage | None = None
    tool_use_id: str = ""
    tool_name: str = ""
    error: str = ""


# ── MCP SDK v2 Models ─────────────────────────────────────────
# Mirrors key types from mcp (modelcontextprotocol/python-sdk)


class MCPTransportType(StrEnum):
    """MCP transport types."""

    STDIO = "stdio"
    HTTP = "http"
    SSE = "sse"
    STREAMABLE_HTTP = "streamable-http"


class MCPToolSchema(BaseModel):
    """MCP tool definition schema.

    Maps to the Tool type from mcp.types.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    description: str = ""
    input_schema: dict[str, Any] = Field(default_factory=dict)


class MCPResourceType(StrEnum):
    """MCP resource types."""

    TEXT = "text"
    BLOB = "blob"


class MCPResource(BaseModel):
    """MCP resource definition.

    Maps to the Resource type from mcp.types.
    """

    model_config = ConfigDict(frozen=True)

    uri: str
    name: str
    description: str = ""
    mime_type: str = ""


class MCPPromptArgument(BaseModel):
    """MCP prompt argument definition."""

    model_config = ConfigDict(frozen=True)

    name: str
    description: str = ""
    required: bool = False


class MCPPrompt(BaseModel):
    """MCP prompt definition.

    Maps to the Prompt type from mcp.types.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    description: str = ""
    arguments: list[MCPPromptArgument] = Field(default_factory=list)


class MCPServerConfig(BaseModel):
    """MCP server configuration for .mcp.json files."""

    model_config = ConfigDict(frozen=True)

    transport: MCPTransportType = MCPTransportType.HTTP
    url: str = ""
    command: str = ""  # for stdio transport
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)


class MCPCapabilities(BaseModel):
    """MCP server capability advertisement."""

    model_config = ConfigDict(frozen=True)

    tools: bool = False
    resources: bool = False
    prompts: bool = False
    logging: bool = False
    sampling: bool = False
    roots: bool = False


# ── Version Manifest ──────────────────────────────────────────


class SDKVersionManifest(BaseModel):
    """Tracks all upstream SDK versions and their constraints.

    Used by release-please to determine when to bump the project
    version based on upstream dependency changes.
    """

    project_version: SemverStr
    updated_at: datetime = Field(default_factory=datetime.now)
    dependencies: list[UpstreamDependency] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_all_satisfied(self) -> SDKVersionManifest:
        """Warn if any dependency constraint is not satisfied."""
        for dep in self.dependencies:
            if not dep.is_satisfied():
                # Don't raise — just flag for release-please to process
                pass
        return self

    def outdated(self) -> list[UpstreamDependency]:
        """Return dependencies that no longer satisfy their constraints."""
        return [d for d in self.dependencies if not d.is_satisfied()]

    def compute_bump(self, commits: list[ConventionalCommit]) -> SemverBump:
        """Compute the highest bump level from a list of commits."""
        bumps = [c.bump for c in commits]
        if SemverBump.MAJOR in bumps:
            return SemverBump.MAJOR
        if SemverBump.MINOR in bumps:
            return SemverBump.MINOR
        if SemverBump.PATCH in bumps:
            return SemverBump.PATCH
        return SemverBump.NONE

    def next_version(self, commits: list[ConventionalCommit]) -> str:
        """Compute the next version based on conventional commits."""
        bump = self.compute_bump(commits)
        current = SemverVersion.parse(self.project_version)
        if bump == SemverBump.MAJOR:
            return str(current.bump_major())
        if bump == SemverBump.MINOR:
            return str(current.bump_minor())
        if bump == SemverBump.PATCH:
            return str(current.bump_patch())
        return self.project_version


# ── Default Manifest ──────────────────────────────────────────


def default_manifest() -> SDKVersionManifest:
    """Build the default version manifest for agentstreams."""
    return SDKVersionManifest(
        project_version="0.4.0",
        dependencies=[
            UpstreamDependency(
                name="Anthropic SDK",
                package="anthropic",
                constraint=">=0.42.0",
                current_version="0.49.0",
                repo="anthropics/anthropic-sdk-python",
                changelog_url="https://github.com/anthropics/anthropic-sdk-python/blob/main/CHANGELOG.md",
            ),
            UpstreamDependency(
                name="Claude Agent SDK",
                package="claude-code-sdk",
                constraint=">=0.1.53",
                current_version="0.1.53",
                repo="anthropics/claude-code-sdk-python",
                changelog_url="https://github.com/anthropics/claude-code-sdk-python/blob/main/CHANGELOG.md",
            ),
            UpstreamDependency(
                name="MCP SDK",
                package="mcp",
                constraint=">=1.26.0",
                current_version="1.29.0",
                repo="modelcontextprotocol/python-sdk",
                changelog_url="https://github.com/modelcontextprotocol/python-sdk/blob/main/CHANGELOG.md",
            ),
            UpstreamDependency(
                name="FastAPI",
                package="fastapi",
                constraint=">=0.115.0",
                current_version="0.115.12",
                repo="fastapi/fastapi",
            ),
            UpstreamDependency(
                name="Pydantic",
                package="pydantic",
                constraint=">=2.0.0",
                current_version="2.11.3",
                repo="pydantic/pydantic",
                changelog_url="https://github.com/pydantic/pydantic/blob/main/HISTORY.md",
            ),
        ],
    )


# ── Release-Please Config Model ──────────────────────────────


class ReleasePleasePackage(BaseModel):
    """A package entry in release-please-config.json."""

    model_config = ConfigDict(frozen=True)

    release_type: str = "python"
    component: str = ""
    package_name: str = ""
    bump_minor_pre_major: bool = True
    bump_patch_for_minor_pre_major: bool = True
    changelog_path: str = "CHANGELOG.md"
    versioning: str = "default"
    extra_files: list[str] = Field(default_factory=list)


class ReleasePleaseConfig(BaseModel):
    """release-please-config.json schema.

    Defines how release-please manages versioning and changelogs.
    """

    schema_url: str = Field(
        default="https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
        alias="$schema",
    )
    packages: dict[str, ReleasePleasePackage] = Field(default_factory=dict)
    changelog_sections: list[dict[str, str]] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


def default_release_please_config() -> ReleasePleaseConfig:
    """Build the default release-please configuration for agentstreams."""
    return ReleasePleaseConfig(
        packages={
            ".": ReleasePleasePackage(
                release_type="python",
                component="agentstreams",
                package_name="agentstreams",
                bump_minor_pre_major=True,
                bump_patch_for_minor_pre_major=True,
                extra_files=["src/sdk_models.py"],
            ),
        },
        changelog_sections=[
            {"type": "feat", "section": "Features"},
            {"type": "fix", "section": "Bug Fixes"},
            {"type": "perf", "section": "Performance"},
            {"type": "refactor", "section": "Refactoring"},
            {"type": "docs", "section": "Documentation"},
            {"type": "build", "section": "Build System"},
            {"type": "ci", "section": "CI/CD"},
            {"type": "chore", "section": "Miscellaneous"},
        ],
    )
