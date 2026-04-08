#!/usr/bin/env python3
"""RSS XML spider crawler for Claude Code changelog.

Fetches the Claude Code changelog, parses each version entry and bullet point,
applies bloom-filter-style deduplication via content hashing, and emits
structured XML tasks for codebase improvement.

Inspired by Scrapy's XMLFeedSpider pattern:
- itertag-based parsing of changelog sections
- parse_node method per entry
- adapt_response for HTML→structured conversion

Usage:
    uv run scripts/crawl_changelog.py                              # fetch + emit XML tasks
    uv run scripts/crawl_changelog.py --cached taxonomy/changelog.md   # use cached file
    uv run scripts/crawl_changelog.py --format json                # JSON output
    uv run scripts/crawl_changelog.py --filter feat                # only features
    uv run scripts/crawl_changelog.py --decompose                  # decompose into subtasks
    uv run scripts/crawl_changelog.py --rss                        # emit RSS 2.0 XML feed
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import aiohttp
from spiders import content_hash as _base_hash
from spiders import html_to_text  # shared base module

# UDA integration: use src/bloom.py BloomFilter when available
try:
    from src.bloom import BloomFilter as _BloomFilter

    _DEDUP = _BloomFilter(expected_items=10_000, fp_rate=0.01)
    _use_src_bloom = True
except ImportError:
    from spiders import BloomDedup

    _DEDUP = BloomDedup(hash_length=16)
    _use_src_bloom = False

# ── Constants ────────────────────────────────────────────────

CHANGELOG_URL = "https://code.claude.com/docs/en/changelog"
USER_AGENT = "agentstreams-crawler/2.0 (changelog spider)"


# ── Content hashing / bloom filter dedup ─────────────────────


def content_hash(text: str) -> str:
    """SHA-256 content hash (16 chars) for bloom-filter-style deduplication."""
    return _base_hash(text, length=16)


def is_new(text: str) -> bool:
    """Check if content is new (not seen before). Uses src/bloom.BloomFilter when available."""
    return _DEDUP.is_new(text)


# ── Data models ──────────────────────────────────────────────


@dataclass
class ChangelogBullet:
    """Single changelog bullet point."""

    version: str
    date: str
    text: str
    category: str  # feat | fix | improve | remove | other
    hash: str = ""

    def __post_init__(self):
        if not self.hash:
            self.hash = content_hash(f"{self.version}:{self.text}")


@dataclass
class ChangelogEntry:
    """A version release with its bullet points."""

    version: str
    date: str
    bullets: list[ChangelogBullet] = field(default_factory=list)


@dataclass
class XMLTask:
    """A structured XML task derived from a changelog bullet."""

    task_id: str
    source_version: str
    source_date: str
    category: str
    title: str
    description: str
    subtasks: list[str] = field(default_factory=list)
    priority: str = "medium"  # low | medium | high
    hash: str = ""

    def to_xml(self) -> str:
        lines = [
            f'<task id="{_esc(self.task_id)}" category="{_esc(self.category)}" '
            f'priority="{self.priority}">',
            f'  <source version="{_esc(self.source_version)}" date="{_esc(self.source_date)}"/>',
            f"  <title>{_esc(self.title)}</title>",
            f"  <description>{_esc(self.description)}</description>",
        ]
        if self.subtasks:
            lines.append("  <subtasks>")
            for i, st in enumerate(self.subtasks, 1):
                lines.append(f'    <subtask id="{self.task_id}.{i}">{_esc(st)}</subtask>')
            lines.append("  </subtasks>")
        lines.append("</task>")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        d = {
            "task_id": self.task_id,
            "source_version": self.source_version,
            "source_date": self.source_date,
            "category": self.category,
            "priority": self.priority,
            "title": self.title,
            "description": self.description,
            "hash": self.hash,
        }
        if self.subtasks:
            d["subtasks"] = self.subtasks
        return d


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── XMLFeedSpider-style parser ───────────────────────────────


def classify_bullet(text: str) -> str:
    """Classify a changelog bullet into a category (Scrapy parse_node pattern)."""
    t = text.lower()
    if t.startswith("added") or t.startswith("new "):
        return "feat"
    if t.startswith("fixed"):
        return "fix"
    if t.startswith("improved") or t.startswith("reduced") or t.startswith("optimized"):
        return "improve"
    if t.startswith("removed") or t.startswith("changed") or t.startswith("deprecated"):
        return "remove"
    return "other"


def priority_from_bullet(text: str) -> str:
    """Assign priority based on bullet content."""
    t = text.lower()
    if any(kw in t for kw in ["security", "crash", "oom", "critical", "breaking"]):
        return "high"
    if any(kw in t for kw in ["performance", "fixed", "regression", "leak"]):
        return "medium"
    return "low"


def decompose_bullet(bullet: ChangelogBullet) -> list[str]:
    """Decompose a bullet into subtasks for codebase improvements."""
    subtasks = []
    text = bullet.text.lower()

    if bullet.category == "feat":
        subtasks.append(f"Evaluate adding equivalent of: {bullet.text}")
        subtasks.append("Update SKILL.md if new capability applies to agentstreams")
        if any(kw in text for kw in ["agent", "subagent", "hook", "mcp"]):
            subtasks.append("Update .claude/agents/ or .claude/skills/ manifests")
        if any(kw in text for kw in ["env", "setting", "config"]):
            subtasks.append("Update .claude/settings.json if applicable")

    elif bullet.category == "fix":
        subtasks.append(f"Check if agentstreams is affected by: {bullet.text}")
        subtasks.append("Run related test suite to verify")
        if "edit" in text or "write" in text:
            subtasks.append("Review Edit/Write tool usage in scripts/")

    elif bullet.category == "improve":
        subtasks.append(f"Evaluate applying optimization: {bullet.text}")
        if "performance" in text or "speed" in text:
            subtasks.append("Profile relevant scripts for performance regression")
        if "cache" in text:
            subtasks.append("Review caching strategy in crawl/extract scripts")

    elif bullet.category == "remove":
        subtasks.append(f"Check for usage of removed feature: {bullet.text}")
        subtasks.append("Update documentation if referencing removed functionality")

    if not subtasks:
        subtasks.append(f"Review changelog item: {bullet.text}")

    return subtasks


# ── Changelog parsing (adapt_response pattern) ──────────────


VERSION_RE = re.compile(r"^#+\s*([\d.]+)\s*[-–—]\s*(.+)$", re.MULTILINE)
BULLET_RE = re.compile(r"^\s*[\*\-]\s+(.+)$", re.MULTILINE)


def parse_changelog_text(text: str) -> list[ChangelogEntry]:
    """Parse markdown changelog into structured entries (adapt_response)."""
    entries = []
    sections = VERSION_RE.split(text)

    # sections: [preamble, ver1, date1, body1, ver2, date2, body2, ...]
    i = 1
    while i + 2 <= len(sections):
        version = sections[i].strip()
        date = sections[i + 1].strip()
        body = sections[i + 2] if i + 2 < len(sections) else ""

        entry = ChangelogEntry(version=version, date=date)
        for match in BULLET_RE.finditer(body):
            bullet_text = match.group(1).strip()
            if is_new(f"{version}:{bullet_text}"):
                entry.bullets.append(
                    ChangelogBullet(
                        version=version,
                        date=date,
                        text=bullet_text,
                        category=classify_bullet(bullet_text),
                    )
                )
        if entry.bullets:
            entries.append(entry)
        i += 3

    return entries


# ── Async fetch ──────────────────────────────────────────────


async def fetch_changelog(url: str) -> str:
    """Fetch changelog HTML and convert to text."""
    async with (
        aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session,
        session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp,
    ):
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} fetching {url}")
        html = await resp.text()
        return html_to_text(html)


# ── Task generation ──────────────────────────────────────────


def bullets_to_tasks(
    entries: list[ChangelogEntry],
    decompose: bool = False,
    category_filter: str | None = None,
) -> list[XMLTask]:
    """Convert changelog bullets to structured XML tasks."""
    tasks = []
    task_num = 0

    for entry in entries:
        for bullet in entry.bullets:
            if category_filter and bullet.category != category_filter:
                continue

            task_num += 1
            task_id = f"CL-{entry.version.replace('.', '')}-{task_num:03d}"

            subtasks = decompose_bullet(bullet) if decompose else []

            tasks.append(
                XMLTask(
                    task_id=task_id,
                    source_version=entry.version,
                    source_date=entry.date,
                    category=bullet.category,
                    title=bullet.text[:120],
                    description=bullet.text,
                    subtasks=subtasks,
                    priority=priority_from_bullet(bullet.text),
                    hash=bullet.hash,
                )
            )

    return tasks


# ── RSS 2.0 Output ──────────────────────────────────────────


def render_rss(entries: list[ChangelogEntry]) -> str:
    """Render changelog as RSS 2.0 XML feed."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "  <channel>",
        "    <title>Claude Code Changelog</title>",
        "    <link>https://code.claude.com/docs/en/changelog</link>",
        "    <description>Claude Code release notes and changelog</description>",
    ]
    for entry in entries:
        desc_bullets = "\n".join(f"- {b.text}" for b in entry.bullets)
        lines.extend(
            [
                "    <item>",
                f"      <title>Claude Code {_esc(entry.version)} - {_esc(entry.date)}</title>",
                "      <link>https://code.claude.com/docs/en/changelog</link>",
                f"      <guid>claude-code-{_esc(entry.version)}</guid>",
                f"      <pubDate>{_esc(entry.date)}</pubDate>",
                f"      <description>{_esc(desc_bullets)}</description>",
                "    </item>",
            ]
        )
    lines.extend(
        [
            "  </channel>",
            "</rss>",
        ]
    )
    return "\n".join(lines)


# ── XML Task Output ─────────────────────────────────────────


def render_xml_tasks(tasks: list[XMLTask]) -> str:
    """Render all tasks as XML document."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<changelog-tasks count="{len(tasks)}">',
    ]
    for task in tasks:
        lines.append(task.to_xml())
    lines.append("</changelog-tasks>")
    return "\n".join(lines)


def render_json_tasks(tasks: list[XMLTask]) -> str:
    """Render as JSON array."""
    return json.dumps([t.to_dict() for t in tasks], indent=2)


# ── CLI ──────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="RSS XML spider crawler for Claude Code changelog")
    parser.add_argument("--cached", help="Use a cached markdown file instead of fetching")
    parser.add_argument(
        "--format",
        choices=["xml", "json", "rss"],
        default="xml",
        help="Output format (default: xml)",
    )
    parser.add_argument(
        "--filter", choices=["feat", "fix", "improve", "remove", "other"], help="Filter by category"
    )
    parser.add_argument("--decompose", action="store_true", help="Decompose bullets into subtasks")
    parser.add_argument("--rss", action="store_true", help="Emit RSS 2.0 feed")
    parser.add_argument("--save-taxonomy", help="Save fetched changelog to taxonomy file")
    parser.add_argument(
        "--max-entries",
        type=int,
        default=10,
        help="Maximum changelog entries to process (default: 10)",
    )
    args = parser.parse_args()

    # Fetch or load changelog
    if args.cached:
        text = Path(args.cached).read_text(encoding="utf-8")
    else:
        try:
            text = asyncio.run(fetch_changelog(CHANGELOG_URL))
        except Exception as e:
            print(f"ERROR: failed to fetch changelog: {e}", file=sys.stderr)
            print("Use --cached with a local file instead.", file=sys.stderr)
            return 1

    # Save taxonomy if requested
    if args.save_taxonomy:
        Path(args.save_taxonomy).write_text(text, encoding="utf-8")
        print(f"Saved to {args.save_taxonomy}", file=sys.stderr)

    # Parse
    entries = parse_changelog_text(text)[: args.max_entries]

    if not entries:
        print("No changelog entries found.", file=sys.stderr)
        return 1

    print(
        f"Parsed {len(entries)} entries, {sum(len(e.bullets) for e in entries)} bullets",
        file=sys.stderr,
    )

    # RSS mode
    if args.rss or args.format == "rss":
        print(render_rss(entries))
        return 0

    # Task mode
    tasks = bullets_to_tasks(entries, decompose=args.decompose, category_filter=args.filter)

    if not tasks:
        print("No tasks matched filter.", file=sys.stderr)
        return 1

    print(f"Generated {len(tasks)} tasks", file=sys.stderr)

    if args.format == "json":
        print(render_json_tasks(tasks))
    else:
        print(render_xml_tasks(tasks))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
