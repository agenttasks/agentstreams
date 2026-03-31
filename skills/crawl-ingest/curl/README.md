# cURL / Shell Stack

## Overview

For quick prototyping, scripting, or environments where no SDK is available. Uses raw HTTP to the Anthropic API + standard Unix tools for crawling.

## Web Crawling with wget + curl

### Basic Site Mirror

```bash
# Mirror a site (respects robots.txt)
wget --mirror \
     --convert-links \
     --adjust-extension \
     --page-requisites \
     --no-parent \
     --wait=1 \
     --random-wait \
     --user-agent="MyCrawler/1.0" \
     -P ./data/mirror \
     https://example.com/

# Crawl and save URL list
wget --spider \
     --recursive \
     --no-verbose \
     --output-file=./data/crawl.log \
     https://example.com/ 2>&1 | grep -oP '(?<=URL:)\S+' > ./data/urls.txt
```

### URL Deduplication (Shell-Based Bloom Filter Alternative)

Since true bloom filters need a runtime, use `sort -u` for exact dedup in shell:

```bash
# Deduplicate URLs
sort -u ./data/urls.txt > ./data/urls-unique.txt

# Track seen URLs across sessions
touch ./data/seen.txt
comm -23 <(sort ./data/new-urls.txt) <(sort ./data/seen.txt) > ./data/to-crawl.txt
cat ./data/to-crawl.txt >> ./data/seen.txt
```

For larger scale, use a SQLite-based approach:

```bash
sqlite3 ./data/crawl.db "CREATE TABLE IF NOT EXISTS seen_urls (url TEXT PRIMARY KEY);"

# Check and insert
check_url() {
    local url="$1"
    local exists=$(sqlite3 ./data/crawl.db "SELECT COUNT(*) FROM seen_urls WHERE url='$url';")
    if [ "$exists" -eq "0" ]; then
        sqlite3 ./data/crawl.db "INSERT INTO seen_urls VALUES ('$url');"
        echo "new"
    else
        echo "seen"
    fi
}
```

## Claude API (Raw HTTP)

### Basic Extraction

```bash
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": "Extract product data from this HTML:\n'"$(cat page.html | head -c 30000)"'"
    }]
  }' | jq '.content[0].text'
```

### Streaming

```bash
curl -sN https://api.anthropic.com/v1/messages \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "stream": true,
    "messages": [{
      "role": "user",
      "content": "Extract: '"$(cat page.html | head -c 30000 | jq -Rs .)"'"
    }]
  }' | grep '^data: ' | sed 's/^data: //' | jq -r 'select(.type=="content_block_delta") | .delta.text'
```

### Batch Processing Script

```bash
#!/bin/bash
# Process all crawled pages through Claude
RESULTS_DIR="./data/extracted"
mkdir -p "$RESULTS_DIR"

for html_file in ./data/mirror/**/*.html; do
    basename=$(basename "$html_file" .html)
    output="$RESULTS_DIR/${basename}.json"

    [ -f "$output" ] && continue  # Skip already processed

    echo "Processing: $html_file"

    content=$(head -c 30000 "$html_file" | jq -Rs .)
    curl -s https://api.anthropic.com/v1/messages \
      -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \ \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d "{
        \"model\": \"claude-sonnet-4-6\",
        \"max_tokens\": 1024,
        \"messages\": [{
          \"role\": \"user\",
          \"content\": \"Extract structured data as JSON:\\n\"$content
        }]
      }" > "$output"

    sleep 1  # Rate limiting
done
```

### Required Headers

| Header | Value |
|--------|-------|
| `x-api-key` | Your `CLAUDE_CODE_OAUTH_TOKEN` |
| `anthropic-version` | `2023-06-01` |
| `content-type` | `application/json` |
| `anthropic-beta` | `tool-use-2024-04-04` (for tool use) |

## Tools

- `jq` — JSON processing
- `wget` / `curl` — HTTP requests
- `sqlite3` — Local database
- `parallel` — GNU Parallel for concurrent processing
- `pup` — HTML parser for command line (CSS selectors)
