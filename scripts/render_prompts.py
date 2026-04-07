#!/usr/bin/env python3
"""Render agentic prompt patterns as structured XML tasks.

Reads 30 prompt files from vendors/agentic-ai-prompt-research/prompts/
and emits structured XML suitable for programmatic consumption by
Claude Code agents and skills.

Usage:
    uv run scripts/render_prompts.py                    # all prompts
    uv run scripts/render_prompts.py --type agent       # filter by type
    uv run scripts/render_prompts.py --id 07            # single prompt
    uv run scripts/render_prompts.py --tag security     # filter by tag
    uv run scripts/render_prompts.py --format json      # JSON output
    uv run scripts/render_prompts.py --validate         # validate sources exist
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add scripts/ to path for import
sys.path.insert(0, str(Path(__file__).parent))

from prompt_registry import (
    PromptEntry,
    extract_prompt_body,
    get_by_id,
    get_by_tag,
    get_by_type,
    get_registry,
)


def validate_sources() -> list[str]:
    """Check that all source prompt files exist and are non-empty."""
    errors = []
    for entry in get_registry():
        path = entry.source_path()
        if not path.exists():
            errors.append(f"[{entry.id}] Missing: {path}")
        elif path.stat().st_size == 0:
            errors.append(f"[{entry.id}] Empty: {path}")
    return errors


def render_json(entries: list[PromptEntry], include_body: bool = False) -> str:
    """Render entries as JSON."""
    items = []
    for e in entries:
        item = {
            "id": e.id,
            "name": e.name,
            "type": e.prompt_type,
            "purpose": e.purpose,
            "constraints": e.constraints,
            "tools_allowed": e.tools_allowed,
            "tools_denied": e.tools_denied,
            "output_format": e.output_format,
            "tags": e.tags,
            "source": str(e.source_path()),
        }
        if include_body:
            try:
                content = e.read_source()
                item["body"] = extract_prompt_body(content)
            except FileNotFoundError:
                item["body"] = ""
        items.append(item)
    return json.dumps(items, indent=2)


def render_xml(entries: list[PromptEntry]) -> str:
    """Render entries as XML task document."""
    if len(entries) == 1:
        return entries[0].to_xml()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<prompt-tasks>"]
    for entry in entries:
        lines.append(entry.to_xml())
    lines.append("</prompt-tasks>")
    return "\n".join(lines)


def render_table(entries: list[PromptEntry]) -> str:
    """Render entries as a markdown table."""
    lines = ["| ID | Name | Type | Purpose |", "|-----|------|------|---------|"]
    for e in entries:
        lines.append(f"| {e.id} | {e.name} | {e.prompt_type} | {e.purpose} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render agentic prompt patterns as XML tasks")
    parser.add_argument(
        "--type", choices=["system", "agent", "tool", "skill"], help="Filter by prompt type"
    )
    parser.add_argument("--id", help="Render a single prompt by ID (e.g., 07)")
    parser.add_argument("--tag", help="Filter by tag (e.g., security, parallel)")
    parser.add_argument(
        "--format",
        choices=["xml", "json", "table"],
        default="xml",
        help="Output format (default: xml)",
    )
    parser.add_argument("--body", action="store_true", help="Include prompt body in JSON output")
    parser.add_argument("--validate", action="store_true", help="Validate all source files exist")
    args = parser.parse_args()

    if args.validate:
        errors = validate_sources()
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        print(f"OK: all {len(get_registry())} source files present")
        return 0

    # Filter entries
    if args.id:
        entry = get_by_id(args.id)
        if not entry:
            print(f"ERROR: no prompt with ID '{args.id}'", file=sys.stderr)
            return 1
        entries = [entry]
    elif args.type:
        entries = get_by_type(args.type)
    elif args.tag:
        entries = get_by_tag(args.tag)
    else:
        entries = get_registry()

    if not entries:
        print("No prompts matched the filter", file=sys.stderr)
        return 1

    # Render
    if args.format == "json":
        print(render_json(entries, include_body=args.body))
    elif args.format == "table":
        print(render_table(entries))
    else:
        print(render_xml(entries))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
