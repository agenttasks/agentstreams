# Python Stack Setup

## Installation (uv)

```bash
# Initialize project
uv init veo-video-project && cd veo-video-project

# Google GenAI SDK
uv add google-genai

# Testing
uv add --dev pytest==8.4.0
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `google-genai` | 1.14.0 | Official Google GenAI SDK — Veo video generation, async polling |

## Environment Setup

Set your Gemini API key:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

The `google-genai` client reads `GEMINI_API_KEY` from the environment automatically.

## Quick Start: Generate a Video

```python
import os
import time
from google import genai
from google.genai import types

client = genai.Client()

def generate_veo_video(prompt: str, aspect_ratio: str, output_filename: str):
    """Generate a video using Veo 3.1 Lite via the Gemini API."""
    response = client.models.generate_videos(
        model="veo-3.1-lite",
        prompt=prompt,
        config=types.GenerateVideoConfig(
            aspect_ratio=aspect_ratio,
        )
    )

    operation = response.operation
    while not operation.done:
        time.sleep(10)
        operation = client.operations.get(operation.name)

    if operation.error:
        raise RuntimeError(f"Video generation failed: {operation.error}")

    with open(output_filename, "wb") as f:
        f.write(operation.response.video_bytes)

    print(f"Video saved to: {output_filename}")


if __name__ == "__main__":
    # YouTube Wide (16:9)
    generate_veo_video(
        prompt="A cinematic sweeping drone shot of a futuristic cyberpunk city at sunset, highly detailed.",
        aspect_ratio="16:9",
        output_filename="youtube_wide_content.mp4",
    )

    # TikTok / Instagram Reels (9:16)
    generate_veo_video(
        prompt="A vertical tracking shot of a person skateboarding down a neon-lit street, dynamic lighting, 4K.",
        aspect_ratio="9:16",
        output_filename="tiktok_vertical_content.mp4",
    )
```

## Advanced: Batch Generation with Error Handling

```python
import time
import concurrent.futures
from google import genai
from google.genai import types

client = genai.Client()


def generate_video(prompt: str, aspect_ratio: str, output_filename: str) -> str:
    """Generate a single video with error handling."""
    try:
        response = client.models.generate_videos(
            model="veo-3.1-lite",
            prompt=prompt,
            config=types.GenerateVideoConfig(
                aspect_ratio=aspect_ratio,
            )
        )

        operation = response.operation
        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation.name)

        if operation.error:
            return f"FAILED ({output_filename}): {operation.error}"

        with open(output_filename, "wb") as f:
            f.write(operation.response.video_bytes)

        return f"OK: {output_filename}"

    except Exception as e:
        return f"ERROR ({output_filename}): {e}"


def batch_generate(jobs: list[tuple[str, str, str]]) -> list[str]:
    """Generate multiple videos in parallel."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(generate_video, prompt, ratio, filename)
            for prompt, ratio, filename in jobs
        ]
        return [f.result() for f in concurrent.futures.as_completed(futures)]


if __name__ == "__main__":
    jobs = [
        ("Drone shot of mountain range at sunrise, golden hour, cinematic.", "16:9", "mountains_wide.mp4"),
        ("Vertical shot of rain falling on a city street at night, neon reflections.", "9:16", "rain_vertical.mp4"),
        ("Slow motion wave crashing on a rocky coastline, dramatic lighting.", "16:9", "wave_wide.mp4"),
    ]

    results = batch_generate(jobs)
    for result in results:
        print(result)
```

## Further Reading

- `shared/veo-generation.md` — full generation API reference
- `shared/prompt-engineering.md` — prompt crafting guide
- [googleapis/python-genai](https://github.com/googleapis/python-genai) — SDK source and docs
- [google-gemini/cookbook](https://github.com/google-gemini/cookbook) — official Jupyter notebooks
