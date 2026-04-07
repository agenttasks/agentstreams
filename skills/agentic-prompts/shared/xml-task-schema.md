# XML Task Schema

Specification for structured XML task format used to represent agentic prompt patterns.

## Schema

```xml
<task id="{2-digit ID}" type="{system|agent|tool|skill}" name="{kebab-case name}">
  <purpose>{1-sentence description of what this prompt does}</purpose>

  <constraints>
    <constraint>{behavioral boundary or operating rule}</constraint>
    <!-- 0..N constraints -->
  </constraints>

  <tools allowed="{comma-separated tool names}" denied="{comma-separated tool names}"/>

  <output format="{description of expected output format}">
    <section name="{section name}">{section description}</section>
    <!-- Optional structured output sections -->
    <verdict options="{comma-separated verdict options}"/>
  </output>

  <tags>{comma-separated tags}</tags>
</task>
```

## Container

Multiple tasks are wrapped in a `<prompt-tasks>` container:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<prompt-tasks>
  <task id="01" type="system" name="main-system-prompt">...</task>
  <task id="02" type="system" name="simple-mode">...</task>
  <!-- ... -->
</prompt-tasks>
```

## Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `task/@id` | Yes | 2-digit zero-padded identifier |
| `task/@type` | Yes | One of: system, agent, tool, skill |
| `task/@name` | Yes | Kebab-case identifier (2-4 words) |
| `purpose` | Yes | Single sentence describing the prompt's function |
| `constraints` | No | List of behavioral boundaries and rules |
| `tools/@allowed` | No | Comma-separated list of allowed tools |
| `tools/@denied` | No | Comma-separated list of denied tools |
| `output/@format` | No | Description of expected output format |
| `output/section` | No | Named sections within structured output |
| `output/verdict` | No | Verdict options (e.g., PASS,FAIL,PARTIAL) |
| `tags` | No | Comma-separated classification tags |

## Type Definitions

### system
Core behavioral instructions defining agent identity, boundaries, and operating modes.
Loaded at session start or injected based on feature flags.

### agent
Specialized agent configurations for delegated task execution.
Spawned via the Agent tool with specific tool allowlists/denylists.

### tool
Guidance embedded in tool schemas or invoked alongside specific tool operations.
Often uses forced tool calls for structured output.

### skill
Reusable workflow definitions invoked via slash commands.
Typically generates files or performs multi-step processes.

## Rendering

Generate XML tasks from the prompt registry:

```bash
# All prompts as XML
uv run scripts/render_prompts.py

# Single prompt
uv run scripts/render_prompts.py --id 07

# Filter by type
uv run scripts/render_prompts.py --type agent

# Filter by tag
uv run scripts/render_prompts.py --tag security

# JSON output with prompt bodies
uv run scripts/render_prompts.py --format json --body
```

## Validation

```bash
uv run scripts/render_prompts.py --validate
```

Checks that all 30 source files exist and are non-empty.
