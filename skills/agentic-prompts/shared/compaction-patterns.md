# Compaction Patterns

Extracted from prompt 21 (Compact Service). Strategies for summarizing conversations
when context window approaches limits.

## Three Compaction Modes

### Full Compaction
Summarize the entire conversation. Used when everything must be compressed.

### Partial Compaction (Recent)
Summarize only recent messages while older context is retained intact.
Focus on what was discussed, learned, and accomplished recently.

### Partial Compaction (Older)
Summarize older messages to make room, keeping newer messages intact.
The summary is placed at the start of continuing context.

## Required Summary Sections

Every compaction summary must include these nine sections:

1. **Primary Request and Intent** — All explicit user requests and intents
2. **Key Technical Concepts** — Technologies, frameworks, patterns discussed
3. **Files and Code Sections** — Files examined/modified/created with full code snippets
4. **Errors and Fixes** — Errors encountered and resolution steps
5. **Problem Solving** — Solved problems and ongoing troubleshooting
6. **All User Messages** — Every non-tool-result user message (tracks intent drift)
7. **Pending Tasks** — Outstanding work items
8. **Current Work** — Precise description of work in progress
9. **Optional Next Step** — Only if directly aligned with recent requests

## Analysis Scratchpad

Use `<analysis>` tags as a drafting scratchpad before the `<summary>`.
The analysis is stripped before reaching context:

```xml
<analysis>
1. Chronologically analyze each message
2. Identify explicit requests and intents
3. Note key decisions and code patterns
4. Capture file names, code snippets, function signatures
5. Record errors and fixes
6. Double-check for technical accuracy
</analysis>

<summary>
## Primary Request and Intent
...
</summary>
```

## Critical Constraint: No Tool Calls

Compaction prompts must include a no-tools preamble:

```
CRITICAL: Respond with TEXT ONLY. Do NOT call any tools.
Tool calls will be REJECTED and will waste your only turn.
Your entire response must be plain text: an <analysis> block
followed by a <summary> block.
```

This is critical when the compaction runs in a cache-sharing fork that
inherits the parent's full tool set.

## Integration with agentstreams

The compaction pattern applies to any long-running agent workflow:
- Multi-skill crawl-ingest pipelines that accumulate large contexts
- Iterative eval runs with progressively more test results
- Extended code review sessions across many files
