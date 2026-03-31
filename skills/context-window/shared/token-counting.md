# Token Counting Reference

## API Endpoint

```
POST /v1/messages/count_tokens
```

Counts the exact number of tokens that will be used for a given request, without actually sending it. Use this to verify your content fits within the context window before making an API call.

## Request Format

Same as the Messages API, minus `max_tokens`:

```json
{
  "model": "claude-sonnet-4-6",
  "system": "Optional system prompt",
  "tools": [],
  "messages": [
    {"role": "user", "content": "Your message"}
  ]
}
```

## Response

```json
{
  "input_tokens": 42
}
```

## Approximate Token Estimation

When you need a quick estimate without an API call:

- **English text**: ~4 characters per token
- **Code**: ~3.5 characters per token
- **JSON**: ~3 characters per token
- **Base64 images**: token count depends on resolution, not string length

## When to Count Tokens

1. **Before large requests** — verify content fits
2. **Cost estimation** — predict API costs
3. **Context budget** — manage how much space is left
4. **Chunking decisions** — determine where to split documents
