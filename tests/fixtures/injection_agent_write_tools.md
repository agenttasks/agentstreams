---
name: Overprivileged Write Agent
description: Reads and extracts patterns from documentation
model: haiku
tools: Read, Write, Bash, Glob, Grep
---

This agent definition has write tools (Write, Bash) despite read-only intent.
It should be flagged by the agent boundary checker.
