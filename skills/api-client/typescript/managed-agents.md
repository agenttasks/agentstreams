# Managed Agents — TypeScript

## Installation

```bash
npm install @anthropic-ai/sdk
```

The `@anthropic-ai/sdk` includes full Managed Agents support via `client.beta.agents`, `client.beta.environments`, `client.beta.sessions`, and `client.beta.sessions.events`.

## Quick Start

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// 1. Create an agent
const agent = await client.beta.agents.create({
  name: "Coding Assistant",
  model: "claude-sonnet-4-6",
  system: "You are a helpful coding assistant.",
  tools: [{ type: "agent_toolset_20260401" }],
});

// 2. Create an environment
const environment = await client.beta.environments.create({
  name: "node-dev",
  config: {
    type: "cloud",
    packages: { npm: ["express", "zod"] },
    networking: { type: "unrestricted" },
  },
});

// 3. Start a session
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  title: "My first session",
});

// 4. Stream events
const stream = await client.beta.sessions.events.stream(session.id);

await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.message",
      content: [
        { type: "text", text: "Create an Express API with health check endpoint" },
      ],
    },
  ],
});

for await (const event of stream) {
  if (event.type === "agent.message") {
    for (const block of event.content) {
      process.stdout.write(block.text);
    }
  } else if (event.type === "agent.tool_use") {
    console.log(`\n[Using tool: ${event.name}]`);
  } else if (event.type === "session.status_idle") {
    console.log("\n\nAgent finished.");
    break;
  }
}
```

## Custom Tools

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Define agent with custom tool
const agent = await client.beta.agents.create({
  name: "Weather Agent",
  model: "claude-sonnet-4-6",
  tools: [
    { type: "agent_toolset_20260401" },
    {
      type: "custom",
      name: "get_weather",
      description: "Get current weather for a location",
      input_schema: {
        type: "object",
        properties: {
          location: { type: "string", description: "City name" },
        },
        required: ["location"],
      },
    },
  ],
});

const env = await client.beta.environments.create({
  name: "weather-env",
  config: { type: "cloud", networking: { type: "unrestricted" } },
});

const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: env.id,
});

// Stream and handle custom tool calls
const stream = await client.beta.sessions.events.stream(session.id);

await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.message",
      content: [{ type: "text", text: "What's the weather in Tokyo?" }],
    },
  ],
});

for await (const event of stream) {
  if (event.type === "agent.message") {
    for (const block of event.content) {
      process.stdout.write(block.text);
    }
  } else if (event.type === "agent.custom_tool_use") {
    // Execute your custom tool
    const result = `72°F and sunny in ${event.input.location}`;

    await client.beta.sessions.events.send(session.id, {
      events: [
        {
          type: "user.custom_tool_result",
          custom_tool_use_id: event.id,
          content: [{ type: "text", text: result }],
          is_error: false,
        },
      ],
    });
  } else if (event.type === "session.status_idle") {
    break;
  }
}
```

## Disable Specific Tools

```typescript
const agent = await client.beta.agents.create({
  name: "Read-Only Auditor",
  model: "claude-opus-4-6",
  tools: [
    {
      type: "agent_toolset_20260401",
      default_config: { enabled: false },
      configs: [
        { name: "bash", enabled: true },
        { name: "read", enabled: true },
        { name: "glob", enabled: true },
        { name: "grep", enabled: true },
      ],
    },
  ],
});
```

## MCP Servers

```typescript
const agent = await client.beta.agents.create({
  name: "GitHub Assistant",
  model: "claude-sonnet-4-6",
  mcp_servers: [
    {
      type: "url",
      name: "github",
      url: "https://api.githubcopilot.com/mcp/",
    },
  ],
  tools: [
    { type: "agent_toolset_20260401" },
    { type: "mcp_toolset", mcp_server_name: "github" },
  ],
});

// Provide auth at session creation via vault
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  vault_ids: ["vault_xxx"],
});
```

## Pin Agent Version

```typescript
const session = await client.beta.sessions.create({
  agent: { type: "agent", id: agent.id, version: 1 },
  environment_id: environment.id,
});
```

## Mount GitHub Repository

```typescript
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  resources: [
    {
      type: "github_repository",
      url: "https://github.com/org/repo",
      authorization_token: "ghp_xxx",
      checkout: { type: "branch", name: "main" },
    },
  ],
});
```

## Limited Networking

```typescript
const env = await client.beta.environments.create({
  name: "restricted-env",
  config: {
    type: "cloud",
    networking: {
      type: "limited",
      allowed_hosts: ["api.example.com"],
      allow_mcp_servers: true,
      allow_package_managers: true,
    },
  },
});
```

## Agent Lifecycle

```typescript
// Update agent (creates new version)
const updated = await client.beta.agents.update(agent.id, {
  version: agent.version,
  system: "Updated system prompt with new instructions.",
});
console.log(`New version: ${updated.version}`);

// List versions
for await (const version of client.beta.agents.versions.list(agent.id)) {
  console.log(`Version ${version.version}: ${version.updated_at}`);
}

// Archive (read-only, no new sessions)
await client.beta.agents.archive(agent.id);
```

## Session Management

```typescript
// List sessions
for await (const session of client.beta.sessions.list()) {
  console.log(`${session.id}: ${session.status}`);
}

// Interrupt
await client.beta.sessions.events.send(session.id, {
  events: [{ type: "user.interrupt" }],
});

// Multi-turn follow-up
await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.message",
      content: [{ type: "text", text: "Now add error handling" }],
    },
  ],
});

// Archive
await client.beta.sessions.archive(session.id);

// Delete
await client.beta.sessions.delete(session.id);
```

## Fast Mode (Opus)

```typescript
const agent = await client.beta.agents.create({
  name: "Fast Agent",
  model: { id: "claude-opus-4-6", speed: "fast" },
  tools: [{ type: "agent_toolset_20260401" }],
});
```
