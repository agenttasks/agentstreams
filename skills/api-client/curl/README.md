# cURL / Shell Stack

## API Client Patterns

### Basic Request with Retry

```bash
#!/bin/bash
set -euo pipefail

# Retry with exponential backoff
retry_request() {
    local url="$1"
    local max_retries=3
    local base_delay=1

    for attempt in $(seq 0 "$max_retries"); do
        local status
        status=$(curl -s -o /tmp/response.json -w "%{http_code}" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            --connect-timeout 5 \
            --max-time 30 \
            "$url")

        case "$status" in
            2*) cat /tmp/response.json; return 0 ;;
            429|500|502|503|504)
                if [ "$attempt" -eq "$max_retries" ]; then
                    echo "Failed after $max_retries retries (HTTP $status)" >&2
                    return 1
                fi
                local delay=$((base_delay * (2 ** attempt)))
                echo "Retry $((attempt + 1))/$max_retries in ${delay}s (HTTP $status)" >&2
                sleep "$delay"
                ;;
            *)
                echo "Non-retryable error: HTTP $status" >&2
                cat /tmp/response.json >&2
                return 1
                ;;
        esac
    done
}
```

### Claude-Powered API Exploration

```bash
# Explore an API endpoint with Claude
explore_api() {
    local url="$1"
    local response
    response=$(curl -s -H "Authorization: Bearer $API_KEY" "$url")

    curl -s https://api.anthropic.com/v1/messages \
        -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d "{
            \"model\": \"claude-sonnet-4-6\",
            \"max_tokens\": 2048,
            \"messages\": [{
                \"role\": \"user\",
                \"content\": \"Analyze this API response and describe the schema:\\n$(echo "$response" | head -c 10000 | jq -Rs .)\"
            }]
        }" | jq -r '.content[0].text'
}
```

### OAuth 2.0 Client Credentials

```bash
get_oauth_token() {
    local token_url="$1"
    local client_id="$2"
    local client_secret="$3"

    curl -s -X POST "$token_url" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "grant_type=client_credentials" \
        -d "client_id=$client_id" \
        -d "client_secret=$client_secret" | jq -r '.access_token'
}
```

## Further Reading

- `shared/retry-patterns.md` — Retry strategy, circuit breaker, timeouts
- `shared/auth-patterns.md` — API key, OAuth 2.0, JWT, mTLS
