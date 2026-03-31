# Content Moderation Reference

## Overview

Claude can classify images for content moderation — detecting unsafe, inappropriate, or policy-violating content. Combine vision with structured output for automated moderation pipelines.

## Moderation Categories

| Category | Description |
|----------|-------------|
| **Violence** | Graphic violence, weapons, gore |
| **Adult content** | Nudity, sexual content |
| **Hate symbols** | Extremist imagery, hate speech |
| **Self-harm** | Content promoting self-harm |
| **Misinformation** | Manipulated images, deepfakes |
| **PII** | Visible personal information |

## Structured Output Pattern

```
Classify this image for content moderation. Respond in JSON:
{
  "safe": true/false,
  "categories": {
    "violence": "none|mild|graphic",
    "adult": "none|suggestive|explicit",
    "hate": "none|mild|explicit",
    "self_harm": "none|present",
    "pii_visible": true/false
  },
  "confidence": 0.0-1.0,
  "explanation": "brief reasoning"
}
```

## Pipeline Pattern

1. **Receive image** — from upload, URL, or stream
2. **Resize** — reduce to 512x512 for classification (fast, cheap)
3. **Classify** — send to Claude with moderation prompt
4. **Route** — auto-approve safe, queue borderline for human review
5. **Log** — store decision with confidence for audit

## Best Practices

1. **Use lower resolution** — 512px is enough for moderation
2. **Batch requests** — process multiple images per API call
3. **Set confidence thresholds** — auto-approve above 0.95, review below
4. **Human-in-the-loop** — always have human review for borderline cases
5. **Audit trail** — log all decisions for compliance
