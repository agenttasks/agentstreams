"""Tests for RSS XML spider crawler for Claude Code changelog."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from crawl_changelog import (
    DEDUP_SEEN,
    ChangelogBullet,
    XMLTask,
    bullets_to_tasks,
    classify_bullet,
    content_hash,
    decompose_bullet,
    is_new,
    parse_changelog_text,
    priority_from_bullet,
    render_rss,
    render_xml_tasks,
)

SAMPLE_CHANGELOG = """# Changelog

## 2.1.92 - April 4, 2026
* Added `forceRemoteSettingsRefresh` policy setting for fail-closed remote settings
* Fixed subagent spawning permanently failing after tmux windows killed
* Improved Write tool diff computation speed (60% faster)
* Removed `/tag` command

## 2.1.91 - April 2, 2026
* Added MCP tool result persistence override via `_meta["anthropic/maxResultSizeChars"]`
* Fixed transcript chain breaks on `--resume`
* Improved `/claude-api` skill guidance

## 2.1.90 - April 1, 2026
* Added `/powerup` interactive lessons with animated demos
* Fixed infinite loop with rate-limit dialog
* Improved performance: eliminated per-turn JSON.stringify of MCP schemas
"""


@pytest.fixture(autouse=True)
def clear_dedup():
    """Clear dedup set before each test."""
    DEDUP_SEEN.clear()


class TestContentHash:
    def test_deterministic(self):
        assert content_hash("hello") == content_hash("hello")

    def test_different_inputs(self):
        assert content_hash("hello") != content_hash("world")

    def test_length(self):
        assert len(content_hash("test")) == 16


class TestDedup:
    def test_first_seen_is_new(self):
        assert is_new("unique text") is True

    def test_second_seen_is_not_new(self):
        is_new("duplicate")
        assert is_new("duplicate") is False

    def test_different_texts_both_new(self):
        assert is_new("text a") is True
        assert is_new("text b") is True


class TestClassifyBullet:
    def test_feat(self):
        assert classify_bullet("Added new feature X") == "feat"

    def test_fix(self):
        assert classify_bullet("Fixed crash in module Y") == "fix"

    def test_improve(self):
        assert classify_bullet("Improved performance of Z") == "improve"

    def test_remove(self):
        assert classify_bullet("Removed deprecated API") == "remove"

    def test_other(self):
        assert classify_bullet("Some other change") == "other"


class TestPriority:
    def test_high_security(self):
        assert priority_from_bullet("Fixed critical security vulnerability") == "high"

    def test_high_crash(self):
        assert priority_from_bullet("Fixed crash with OOM error") == "high"

    def test_medium_performance(self):
        assert priority_from_bullet("Improved performance of parser") == "medium"

    def test_medium_fix(self):
        assert priority_from_bullet("Fixed rendering issue") == "medium"

    def test_low_default(self):
        assert priority_from_bullet("Added new color option") == "low"


class TestParseChangelog:
    def test_parses_entries(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        assert len(entries) == 3
        assert entries[0].version == "2.1.92"
        assert entries[0].date == "April 4, 2026"

    def test_parses_bullets(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        assert len(entries[0].bullets) == 4
        assert entries[0].bullets[0].text.startswith("Added")

    def test_classifies_bullets(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        cats = [b.category for b in entries[0].bullets]
        assert cats == ["feat", "fix", "improve", "remove"]

    def test_deduplicates(self):
        entries1 = parse_changelog_text(SAMPLE_CHANGELOG)
        count1 = sum(len(e.bullets) for e in entries1)
        DEDUP_SEEN.clear()
        entries2 = parse_changelog_text(SAMPLE_CHANGELOG)
        count2 = sum(len(e.bullets) for e in entries2)
        assert count1 == count2  # same content parses same count independently

    def test_empty_input(self):
        entries = parse_changelog_text("No changelog here")
        assert entries == []


class TestXMLTask:
    def test_basic_xml(self):
        task = XMLTask(
            task_id="CL-2192-001",
            source_version="2.1.92",
            source_date="April 4, 2026",
            category="feat",
            title="Added new feature",
            description="Added new feature for X",
        )
        xml = task.to_xml()
        assert '<task id="CL-2192-001"' in xml
        assert 'category="feat"' in xml
        assert "<title>" in xml

    def test_xml_with_subtasks(self):
        task = XMLTask(
            task_id="CL-001",
            source_version="2.1.92",
            source_date="April 4, 2026",
            category="feat",
            title="Test",
            description="Test desc",
            subtasks=["Do A", "Do B"],
        )
        xml = task.to_xml()
        assert "<subtasks>" in xml
        assert 'id="CL-001.1"' in xml
        assert 'id="CL-001.2"' in xml

    def test_xml_parses(self):
        task = XMLTask(
            task_id="CL-001",
            source_version="2.1.92",
            source_date="April 4, 2026",
            category="fix",
            title="Test fix",
            description="Fixed something",
        )
        root = ElementTree.fromstring(task.to_xml())
        assert root.tag == "task"
        assert root.attrib["id"] == "CL-001"

    def test_to_dict(self):
        task = XMLTask(
            task_id="CL-001",
            source_version="2.1.92",
            source_date="April 4, 2026",
            category="feat",
            title="Test",
            description="Test desc",
        )
        d = task.to_dict()
        assert d["task_id"] == "CL-001"
        assert d["category"] == "feat"


class TestBulletsToTasks:
    def test_generates_tasks(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        tasks = bullets_to_tasks(entries)
        assert len(tasks) > 0
        assert all(t.task_id.startswith("CL-") for t in tasks)

    def test_filter_by_category(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        tasks = bullets_to_tasks(entries, category_filter="feat")
        assert all(t.category == "feat" for t in tasks)

    def test_decompose(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        tasks = bullets_to_tasks(entries, decompose=True)
        assert any(len(t.subtasks) > 0 for t in tasks)


class TestDecomposeBullet:
    def test_feat_decomposition(self):
        bullet = ChangelogBullet("2.1.92", "April 4", "Added new agent hook system", "feat")
        subtasks = decompose_bullet(bullet)
        assert len(subtasks) >= 2
        assert any("agent" in s.lower() or "manifest" in s.lower() for s in subtasks)

    def test_fix_decomposition(self):
        bullet = ChangelogBullet("2.1.92", "April 4", "Fixed crash in edit tool", "fix")
        subtasks = decompose_bullet(bullet)
        assert len(subtasks) >= 2


class TestRSSOutput:
    def test_renders_rss(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        rss = render_rss(entries)
        assert '<rss version="2.0"' in rss
        assert "<channel>" in rss
        assert "<item>" in rss
        assert "Claude Code" in rss

    def test_rss_parses(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        rss = render_rss(entries)
        root = ElementTree.fromstring(rss)
        assert root.tag == "rss"
        items = root.findall(".//item")
        assert len(items) == 3


class TestXMLTasksOutput:
    def test_renders_xml(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        tasks = bullets_to_tasks(entries)
        xml = render_xml_tasks(tasks)
        assert "<changelog-tasks" in xml
        assert 'count="' in xml

    def test_xml_parses(self):
        entries = parse_changelog_text(SAMPLE_CHANGELOG)
        tasks = bullets_to_tasks(entries)
        xml = render_xml_tasks(tasks)
        root = ElementTree.fromstring(xml)
        assert root.tag == "changelog-tasks"


class TestCLI:
    SCRIPT = str(Path(__file__).parent.parent / "scripts" / "crawl_changelog.py")

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, self.SCRIPT, *args],
            capture_output=True,
            text=True,
        )

    def test_cached_xml(self, tmp_path):
        md = tmp_path / "changelog.md"
        md.write_text(SAMPLE_CHANGELOG)
        result = self._run("--cached", str(md))
        assert result.returncode == 0
        assert "<changelog-tasks" in result.stdout

    def test_cached_json(self, tmp_path):
        md = tmp_path / "changelog.md"
        md.write_text(SAMPLE_CHANGELOG)
        result = self._run("--cached", str(md), "--format", "json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert len(data) > 0

    def test_cached_rss(self, tmp_path):
        md = tmp_path / "changelog.md"
        md.write_text(SAMPLE_CHANGELOG)
        result = self._run("--cached", str(md), "--rss")
        assert result.returncode == 0
        assert "<rss" in result.stdout

    def test_filter(self, tmp_path):
        md = tmp_path / "changelog.md"
        md.write_text(SAMPLE_CHANGELOG)
        result = self._run("--cached", str(md), "--filter", "feat", "--format", "json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert all(t["category"] == "feat" for t in data)

    def test_decompose(self, tmp_path):
        md = tmp_path / "changelog.md"
        md.write_text(SAMPLE_CHANGELOG)
        result = self._run("--cached", str(md), "--decompose")
        assert result.returncode == 0
        assert "<subtask" in result.stdout

    def test_empty_file(self, tmp_path):
        md = tmp_path / "empty.md"
        md.write_text("nothing here")
        result = self._run("--cached", str(md))
        assert result.returncode == 1


class TestAgentFrontmatter:
    """Verify all agents have updated frontmatter with new keys."""

    REQUIRED_NEW_KEYS = {"model", "color"}

    def test_all_agents_have_model_and_color(self):
        agents_dir = Path(__file__).parent.parent / ".claude" / "agents"
        for agent_file in agents_dir.glob("*.md"):
            content = agent_file.read_text()
            frontmatter_end = content.find("---", 3)
            frontmatter = content[3:frontmatter_end]
            for key in self.REQUIRED_NEW_KEYS:
                assert f"{key}:" in frontmatter, f"{agent_file.name} missing '{key}' in frontmatter"
