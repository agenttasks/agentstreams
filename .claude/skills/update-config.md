---
name: update-config
description: "Manage settings.json configuration including hooks, permissions, and general settings"
trigger: "user asks to configure hooks, update permissions, modify settings.json, or change Claude Code behavior"
---

Manage Claude Code `settings.json` configuration files.

## Settings Hierarchy (highest to lowest priority)

1. **Project**: `.claude/settings.json` (checked into repo)
2. **User**: `~/.claude/settings.json` (private, all projects)
3. **Enterprise**: `/etc/claude-code/settings.json` (managed by admins)

## Hook System

Hooks run at specific lifecycle points:

| Hook | When | Can Block? |
|------|------|-----------|
| PreToolUse | Before tool execution | Yes (exit 2) |
| PostToolUse | After tool completes | No |
| PreCompact | Before conversation compaction | No |
| PostCompact | After conversation compaction | No |
| Notification | When Claude wants to notify user | No |
| Stop | When Claude's turn ends | No |

Hooks receive JSON on stdin with: session_id, tool_name, tool_input, tool_output.

**Exit codes**: 0 = success, 2 = block tool (PreToolUse only), other = log error and continue.

## Permission Arrays

- `allowedTools`: Tool names/patterns that are auto-approved
- `deniedTools`: Tool names/patterns that are always blocked
- `trust`: Trust levels for tool categories

## Process

1. Determine which settings level to modify (project/user)
2. Read the current settings.json
3. Apply the requested changes
4. Validate JSON syntax after editing
5. Report what was changed
