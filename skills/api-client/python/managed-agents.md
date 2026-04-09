# Managed Agents — Python

## Installation

```bash
uv add anthropic
```

The `anthropic` SDK (v0.86+) includes full Managed Agents support via `client.beta.agents`, `client.beta.environments`, `client.beta.sessions`, and `client.beta.sessions.events`.

## Quick Start

```python
from anthropic import Anthropic

client = Anthropic()

# 1. Create an agent
agent = client.beta.agents.create(
    name="Coding Assistant",
    model="claude-sonnet-4-6",
    system="You are a helpful coding assistant.",
    tools=[{"type": "agent_toolset_20260401"}],
)

# 2. Create an environment
environment = client.beta.environments.create(
    name="python-dev",
    config={
        "type": "cloud",
        "packages": {"pip": ["pandas", "numpy"]},
        "networking": {"type": "unrestricted"},
    },
)

# 3. Start a session
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="My first session",
)

# 4. Stream events
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{
            "type": "user.message",
            "content": [{"type": "text", "text": "Write a fibonacci script"}],
        }],
    )

    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    print(block.text, end="")
            case "agent.tool_use":
                print(f"\n[Using tool: {event.name}]")
            case "session.status_idle":
                print("\n\nAgent finished.")
                break
```

## AgentStreams Wrapper

The `src/managed_agents.py` module provides typed dataclasses and a high-level client:

```python
from src.managed_agents import (
    ManagedAgentsClient,
    ManagedAgentConfig,
    EnvironmentConfig,
    Packages,
    AgentMessageEvent,
    SessionStatus,
    SessionStatusEvent,
    coding_agent,
    data_analysis_env,
)

client = ManagedAgentsClient()

# Use factory functions for common configurations
agent_id = client.create_agent(coding_agent())
env_id = client.create_environment(data_analysis_env())

# Start session and stream
session_id = client.create_session(agent_id, env_id)
client.send_message(session_id, "Analyze the data in /data/sales.csv")

for event in client.stream_events(session_id):
    if isinstance(event, AgentMessageEvent):
        print(event.text, end="")
    elif isinstance(event, SessionStatusEvent):
        if event.status == SessionStatus.IDLE:
            break
```

## Custom Tools

```python
from src.managed_agents import (
    ManagedAgentsClient,
    ManagedAgentConfig,
    CustomTool,
    EnvironmentConfig,
)

client = ManagedAgentsClient()

# Define agent with custom tool
config = ManagedAgentConfig(
    name="Weather Agent",
    model="claude-sonnet-4-6",
    custom_tools=[
        CustomTool(
            name="get_weather",
            description="Get current weather for a location",
            input_schema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                },
                "required": ["location"],
            },
        ),
    ],
)

agent_id = client.create_agent(config)
env_id = client.create_environment(EnvironmentConfig(name="weather-env"))
session_id = client.create_session(agent_id, env_id)

# Handle custom tool calls automatically
def get_weather(input: dict) -> str:
    return f"72°F and sunny in {input['location']}"

events = client.run_with_custom_tools(
    session_id,
    "What's the weather in San Francisco?",
    tool_handlers={"get_weather": get_weather},
)
```

## Managed Harness (Pipeline Bridge)

Run orchestrator pipelines in cloud containers:

```python
import asyncio
from src.managed_harness import ManagedOrchestrator

async def main():
    # Auto-register local agent configs as managed agents
    orch = ManagedOrchestrator.from_local_configs(
        environment_name="pipeline-env",
        pip_packages=["ruff", "pytest"],
    )

    # Run standard codegen pipeline in the cloud
    result = await orch.run(
        "standard-codegen",
        "Add input validation to the user registration endpoint",
    )

    print(f"Gate: {result.gate_action.value}")
    for step in result.step_results:
        print(f"  {step.agent_name}: {step.verdict or 'completed'}")

asyncio.run(main())
```

## Disable Specific Tools

```python
agent = client.beta.agents.create(
    name="Read-Only Auditor",
    model="claude-opus-4-6",
    tools=[{
        "type": "agent_toolset_20260401",
        "default_config": {"enabled": False},
        "configs": [
            {"name": "bash", "enabled": True},
            {"name": "read", "enabled": True},
            {"name": "glob", "enabled": True},
            {"name": "grep", "enabled": True},
        ],
    }],
)
```

## MCP Servers

```python
agent = client.beta.agents.create(
    name="GitHub Assistant",
    model="claude-sonnet-4-6",
    mcp_servers=[{
        "type": "url",
        "name": "github",
        "url": "https://api.githubcopilot.com/mcp/",
    }],
    tools=[
        {"type": "agent_toolset_20260401"},
        {"type": "mcp_toolset", "mcp_server_name": "github"},
    ],
)

# Provide auth at session creation via vault
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    vault_ids=["vault_xxx"],
)
```

## Pin Agent Version

```python
# Use specific agent version for reproducibility
session = client.beta.sessions.create(
    agent={"type": "agent", "id": agent.id, "version": 1},
    environment_id=environment.id,
)
```

## Mount GitHub Repository

```python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    resources=[{
        "type": "github_repository",
        "url": "https://github.com/org/repo",
        "authorization_token": "ghp_xxx",
        "checkout": {"type": "branch", "name": "main"},
    }],
)
```

## Interrupt and Multi-Turn

```python
# Interrupt a running session
client.beta.sessions.events.send(
    session.id,
    events=[{"type": "user.interrupt"}],
)

# Send a follow-up message (multi-turn)
client.beta.sessions.events.send(
    session.id,
    events=[{
        "type": "user.message",
        "content": [{"type": "text", "text": "Now add error handling"}],
    }],
)
```
