---
name: agentic-prompts
description: "Structured prompt engineering patterns from multi-agent AI system architectures — 30 prompt types with XML task rendering"
---

# Agentic Prompts Skill

## Overview

Structured prompt engineering patterns extracted from multi-agent AI system architectures.
Provides a catalog of 30 prompt types spanning system prompts, agent prompts, tool prompts,
and skill prompts — each with XML task rendering for programmatic consumption.

## Defaults

| Setting | Value |
|---------|-------|
| Tier 1 | Python |
| Tier 3 | cURL |
| Source | `vendors/agentic-ai-prompt-research/prompts/` |
| Registry | `scripts/prompt_registry.py` |
| Renderer | `scripts/render_prompts.py` |

## Prompt Categories

### System Prompts (10)

Core behavioral instructions that define agent identity, boundaries, and operating modes.

| ID | Name | Purpose |
|----|------|---------|
| 01 | Main System Prompt | Dynamic master prompt assembled from sections |
| 02 | Simple Mode | Minimal stripped-down prompt for basic contexts |
| 04 | Cyber Risk Instruction | Security boundary definitions |
| 06 | Teammate Addendum | Inter-agent communication protocol |
| 12 | Auto-Mode Classifier | 2-stage security classification for tool approval |
| 15 | Session Search | Semantic search across past conversations |
| 18 | Proactive Mode | Autonomous agent with tick-based keep-alive |
| 21 | Compact Service | Context window summarization on limit approach |
| 23 | Chrome Browser Automation | Browser automation via MCP extension |
| 24 | Memory Instruction | CLAUDE.md memory file hierarchy |

### Agent Prompts (5)

Specialized agent configurations for delegated task execution.

| ID | Name | Purpose |
|----|------|---------|
| 03 | Default Agent | Base prompt for all sub-agents |
| 05 | Coordinator | Multi-worker orchestration with synthesis phases |
| 07 | Verification Agent | Adversarial testing specialist (read-only) |
| 08 | Explore Agent | Fast read-only codebase search |
| 09 | Agent Creation Architect | Meta-agent that designs new agent configs |

### Tool Prompts (8)

Guidance embedded in tool schemas for specific tool behaviors.

| ID | Name | Purpose |
|----|------|---------|
| 11 | Permission Explainer | Risk-level explanation before tool approval |
| 13 | Tool Prompts | Compendium of tool-specific guidance |
| 14 | Tool Use Summary | Git-commit-style labels for tool calls |
| 16 | Memory Selection | Semantic matching for relevant memory files |
| 17 | Auto-Mode Critique | Quality review of classifier rules |
| 20 | Session Title | Concise session title generation |
| 22 | Away Summary | "While you were away" recap |
| 29 | Agent Summary | 1-sentence progress updates for sub-agents |
| 30 | Prompt Suggestion | Predict next likely user command |

### Skill Prompts (6)

Reusable workflow definitions invoked via slash commands.

| ID | Name | Purpose |
|----|------|---------|
| 10 | Statusline Setup | Configure terminal status line |
| 19 | Simplify | 3-agent parallel code review on recent changes |
| 25 | Skillify | Interview-based skill creation |
| 26 | Stuck | Diagnostic for frozen sessions (internal) |
| 27 | Remember | Organize auto-memory into structured files |
| 28 | Update Config | Manage settings.json hooks and permissions |

## XML Task Format

All prompts can be rendered as structured XML tasks via `scripts/render_prompts.py`:

```xml
<task id="07" type="agent" name="verification-agent">
  <purpose>Adversarial testing specialist that tries to break implementations</purpose>
  <constraints>
    <constraint>Read-only — no file modifications in project directory</constraint>
    <constraint>Must end with VERDICT: PASS, FAIL, or PARTIAL</constraint>
  </constraints>
  <tools allowed="Bash,Read,Glob,Grep" denied="Edit,Write,Agent,NotebookEdit"/>
  <output format="structured">
    <section name="check">Command run + Output observed + Result</section>
    <verdict options="PASS,FAIL,PARTIAL"/>
  </output>
</task>
```

## Integration Points

- **Agent manifests**: `.claude/agents/` — coordinator, verification, explore, agent-architect, default-agent, statusline-setup, proactive, browser-automation
- **Skill manifests**: `.claude/skills/` — simplify-review, skillify, prompt-suggest, remember, update-config, stuck-diagnostic, away-summary, auto-mode-critique
- **Prompt registry**: `scripts/prompt_registry.py` — catalog with metadata
- **Prompt renderer**: `scripts/render_prompts.py` — XML task emission
- **Apply runner**: `scripts/apply_prompts.py` — loop through all 30 with integration manifest
- **Validation**: `tests/test_render_prompts.py` — schema and rendering tests

## Key Patterns

See `shared/prompt-patterns.md` for the full pattern catalog:

1. **Section composition** — Dynamic assembly from feature-flagged sections
2. **XML task notifications** — Structured inter-agent communication
3. **Forced tool schemas** — Structured output via tool_choice
4. **Adversarial verification** — Break-it mindset with rationalization guards
5. **Read-only enforcement** — Tool denylists for safe exploration
6. **Cache-aware pacing** — Sleep duration vs 5-minute cache expiry
7. **Anti-narration** — Explicit prohibition of play-by-play output
8. **Memory hierarchy** — Layered CLAUDE.md with @include directives

## Further Reading

- `shared/prompt-patterns.md` — Full pattern catalog with examples
- `shared/xml-task-schema.md` — XML task format specification
- `shared/security-boundaries.md` — Security control matrix from prompt 04
- `shared/compaction-patterns.md` — Context window summarization from prompt 21
- `shared/team-communication.md` — Inter-agent communication from prompt 06
- `shared/tool-best-practices.md` — Canonical tool usage guidance from prompt 13
- `references/prompt-catalog.md` — Quick-reference table of all 30 prompts
- `vendors/agentic-ai-prompt-research/README.md` — Source research repository
