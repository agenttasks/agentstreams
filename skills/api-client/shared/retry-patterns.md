# Retry & Resilience Patterns

## Exponential Backoff

All API clients should implement retry with jittered exponential backoff:

```
delay = min(base * 2^attempt + random_jitter, max_delay)
```

### Retry Decision Matrix

| Status Code | Retry? | Notes |
|-------------|--------|-------|
| 400 | No | Bad request — fix the input |
| 401 | Once | Refresh auth token, then retry |
| 403 | No | Forbidden — permissions issue |
| 404 | No | Not found — wrong endpoint |
| 408 | Yes | Request timeout |
| 429 | Yes | Rate limited — use `Retry-After` header |
| 500 | Yes | Internal server error |
| 502 | Yes | Bad gateway |
| 503 | Yes | Service unavailable |
| 504 | Yes | Gateway timeout |

### Circuit Breaker

For high-throughput clients, add circuit breaker logic:

```
States: CLOSED → OPEN → HALF_OPEN → CLOSED

CLOSED:   Normal operation. Track failure rate.
          If failure rate > threshold (50%) in window (60s) → OPEN
OPEN:     All requests fail fast (no actual HTTP call).
          After timeout (30s) → HALF_OPEN
HALF_OPEN: Allow 1 probe request.
          If success → CLOSED. If failure → OPEN.
```

## Timeout Strategy

| Timeout Type | Default | Purpose |
|-------------|---------|---------|
| Connection | 5s | TCP handshake |
| Read | 30s | Waiting for response body |
| Write | 10s | Sending request body |
| Total | 60s | End-to-end request lifecycle |

## Idempotency

For non-idempotent operations (POST, PATCH, DELETE), include an `Idempotency-Key` header to make retries safe:

```
Idempotency-Key: <client-generated-uuid>
```

The server should:
1. Store the key → response mapping
2. On duplicate key, return the stored response without re-executing
