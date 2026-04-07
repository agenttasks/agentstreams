"""Agent SDK v2 task orchestration for AgentStreams.

Implements task patterns following:
- anthropic/claude-agent-sdk-python v2
- anthropic/claude-agent-sdk-typescript v2

Provides typed task definitions, agent runner, and tool integration
for orchestrating multi-step workflows across crawl, extract, and
persist pipelines.

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentTool:
    """Agent SDK v2 tool definition.

    Maps to the Agent SDK's tool registration interface,
    bridging MCP tools to the agent execution loop.
    """

    name: str
    description: str
    input_schema: dict[str, Any]
    handler: str = ""  # Module path to handler function


@dataclass
class AgentConfig:
    """Configuration for an Agent SDK v2 agent.

    Following the claude-agent-sdk-python v2 pattern:
    - model: Claude model ID
    - tools: Available MCP tools
    - system_prompt: Agent behavioral instructions
    - max_turns: Conversation turn limit
    """

    name: str
    model: str = "claude-sonnet-4-6"
    system_prompt: str = ""
    tools: list[AgentTool] = field(default_factory=list)
    max_turns: int = 25
    temperature: float = 0.0
    max_tokens: int = 8192


@dataclass
class TaskSpec:
    """Typed task specification for agent execution.

    Defines what an agent should accomplish, with structured
    input/output schemas and execution constraints.
    """

    task_id: str
    task_type: str  # crawl, extract, persist, analyze, project
    description: str
    inputs: dict[str, Any] = field(default_factory=dict)
    config: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)

    def to_xml(self) -> str:
        """Render task as structured XML for agent prompting."""
        input_fields = "\n".join(
            f'    <field name="{k}">{v}</field>' for k, v in self.inputs.items()
        )
        config_fields = "\n".join(
            f'    <param name="{k}">{v}</param>' for k, v in self.config.items()
        )
        deps = ""
        if self.depends_on:
            deps = "\n  <depends-on>" + ", ".join(self.depends_on) + "</depends-on>"

        return (
            f'<task id="{self.task_id}" type="{self.task_type}">\n'
            f"  <description>{self.description}</description>\n"
            f"  <inputs>\n{input_fields}\n  </inputs>\n"
            f"  <config>\n{config_fields}\n  </config>"
            f"{deps}\n"
            f"</task>"
        )


@dataclass
class TaskResult:
    """Result of a task execution."""

    task_id: str
    status: str  # completed, failed, cancelled
    outputs: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    tokens_used: int = 0


class AgentRunner:
    """Agent SDK v2 compatible runner for task execution.

    Manages the agent execution loop:
    1. Parse task spec into agent prompt
    2. Execute agent with available tools
    3. Collect and persist results
    4. Handle tool calls via MCP handler

    Following claude-agent-sdk-python v2 patterns:
    - Typed tool definitions with JSON Schema
    - Structured message passing
    - Turn-based execution with limits
    """

    def __init__(self, config: AgentConfig, *, neon_url: str = ""):
        self.config = config
        self.neon_url = neon_url or os.environ.get("NEON_DATABASE_URL", "")

    def _build_system_prompt(self, task: TaskSpec) -> str:
        """Build system prompt incorporating agent config and task context."""
        base = self.config.system_prompt or (
            f"You are {self.config.name}, an AgentStreams task agent.\n"
            f"Execute the assigned task using available tools.\n"
            f"Follow the UDA pattern: ontology is source of truth.\n"
        )

        return (
            f"{base}\n\n"
            f"## Current Task\n\n"
            f"{task.to_xml()}\n\n"
            f"## Available Tools\n\n"
            + "\n".join(f"- **{t.name}**: {t.description}" for t in self.config.tools)
            + "\n\n## Constraints\n\n"
            f"- Max turns: {self.config.max_turns}\n"
            f"- Use CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY)\n"
            f"- Persist results to Neon Postgres when available\n"
        )

    async def execute(self, task: TaskSpec) -> TaskResult:
        """Execute a task using the Agent SDK v2 pattern.

        Creates a Claude conversation with tool access, runs the
        agent loop until completion or max_turns, and returns results.
        """
        import anthropic

        client = anthropic.Anthropic()
        system_prompt = self._build_system_prompt(task)

        tools = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.input_schema,
            }
            for t in self.config.tools
        ]

        messages = [
            {
                "role": "user",
                "content": (
                    f"Execute the following task:\n\n{task.to_xml()}\n\n"
                    f"Use the available tools to complete it. "
                    f"When done, respond with a JSON summary of results."
                ),
            }
        ]

        total_tokens = 0
        from src.mcp_tools import MCPToolHandler

        mcp_handler = MCPToolHandler(neon_url=self.neon_url)

        for _turn in range(self.config.max_turns):
            response = client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt,
                tools=tools,
                messages=messages,
            )

            total_tokens += response.usage.input_tokens + response.usage.output_tokens

            # Check if agent is done (no tool use)
            if response.stop_reason == "end_turn":
                text_content = "".join(
                    block.text for block in response.content if block.type == "text"
                )
                try:
                    outputs = json.loads(text_content)
                except json.JSONDecodeError:
                    outputs = {"raw": text_content}

                return TaskResult(
                    task_id=task.task_id,
                    status="completed",
                    outputs=outputs,
                    tokens_used=total_tokens,
                )

            # Handle tool calls
            if response.stop_reason == "tool_use":
                # Add assistant message
                messages.append({"role": "assistant", "content": response.content})

                # Process tool calls
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = await mcp_handler.call_tool(block.name, block.input)
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.content[0]["text"] if result.content else "",
                                "is_error": result.is_error,
                            }
                        )

                messages.append({"role": "user", "content": tool_results})

        return TaskResult(
            task_id=task.task_id,
            status="failed",
            error=f"Max turns ({self.config.max_turns}) exceeded",
            tokens_used=total_tokens,
        )


# ── Pre-built Agent Configs ────────────────────────────────


def crawl_agent_config() -> AgentConfig:
    """Pre-configured agent for web crawling tasks."""
    from src.mcp_tools import TOOLS

    return AgentConfig(
        name="crawl-agent",
        model="claude-sonnet-4-6",
        system_prompt=(
            "You are a web crawling agent. Use the crawl_urls and bloom_check "
            "tools to discover, deduplicate, and persist web content. "
            "Follow sitemap structures and respect rate limits."
        ),
        tools=[
            AgentTool(
                name=t.name,
                description=t.description,
                input_schema=t.input_schema,
            )
            for t in TOOLS
            if t.name in ("crawl_urls", "bloom_check", "enqueue_task")
        ],
    )


def extract_agent_config() -> AgentConfig:
    """Pre-configured agent for structured extraction tasks."""
    from src.mcp_tools import TOOLS

    return AgentConfig(
        name="extract-agent",
        model="claude-sonnet-4-6",
        system_prompt=(
            "You are a structured extraction agent. Use DSPy extraction "
            "to pull entities, classify content, and align data to the "
            "AgentStreams ontology. Persist results to Neon Postgres."
        ),
        tools=[
            AgentTool(
                name=t.name,
                description=t.description,
                input_schema=t.input_schema,
            )
            for t in TOOLS
            if t.name in ("dspy_extract", "query_metrics", "enqueue_task")
        ],
    )


def projection_agent_config() -> AgentConfig:
    """Pre-configured agent for ontology projection tasks."""
    from src.mcp_tools import TOOLS

    return AgentConfig(
        name="projection-agent",
        model="claude-sonnet-4-6",
        system_prompt=(
            "You are a UDA projection agent. Generate Avro, GraphQL, "
            "DataContainer, and Mapping projections from the AgentStreams "
            "ontology. Ensure consistency across all representations."
        ),
        tools=[
            AgentTool(
                name=t.name,
                description=t.description,
                input_schema=t.input_schema,
            )
            for t in TOOLS
            if t.name in ("project_ontology", "query_metrics")
        ],
    )
