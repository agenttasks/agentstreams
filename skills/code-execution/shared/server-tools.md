# Server Tools Reference

## Overview

Server tools are Claude-hosted tools that run on Anthropic's infrastructure. No client-side implementation needed — just declare the tool and Claude handles execution.

## Available Server Tools

### Code Execution (Server)

```json
{
  "type": "server_tool",
  "name": "code_execution"
}
```

Runs Python code on Anthropic's servers. Similar to the code execution tool but hosted server-side.

### Web Search (Server)

```json
{
  "type": "server_tool",
  "name": "web_search"
}
```

Searches the web and returns results. Claude can use this to find current information.

## Key Differences from Client Tools

| Aspect | Server Tools | Client Tools |
|--------|-------------|--------------|
| **Implementation** | Anthropic-hosted | You implement |
| **Setup** | None | Container/VM/sandbox |
| **Customization** | Limited | Full control |
| **Network** | Anthropic-managed | Your control |
| **Timeout** | Anthropic-managed | Your control |
| **Libraries** | Pre-installed set | Your choice |

## When to Use Server Tools

- **Prototyping** — quick iteration without sandbox setup
- **Simple tasks** — calculations, data analysis, web search
- **No infrastructure** — when you can't run containers

## When to Use Client Tools

- **Custom environments** — specific libraries, configurations
- **Security requirements** — your own sandbox, audit logging
- **Long-running tasks** — custom timeouts and resource limits
- **Network access** — controlled access to internal services
