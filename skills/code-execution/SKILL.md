---
name: code-execution
description: "Sandboxed code execution, computer use, and tool-based automation with Claude. TRIGGER when: user asks to run code in a sandbox, use computer use (screenshots, mouse, keyboard), execute bash commands via the API, build tool-use agents that execute code, or set up sandboxed environments for Claude. Also triggers for server tools, code execution tool configuration, or computer use automation. DO NOT TRIGGER for: API client generation (use api-client), web crawling (use crawl-ingest), or data pipeline orchestration (use data-pipeline)."
---

# Code Execution: Sandboxed Code & Computer Use Skill

Build agents that execute code in sandboxed environments, automate desktop/browser tasks with computer use, and run bash commands — using Claude's built-in tool types (code execution tool, computer use tool, bash tool, server tools) across TypeScript, Python, or cURL.

## Defaults

- Use `claude-sonnet-4-6` for code execution tasks, `claude-opus-4-6` for complex multi-step automation
- Use `claude-mythos-preview` for vulnerability detection and exploit analysis (partner-only)
- Always sandbox code execution — never run untrusted code on host
- Computer use requires `anthropic-beta: computer-use-2025-01-24` header
- Default container: E2B, Modal, or Docker for sandboxed execution
- Max execution timeout: 30 seconds for code execution tool, configurable for bash

---

## Tool Selection

Before reading setup docs, determine which tool type the user needs:

1. **Code Execution Tool** — Run Python/JS in Anthropic's managed sandbox
   - Best for: data analysis, visualization, file processing, calculations
   - No setup needed — built into the API
   - Read from `shared/code-execution-tool.md`

2. **Computer Use Tool** — Control mouse, keyboard, screenshots
   - Best for: browser automation, GUI testing, desktop apps
   - Requires beta header and display server
   - Read from `shared/computer-use-tool.md`

3. **Bash Tool** — Execute shell commands
   - Best for: system admin, CI/CD, file operations, build scripts
   - Requires sandboxing (Docker, VM, or container)
   - Read from `shared/bash-tool.md`

4. **Server Tools** — Claude-hosted tools (web search, code execution)
   - Best for: quick prototyping without tool implementation
   - No client-side implementation needed
   - Read from `shared/server-tools.md`

---

## Core Capabilities by Tool Type

| Capability | Code Execution | Computer Use | Bash Tool | Server Tools |
|---|---|---|---|---|
| **Sandbox** | Anthropic-managed | User-managed VM | User-managed container | Anthropic-managed |
| **Languages** | Python, JavaScript | N/A (GUI) | Any shell | Python |
| **File I/O** | Yes (sandbox fs) | Yes (host fs) | Yes (container fs) | Limited |
| **Network** | Restricted | Full (in VM) | Configurable | Restricted |
| **Timeout** | 30s default | Per-action | Configurable | Per-request |
| **Beta header** | No | Yes | Yes | No |

---

## Workflow

### 1. Code Execution Tool (Managed Sandbox)

```
User Request
      │
      ▼
┌──────────────────┐
│ Claude Generates  │ ← Writes Python/JS code
│ Code              │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Sandbox Executes  │ ← Anthropic-managed, isolated
│ Code              │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Return Results    │ ← stdout, stderr, files, images
│                   │
└──────────────────┘
```

### 2. Computer Use (Desktop/Browser Automation)

```
User Request
      │
      ▼
┌──────────────────┐
│ Claude Observes   │ ← Takes screenshot of display
│ Screen            │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Claude Plans      │ ← Identifies UI elements, plans actions
│ Actions           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Execute Action    │ ← mouse_move, click, type, screenshot
│                   │
└────────┬─────────┘
         │
         ▼
   (loop back to observe)
```

### 3. Bash Tool (Shell Execution)

```
User Request
      │
      ▼
┌──────────────────┐
│ Claude Generates  │ ← Writes shell command
│ Command           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Container Runs    │ ← Docker/VM, resource-limited
│ Command           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Return Output     │ ← stdout, stderr, exit code
│                   │
└──────────────────┘
```

---

## Safety Patterns

### Sandboxing Requirements

- **Code execution tool**: Anthropic-managed, no additional sandboxing needed
- **Bash tool**: MUST run in container/VM — never on host
- **Computer use**: Run in headless VM with no access to sensitive data
- **Server tools**: Anthropic-managed, no additional sandboxing needed

### Resource Limits

- CPU: 1-2 cores per sandbox
- Memory: 512MB-2GB per sandbox
- Disk: 1GB ephemeral storage
- Network: Restricted or disabled for untrusted code
- Timeout: Enforce per-execution limits

### Input Validation

- Never pass user input directly to `eval()` or `exec()`
- Sanitize file paths to prevent directory traversal
- Validate command arguments before shell execution
- Use allowlists for permitted commands when possible
