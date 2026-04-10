---
name: simplify-review
description: "Three-agent parallel code review on recent changes: reuse, quality, and efficiency"
trigger: "user asks to simplify, review, or clean up recent code changes before committing"
context: fork
---

Review recent changes using three parallel perspectives:

## Phase 1: Change Detection

Run `git diff` (or `git diff HEAD` for staged changes) to identify the scope.

## Phase 2: Three-Agent Review

Spawn three agents in parallel, each receiving the full diff:

### Code Reuse Agent
- Duplicated logic that could be extracted
- Existing utilities that should be used instead of new code
- Redundant patterns

### Code Quality Agent
- Naming consistency and readability
- Function decomposition and control flow clarity
- Compliance with CLAUDE.md standards
- Code smells: leaky abstractions, unnecessary nesting, over-engineering

### Efficiency Agent
- Unnecessary allocations and redundant computations
- N+1 query patterns
- Missed concurrency opportunities

## Phase 3: Aggregation

1. Aggregate and deduplicate findings
2. Skip false positives
3. Apply fixes directly
4. Report summary to user
