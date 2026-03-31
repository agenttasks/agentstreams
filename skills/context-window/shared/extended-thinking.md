# Extended Thinking Reference

## Overview

Extended thinking gives Claude a dedicated "thinking" budget for complex reasoning before generating a response. The thinking process is visible in the response as `thinking` content blocks.

## Configuration

```json
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  }
}
```

## Budget Guidelines

| Task Complexity | Budget Tokens | Use Case |
|----------------|---------------|----------|
| Simple | 2,000-5,000 | Straightforward analysis |
| Medium | 5,000-15,000 | Multi-step reasoning |
| Complex | 15,000-50,000 | Math proofs, architecture design |
| Maximum | 50,000-128,000 | Research synthesis, complex debugging |

## Response Format

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me work through this step by step..."
    },
    {
      "type": "text",
      "text": "The answer is..."
    }
  ],
  "usage": {
    "input_tokens": 150,
    "output_tokens": 500,
    "thinking_tokens": 8432
  }
}
```

## Best Practices

1. **Match budget to task** — over-allocating wastes tokens
2. **Use with Opus** — Opus benefits most from extended thinking
3. **Monitor usage** — check `usage.thinking_tokens` in responses
4. **Combine with streaming** — stream thinking blocks for real-time progress
5. **Don't force thinking** — some tasks are better without it

## Interaction with Context Window

Thinking tokens count toward the context window:

```
available_output = max_tokens
thinking uses up to budget_tokens from available_output
actual_response = max_tokens - thinking_tokens_used
```

Set `max_tokens` high enough to accommodate both thinking and response.
