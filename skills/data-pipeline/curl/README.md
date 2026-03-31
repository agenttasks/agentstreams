# Shell Stack

## Pipeline Patterns

### Basic ETL with Shell Pipes

```bash
#!/bin/bash
set -euo pipefail

SOURCE="data/input.csv"
TARGET="data/output.parquet"
STAGING="data/staging"
mkdir -p "$STAGING"

# Extract — skip header, clean whitespace
tail -n +2 "$SOURCE" \
  | sed 's/[[:space:]]*,[[:space:]]*/,/g' \
  > "$STAGING/extracted.csv"

# Transform — deduplicate by first column (ID)
sort -t',' -k1,1 -u "$STAGING/extracted.csv" \
  > "$STAGING/transformed.csv"

# Quality check
ROW_COUNT=$(wc -l < "$STAGING/transformed.csv")
if [ "$ROW_COUNT" -eq 0 ]; then
    echo "ERROR: No rows after transform" >&2
    exit 1
fi
echo "Quality check passed: $ROW_COUNT rows"

# Load (convert to JSON for Claude processing)
jq -R -s 'split("\n") | map(select(length > 0) | split(",") | {id: .[0], name: .[1], value: .[2]})' \
  "$STAGING/transformed.csv" > "$STAGING/output.json"

echo "Pipeline complete: $ROW_COUNT rows → $STAGING/output.json"
```

### Claude-Powered Classification

```bash
classify_batch() {
    local input_file="$1"
    local batch_size="${2:-50}"

    # Read batch of descriptions
    local descriptions
    descriptions=$(head -n "$batch_size" "$input_file" | jq -Rs .)

    curl -s https://api.anthropic.com/v1/messages \
        -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d "{
            \"model\": \"claude-sonnet-4-6\",
            \"max_tokens\": 2048,
            \"messages\": [{
                \"role\": \"user\",
                \"content\": \"Classify each line into a category. One category per line:\\n$descriptions\"
            }]
        }" | jq -r '.content[0].text'
}
```

### Cron-Based Scheduling

```bash
# Add to crontab: run ETL daily at 2am
# 0 2 * * * /path/to/scripts/etl.sh >> /var/log/etl.log 2>&1
```

## Further Reading

- `shared/pipeline-patterns.md` — Idempotency, backpressure, DLQ
- `shared/orchestration.md` — DAGs, scheduling
