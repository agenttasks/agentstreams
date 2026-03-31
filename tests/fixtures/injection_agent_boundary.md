---
name: Overprivileged Test Agent
description: Reads and analyzes crawled data for patterns
model: haiku
---

This agent definition intentionally has NO tools restriction.
It should be flagged by the agent boundary checker because:
1. Description says "reads and analyzes" (read-only intent)
2. No tools field = defaults to all tools (dangerous)
