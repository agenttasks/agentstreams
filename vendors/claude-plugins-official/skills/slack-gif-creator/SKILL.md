---
name: slack-gif-creator
description: Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack."
license: Complete terms in LICENSE.txt
---

# Slack GIF Creator

A toolkit providing utilities and knowledge for creating animated GIFs optimized for Slack.

## Slack Requirements

- Emoji GIFs: 128x128 (recommended)
- Message GIFs: 480x480
- FPS: 10-30
- Colors: 48-128
- Duration: Under 3 seconds for emoji GIFs

## Available Utilities

- `core/gif_builder.py` - GIFBuilder: assembles frames and optimizes for Slack
- `core/validators.py` - validate_gif, is_slack_ready
- `core/easing.py` - Easing functions (linear, ease_in, ease_out, bounce_out, elastic_out, back_out)
- `core/frame_composer.py` - Frame helpers (create_blank_frame, create_gradient_background, draw_circle, draw_text, draw_star)

## Animation Concepts

Shake/Vibrate, Pulse/Heartbeat, Bounce, Spin/Rotate, Fade In/Out, Slide, Zoom, Explode/Particle Burst

## Dependencies

```bash
pip install pillow imageio numpy
```
