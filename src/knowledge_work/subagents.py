"""Layer 6: knowledge-work-subagents — Subagent orchestration.

Maps Subtasks (Layer 5) to Claude Code subagent specifications. Each
SubagentSpec defines the tools, model, skills, and MCP servers a
subagent needs to execute its assigned subtask.

Bridges:
    Layer 5 (subtasks)               → Subtasks assigned to subagents
    src/knowledge_subagents.py       → AGENT_TOOLS, AGENT_COLORS
    vendors/knowledge-work-plugins   → MCP server configs from .mcp.json
    Layer 7 (harness)                → Harness executes subagent pool

Architecture note (from Anthropic's Managed Agents blog):
    "Decouple the brain from the hands" — subagents are cattle, not pets.
    Each is stateless and replaceable. If one fails, a new one can be
    reinitialized. The session log (Layer 7) survives subagent crashes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.knowledge_work.subtasks import Subtask

PROJECT_ROOT = Path(__file__).parent.parent.parent


@dataclass
class SubagentSpec:
    """Specification for a Claude Code subagent.

    Generates the .claude/agents/*.md frontmatter and system prompt
    needed to execute a subtask.
    """

    name: str
    description: str
    tools: str = "Read, Glob, Grep, Bash"
    model: str = "claude-opus-4-6"
    color: str = "blue"
    skills: list[str] = field(default_factory=list)  # Paths to SKILL.md
    mcp_servers: list[dict[str, Any]] = field(default_factory=list)
    system_prompt: str = ""
    max_turns: int = 20

    def to_frontmatter(self) -> str:
        """Generate YAML frontmatter for .claude/agents/*.md."""
        lines = [
            "---",
            f"name: {self.name}",
            f"description: {self.description}",
            f"tools: {self.tools}",
            f"model: {self.model}",
            f"color: {self.color}",
            f"maxTurns: {self.max_turns}",
        ]
        if self.skills:
            lines.append("skills:")
            for skill in self.skills:
                lines.append(f"  - {skill}")
        if self.mcp_servers:
            lines.append("mcpServers:")
            for server in self.mcp_servers:
                for name, config in server.items():
                    lines.append(f"  - {name}:")
                    for k, v in config.items():
                        lines.append(f"      {k}: {v}")
        lines.append("---")
        return "\n".join(lines)

    def to_markdown(self) -> str:
        """Generate complete .claude/agents/*.md file content."""
        return f"{self.to_frontmatter()}\n\n{self.system_prompt}\n"


@dataclass
class SubagentPool:
    """Pool of subagent specs for executing a SubtaskGraph.

    Manages the lifecycle of subagents: creation, assignment, and
    status tracking. Follows the "cattle not pets" pattern — subagents
    are interchangeable and restartable.
    """

    specs: dict[str, SubagentSpec] = field(default_factory=dict)
    assignments: dict[str, str] = field(default_factory=dict)  # subtask_id → spec_name

    def register(self, spec: SubagentSpec) -> None:
        """Register a subagent spec in the pool."""
        self.specs[spec.name] = spec

    def assign(self, subtask: Subtask) -> SubagentSpec | None:
        """Assign a subagent spec to a subtask.

        Looks up by agent_name first, then falls back to plugin category.
        """
        # Direct match by agent name
        if subtask.agent_name and subtask.agent_name in self.specs:
            self.assignments[subtask.id] = subtask.agent_name
            return self.specs[subtask.agent_name]

        # Match by plugin category
        for name, spec in self.specs.items():
            if subtask.plugin_category and subtask.plugin_category in name:
                self.assignments[subtask.id] = name
                return spec

        return None

    def get_spec(self, subtask_id: str) -> SubagentSpec | None:
        """Get the assigned spec for a subtask."""
        name = self.assignments.get(subtask_id)
        return self.specs.get(name) if name else None

    @classmethod
    def from_knowledge_agents(cls) -> SubagentPool:
        """Build pool from existing knowledge agent definitions.

        Reads src/knowledge_subagents.py AGENT_TOOLS and AGENT_COLORS
        to populate specs matching the 17 knowledge-work categories.
        """
        try:
            from src.knowledge_subagents import (
                AGENT_COLORS,
                AGENT_TOOLS,
            )
        except ImportError:
            return cls()

        pool = cls()
        for agent_name, tools in AGENT_TOOLS.items():
            color = AGENT_COLORS.get(agent_name, "blue")
            pool.register(
                SubagentSpec(
                    name=agent_name,
                    description=f"Knowledge-work agent: {agent_name}",
                    tools=tools,
                    color=color,
                )
            )

        return pool
