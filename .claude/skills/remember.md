---
name: remember
description: "Organize auto-memory entries into structured CLAUDE.md and CLAUDE.local.md files"
trigger: "user asks to organize memories, promote auto-memory, or clean up CLAUDE.md files"
---

Review auto-memory entries and organize them into the appropriate memory files.

## Memory File Hierarchy

- `CLAUDE.md` (project root): Shared with team, checked into version control
- `CLAUDE.local.md` (project root): Private project-specific, git-ignored
- `~/.claude/CLAUDE.md`: Private global instructions across all projects

## Process

1. Read current auto-captured memories (MEMORY.md or equivalent)
2. Read existing CLAUDE.md and CLAUDE.local.md files
3. For each entry, determine:
   - Is this relevant enough to keep permanently?
   - Should it be shared (CLAUDE.md) or private (CLAUDE.local.md)?
   - Does a similar instruction already exist?
4. Propose organized changes
5. Apply after user confirmation

## Guidelines

- Deduplicate entries that capture the same instruction
- Merge related entries into coherent instructions
- Preserve the user's original intent and wording
- Remove entries too session-specific for long-term use
- Format as clear, actionable instructions
