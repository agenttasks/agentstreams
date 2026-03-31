#!/usr/bin/env python3
"""Validate the three-layer auto-memory architecture.

Checks the self-healing memory system for integrity:
1. MEMORY.md index — entries point to files that exist, lines under 150 chars
2. Topic files — valid frontmatter (name, description, type), not orphaned
3. Architecture constraints — index under 200 lines, no content in index

This implements the "strict write discipline" pattern: the index stores
only pointers, actual knowledge lives in topic files, and raw transcripts
are never loaded — only grep'd for specific identifiers.

Usage:
  uv run scripts/validate-memory.py <memory_dir>
  uv run scripts/validate-memory.py <memory_dir> --check-only
  uv run scripts/validate-memory.py <memory_dir> --fix

Examples:
  uv run scripts/validate-memory.py ~/.claude/projects/-Users-alexzh-agenttasks/memory/
"""

import argparse
import re
import sys
from pathlib import Path

# ── Constants ──────────────────────────────────────────────

MAX_INDEX_LINES = 200
MAX_LINE_LENGTH = 150
VALID_MEMORY_TYPES = {"user", "feedback", "project", "reference"}
REQUIRED_FRONTMATTER_FIELDS = {"name", "description", "type"}


# ── Index validation ──────────────────────────────────────


def parse_index_entries(index_text: str) -> list[dict]:
    """Parse MEMORY.md index into structured entries."""
    entries = []
    for i, line in enumerate(index_text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Match markdown link pattern: - [Title](file.md) — description
        match = re.match(r"^-\s+\[([^\]]+)\]\(([^)]+)\)\s*(?:—\s*(.*))?$", stripped)
        if match:
            entries.append(
                {
                    "line": i,
                    "title": match.group(1),
                    "file": match.group(2),
                    "description": match.group(3) or "",
                    "raw": stripped,
                }
            )
        elif stripped.startswith("-"):
            # Non-link list item — might be malformed
            entries.append(
                {
                    "line": i,
                    "title": None,
                    "file": None,
                    "description": stripped,
                    "raw": stripped,
                }
            )

    return entries


def validate_index(index_text: str, memory_dir: Path) -> tuple[list[str], list[str]]:
    """Validate MEMORY.md index. Returns (errors, warnings)."""
    errors = []
    warnings = []
    lines = index_text.splitlines()

    # Check line count
    if len(lines) > MAX_INDEX_LINES:
        errors.append(
            f"MEMORY.md has {len(lines)} lines (max {MAX_INDEX_LINES}) — "
            "content beyond line 200 won't be loaded at session start"
        )

    # Check individual lines
    for i, line in enumerate(lines, 1):
        if len(line) > MAX_LINE_LENGTH:
            warnings.append(f"Line {i}: {len(line)} chars (recommended max {MAX_LINE_LENGTH})")

    # Check entries
    entries = parse_index_entries(index_text)
    for entry in entries:
        if entry["file"] is None:
            warnings.append(
                f"Line {entry['line']}: entry without file link — '{entry['raw'][:60]}'"
            )
            continue

        # Check file exists
        target = memory_dir / entry["file"]
        if not target.exists():
            errors.append(f"Line {entry['line']}: broken link — '{entry['file']}' does not exist")

    # Check for content in index (index should only have pointers)
    content_patterns = [
        r"^#{2,}\s",  # Sub-headings (## or deeper)
        r"^```",  # Code blocks
        r"^\*\*\w+\*\*:",  # Bold key-value pairs suggesting inline content
    ]
    for i, line in enumerate(lines, 1):
        for pattern in content_patterns:
            if re.match(pattern, line.strip()):
                warnings.append(
                    f"Line {i}: possible content in index — "
                    "MEMORY.md should store pointers, not content"
                )
                break

    return errors, warnings


# ── Topic file validation ─────────────────────────────────


def parse_frontmatter(content: str) -> dict | None:
    """Parse YAML frontmatter from a markdown file."""
    if not content.startswith("---"):
        return None

    end = content.find("---", 3)
    if end == -1:
        return None

    frontmatter_text = content[3:end].strip()
    fields = {}
    for line in frontmatter_text.splitlines():
        match = re.match(r"^(\w+):\s*(.+)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()

    return fields


def validate_topic_file(file: Path) -> tuple[list[str], list[str]]:
    """Validate a single topic/memory file. Returns (errors, warnings)."""
    errors = []
    warnings = []

    try:
        content = file.read_text()
    except (OSError, UnicodeDecodeError) as e:
        errors.append(f"{file.name}: cannot read — {e}")
        return errors, warnings

    if not content.strip():
        errors.append(f"{file.name}: empty file")
        return errors, warnings

    # Check frontmatter
    frontmatter = parse_frontmatter(content)
    if frontmatter is None:
        errors.append(f"{file.name}: missing YAML frontmatter (---)")
        return errors, warnings

    # Check required fields
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in frontmatter:
            errors.append(f"{file.name}: missing required field '{field}'")

    # Validate type field
    if "type" in frontmatter and frontmatter["type"] not in VALID_MEMORY_TYPES:
        errors.append(
            f"{file.name}: invalid type '{frontmatter['type']}' — "
            f"must be one of {', '.join(sorted(VALID_MEMORY_TYPES))}"
        )

    # Check description is specific enough (not just the name repeated)
    if "description" in frontmatter and "name" in frontmatter:
        if frontmatter["description"].lower() == frontmatter["name"].lower():
            warnings.append(
                f"{file.name}: description is identical to name — should be more specific"
            )

    return errors, warnings


# ── Orphan detection ──────────────────────────────────────


def find_orphaned_files(memory_dir: Path, index_text: str) -> list[Path]:
    """Find topic files not referenced in MEMORY.md."""
    entries = parse_index_entries(index_text)
    referenced = {e["file"] for e in entries if e["file"]}

    orphans = []
    for file in sorted(memory_dir.glob("*.md")):
        if file.name == "MEMORY.md":
            continue
        if file.name not in referenced:
            orphans.append(file)

    return orphans


# ── Full validation ───────────────────────────────────────


def validate_memory_dir(memory_dir: Path) -> tuple[list[str], list[str]]:
    """Run all validation checks on a memory directory."""
    all_errors = []
    all_warnings = []

    index_path = memory_dir / "MEMORY.md"
    if not index_path.exists():
        all_errors.append("MEMORY.md not found")
        return all_errors, all_warnings

    index_text = index_path.read_text()

    # Validate index
    errors, warnings = validate_index(index_text, memory_dir)
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # Validate each topic file
    for file in sorted(memory_dir.glob("*.md")):
        if file.name == "MEMORY.md":
            continue
        errors, warnings = validate_topic_file(file)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    # Check for orphans
    orphans = find_orphaned_files(memory_dir, index_text)
    for orphan in orphans:
        all_warnings.append(f"Orphaned file: {orphan.name} — not referenced in MEMORY.md")

    return all_errors, all_warnings


# ── Report ────────────────────────────────────────────────


def print_report(
    memory_dir: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    """Print validation report."""
    index_path = memory_dir / "MEMORY.md"
    topic_files = list(memory_dir.glob("*.md"))
    topic_count = len([f for f in topic_files if f.name != "MEMORY.md"])

    print(f"\nMemory Validation — {memory_dir}", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    if index_path.exists():
        lines = index_path.read_text().splitlines()
        entries = parse_index_entries(index_path.read_text())
        print(f"Index: {len(lines)} lines, {len(entries)} entries", file=sys.stderr)
    print(f"Topic files: {topic_count}", file=sys.stderr)

    if errors:
        print(f"\nErrors ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)

    if warnings:
        print(f"\nWarnings ({len(warnings)}):", file=sys.stderr)
        for w in warnings:
            print(f"  ⚠ {w}", file=sys.stderr)

    if not errors and not warnings:
        print("\n✓ All checks passed", file=sys.stderr)
    elif not errors:
        print(f"\n✓ No errors ({len(warnings)} warnings)", file=sys.stderr)
    else:
        print(f"\n✗ {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)

    print(f"{'=' * 60}", file=sys.stderr)


# ── Main ─────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Validate auto-memory architecture")
    parser.add_argument("memory_dir", help="Path to memory directory containing MEMORY.md")
    parser.add_argument("--check-only", action="store_true", help="Exit 1 on any error")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix: remove broken index entries, add orphans to index",
    )
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir)
    if not memory_dir.is_dir():
        print(f"Error: {memory_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    errors, warnings = validate_memory_dir(memory_dir)
    print_report(memory_dir, errors, warnings)

    if args.fix and errors:
        fix_memory(memory_dir, errors)

    if args.check_only and errors:
        sys.exit(1)


def fix_memory(memory_dir: Path, errors: list[str]) -> None:
    """Auto-fix common memory issues."""
    index_path = memory_dir / "MEMORY.md"
    if not index_path.exists():
        return

    content = index_path.read_text()
    lines = content.splitlines()
    fixed = []

    # Remove lines with broken links
    broken_files = set()
    for error in errors:
        match = re.search(r"broken link — '([^']+)'", error)
        if match:
            broken_files.add(match.group(1))

    if broken_files:
        new_lines = []
        removed = 0
        for line in lines:
            matched_file = None
            for bf in broken_files:
                if f"]({bf})" in line:
                    matched_file = bf
                    break
            if matched_file:
                removed += 1
                fixed.append(f"Removed broken link: {matched_file}")
            else:
                new_lines.append(line)

        if removed:
            index_path.write_text("\n".join(new_lines) + "\n")
            print(f"\nFixed {removed} broken link(s) in MEMORY.md", file=sys.stderr)

    # Add orphaned files to index
    orphans = find_orphaned_files(memory_dir, index_path.read_text())
    if orphans:
        with open(index_path, "a") as f:
            for orphan in orphans:
                fm = parse_frontmatter(orphan.read_text())
                title = fm.get("name", orphan.stem) if fm else orphan.stem
                desc = fm.get("description", "needs description") if fm else "needs description"
                f.write(f"- [{title}]({orphan.name}) — {desc}\n")
                fixed.append(f"Added orphan to index: {orphan.name}")

        print(f"Added {len(orphans)} orphan(s) to MEMORY.md", file=sys.stderr)

    if fixed:
        print("\nFixes applied:", file=sys.stderr)
        for f in fixed:
            print(f"  ✓ {f}", file=sys.stderr)


if __name__ == "__main__":
    main()
