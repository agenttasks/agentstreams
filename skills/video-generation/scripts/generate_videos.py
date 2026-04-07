#!/usr/bin/env python3
"""Structured video generation pipeline using agentic prompt patterns.

Applies coordinator, verification, and XML task patterns from the
agentic-prompts skill to orchestrate Veo video generation workflows.

Usage:
    uv run skills/video-generation/scripts/generate_videos.py --prompt "drone shot of city"
    uv run skills/video-generation/scripts/generate_videos.py --batch prompts.json
    uv run skills/video-generation/scripts/generate_videos.py --validate-prompts prompts.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree


# ── XML Task Rendering (from agentic-prompts pattern) ────


@dataclass
class VideoTask:
    """A structured video generation task in XML format."""

    task_id: str
    prompt: str
    aspect_ratio: str = "16:9"
    model: str = "veo-3.1-lite"
    output_file: str = "output.mp4"
    platform: str = "youtube"
    status: str = "pending"
    error: str = ""

    def to_xml(self) -> str:
        """Render as structured XML task (agentic-prompts pattern)."""
        lines = [
            f'<video-task id="{self.task_id}" status="{self.status}">',
            f"  <prompt>{_escape_xml(self.prompt)}</prompt>",
            f'  <config model="{self.model}" aspect_ratio="{self.aspect_ratio}" '
            f'platform="{self.platform}"/>',
            f"  <output file=\"{self.output_file}\"/>",
        ]
        if self.error:
            lines.append(f"  <error>{_escape_xml(self.error)}</error>")
        lines.append("</video-task>")
        return "\n".join(lines)

    @classmethod
    def from_dict(cls, data: dict, task_id: str = "01") -> VideoTask:
        """Create from a dictionary (JSON batch input)."""
        platform = "tiktok" if data.get("aspect_ratio") == "9:16" else "youtube"
        return cls(
            task_id=task_id,
            prompt=data["prompt"],
            aspect_ratio=data.get("aspect_ratio", "16:9"),
            model=data.get("model", "veo-3.1-lite"),
            output_file=data.get("output_file", f"video_{task_id}.mp4"),
            platform=data.get("platform", platform),
        )


def _escape_xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── Prompt Validation (verification agent pattern) ───────

PROMPT_RULES = [
    ("camera_movement", [
        "drone", "tracking", "pan", "tilt", "dolly", "static",
        "handheld", "slow motion", "timelapse", "aerial", "sweeping",
    ]),
    ("style_modifier", [
        "cinematic", "4k", "detailed", "photorealistic", "animated",
        "minimalist", "vintage", "dramatic", "vibrant",
    ]),
]


@dataclass
class PromptVerdict:
    """Verification verdict for a video prompt (adversarial pattern)."""

    task_id: str
    prompt: str
    verdict: str  # PASS | FAIL | PARTIAL
    checks: list[dict] = field(default_factory=list)

    def to_xml(self) -> str:
        lines = [f'<verification task_id="{self.task_id}">']
        for check in self.checks:
            result = check["result"]
            lines.append(f'  <check name="{check["name"]}" result="{result}">')
            lines.append(f"    {_escape_xml(check['detail'])}")
            lines.append("  </check>")
        lines.append(f"  <verdict>{self.verdict}</verdict>")
        lines.append("</verification>")
        return "\n".join(lines)


def validate_prompt(task: VideoTask) -> PromptVerdict:
    """Apply adversarial verification to a video prompt."""
    checks = []
    prompt_lower = task.prompt.lower()

    # Check 1: Prompt length
    word_count = len(task.prompt.split())
    if word_count < 5:
        checks.append({"name": "prompt-length", "result": "FAIL",
                        "detail": f"Too short ({word_count} words). Minimum 5 for quality output."})
    elif word_count > 50:
        checks.append({"name": "prompt-length", "result": "FAIL",
                        "detail": f"Too long ({word_count} words). Keep to 1-3 sentences."})
    else:
        checks.append({"name": "prompt-length", "result": "PASS",
                        "detail": f"Good length ({word_count} words)."})

    # Check 2: Camera movement keyword
    has_camera = any(kw in prompt_lower for kw in PROMPT_RULES[0][1])
    if has_camera:
        checks.append({"name": "camera-movement", "result": "PASS",
                        "detail": "Camera movement keyword found."})
    else:
        checks.append({"name": "camera-movement", "result": "FAIL",
                        "detail": "Missing camera movement. Add: drone, tracking, pan, etc."})

    # Check 3: Style modifier
    has_style = any(kw in prompt_lower for kw in PROMPT_RULES[1][1])
    if has_style:
        checks.append({"name": "style-modifier", "result": "PASS",
                        "detail": "Style modifier found."})
    else:
        checks.append({"name": "style-modifier", "result": "FAIL",
                        "detail": "Missing style modifier. Add: cinematic, 4K, detailed, etc."})

    # Check 4: Multiple scenes (anti-pattern)
    scene_markers = ["then", "next", "followed by", "after that", "first"]
    has_multi_scene = any(marker in prompt_lower for marker in scene_markers)
    if has_multi_scene:
        checks.append({"name": "single-scene", "result": "FAIL",
                        "detail": "Multiple scenes detected. Generate one scene per request."})
    else:
        checks.append({"name": "single-scene", "result": "PASS",
                        "detail": "Single scene — good."})

    # Check 5: Aspect ratio validity
    valid_ratios = {"16:9", "9:16"}
    if task.aspect_ratio in valid_ratios:
        checks.append({"name": "aspect-ratio", "result": "PASS",
                        "detail": f"Valid aspect ratio: {task.aspect_ratio}"})
    else:
        checks.append({"name": "aspect-ratio", "result": "FAIL",
                        "detail": f"Invalid aspect ratio: {task.aspect_ratio}. Use 16:9 or 9:16."})

    # Determine verdict
    fails = sum(1 for c in checks if c["result"] == "FAIL")
    if fails == 0:
        verdict = "PASS"
    elif fails <= 1:
        verdict = "PARTIAL"
    else:
        verdict = "FAIL"

    return PromptVerdict(
        task_id=task.task_id,
        prompt=task.prompt,
        verdict=verdict,
        checks=checks,
    )


# ── Task Notification (coordinator pattern) ──────────────

def render_task_notification(
    task_id: str,
    status: str,
    summary: str,
    result: str = "",
) -> str:
    """Emit coordinator-style task notification XML."""
    lines = [
        "<task-notification>",
        f"  <task-id>{task_id}</task-id>",
        f"  <status>{status}</status>",
        f"  <summary>{_escape_xml(summary)}</summary>",
    ]
    if result:
        lines.append(f"  <result>{_escape_xml(result)}</result>")
    lines.append("</task-notification>")
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate prompts from a JSON batch file."""
    batch_path = Path(args.validate_prompts)
    if not batch_path.exists():
        print(f"ERROR: file not found: {batch_path}", file=sys.stderr)
        return 1

    jobs = json.loads(batch_path.read_text())
    all_pass = True

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print("<verification-report>")

    for i, job in enumerate(jobs):
        task = VideoTask.from_dict(job, task_id=f"{i + 1:02d}")
        verdict = validate_prompt(task)
        print(verdict.to_xml())
        if verdict.verdict == "FAIL":
            all_pass = False

    print("</verification-report>")
    return 0 if all_pass else 1


def cmd_generate(args: argparse.Namespace) -> int:
    """Generate video(s) with XML task output."""
    if args.batch:
        batch_path = Path(args.batch)
        if not batch_path.exists():
            print(f"ERROR: file not found: {batch_path}", file=sys.stderr)
            return 1
        jobs = json.loads(batch_path.read_text())
    else:
        jobs = [{
            "prompt": args.prompt,
            "aspect_ratio": args.aspect_ratio,
            "output_file": args.output or "output.mp4",
        }]

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print("<video-generation-plan>")

    for i, job in enumerate(jobs):
        task = VideoTask.from_dict(job, task_id=f"{i + 1:02d}")

        # Validate first (verification pattern)
        verdict = validate_prompt(task)
        if verdict.verdict == "FAIL":
            task.status = "rejected"
            task.error = "Prompt validation failed"
            print(task.to_xml())
            print(render_task_notification(
                task.task_id, "failed",
                f"Prompt rejected: {verdict.checks}",
            ))
            continue

        # Emit the generation plan
        task.status = "ready"
        print(task.to_xml())

    print("</video-generation-plan>")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Structured video generation pipeline with agentic prompt patterns"
    )
    parser.add_argument("--prompt", help="Single video prompt")
    parser.add_argument("--aspect-ratio", default="16:9", help="Aspect ratio (16:9 or 9:16)")
    parser.add_argument("--output", help="Output filename")
    parser.add_argument("--batch", help="JSON batch file with multiple prompts")
    parser.add_argument("--validate-prompts", help="Validate prompts from JSON without generating")

    args = parser.parse_args()

    if args.validate_prompts:
        return cmd_validate(args)

    if not args.prompt and not args.batch:
        parser.print_help()
        return 1

    return cmd_generate(args)


if __name__ == "__main__":
    raise SystemExit(main())
