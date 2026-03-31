# Computer Use Tool Reference

## Overview

The computer use tool gives Claude the ability to interact with a computer display — taking screenshots, moving the mouse, clicking, typing, and scrolling. Requires a beta header and a display server.

## Tool Definition

```json
{
  "type": "computer_20250124",
  "name": "computer",
  "display_width_px": 1920,
  "display_height_px": 1080,
  "display_number": 0
}
```

**Required header**: `anthropic-beta: computer-use-2025-01-24`

## Actions

| Action | Parameters | Description |
|--------|-----------|-------------|
| `screenshot` | — | Capture current display state |
| `mouse_move` | `coordinate: [x, y]` | Move cursor to position |
| `left_click` | — | Click at current position |
| `right_click` | — | Right-click at current position |
| `double_click` | — | Double-click at current position |
| `middle_click` | — | Middle-click at current position |
| `type` | `text: string` | Type text at current position |
| `key` | `text: string` | Press key combination (e.g., "ctrl+c") |
| `scroll` | `coordinate: [x, y], direction: "up"/"down"` | Scroll at position |
| `drag` | `start_coordinate: [x, y], end_coordinate: [x, y]` | Drag from start to end |

## Agentic Loop

Computer use works as a screenshot → action → screenshot loop:

1. Claude requests a `screenshot` action
2. You capture the display and return the image
3. Claude analyzes the screenshot and decides next action
4. You execute the action (click, type, etc.)
5. Return to step 1

Always return a screenshot after each action so Claude can verify the result.

## Environment Setup

### Headless VM (Recommended)

```bash
# Docker with virtual display
docker run -d \
  -e DISPLAY=:0 \
  -p 5900:5900 \
  kasmweb/ubuntu-desktop:latest
```

### Required Components

- **Display server**: Xvfb, Xephyr, or a real display
- **Screenshot tool**: `scrot`, `gnome-screenshot`, or `xdotool`
- **Input control**: `xdotool` or `ydotool` for mouse/keyboard
- **VNC** (optional): For remote viewing during development

## Safety

- Run in an isolated VM with no access to sensitive data
- Restrict network access to only necessary domains
- Monitor actions in real-time during development
- Set action limits (max clicks, max keystrokes per session)
- Never use computer use with access to production credentials
