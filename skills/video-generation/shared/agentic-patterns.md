# Agentic Patterns Applied to Video Generation

How the agentic prompt patterns from `skills/agentic-prompts/` are applied to
the video-generation skill.

## 1. XML Task Format (Pattern #2)

Each video generation request is represented as a structured XML task:

```xml
<video-task id="01" status="ready">
  <prompt>A cinematic drone shot of a mountain range at sunrise, golden hour, 4K.</prompt>
  <config model="veo-3.1-lite" aspect_ratio="16:9" platform="youtube"/>
  <output file="youtube_mountains.mp4"/>
</video-task>
```

This enables programmatic consumption by coordinators and batch pipelines.

## 2. Verification Pattern (Pattern #4)

Prompts are validated before generation using adversarial checks:

| Check | Rule | Verdict on Fail |
|-------|------|-----------------|
| prompt-length | 5-50 words | FAIL if too short/long |
| camera-movement | Must have drone/tracking/pan/etc. | FAIL |
| style-modifier | Must have cinematic/4K/detailed/etc. | FAIL |
| single-scene | No "then"/"next" multi-scene markers | FAIL |
| aspect-ratio | Must be 16:9 or 9:16 | FAIL |

Verdict output follows the verification agent format:

```xml
<verification task_id="01">
  <check name="camera-movement" result="PASS">
    Camera movement keyword found.
  </check>
  <check name="style-modifier" result="FAIL">
    Missing style modifier. Add: cinematic, 4K, detailed, etc.
  </check>
  <verdict>PARTIAL</verdict>
</verification>
```

## 3. Coordinator Pattern (Pattern #6)

Batch generation uses the coordinator task-notification pattern:

```xml
<task-notification>
  <task-id>video-01</task-id>
  <status>completed</status>
  <summary>Generated youtube_mountains.mp4 (16:9, 12s)</summary>
</task-notification>
```

Workers execute in parallel via `ThreadPoolExecutor`, each generating
a different aspect ratio. The coordinator synthesizes results.

## 4. Three-Agent Review (Pattern #10)

For content pipelines, apply the simplify-review pattern:

| Agent | Focus |
|-------|-------|
| Prompt Quality | Camera movement, lighting, style modifiers |
| Platform Fit | Aspect ratio matches target platform |
| Cost Efficiency | Batch deduplication, avoid redundant generations |

## 5. Tool Best Practices (Pattern from prompt 13)

- Use `uv` for Python dependency management (not pip/npm)
- Auth via `GEMINI_API_KEY` environment variable
- SDK: `google-genai` reads the key automatically
- Shell scripts: `set -euo pipefail`
- Poll at 10-second intervals with exponential backoff on errors

## Script

```bash
# Validate prompts before generation
uv run skills/video-generation/scripts/generate_videos.py --validate-prompts batch.json

# Generate with XML task output
uv run skills/video-generation/scripts/generate_videos.py --batch batch.json
```
