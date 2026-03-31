# Image Analysis Reference

## Capabilities

Claude can analyze images to:

- **Describe content** — objects, scenes, people, text, colors
- **Extract text (OCR)** — screenshots, documents, handwriting, signs
- **Classify images** — categorize by content, style, quality
- **Answer questions** — visual QA about image content
- **Read charts/graphs** — extract data points, trends, labels
- **Understand diagrams** — flowcharts, architecture, UML

## Token Cost by Resolution

| Resolution | Approximate Tokens |
|------------|-------------------|
| 200x200 | ~200 |
| 512x512 | ~600 |
| 1024x1024 | ~1,600 |
| 1920x1080 | ~2,700 |
| 4096x4096 | ~6,400 |

## Optimization Tips

1. **Crop first** — only send the relevant portion of the image
2. **Resize large images** — 1024px max dimension is usually sufficient
3. **Use JPEG for photos** — smaller file size, same quality for analysis
4. **Use PNG for screenshots** — preserves text clarity
5. **Batch similar images** — send multiple images in one request

## Structured Output for Classification

Use system prompts to get structured JSON output:

```
Analyze this image and respond in JSON format:
{
  "description": "brief description",
  "objects": ["list", "of", "objects"],
  "text_content": "any text found",
  "dominant_colors": ["color1", "color2"],
  "quality": "high|medium|low"
}
```
