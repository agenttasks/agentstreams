#!/usr/bin/env python3
"""Apply all 30 agentic prompts as structured XML tasks.

Loops through each prompt in the registry, renders it as an XML task,
and emits a manifest mapping each prompt to its codebase integration point
(agent manifest, skill manifest, or shared documentation).

Usage:
    uv run scripts/apply_prompts.py                  # full manifest
    uv run scripts/apply_prompts.py --check          # verify all integrations exist
    uv run scripts/apply_prompts.py --xml            # emit all XML tasks
    uv run scripts/apply_prompts.py --summary        # one-line per prompt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from prompt_registry import get_registry, PromptEntry

# Map each prompt ID to its codebase integration point(s)
INTEGRATION_MAP: dict[str, list[str]] = {
    "01": [
        "skills/agentic-prompts/shared/prompt-patterns.md  # Section composition pattern",
    ],
    "02": [
        "skills/agentic-prompts/SKILL.md  # Documented in system prompts table",
    ],
    "03": [
        ".claude/agents/default-agent.md  # Agent manifest",
    ],
    "04": [
        "skills/agentic-prompts/shared/security-boundaries.md  # Security control matrix",
    ],
    "05": [
        ".claude/agents/coordinator.md  # Agent manifest",
        "skills/agentic-prompts/shared/prompt-patterns.md  # Synthesis pattern",
    ],
    "06": [
        "skills/agentic-prompts/shared/team-communication.md  # Communication protocol",
    ],
    "07": [
        ".claude/agents/verification.md  # Agent manifest",
        "skills/agentic-prompts/shared/prompt-patterns.md  # Adversarial verification",
    ],
    "08": [
        ".claude/agents/explore.md  # Agent manifest",
    ],
    "09": [
        ".claude/agents/agent-architect.md  # Agent manifest",
    ],
    "10": [
        ".claude/agents/statusline-setup.md  # Agent manifest",
    ],
    "11": [
        "skills/agentic-prompts/shared/prompt-patterns.md  # Forced tool schema pattern",
    ],
    "12": [
        "skills/agentic-prompts/shared/prompt-patterns.md  # Anti-injection pattern",
        "skills/agentic-prompts/SKILL.md  # Documented in system prompts table",
    ],
    "13": [
        "skills/agentic-prompts/shared/tool-best-practices.md  # Full tool guidance",
    ],
    "14": [
        "skills/agentic-prompts/SKILL.md  # Documented in tool prompts table",
    ],
    "15": [
        "skills/agentic-prompts/SKILL.md  # Documented in system prompts table",
    ],
    "16": [
        "skills/agentic-prompts/shared/prompt-patterns.md  # Memory hierarchy pattern",
    ],
    "17": [
        ".claude/skills/auto-mode-critique.md  # Skill manifest",
    ],
    "18": [
        ".claude/agents/proactive.md  # Agent manifest",
        "skills/agentic-prompts/shared/prompt-patterns.md  # Cache-aware pacing",
    ],
    "19": [
        ".claude/skills/simplify-review.md  # Skill manifest",
        "skills/agentic-prompts/shared/prompt-patterns.md  # Three-agent review",
    ],
    "20": [
        "skills/agentic-prompts/SKILL.md  # Documented in tool prompts table",
    ],
    "21": [
        "skills/agentic-prompts/shared/compaction-patterns.md  # Full compaction guide",
    ],
    "22": [
        ".claude/skills/away-summary.md  # Skill manifest",
    ],
    "23": [
        ".claude/agents/browser-automation.md  # Agent manifest",
    ],
    "24": [
        "skills/agentic-prompts/shared/prompt-patterns.md  # Memory hierarchy pattern",
    ],
    "25": [
        ".claude/skills/skillify.md  # Skill manifest",
    ],
    "26": [
        ".claude/skills/stuck-diagnostic.md  # Skill manifest",
    ],
    "27": [
        ".claude/skills/remember.md  # Skill manifest",
    ],
    "28": [
        ".claude/skills/update-config.md  # Skill manifest",
    ],
    "29": [
        "skills/agentic-prompts/SKILL.md  # Documented in tool prompts table",
    ],
    "30": [
        ".claude/skills/prompt-suggest.md  # Skill manifest",
    ],
}

ROOT = Path(__file__).parent.parent


def check_integrations() -> list[str]:
    """Verify all integration files exist."""
    errors = []
    for prompt_id, paths in INTEGRATION_MAP.items():
        for path_comment in paths:
            rel_path = path_comment.split("#")[0].strip()
            full_path = ROOT / rel_path
            if not full_path.exists():
                errors.append(f"[{prompt_id}] Missing: {rel_path}")
    return errors


def print_manifest(entries: list[PromptEntry]) -> None:
    """Print the full integration manifest."""
    print("=" * 72)
    print("AGENTIC PROMPT INTEGRATION MANIFEST")
    print(f"Total prompts: {len(entries)}")
    print("=" * 72)

    for entry in entries:
        integrations = INTEGRATION_MAP.get(entry.id, [])
        print(f"\n[{entry.id}] {entry.name} ({entry.prompt_type})")
        print(f"     Purpose: {entry.purpose}")
        print(f"     Source:  vendors/agentic-ai-prompt-research/prompts/{entry.filename}")
        if integrations:
            print("     Integrations:")
            for path in integrations:
                print(f"       -> {path}")
        else:
            print("     Integrations: (none)")


def print_summary(entries: list[PromptEntry]) -> None:
    """One-line summary per prompt."""
    for entry in entries:
        n_integrations = len(INTEGRATION_MAP.get(entry.id, []))
        status = f"{n_integrations} integration(s)"
        print(f"  [{entry.id}] {entry.name:<30} {entry.prompt_type:<8} {status}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply all 30 agentic prompts as XML tasks")
    parser.add_argument("--check", action="store_true", help="Verify all integrations exist")
    parser.add_argument("--xml", action="store_true", help="Emit all prompts as XML tasks")
    parser.add_argument("--summary", action="store_true", help="One-line per prompt")
    args = parser.parse_args()

    entries = get_registry()

    if args.check:
        errors = check_integrations()
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        total = sum(len(v) for v in INTEGRATION_MAP.values())
        print(f"OK: all {total} integration points verified across {len(entries)} prompts")
        return 0

    if args.xml:
        from prompt_registry import render_all_xml
        print(render_all_xml())
        return 0

    if args.summary:
        print_summary(entries)
        return 0

    # Default: full manifest
    print_manifest(entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
