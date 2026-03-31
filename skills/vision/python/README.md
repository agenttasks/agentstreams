# Python Stack Setup

## Installation (uv)

```bash
# Initialize project
uv init vision-project && cd vision-project

# Core Anthropic packages
uv add anthropic

# Image processing
uv add pillow==11.1.0              # Image manipulation, resizing
uv add httpx==0.28.1               # Fetch images from URLs

# PDF processing
uv add pymupdf==1.25.3             # PDF text extraction (alternative to files API)

# Testing
uv add --dev pytest==8.4.0
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | 0.86.0 | Official Python SDK — messages, vision, files API |
| `pillow` | 11.1.0 | Image manipulation — resize, crop, format conversion |
| `httpx` | 0.28.1 | HTTP client — fetch images from URLs |
| `pymupdf` | 1.25.3 | PDF text extraction — local alternative to files API |

## Quick Start: Analyze a Single Image

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

# Load image as base64
image_data = base64.standard_b64encode(
    Path("screenshot.png").read_bytes()
).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe what you see in this image.",
                },
            ],
        }
    ],
)

print(response.content[0].text)
```

## Image from URL

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/chart.png",
                    },
                },
                {
                    "type": "text",
                    "text": "Extract all data points from this chart.",
                },
            ],
        }
    ],
)
```

## Multi-Image Comparison

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

def encode_image(path: str) -> dict:
    data = base64.standard_b64encode(Path(path).read_bytes()).decode("utf-8")
    suffix = Path(path).suffix.lstrip(".")
    media_type = f"image/{'jpeg' if suffix == 'jpg' else suffix}"
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": data},
    }

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": [
                encode_image("before.png"),
                encode_image("after.png"),
                {
                    "type": "text",
                    "text": "Compare these two screenshots. What changed?",
                },
            ],
        }
    ],
)
```

## PDF Processing via Files API (Beta)

```python
import anthropic
from pathlib import Path

client = anthropic.Anthropic()

# Upload PDF
with open("document.pdf", "rb") as f:
    file = client.beta.files.upload(file=f)

# Reference in message
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "file",
                    "source": {
                        "type": "file",
                        "file_id": file.id,
                    },
                },
                {
                    "type": "text",
                    "text": "Summarize the key findings in this document.",
                },
            ],
        }
    ],
)
```

## Resize Images to Reduce Tokens

```python
from PIL import Image
import base64
import io

def resize_for_claude(path: str, max_dim: int = 1024) -> str:
    """Resize image to max dimension while preserving aspect ratio."""
    img = Image.open(path)
    img.thumbnail((max_dim, max_dim))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")
```

## MCP SDK Availability

Python MCP SDK: `mcp` (PyPI) — build MCP servers that provide vision tools.

```bash
uv add mcp
```
