# Python Stack Setup

## Installation (uv)

```bash
# Initialize project
uv init code-execution-project && cd code-execution-project

# Core Anthropic packages
uv add anthropic

# Sandbox providers
uv add e2b-code-interpreter==1.1.0   # E2B managed sandbox
uv add modal==0.73.0                  # Modal serverless execution

# Container management
uv add docker==7.1.0                  # Docker SDK for Python

# Image handling (for computer use screenshots)
uv add pillow==11.1.0

# Testing
uv add --dev pytest==8.4.0
uv add --dev pytest-asyncio==0.25.3
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | 0.87.0 | Official Python SDK — messages, tool use, beta features |
| `e2b-code-interpreter` | 1.1.0 | E2B sandbox — run Python/JS with file I/O |
| `modal` | 0.73.0 | Modal serverless — GPU, long-running, custom images |
| `docker` | 7.1.0 | Docker SDK — container lifecycle, exec, logs |
| `pillow` | 11.1.0 | Image processing — screenshot handling for computer use |

## Quick Start: Code Execution Tool

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    tools=[
        {
            "type": "code_execution",
            "name": "code_execution",
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Calculate the first 20 Fibonacci numbers and plot them",
        }
    ],
)

# Process results — code execution returns text and images
for block in response.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "tool_use" and block.name == "code_execution":
        print(f"Code: {block.input.get('code', '')}")
    elif block.type == "tool_result":
        for item in block.content:
            if item.get("type") == "image":
                print(f"Generated image: {item['source']['media_type']}")
```

## Computer Use with Screenshot Loop

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Computer use requires beta header
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["computer-use-2025-01-24"],
    tools=[
        {
            "type": "computer_20250124",
            "name": "computer",
            "display_width_px": 1920,
            "display_height_px": 1080,
            "display_number": 0,
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Open the browser and navigate to example.com",
        }
    ],
)

# Process computer use actions
for block in response.content:
    if block.type == "tool_use" and block.name == "computer":
        action = block.input.get("action")
        if action == "screenshot":
            # Take screenshot, return as base64
            pass
        elif action == "mouse_move":
            x, y = block.input["coordinate"]
            # Move mouse to (x, y)
        elif action == "left_click":
            # Click at current position
            pass
        elif action == "type":
            text = block.input["text"]
            # Type text
```

## Bash Tool in Docker Sandbox

```python
import anthropic
import docker

client = anthropic.Anthropic()
docker_client = docker.from_env()

# Create sandboxed container
container = docker_client.containers.run(
    "python:3.12-slim",
    detach=True,
    tty=True,
    mem_limit="512m",
    cpu_period=100000,
    cpu_quota=100000,  # 1 CPU
    network_mode="none",  # No network access
)

def execute_bash(command: str) -> dict:
    """Execute a command in the sandboxed container."""
    exit_code, output = container.exec_run(
        ["bash", "-c", command],
        demux=True,
    )
    stdout = output[0].decode() if output[0] else ""
    stderr = output[1].decode() if output[1] else ""
    return {"exit_code": exit_code, "stdout": stdout, "stderr": stderr}

# Use bash tool with Claude
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["computer-use-2025-01-24"],
    tools=[
        {
            "type": "bash_20250124",
            "name": "bash",
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "List all Python files and count lines of code",
        }
    ],
)

# Process bash commands from Claude
for block in response.content:
    if block.type == "tool_use" and block.name == "bash":
        command = block.input.get("command", "")
        result = execute_bash(command)
        print(f"$ {command}")
        print(result["stdout"])

# Cleanup
container.stop()
container.remove()
```

## Server Tools (No Client Implementation Needed)

```python
import anthropic

client = anthropic.Anthropic()

# Server tools are hosted by Anthropic — no implementation needed
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    tools=[
        {
            "type": "server_tool",
            "name": "code_execution",
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Write and run a Python script to analyze this CSV data",
        }
    ],
)
```

## MCP SDK Availability

Python MCP SDK: `mcp` (PyPI) — build MCP servers that provide code execution as tools.

```bash
uv add mcp
```
