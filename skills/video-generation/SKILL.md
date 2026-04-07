---
name: video-generation
description: "Video generation with Google Veo models via the Gemini API. TRIGGER when: user asks to generate video, create video content, use Veo or Gemini video models, build video generation pipelines, create YouTube/TikTok/Reels content programmatically, or automate video creation workflows. DO NOT TRIGGER for: image analysis or vision tasks (use vision), local model inference with Gemma, or Anthropic Claude API usage (use api-client)."
---

# Video Generation: Veo via Gemini API Skill

Generate videos using Google's Veo models through the Gemini Cloud API — for YouTube wide (16:9), Instagram Reels / TikTok vertical (9:16), and custom aspect ratios.

## Defaults

- Use `veo-3.1-lite` for fast, cost-effective video generation
- Auth via `GEMINI_API_KEY` environment variable
- Video generation is asynchronous — requires polling for completion
- Veo is cloud-only; cannot run locally regardless of GPU hardware
- Supported aspect ratios: `16:9` (landscape), `9:16` (portrait)

---

## Hardware Context

- **Veo models** are cloud-only via the Gemini API — no local GPU inference
- **Gemma** (Google's open-weights text model family) cannot generate video
- A local GPU (e.g., Nvidia RTX 2080 Ti, 11 GB VRAM) can run smaller Gemma text models for prompt brainstorming, but all rendering happens in the cloud

---

## Capability Selection

Before reading setup docs, determine which capability the user needs:

1. **Video Generation** — generate video from a text prompt
   - Best for: content creation, social media, marketing assets
   - Read from `shared/veo-generation.md`

2. **Prompt Engineering** — craft effective prompts for high-quality video output
   - Best for: improving output quality, cinematic styles, aspect ratio planning
   - Read from `shared/prompt-engineering.md`

---

## Core Capabilities

| Capability | Support | Notes |
|---|---|---|
| **Text-to-video** | Veo 3.1 Lite | Generate video from a text prompt |
| **Aspect ratio control** | Veo 3.1 Lite | 16:9 landscape, 9:16 portrait |
| **Async polling** | SDK + cURL | Poll operation status until completion |
| **Image-to-video** | No | Not available via current Veo API |
| **Video editing** | No | Generate only, no post-processing |
| **Local inference** | No | Cloud API only |

---

## Official Repositories

| Repository | Purpose |
|---|---|
| [google-gemini/cookbook](https://github.com/google-gemini/cookbook) | Official Gemini API cookbook — Jupyter notebooks for Veo, prompting, polling |
| [googleapis/python-genai](https://github.com/googleapis/python-genai) | Official Python SDK (`google-genai`) — client, async polling, `GenerateVideoConfig` |
| [googleapis/js-genai](https://github.com/googleapis/js-genai) | Official Node.js/TypeScript SDK (`@google/genai`) — web/backend integration |
| [google-gemini/genai-processors](https://github.com/google-gemini/genai-processors) | Pre/post-processing utilities for Gemini pipelines |

---

## Workflow

### Video Generation Pipeline

```
Text Prompt
        │
        ▼
┌──────────────────┐
│ Gemini API        │ ← POST generate_videos request
│ (Veo 3.1 Lite)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Async Operation   │ ← Returns operation ID
│                   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Poll Status       │ ← GET operation until done
│                   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Download Video    │ ← Extract video bytes, save .mp4
│                   │
└──────────────────┘
```

### Automated Content Pipeline

```
Script / Brief
        │
        ▼
┌──────────────────┐
│ Prompt Generation │ ← Use Gemma or Claude for brainstorming
│                   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Veo Generation    │ ← Batch multiple aspect ratios
│ (16:9 + 9:16)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Post-Processing   │ ← Rename, organize, upload
│                   │
└──────────────────┘
```

---

## Best Practices

### Prompting

- Be specific about camera movement (drone shot, tracking shot, pan)
- Specify lighting conditions (sunset, neon-lit, golden hour)
- Include style descriptors (cinematic, 4K, highly detailed)
- Keep prompts concise but descriptive — one clear scene per generation

### Aspect Ratios

- **16:9** — YouTube, desktop web, presentations
- **9:16** — TikTok, Instagram Reels, YouTube Shorts

### Error Handling

- Always check `operation.error` after polling completes
- Wrap API calls in try/except for network and quota errors
- Implement exponential backoff for rate limiting
- Poll at 10-second intervals to avoid excessive API calls
