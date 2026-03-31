# Bash Tool Reference

## Overview

The bash tool lets Claude execute shell commands. Unlike the code execution tool, bash runs in your environment — always sandbox it in a container or VM.

## Tool Definition

```json
{
  "type": "bash_20250124",
  "name": "bash"
}
```

**Required header**: `anthropic-beta: computer-use-2025-01-24`

## Request/Response

Claude sends:
```json
{
  "type": "tool_use",
  "name": "bash",
  "input": {
    "command": "ls -la /tmp"
  }
}
```

You return:
```json
{
  "type": "tool_result",
  "tool_use_id": "...",
  "content": "total 4\ndrwxrwxrwt 2 root root 4096 ...\n"
}
```

## Sandboxing (Required)

### Docker

```bash
docker run --rm \
  --memory=512m \
  --cpus=1 \
  --network=none \
  --read-only \
  --tmpfs /tmp:size=100m \
  python:3.12-slim \
  bash -c "COMMAND_HERE"
```

### Key restrictions

- `--network=none` — no network access
- `--read-only` — immutable filesystem
- `--memory=512m` — memory cap
- `--cpus=1` — CPU limit
- `--tmpfs /tmp` — writable temp only

## Combining with Computer Use

Bash and computer use tools can be used together in the same request. Claude will choose the appropriate tool for each step:

```json
{
  "tools": [
    {"type": "bash_20250124", "name": "bash"},
    {"type": "computer_20250124", "name": "computer", "display_width_px": 1920, "display_height_px": 1080}
  ]
}
```

## Safety

- **Never run bash on host** — always in container/VM
- **Allowlist commands** when possible
- **Set timeouts** — kill long-running commands
- **Log all commands** — audit trail for debugging
- **Restrict file access** — bind-mount only needed directories
