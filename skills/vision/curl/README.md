# cURL Stack Setup

No installation needed — use `curl`, `jq`, and `base64` for API interaction.

## Analyze Image (Base64)

```bash
# Encode image
IMAGE_DATA=$(base64 -i screenshot.png)

curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d "{
    \"model\": \"claude-sonnet-4-6\",
    \"max_tokens\": 1024,
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": [
          {
            \"type\": \"image\",
            \"source\": {
              \"type\": \"base64\",
              \"media_type\": \"image/png\",
              \"data\": \"$IMAGE_DATA\"
            }
          },
          {
            \"type\": \"text\",
            \"text\": \"Describe what you see in this image.\"
          }
        ]
      }
    ]
  }"
```

## Analyze Image (URL)

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "url",
              "url": "https://example.com/chart.png"
            }
          },
          {
            "type": "text",
            "text": "Extract all data points from this chart."
          }
        ]
      }
    ]
  }'
```

## Multiple Images

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 2048,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {"type": "url", "url": "https://example.com/before.png"}
          },
          {
            "type": "image",
            "source": {"type": "url", "url": "https://example.com/after.png"}
          },
          {
            "type": "text",
            "text": "Compare these two images. What changed?"
          }
        ]
      }
    ]
  }'
```

## Extract Text with jq

```bash
# Get just the text response
curl -s ... | jq -r '.content[] | select(.type == "text") | .text'

# Check token usage
curl -s ... | jq '.usage'
```
