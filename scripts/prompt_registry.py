"""Prompt registry for agentic AI prompt patterns.

Catalogs 30 prompt types from vendors/agentic-ai-prompt-research/prompts/
with metadata for type, category, tools, and XML task rendering.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "vendors" / "agentic-ai-prompt-research" / "prompts"


@dataclass
class PromptEntry:
    """Single prompt entry in the registry."""

    id: str
    name: str
    filename: str
    prompt_type: str  # system | agent | tool | skill
    purpose: str
    constraints: list[str] = field(default_factory=list)
    tools_allowed: list[str] = field(default_factory=list)
    tools_denied: list[str] = field(default_factory=list)
    output_format: str = ""
    tags: list[str] = field(default_factory=list)

    def to_xml(self) -> str:
        """Render this prompt as a structured XML task."""
        lines = [f'<task id="{self.id}" type="{self.prompt_type}" name="{self.name}">']
        lines.append(f"  <purpose>{_escape_xml(self.purpose)}</purpose>")

        if self.constraints:
            lines.append("  <constraints>")
            for c in self.constraints:
                lines.append(f"    <constraint>{_escape_xml(c)}</constraint>")
            lines.append("  </constraints>")

        if self.tools_allowed or self.tools_denied:
            allowed = ",".join(self.tools_allowed) if self.tools_allowed else ""
            denied = ",".join(self.tools_denied) if self.tools_denied else ""
            attrs = []
            if allowed:
                attrs.append(f'allowed="{allowed}"')
            if denied:
                attrs.append(f'denied="{denied}"')
            lines.append(f"  <tools {' '.join(attrs)}/>")

        if self.output_format:
            lines.append(f'  <output format="{_escape_xml(self.output_format)}"/>')

        if self.tags:
            lines.append(f"  <tags>{','.join(self.tags)}</tags>")

        lines.append("</task>")
        return "\n".join(lines)

    def source_path(self) -> Path:
        """Path to the source prompt file."""
        return PROMPTS_DIR / self.filename

    def read_source(self) -> str:
        """Read the raw source prompt content."""
        return self.source_path().read_text(encoding="utf-8")


def _escape_xml(text: str) -> str:
    """Escape XML special characters."""
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


# --- Registry ---

REGISTRY: list[PromptEntry] = [
    PromptEntry(
        id="01",
        name="main-system-prompt",
        filename="01_main_system_prompt.md",
        prompt_type="system",
        purpose="Dynamic master prompt assembled from feature-flagged sections",
        constraints=[
            "Sections composed via functions based on feature flags",
            "Global cache scope above dynamic boundary marker",
            "Session-specific content below boundary",
        ],
        tags=["core", "composition", "caching"],
    ),
    PromptEntry(
        id="02",
        name="simple-mode",
        filename="02_simple_mode.md",
        prompt_type="system",
        purpose="Minimal prompt activated by CLAUDE_CODE_SIMPLE=true",
        constraints=["Under 3 sentences", "No tool guidance"],
        tags=["minimal", "feature-gate"],
    ),
    PromptEntry(
        id="03",
        name="default-agent",
        filename="03_default_agent_prompt.md",
        prompt_type="agent",
        purpose="Base prompt for all sub-agents enhanced at runtime with environment info",
        constraints=[
            "Use absolute paths",
            "Avoid emojis",
            "Include code snippets per guidelines",
        ],
        tags=["agent", "base", "runtime-enhancement"],
    ),
    PromptEntry(
        id="04",
        name="cyber-risk-instruction",
        filename="04_cyber_risk_instruction.md",
        prompt_type="system",
        purpose="Security boundary definitions for defensive vs harmful activities",
        constraints=[
            "Explicit allowlist/blocklist for security operations",
            "Authorization context required for dual-use tools",
        ],
        tags=["security", "safeguard", "boundary"],
    ),
    PromptEntry(
        id="05",
        name="coordinator",
        filename="05_coordinator_system_prompt.md",
        prompt_type="agent",
        purpose="Multi-worker orchestration with synthesis, research, implementation, verification",
        constraints=[
            "Never delegate understanding — synthesize findings yourself",
            "Never write 'based on your findings'",
            "Include file paths, line numbers, exact changes in specs",
        ],
        tools_allowed=["Agent", "SendMessage", "TaskStop"],
        output_format="task-notification XML",
        tags=["orchestration", "parallel", "synthesis"],
    ),
    PromptEntry(
        id="06",
        name="teammate-addendum",
        filename="06_teammate_prompt_addendum.md",
        prompt_type="system",
        purpose="Inter-agent communication protocol via SendMessage tool",
        constraints=["Named targeting", "Broadcast via to: '*'"],
        tools_allowed=["SendMessage"],
        tags=["team", "communication", "swarm"],
    ),
    PromptEntry(
        id="07",
        name="verification-agent",
        filename="07_verification_agent.md",
        prompt_type="agent",
        purpose="Adversarial testing specialist that tries to break implementations",
        constraints=[
            "Read-only — no file modifications in project directory",
            "Must end with VERDICT: PASS, FAIL, or PARTIAL",
            "Every check must have Command run block with actual output",
            "At least one adversarial probe required before PASS",
        ],
        tools_allowed=["Read", "Glob", "Grep", "Bash"],
        tools_denied=["Agent", "Edit", "Write", "NotebookEdit"],
        output_format="structured checks with VERDICT",
        tags=["verification", "adversarial", "read-only"],
    ),
    PromptEntry(
        id="08",
        name="explore-agent",
        filename="08_explore_agent.md",
        prompt_type="agent",
        purpose="Fast read-only codebase search specialist",
        constraints=[
            "Read-only — no file creation or modification",
            "No state-changing Bash operations",
            "Parallel tool calls for speed",
        ],
        tools_allowed=["Read", "Glob", "Grep", "Bash"],
        tools_denied=["Agent", "Edit", "Write", "NotebookEdit"],
        tags=["exploration", "search", "read-only", "fast"],
    ),
    PromptEntry(
        id="09",
        name="agent-creation-architect",
        filename="09_agent_creation_architect.md",
        prompt_type="agent",
        purpose="Meta-agent that designs new agent configurations from user requirements",
        constraints=[
            "Output must be valid JSON with identifier, whenToUse, systemPrompt",
            "Identifiers: lowercase, 2-4 words, hyphens, no generic terms",
        ],
        output_format="JSON agent specification",
        tags=["meta-agent", "design", "configuration"],
    ),
    PromptEntry(
        id="10",
        name="statusline-setup",
        filename="10_statusline_setup_agent.md",
        prompt_type="skill",
        purpose="Configure terminal status line from shell PS1 configuration",
        constraints=["Map shell escape sequences to statusLine format"],
        tools_allowed=["Read", "Edit"],
        tags=["terminal", "configuration", "shell"],
    ),
    PromptEntry(
        id="11",
        name="permission-explainer",
        filename="11_permission_explainer.md",
        prompt_type="tool",
        purpose="Explain tool/command purpose, reasoning, and risk level before approval",
        output_format="JSON with tool, purpose, reasoning, risk_level",
        tags=["permissions", "risk", "explanation"],
    ),
    PromptEntry(
        id="12",
        name="auto-mode-classifier",
        filename="12_yolo_auto_mode_classifier.md",
        prompt_type="system",
        purpose="2-stage security classification for auto-approving or blocking tool invocations",
        constraints=[
            "Forced tool call for structured output (classify_result)",
            "Assistant text excluded from transcript to prevent injection",
            "Cache-friendly with CLAUDE.md prefix",
        ],
        output_format="forced tool call: classify_result",
        tags=["security", "classifier", "auto-mode"],
    ),
    PromptEntry(
        id="13",
        name="tool-prompts",
        filename="13_tool_prompts.md",
        prompt_type="tool",
        purpose="Compendium of tool-specific guidance embedded in tool schemas",
        constraints=["Prefer dedicated tools over Bash equivalents"],
        tags=["tools", "guidance", "compendium"],
    ),
    PromptEntry(
        id="14",
        name="tool-use-summary",
        filename="14_tool_use_summary.md",
        prompt_type="tool",
        purpose="Generate short git-commit-style labels summarizing tool call results",
        constraints=["Truncated to ~30 chars", "Past-tense verb/noun"],
        output_format="single-line label",
        tags=["summary", "label", "mobile"],
    ),
    PromptEntry(
        id="15",
        name="session-search",
        filename="15_session_search.md",
        prompt_type="system",
        purpose="Semantic search across past conversation sessions",
        constraints=[
            "Priority: tags > title > branch > summary > transcript",
            "Bias toward inclusion when uncertain",
        ],
        output_format="JSON ranked results",
        tags=["search", "sessions", "semantic"],
    ),
    PromptEntry(
        id="16",
        name="memory-selection",
        filename="16_memory_selection.md",
        prompt_type="tool",
        purpose="Select up to 5 relevant memory files from .claude/ for current query",
        constraints=[
            "Discard uncertain matches",
            "Exclude duplicate API docs for recently-used tools",
            "Include gotchas and warnings",
        ],
        output_format="JSON selected_memories array",
        tags=["memory", "selection", "semantic"],
    ),
    PromptEntry(
        id="17",
        name="auto-mode-critique",
        filename="17_auto_mode_critique.md",
        prompt_type="tool",
        purpose="Review auto-mode classifier rules for quality and conflicts",
        constraints=[
            "Four criteria: clarity, completeness, conflicts, actionability",
            "Concise constructive feedback",
        ],
        tags=["classifier", "review", "meta"],
    ),
    PromptEntry(
        id="18",
        name="proactive-mode",
        filename="18_proactive_mode.md",
        prompt_type="system",
        purpose="Autonomous agent behavior with tick-based keep-alive and focus awareness",
        constraints=[
            "Must call Sleep when idle — no status-only messages",
            "Cache expires after 5 minutes — balance sleep duration",
            "Unfocused terminal = more autonomous, focused = more collaborative",
        ],
        tools_allowed=["Sleep"],
        tags=["autonomous", "proactive", "tick", "pacing"],
    ),
    PromptEntry(
        id="19",
        name="simplify-skill",
        filename="19_simplify_skill.md",
        prompt_type="skill",
        purpose="3-agent parallel code review on recent changes (reuse, quality, efficiency)",
        constraints=[
            "Scope limited to git diff",
            "Three agents run in parallel",
            "False positives skipped not argued",
        ],
        tags=["review", "parallel", "cleanup"],
    ),
    PromptEntry(
        id="20",
        name="session-title",
        filename="20_session_title.md",
        prompt_type="tool",
        purpose="Generate concise 3-7 word session titles in sentence case",
        constraints=["Sentence case", "3-7 words", "Last 1000 chars for context"],
        output_format="JSON title",
        tags=["title", "session", "summary"],
    ),
    PromptEntry(
        id="21",
        name="compact-service",
        filename="21_compact_service.md",
        prompt_type="system",
        purpose="Generate detailed conversation summaries when context approaches limits",
        constraints=[
            "No tool calls — text only",
            "Analysis in <analysis> tags (stripped before context)",
            "Nine required summary sections",
            "Three modes: full, partial-recent, partial-older",
        ],
        output_format="<analysis> + <summary> blocks",
        tags=["compaction", "context", "summary"],
    ),
    PromptEntry(
        id="22",
        name="away-summary",
        filename="22_away_summary.md",
        prompt_type="tool",
        purpose="Generate 1-3 sentence recap when user returns after stepping away",
        constraints=["Exactly 1-3 sentences", "Task-first with concrete next step"],
        output_format="short prose",
        tags=["summary", "away", "recap"],
    ),
    PromptEntry(
        id="23",
        name="chrome-browser-automation",
        filename="23_chrome_browser_automation.md",
        prompt_type="system",
        purpose="Browser automation via Claude-in-Chrome MCP extension",
        constraints=[
            "Avoid dialogs (blocks extension event loop)",
            "Tab context required at startup",
            "Tool-search before use",
        ],
        tags=["browser", "automation", "chrome", "mcp"],
    ),
    PromptEntry(
        id="24",
        name="memory-instruction",
        filename="24_memory_instruction.md",
        prompt_type="system",
        purpose="Meta-instruction wrapping CLAUDE.md memory files with hierarchy and includes",
        constraints=[
            "Hierarchy: managed > user > project > local",
            "@include with circular reference prevention",
            "YAML frontmatter with path globbing",
            "MAX_INCLUDE_DEPTH=5",
        ],
        tags=["memory", "hierarchy", "includes"],
    ),
    PromptEntry(
        id="25",
        name="skillify",
        filename="25_skillify.md",
        prompt_type="skill",
        purpose="Interactive interview to capture repeatable processes into SKILL.md files",
        constraints=[
            "Multi-question interview workflow",
            "YAML frontmatter with name/description",
            "Output to .claude/skills/",
        ],
        output_format="SKILL.md file",
        tags=["skill-creation", "interview", "workflow"],
    ),
    PromptEntry(
        id="26",
        name="stuck-skill",
        filename="26_stuck_skill.md",
        prompt_type="skill",
        purpose="Diagnostic for frozen/hung sessions via system inspections",
        constraints=["Internal only (USER_TYPE=ant)", "CPU/memory/disk/network checks"],
        tags=["diagnostic", "internal", "debugging"],
    ),
    PromptEntry(
        id="27",
        name="remember-skill",
        filename="27_remember_skill.md",
        prompt_type="skill",
        purpose="Organize auto-memory entries into structured CLAUDE.md files",
        constraints=[
            "Memory hierarchy: CLAUDE.md > CLAUDE.local.md > ~/.claude/CLAUDE.md",
            "Deduplication logic",
            "Shared vs private distinction",
        ],
        tags=["memory", "organization", "persistence"],
    ),
    PromptEntry(
        id="28",
        name="update-config-skill",
        filename="28_update_config_skill.md",
        prompt_type="skill",
        purpose="Manage settings.json configuration including hooks and permissions",
        constraints=[
            "3-level settings hierarchy: project > user > enterprise",
            "Hook lifecycle: PreToolUse, PostToolUse, PreCompact",
            "Hook exit codes: 0=success, 2=block",
        ],
        tags=["config", "hooks", "permissions", "settings"],
    ),
    PromptEntry(
        id="29",
        name="agent-summary",
        filename="29_agent_summary.md",
        prompt_type="tool",
        purpose="Generate 1-sentence progress updates for sub-agents in coordinator mode",
        constraints=["Single sentence", "Present-tense verbs", "Action-specific"],
        output_format="single sentence",
        tags=["progress", "summary", "coordinator"],
    ),
    PromptEntry(
        id="30",
        name="prompt-suggestion",
        filename="30_prompt_suggestion.md",
        prompt_type="tool",
        purpose="Predict next likely user command/question for clickable UI suggestions",
        constraints=[
            "1-3 suggestions",
            "2-8 words each",
            "Match user style",
            "Deduplicate against recent commands",
        ],
        output_format="JSON array",
        tags=["suggestion", "prediction", "ui"],
    ),
]


def get_registry() -> list[PromptEntry]:
    """Return the full prompt registry."""
    return REGISTRY


def get_by_id(prompt_id: str) -> PromptEntry | None:
    """Look up a prompt by its 2-digit ID."""
    for entry in REGISTRY:
        if entry.id == prompt_id:
            return entry
    return None


def get_by_type(prompt_type: str) -> list[PromptEntry]:
    """Filter prompts by type (system, agent, tool, skill)."""
    return [e for e in REGISTRY if e.prompt_type == prompt_type]


def get_by_tag(tag: str) -> list[PromptEntry]:
    """Filter prompts by tag."""
    return [e for e in REGISTRY if tag in e.tags]


def render_all_xml() -> str:
    """Render all prompts as a single XML document."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<prompt-tasks>"]
    for entry in REGISTRY:
        lines.append(entry.to_xml())
    lines.append("</prompt-tasks>")
    return "\n".join(lines)


def extract_prompt_body(content: str) -> str:
    """Extract the prompt body from a markdown file (content between ``` fences)."""
    matches = re.findall(r"```\n(.*?)```", content, re.DOTALL)
    return "\n\n---\n\n".join(matches) if matches else ""
