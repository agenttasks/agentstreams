# cURL Stack Setup

## Environment Setup

```bash
export GEMINI_API_KEY="your-api-key-here"
```

## API Base URL

```
https://generativelanguage.googleapis.com/v1beta
```

## Quick Start: Generate a Video

### 1. Submit Generation Request

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-lite:generateVideos" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cinematic sweeping drone shot of a futuristic cyberpunk city at sunset, highly detailed.",
    "config": {
      "aspectRatio": "16:9"
    }
  }'
```

Response returns an operation object:

```json
{
  "name": "operations/abc123",
  "done": false
}
```

### 2. Poll Operation Status

```bash
curl -X GET \
  "https://generativelanguage.googleapis.com/v1beta/operations/abc123" \
  -H "x-goog-api-key: $GEMINI_API_KEY"
```

Repeat every 10 seconds until `"done": true`.

### 3. Download Video

Once complete, the response includes video bytes (base64-encoded). Decode and save:

```bash
curl -s -X GET \
  "https://generativelanguage.googleapis.com/v1beta/operations/abc123" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
video_b64 = data['response']['videoBytes']
sys.stdout.buffer.write(base64.b64decode(video_b64))
" > output.mp4
```

## Shell Script: Full Generation Pipeline

```bash
#!/usr/bin/env bash
set -euo pipefail

PROMPT="${1:?Usage: generate-video.sh PROMPT ASPECT_RATIO OUTPUT_FILE}"
ASPECT_RATIO="${2:-16:9}"
OUTPUT_FILE="${3:-output.mp4}"
API_BASE="https://generativelanguage.googleapis.com/v1beta"

echo "Submitting video generation request..."
RESPONSE=$(curl -s -X POST \
  "${API_BASE}/models/veo-3.1-lite:generateVideos" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(printf '{"prompt": "%s", "config": {"aspectRatio": "%s"}}' "$PROMPT" "$ASPECT_RATIO")")

OPERATION_NAME=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])")
echo "Operation: $OPERATION_NAME"

# Poll until done
while true; do
  STATUS=$(curl -s -X GET \
    "${API_BASE}/${OPERATION_NAME}" \
    -H "x-goog-api-key: $GEMINI_API_KEY")

  DONE=$(echo "$STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('done', False))")

  if [ "$DONE" = "True" ]; then
    # Check for error
    ERROR=$(echo "$STATUS" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('error', ''))
")
    if [ -n "$ERROR" ]; then
      echo "Error: $ERROR"
      exit 1
    fi

    # Extract and save video
    echo "$STATUS" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
video_b64 = data['response']['videoBytes']
sys.stdout.buffer.write(base64.b64decode(video_b64))
" > "$OUTPUT_FILE"

    echo "Video saved to: $OUTPUT_FILE"
    exit 0
  fi

  echo "Generating... (polling in 10s)"
  sleep 10
done
```

### Usage

```bash
# YouTube Wide
./generate-video.sh "Drone shot of a mountain range at sunrise, cinematic." "16:9" youtube.mp4

# TikTok Vertical
./generate-video.sh "Vertical tracking shot of a surfer riding a wave, 4K." "9:16" tiktok.mp4
```

## Further Reading

- `shared/veo-generation.md` — full generation API reference
- `shared/prompt-engineering.md` — prompt crafting guide
- [google-gemini/cookbook](https://github.com/google-gemini/cookbook) — official API cookbook
