# cURL Stack Setup

No installation needed — use `curl` and `jq` for API interaction.

## Count Tokens

```bash
curl https://api.anthropic.com/v1/messages/count_tokens \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-6",
    "messages": [
      {
        "role": "user",
        "content": "Your message here..."
      }
    ]
  }' | jq '.input_tokens'
```

## Prompt Caching

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "system": [
      {
        "type": "text",
        "text": "You are an expert analyst. Reference: ...",
        "cache_control": {"type": "ephemeral"}
      }
    ],
    "messages": [
      {"role": "user", "content": "Summarize the key points."}
    ]
  }'
```

## Extended Thinking

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 16384,
    "thinking": {
      "type": "enabled",
      "budget_tokens": 10000
    },
    "messages": [
      {"role": "user", "content": "Solve this problem step by step..."}
    ]
  }'
```

## Check Cache and Token Usage

```bash
# Cache performance
curl -s ... | jq '.usage | {input_tokens, cache_creation_input_tokens, cache_read_input_tokens}'

# Total usage
curl -s ... | jq '.usage'

# Thinking tokens
curl -s ... | jq '.usage.thinking_tokens'
```
