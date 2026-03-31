---
name: vision
description: "Image understanding, PDF processing, and multimodal content analysis with Claude. TRIGGER when: user asks to analyze images, extract text from screenshots, process PDFs, build content moderation with images, compare visual content, generate image descriptions, handle base64 image encoding, or work with multimodal prompts. Also triggers for document OCR, chart/diagram understanding, or visual QA. DO NOT TRIGGER for: computer use automation (use code-execution), web crawling (use crawl-ingest), or API client generation (use api-client)."
---

# Vision: Image Understanding & Multimodal Analysis Skill

Analyze images, extract text from documents, process PDFs, moderate visual content, and build multimodal workflows — using Claude's vision capabilities across TypeScript, Python, or cURL.

## Defaults

- Use `claude-sonnet-4-6` for image analysis, `claude-opus-4-6` for complex multi-image reasoning
- Support base64 and URL image sources
- Accepted formats: JPEG, PNG, GIF, WebP (max 5MB per image)
- PDF support via the files API (beta)
- Max 20 images per request

---

## Capability Selection

Before reading setup docs, determine which capability the user needs:

1. **Single Image Analysis** — describe, extract text, classify
   - Best for: OCR, image description, content moderation
   - Read from `shared/image-analysis.md`

2. **Multi-Image Comparison** — compare, diff, combine
   - Best for: before/after, A/B testing, visual QA
   - Read from `shared/multi-image.md`

3. **PDF Processing** — extract text, summarize, analyze
   - Best for: document understanding, legal review, data extraction
   - Read from `shared/pdf-processing.md`

4. **Content Moderation** — detect unsafe content in images
   - Best for: UGC moderation, compliance, safety filters
   - Read from `shared/content-moderation.md`

---

## Core Capabilities

| Capability | Support | Notes |
|---|---|---|
| **Image description** | All models | Describe image content, objects, text |
| **OCR / text extraction** | All models | Extract text from screenshots, photos, documents |
| **Chart understanding** | All models | Read charts, graphs, diagrams |
| **Multi-image** | All models | Up to 20 images per request |
| **PDF** | Beta (files API) | Upload then reference in messages |
| **Image generation** | No | Claude cannot generate images |
| **Video** | No | Claude cannot process video |

---

## Image Input Formats

### Base64 Encoded

```json
{
  "type": "image",
  "source": {
    "type": "base64",
    "media_type": "image/jpeg",
    "data": "<base64-encoded-data>"
  }
}
```

### URL Reference

```json
{
  "type": "image",
  "source": {
    "type": "url",
    "url": "https://example.com/image.jpg"
  }
}
```

### Supported Media Types

- `image/jpeg`
- `image/png`
- `image/gif`
- `image/webp`

---

## Workflow

### Image Analysis Pipeline

```
Image Input (base64/URL)
        │
        ▼
┌──────────────────┐
│ Claude Processes  │ ← Understands visual content
│ Image             │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Structured Output │ ← JSON, text, or classification
│                   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Post-Processing   │ ← Validation, storage, routing
│                   │
└──────────────────┘
```

### PDF Processing Pipeline

```
PDF Upload (files API)
        │
        ▼
┌──────────────────┐
│ Upload to Files   │ ← POST /v1/files
│ API               │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Reference in      │ ← file_id in message content
│ Message           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Claude Analyzes   │ ← Extract, summarize, Q&A
│ Document          │
└──────────────────┘
```

---

## Best Practices

### Image Quality

- Higher resolution = better results (but more tokens)
- Crop to relevant area when possible
- Ensure text is readable (min ~12px effective font size)
- Use PNG for screenshots, JPEG for photos

### Token Usage

- Images consume tokens based on dimensions
- A 1024x1024 image uses ~1,600 tokens
- Resize large images before sending to reduce cost
- Use thumbnails for classification, full-res for OCR

### Multi-Image Prompting

- Place images before the question in the message
- Reference images by position ("the first image", "image 2")
- For comparison, explicitly ask Claude to compare specific aspects
