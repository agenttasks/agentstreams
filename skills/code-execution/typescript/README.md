# TypeScript Stack Setup

## Installation

```bash
# Initialize project
mkdir code-execution-project && cd code-execution-project
npm init -y

# Core Anthropic packages
npm install @anthropic-ai/sdk

# Sandbox providers
npm install @e2b/code-interpreter    # E2B managed sandbox

# Container management (Docker via API)
npm install dockerode                 # Docker SDK for Node.js

# Image handling (for computer use screenshots)
npm install sharp                     # Image processing

# Testing
npm install --save-dev vitest
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `@anthropic-ai/sdk` | 0.52.0 | Official TypeScript SDK — messages, tool use, beta features |
| `@e2b/code-interpreter` | 1.1.0 | E2B sandbox — run Python/JS with file I/O |
| `dockerode` | 4.0.4 | Docker SDK — container lifecycle, exec, logs |
| `sharp` | 0.33.5 | Image processing — screenshot handling for computer use |

## Quick Start: Code Execution Tool

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 4096,
  tools: [
    {
      type: "code_execution",
      name: "code_execution",
    },
  ],
  messages: [
    {
      role: "user",
      content: "Calculate the first 20 Fibonacci numbers and plot them",
    },
  ],
});

for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  } else if (block.type === "tool_use" && block.name === "code_execution") {
    console.log("Code:", block.input.code);
  }
}
```

## Computer Use with Screenshot Loop

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 4096,
  betas: ["computer-use-2025-01-24"],
  tools: [
    {
      type: "computer_20250124",
      name: "computer",
      display_width_px: 1920,
      display_height_px: 1080,
      display_number: 0,
    },
  ],
  messages: [
    {
      role: "user",
      content: "Open the browser and navigate to example.com",
    },
  ],
});

for (const block of response.content) {
  if (block.type === "tool_use" && block.name === "computer") {
    const { action, coordinate, text } = block.input as any;
    switch (action) {
      case "screenshot":
        // Take screenshot, return base64
        break;
      case "mouse_move":
        // Move mouse to coordinate
        break;
      case "left_click":
        // Click at current position
        break;
      case "type":
        // Type text
        break;
    }
  }
}
```

## Bash Tool in Docker Sandbox

```typescript
import Anthropic from "@anthropic-ai/sdk";
import Docker from "dockerode";

const client = new Anthropic();
const docker = new Docker();

// Create sandboxed container
const container = await docker.createContainer({
  Image: "node:20-slim",
  Tty: true,
  HostConfig: {
    Memory: 512 * 1024 * 1024, // 512MB
    CpuPeriod: 100000,
    CpuQuota: 100000, // 1 CPU
    NetworkMode: "none", // No network access
  },
});
await container.start();

async function executeBash(
  command: string
): Promise<{ exitCode: number; stdout: string; stderr: string }> {
  const exec = await container.exec({
    Cmd: ["bash", "-c", command],
    AttachStdout: true,
    AttachStderr: true,
  });
  const stream = await exec.start({ Detach: false });
  // Process stream for stdout/stderr
  return { exitCode: 0, stdout: "", stderr: "" };
}

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 4096,
  betas: ["computer-use-2025-01-24"],
  tools: [
    {
      type: "bash_20250124",
      name: "bash",
    },
  ],
  messages: [
    {
      role: "user",
      content: "List all TypeScript files and count lines of code",
    },
  ],
});

// Cleanup
await container.stop();
await container.remove();
```

## MCP SDK Availability

TypeScript MCP SDK: `@modelcontextprotocol/sdk` (npm) — build MCP servers that provide code execution as tools.

```bash
npm install @modelcontextprotocol/sdk
```
