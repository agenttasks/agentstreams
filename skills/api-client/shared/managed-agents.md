# Managed Agents API Reference

## Overview

Claude Managed Agents provides a pre-built, configurable agent harness running in managed infrastructure. Instead of building your own agent loop, tool execution, and runtime, you get a fully managed environment where Claude can read files, run commands, browse the web, and execute code securely.

**Beta header:** `managed-agents-2026-04-01` (set automatically by the SDK).

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Agent** | Model, system prompt, tools, MCP servers, and skills |
| **Environment** | Configured container template (packages, network access) |
| **Session** | Running agent instance within an environment |
| **Events** | Messages exchanged between your application and the agent |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/agents` | Create agent |
| GET | `/v1/agents/{id}` | Retrieve agent |
| POST | `/v1/agents/{id}` | Update agent (new version) |
| POST | `/v1/agents/{id}/archive` | Archive agent |
| GET | `/v1/agents/{id}/versions` | List agent versions |
| POST | `/v1/environments` | Create environment |
| GET | `/v1/environments/{id}` | Retrieve environment |
| POST | `/v1/environments/{id}/archive` | Archive environment |
| DELETE | `/v1/environments/{id}` | Delete environment |
| POST | `/v1/sessions` | Create session |
| GET | `/v1/sessions/{id}` | Retrieve session |
| POST | `/v1/sessions/{id}` | Update session |
| POST | `/v1/sessions/{id}/archive` | Archive session |
| DELETE | `/v1/sessions/{id}` | Delete session |
| POST | `/v1/sessions/{id}/events` | Send events |
| GET | `/v1/sessions/{id}/events` | List events |
| GET | `/v1/sessions/{id}/stream` | SSE event stream |

## Available Tools (agent_toolset_20260401)

| Tool | Name | Description |
|------|------|-------------|
| Bash | `bash` | Execute bash commands in a shell session |
| Read | `read` | Read a file from the local filesystem |
| Write | `write` | Write a file to the local filesystem |
| Edit | `edit` | Perform string replacement in a file |
| Glob | `glob` | Fast file pattern matching using glob patterns |
| Grep | `grep` | Text search using regex patterns |
| Web fetch | `web_fetch` | Fetch content from a URL |
| Web search | `web_search` | Search the web for information |

## Event Types

### User Events (you send)

| Type | Description |
|------|-------------|
| `user.message` | Text message with content blocks |
| `user.interrupt` | Stop the agent mid-execution |
| `user.custom_tool_result` | Response to custom tool call |
| `user.tool_confirmation` | Approve/deny tool call |

### Agent Events (you receive)

| Type | Description |
|------|-------------|
| `agent.message` | Agent text response |
| `agent.thinking` | Agent thinking content |
| `agent.tool_use` | Built-in tool invocation |
| `agent.tool_result` | Tool execution result |
| `agent.custom_tool_use` | Custom tool invocation (respond with `user.custom_tool_result`) |
| `agent.mcp_tool_use` | MCP tool invocation |

### Session Events

| Type | Description |
|------|-------------|
| `session.status_running` | Agent actively processing |
| `session.status_idle` | Agent waiting for input |
| `session.status_rescheduled` | Transient error, retrying |
| `session.status_terminated` | Unrecoverable error |
| `session.error` | Error with retry_status |

### Span Events (observability)

| Type | Description |
|------|-------------|
| `span.model_request_start` | Model inference started |
| `span.model_request_end` | Model inference completed (includes token counts) |

## Networking Modes

| Mode | Description |
|------|-------------|
| `unrestricted` | Full outbound access (default) |
| `limited` | Restrict to `allowed_hosts` list |

## Package Managers

| Field | Manager | Example |
|-------|---------|---------|
| `apt` | System (apt-get) | `"ffmpeg"` |
| `cargo` | Rust | `"ripgrep@14.0.0"` |
| `gem` | Ruby | `"rails:7.1.0"` |
| `go` | Go modules | `"golang.org/x/tools/cmd/goimports@latest"` |
| `npm` | Node.js | `"express@4.18.0"` |
| `pip` | Python | `"pandas==2.2.0"` |

## Session Statuses

| Status | Description |
|--------|-------------|
| `idle` | Waiting for input (initial state) |
| `running` | Actively executing |
| `rescheduling` | Transient error, retrying |
| `terminated` | Unrecoverable error |

## Supported Models

- `claude-opus-4-6` — Most intelligent
- `claude-sonnet-4-6` — Best speed/intelligence balance
- `claude-haiku-4-5` — Fastest

For fast mode: `{"id": "claude-opus-4-6", "speed": "fast"}`

## Rate Limits

| Operation | Limit |
|-----------|-------|
| Create endpoints | 60 req/min |
| Read endpoints | 600 req/min |
