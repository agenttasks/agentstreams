# Agentic Prompt Engineering Patterns

Extracted from 30 prompt architectures observed in multi-agent AI systems.

## 1. Section Composition

**Used by**: 01 (Main System Prompt)

Assemble prompts dynamically from independent sections gated by feature flags,
user type, and environment variables. Place cacheable content above a boundary
marker and session-specific content below.

```
__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__
```

**Pattern**: Each section is a pure function (`getActionsSection()`) returning
a string. The orchestrator concatenates them with cache scope annotations.

## 2. XML Task Notifications

**Used by**: 05 (Coordinator)

Structured inter-agent communication using XML envelopes:

```xml
<task-notification>
  <task-id>{agentId}</task-id>
  <status>completed|failed|killed</status>
  <summary>{human-readable outcome}</summary>
  <result>{agent's final response}</result>
  <usage>
    <total_tokens>N</total_tokens>
    <tool_uses>N</tool_uses>
    <duration_ms>N</duration_ms>
  </usage>
</task-notification>
```

**Key insight**: Results arrive as user-role messages. Distinguish them by the
`<task-notification>` opening tag, not by message role.

## 3. Forced Tool Schemas

**Used by**: 12 (Auto-Mode Classifier), 14 (Tool Use Summary), 20 (Session Title)

Force structured output by defining a tool schema and using `tool_choice`:

```json
{
  "name": "classify_result",
  "input_schema": {
    "properties": {
      "thinking": {"type": "string"},
      "shouldBlock": {"type": "boolean"},
      "reason": {"type": "string"}
    }
  }
}
```

**Anti-injection**: Exclude assistant text blocks from the classifier transcript
to prevent the model from crafting text that influences its own classification.

## 4. Adversarial Verification

**Used by**: 07 (Verification Agent)

Design verifiers to **break** implementations, not confirm them. Key elements:

- **Rationalization guards**: List common excuses ("the code looks correct based
  on my reading") and instruct the model to recognize and resist them
- **Evidence requirements**: Every PASS must have a Command run block with actual
  terminal output — no narration without execution
- **Adversarial probes**: Concurrency, boundary values, idempotency, orphan operations
- **Verdict protocol**: PASS / FAIL / PARTIAL (PARTIAL only for environmental limits)

## 5. Read-Only Enforcement

**Used by**: 07 (Verification), 08 (Explore)

Prevent file modifications via explicit tool denylists:

```
Denied: Agent, Edit, Write, NotebookEdit
Allowed: Read, Glob, Grep, Bash (read-only commands only)
```

**Reinforcement**: State the constraint in multiple places — heading, body,
and critical reminder block.

## 6. Synthesis Before Delegation

**Used by**: 05 (Coordinator)

The coordinator must understand research findings before directing workers.
Anti-patterns to reject:

- "Based on your findings, fix the bug" — lazy delegation
- "The worker found an issue, please fix it" — no specifics

Good pattern: Include file paths, line numbers, and exact changes:

```
Fix the null pointer in src/auth/validate.ts:42. The user field on Session
(src/auth/types.ts:15) is undefined when sessions expire. Add a null check
before user.id access.
```

## 7. Cache-Aware Pacing

**Used by**: 18 (Proactive Mode)

Balance sleep duration against prompt cache expiry (5 minutes):

- **Too short**: Excessive API calls burn tokens
- **Too long**: Cache expires, next call pays full prefill cost
- **Rule**: If idle, call Sleep tool — never output status-only messages

## 8. Anti-Narration

**Used by**: 18 (Proactive Mode), 01 (Main System, internal)

Explicitly prohibit play-by-play output:

```
Do not narrate each step, list every file you read, or explain routine actions.
If you can say it in one sentence, don't use three.
```

**Focus text output on**: Decisions needing user input, milestone status updates,
errors or blockers that change the plan.

## 9. Memory Hierarchy

**Used by**: 24 (Memory Instruction), 27 (Remember Skill)

Layered memory with precedence:

1. **Managed memory** (system-controlled)
2. **User memory** (`~/.claude/CLAUDE.md`)
3. **Project memory** (`CLAUDE.md` in repo root)
4. **Local memory** (`CLAUDE.local.md`)

Features: `@include` directives with circular reference prevention,
YAML frontmatter with path globbing, `MAX_INCLUDE_DEPTH=5`.

## 10. Three-Agent Parallel Review

**Used by**: 19 (Simplify Skill)

Fan out to three specialized reviewers in parallel:

| Agent | Focus |
|-------|-------|
| Code Reuse | Duplicated logic, existing utilities, redundant patterns |
| Code Quality | Naming, decomposition, CLAUDE.md compliance, code smells |
| Efficiency | Allocations, N+1 queries, concurrency opportunities |

Aggregate, deduplicate, skip false positives, apply fixes, report summary.

## 11. Interview-Based Skill Creation

**Used by**: 25 (Skillify)

Structured multi-question interview to capture workflows:

1. What process to capture
2. Trigger conditions
3. Steps involved
4. Tools and commands
5. Expected outcome
6. Constraints and edge cases

Output: SKILL.md with YAML frontmatter in `.claude/skills/`.

## 12. Focus-Based Autonomy

**Used by**: 18 (Proactive Mode)

Modulate autonomous behavior based on terminal focus state:

- **Unfocused**: User is away — make decisions, explore, commit, push
- **Focused**: User is watching — surface choices, ask before large changes

## 13. Compaction with Analysis Scratchpad

**Used by**: 21 (Compact Service)

When summarizing context, use `<analysis>` tags as a drafting scratchpad.
The analysis is stripped by `formatCompactSummary()` before reaching context.
Nine required summary sections cover request intent, technical concepts,
files, errors, problem solving, user messages, pending tasks, current work,
and optional next step.

## 14. Tick-Based Keep-Alive

**Used by**: 18 (Proactive Mode)

Instead of polling, use `<tick>` messages as heartbeats:

```xml
<tick>2026-04-07T14:30:00-07:00</tick>
```

Multiple ticks may be batched. Process only the latest one.
The time is the user's local time — external tool timestamps may differ.

## 15. Continue vs Spawn Decision Matrix

**Used by**: 05 (Coordinator)

| Situation | Action | Why |
|-----------|--------|-----|
| Research explored target files | Continue | Worker has files in context |
| Broad research, narrow implementation | Spawn fresh | Avoid exploration noise |
| Correcting a failure | Continue | Worker has error context |
| Verifying another's code | Spawn fresh | Fresh eyes, no assumptions |
| Wrong approach entirely | Spawn fresh | Avoid anchoring on failed path |
