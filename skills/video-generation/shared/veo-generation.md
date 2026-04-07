# Veo Video Generation Reference

## Overview

Veo is Google's video generation model family, accessed via the Gemini Cloud API. The `veo-3.1-lite` model generates video from text prompts with configurable aspect ratios. Generation is asynchronous — you submit a request, receive an operation ID, then poll until the video is ready.

## Model Selection

| Model | Speed | Cost | Use Case |
|-------|-------|------|----------|
| `veo-3.1-lite` | Fast | Lower | Content creation, prototyping, social media |

## Supported Aspect Ratios

| Ratio | Orientation | Platforms |
|-------|-------------|-----------|
| `16:9` | Landscape | YouTube, desktop web, presentations |
| `9:16` | Portrait | TikTok, Instagram Reels, YouTube Shorts |

## Generation Flow

### 1. Submit Request

Send a `generate_videos` request with:
- **model** — e.g., `veo-3.1-lite`
- **prompt** — text description of the desired video
- **config** — aspect ratio and other settings

### 2. Poll Operation

The API returns an operation object. Poll it until `operation.done` is `true`:
- Check every 10 seconds
- Handle `operation.error` if generation fails

### 3. Download Output

Once complete, extract `video_bytes` from the response and save to disk as `.mp4`.

## Python Example

```python
import time
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_videos(
    model="veo-3.1-lite",
    prompt="A cinematic sweeping drone shot of a futuristic cyberpunk city at sunset, highly detailed.",
    config=types.GenerateVideoConfig(
        aspect_ratio="16:9",
    )
)

operation = response.operation
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation.name)

if operation.error:
    raise RuntimeError(f"Video generation failed: {operation.error}")

with open("output.mp4", "wb") as f:
    f.write(operation.response.video_bytes)
```

## cURL Example

### Submit Generation Request

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-lite:generateVideos" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cinematic sweeping drone shot of a futuristic cyberpunk city at sunset.",
    "config": {
      "aspectRatio": "16:9"
    }
  }'
```

### Poll Operation Status

```bash
curl -X GET \
  "https://generativelanguage.googleapis.com/v1beta/operations/OPERATION_ID" \
  -H "x-goog-api-key: $GEMINI_API_KEY"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Quota exceeded | Too many requests | Wait and retry with exponential backoff |
| Invalid prompt | Content policy violation | Revise prompt to comply with usage policies |
| Operation timeout | Generation took too long | Retry with a simpler prompt |
| Network error | Connectivity issue | Retry with exponential backoff (2s, 4s, 8s, 16s) |

## Batch Generation

To generate videos for multiple platforms simultaneously, submit parallel requests with different aspect ratios:

```python
import concurrent.futures

prompts_and_ratios = [
    ("Cinematic drone shot of a mountain range at sunrise.", "16:9", "youtube.mp4"),
    ("Vertical tracking shot of a surfer riding a wave.", "9:16", "tiktok.mp4"),
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(generate_veo_video, prompt, ratio, filename)
        for prompt, ratio, filename in prompts_and_ratios
    ]
    concurrent.futures.wait(futures)
```
