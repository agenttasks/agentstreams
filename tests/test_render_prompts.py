"""Tests for prompt registry and XML task rendering."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from prompt_registry import (
    PromptEntry,
    extract_prompt_body,
    get_by_id,
    get_by_tag,
    get_by_type,
    get_registry,
    render_all_xml,
)


class TestRegistry:
    """Test the prompt registry."""

    def test_registry_has_30_entries(self):
        assert len(get_registry()) == 30

    def test_all_ids_unique(self):
        ids = [e.id for e in get_registry()]
        assert len(ids) == len(set(ids))

    def test_all_names_unique(self):
        names = [e.name for e in get_registry()]
        assert len(names) == len(set(names))

    def test_ids_are_zero_padded(self):
        for entry in get_registry():
            assert len(entry.id) == 2, f"ID '{entry.id}' should be 2 digits"

    def test_valid_types(self):
        valid = {"system", "agent", "tool", "skill"}
        for entry in get_registry():
            assert entry.prompt_type in valid, f"Invalid type: {entry.prompt_type}"

    def test_type_counts(self):
        by_type = {}
        for entry in get_registry():
            by_type.setdefault(entry.prompt_type, 0)
            by_type[entry.prompt_type] += 1
        assert by_type["system"] == 10
        assert by_type["agent"] == 5
        assert by_type["tool"] == 9
        assert by_type["skill"] == 6

    def test_all_have_purpose(self):
        for entry in get_registry():
            assert entry.purpose, f"[{entry.id}] missing purpose"

    def test_all_have_filename(self):
        for entry in get_registry():
            assert entry.filename.endswith(".md"), f"[{entry.id}] bad filename"


class TestLookup:
    """Test registry lookup functions."""

    def test_get_by_id_found(self):
        entry = get_by_id("07")
        assert entry is not None
        assert entry.name == "verification-agent"

    def test_get_by_id_not_found(self):
        assert get_by_id("99") is None

    def test_get_by_type_agent(self):
        agents = get_by_type("agent")
        assert len(agents) == 5
        assert all(e.prompt_type == "agent" for e in agents)

    def test_get_by_tag(self):
        security = get_by_tag("security")
        assert len(security) >= 2
        assert all("security" in e.tags for e in security)


class TestXmlRendering:
    """Test XML task rendering."""

    def test_single_entry_xml(self):
        entry = get_by_id("07")
        xml = entry.to_xml()
        assert '<task id="07"' in xml
        assert 'type="agent"' in xml
        assert 'name="verification-agent"' in xml
        assert "<purpose>" in xml
        assert "<constraints>" in xml
        assert "<constraint>" in xml
        assert '<tools allowed=' in xml
        assert '<tools' in xml and 'denied=' in xml

    def test_single_entry_parses(self):
        entry = get_by_id("07")
        xml = entry.to_xml()
        root = ElementTree.fromstring(xml)
        assert root.tag == "task"
        assert root.attrib["id"] == "07"

    def test_all_xml_parses(self):
        xml = render_all_xml()
        root = ElementTree.fromstring(xml)
        assert root.tag == "prompt-tasks"
        tasks = root.findall("task")
        assert len(tasks) == 30

    def test_xml_escaping(self):
        entry = PromptEntry(
            id="99",
            name="test",
            filename="test.md",
            prompt_type="system",
            purpose='Test <purpose> with "quotes" & ampersands',
        )
        xml = entry.to_xml()
        assert "&lt;" in xml
        assert "&amp;" in xml
        assert "&quot;" in xml

    def test_minimal_entry_xml(self):
        entry = PromptEntry(
            id="99",
            name="minimal",
            filename="test.md",
            prompt_type="tool",
            purpose="Minimal test entry",
        )
        xml = entry.to_xml()
        root = ElementTree.fromstring(xml)
        assert root.find("purpose").text == "Minimal test entry"
        assert root.find("constraints") is None


class TestSourceFiles:
    """Test that source prompt files exist."""

    def test_all_sources_exist(self):
        for entry in get_registry():
            path = entry.source_path()
            assert path.exists(), f"[{entry.id}] missing: {path}"

    def test_all_sources_non_empty(self):
        for entry in get_registry():
            path = entry.source_path()
            assert path.stat().st_size > 0, f"[{entry.id}] empty: {path}"


class TestExtractPromptBody:
    """Test prompt body extraction."""

    def test_extracts_fenced_blocks(self):
        content = "# Title\n\n```\nHello world\n```\n\nMore text\n\n```\nSecond block\n```\n"
        body = extract_prompt_body(content)
        assert "Hello world" in body
        assert "Second block" in body
        assert "---" in body  # separator between blocks

    def test_empty_on_no_fences(self):
        assert extract_prompt_body("No fences here") == ""


class TestCLI:
    """Test the render_prompts.py CLI."""

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "scripts/render_prompts.py", *args],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

    def test_validate(self):
        result = self._run("--validate")
        assert result.returncode == 0
        assert "OK" in result.stdout

    def test_xml_output(self):
        result = self._run("--type", "agent")
        assert result.returncode == 0
        assert "<prompt-tasks>" in result.stdout
        assert "<task" in result.stdout

    def test_json_output(self):
        result = self._run("--format", "json", "--id", "07")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert len(data) == 1
        assert data[0]["id"] == "07"

    def test_table_output(self):
        result = self._run("--format", "table", "--type", "skill")
        assert result.returncode == 0
        assert "| ID |" in result.stdout

    def test_tag_filter(self):
        result = self._run("--tag", "security", "--format", "json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert all("security" in item["tags"] for item in data)

    def test_invalid_id(self):
        result = self._run("--id", "99")
        assert result.returncode == 1
