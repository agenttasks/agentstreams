# Prompt Caching Reference

## Overview

Prompt caching reduces costs and latency for repeated content. Mark cacheable blocks with `cache_control`, and subsequent requests reuse the cached content at ~90% reduced cost.

## How It Works

1. Add `"cache_control": {"type": "ephemeral"}` to cacheable content blocks
2. First request creates the cache (charges cache creation fee)
3. Subsequent requests with identical content get cache hits
4. Cache expires after 5 minutes of inactivity (TTL refreshed on each use)

## Cacheable Content Types

- **System prompts** — most common use case
- **Tool definitions** — cache complex tool schemas
- **Large documents** — reference materials in system prompt
- **Few-shot examples** — cache example conversations

## Minimum Cache Size

Content must be at least 1,024 tokens (Haiku) or 2,048 tokens (Sonnet/Opus) to be cached.

## Pricing Impact

| Component | Cost vs Standard |
|-----------|-----------------|
| Cache creation | 25% more than base input |
| Cache read | 90% less than base input |
| Break-even | ~3 requests with same content |

## Best Practices

1. **Cache large, static content** — system prompts, reference docs
2. **Put cached content first** — cache blocks must be contiguous from the start
3. **Monitor cache metrics** — check `cache_creation_input_tokens` and `cache_read_input_tokens`
4. **Keep cache warm** — use within 5 minutes to prevent expiration
5. **Combine with conversation** — cache the system prompt, vary the messages
