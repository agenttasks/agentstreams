# cURL Stack Setup

No installation needed — use `curl` and `jq` for API interaction.

## Code Execution Tool

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 4096,
    "tools": [
      {
        "type": "code_execution",
        "name": "code_execution"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Calculate pi to 100 decimal places"
      }
    ]
  }'
```

## Computer Use Tool

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: computer-use-2025-01-24" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 4096,
    "tools": [
      {
        "type": "computer_20250124",
        "name": "computer",
        "display_width_px": 1920,
        "display_height_px": 1080,
        "display_number": 0
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Take a screenshot of the current display"
      }
    ]
  }'
```

## Bash Tool

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: computer-use-2025-01-24" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 4096,
    "tools": [
      {
        "type": "bash_20250124",
        "name": "bash"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "List all running processes sorted by memory usage"
      }
    ]
  }'
```

## Server Tools

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 4096,
    "tools": [
      {
        "type": "server_tool",
        "name": "code_execution"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Write and run a Python script to sort a list of numbers"
      }
    ]
  }'
```

## Processing Tool Results with jq

```bash
# Extract code execution results
curl -s ... | jq '.content[] | select(.type == "tool_use") | .input'

# Extract text responses
curl -s ... | jq -r '.content[] | select(.type == "text") | .text'

# Check stop reason
curl -s ... | jq -r '.stop_reason'
```
