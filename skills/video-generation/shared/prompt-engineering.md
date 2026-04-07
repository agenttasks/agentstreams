# Video Prompt Engineering Reference

## Prompt Structure

Effective Veo prompts combine these elements in a concise description:

```
[Camera movement] + [Subject/Action] + [Setting/Environment] + [Style/Quality modifiers]
```

### Example Breakdown

| Element | Example |
|---------|---------|
| Camera movement | "A cinematic sweeping drone shot" |
| Subject/Action | "of a person skateboarding" |
| Setting | "down a neon-lit street at night" |
| Style modifiers | "dynamic lighting, 4K, highly detailed" |

**Combined:** "A cinematic sweeping drone shot of a person skateboarding down a neon-lit street at night, dynamic lighting, 4K, highly detailed."

## Camera Movement Keywords

| Keyword | Effect |
|---------|--------|
| `drone shot` | Aerial perspective, sweeping movement |
| `tracking shot` | Camera follows the subject |
| `pan` | Camera rotates horizontally |
| `tilt` | Camera rotates vertically |
| `dolly` | Camera moves toward/away from subject |
| `static shot` | Fixed camera position |
| `handheld` | Slight shake, documentary feel |
| `slow motion` | Reduced playback speed |
| `timelapse` | Accelerated time progression |

## Lighting Keywords

| Keyword | Effect |
|---------|--------|
| `golden hour` | Warm, soft light (sunrise/sunset) |
| `neon-lit` | Colorful artificial lighting |
| `dramatic lighting` | High contrast, strong shadows |
| `natural lighting` | Realistic daylight |
| `backlit` | Light source behind subject |
| `overcast` | Soft, diffused lighting |
| `silhouette` | Subject as dark outline against light |

## Style & Quality Modifiers

| Modifier | Purpose |
|----------|---------|
| `cinematic` | Film-like quality, shallow depth of field |
| `highly detailed` | Increased texture and fine detail |
| `4K` | High resolution output |
| `photorealistic` | Realistic rendering |
| `animated` | Cartoon or animation style |
| `minimalist` | Clean, simple composition |
| `vintage` | Retro color grading and grain |

## Platform-Specific Prompting

### YouTube Wide (16:9)

Landscape format favors wide establishing shots and horizontal movement:

```
"A sweeping aerial drone shot over a vast mountain range at sunrise, 
golden hour lighting, cinematic, highly detailed."
```

### TikTok / Instagram Reels (9:16)

Portrait format favors vertical subjects and tight framing:

```
"A vertical tracking shot of a person walking through a colorful 
flower market, shallow depth of field, vibrant colors, 4K."
```

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Vague prompts | "A nice video of nature" | Be specific: subject, camera, lighting, style |
| Multiple scenes | "First show X, then Y, then Z" | One clear scene per generation |
| Text/dialogue | "Person says hello" | Veo generates visual content, not speech |
| Excessive length | Overly long prompts dilute intent | Keep to 1-3 sentences |
| Missing camera cues | Static, uninteresting output | Always specify camera movement |

## Iterative Refinement

1. **Start simple** — test a basic prompt to establish the scene
2. **Add camera movement** — specify how the camera should move
3. **Refine lighting** — set the mood with lighting descriptors
4. **Polish with style** — add quality and style modifiers
5. **Compare aspect ratios** — generate both 16:9 and 9:16 to see which works better
