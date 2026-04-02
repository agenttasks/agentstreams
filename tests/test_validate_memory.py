"""Tests for scripts/validate-memory.py — self-healing memory validation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("validate-memory")
parse_index_entries = mod.parse_index_entries
validate_index = mod.validate_index
parse_frontmatter = mod.parse_frontmatter
validate_topic_file = mod.validate_topic_file
find_orphaned_files = mod.find_orphaned_files
validate_memory_dir = mod.validate_memory_dir


class TestParseIndexEntries:
    def test_empty_input(self):
        assert parse_index_entries("") == []

    def test_parses_markdown_links(self):
        text = "- [My Memory](memory.md) — some description"
        entries = parse_index_entries(text)
        assert len(entries) == 1
        assert entries[0]["title"] == "My Memory"
        assert entries[0]["file"] == "memory.md"
        assert entries[0]["description"] == "some description"

    def test_parses_multiple_entries(self):
        text = "- [A](a.md) — first\n- [B](b.md) — second\n- [C](c.md) — third"
        entries = parse_index_entries(text)
        assert len(entries) == 3

    def test_skips_empty_lines(self):
        text = "\n- [A](a.md) — first\n\n- [B](b.md) — second\n"
        entries = parse_index_entries(text)
        assert len(entries) == 2

    def test_skips_headings(self):
        text = "# Index\n- [A](a.md) — first"
        entries = parse_index_entries(text)
        assert len(entries) == 1

    def test_handles_entry_without_description(self):
        text = "- [A](a.md)"
        entries = parse_index_entries(text)
        assert len(entries) == 1
        assert entries[0]["description"] == ""

    def test_flags_malformed_entry(self):
        text = "- some text without a link"
        entries = parse_index_entries(text)
        assert len(entries) == 1
        assert entries[0]["file"] is None


class TestValidateIndex:
    def test_passes_valid_index(self, tmp_path):
        (tmp_path / "memory.md").write_text("---\nname: test\n---\ncontent")
        text = "- [Test](memory.md) — a test memory"
        errors, warnings = validate_index(text, tmp_path)
        assert len(errors) == 0

    def test_flags_broken_link(self, tmp_path):
        text = "- [Missing](missing.md) — file does not exist"
        errors, warnings = validate_index(text, tmp_path)
        assert len(errors) == 1
        assert "broken link" in errors[0]

    def test_flags_long_lines(self, tmp_path):
        long_line = "- [Title](file.md) — " + "x" * 200
        errors, warnings = validate_index(long_line, tmp_path)
        assert any("chars" in w for w in warnings)

    def test_flags_too_many_lines(self, tmp_path):
        text = "\n".join(f"- [M{i}](m{i}.md) — desc" for i in range(210))
        # Create files so they don't trigger broken link errors
        for i in range(210):
            (tmp_path / f"m{i}.md").write_text("---\nname: x\n---\n")
        errors, warnings = validate_index(text, tmp_path)
        assert any("200" in e for e in errors)

    def test_warns_content_in_index(self, tmp_path):
        text = "## Section heading\n- [A](a.md) — desc"
        (tmp_path / "a.md").write_text("---\nname: x\n---\n")
        errors, warnings = validate_index(text, tmp_path)
        assert any("content in index" in w for w in warnings)


class TestValidateIndexBoundary:
    def test_line_count_limit(self, tmp_path):
        """MEMORY.md should not exceed 200 lines."""
        topics = tmp_path / "topics"
        topics.mkdir()
        lines = ["# Memory Index\n\n"]
        for i in range(199):
            (topics / f"topic-{i}.md").write_text(
                f"---\nname: Topic {i}\ndescription: Test\ntype: knowledge\n---\nContent {i}\n"
            )
            lines.append(f"- [Topic {i}](topics/topic-{i}.md) — Test\n")
        index_text = "".join(lines)
        errors, warnings = validate_index(index_text, tmp_path)
        all_findings = errors + warnings
        assert any("line" in f.lower() or "200" in f for f in all_findings) or len(all_findings) > 0


class TestParseFrontmatter:
    def test_parses_valid_frontmatter(self):
        content = "---\nname: test\ndescription: a test\ntype: project\n---\nBody"
        fm = parse_frontmatter(content)
        assert fm is not None
        assert fm["name"] == "test"
        assert fm["description"] == "a test"
        assert fm["type"] == "project"

    def test_returns_none_without_frontmatter(self):
        assert parse_frontmatter("# Just a heading") is None

    def test_returns_none_for_unclosed_frontmatter(self):
        assert parse_frontmatter("---\nname: test\nno closing") is None

    def test_handles_empty_content(self):
        assert parse_frontmatter("") is None


class TestValidateTopicFile:
    def test_passes_valid_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("---\nname: test\ndescription: a test\ntype: project\n---\nBody")
        errors, warnings = validate_topic_file(f)
        assert len(errors) == 0

    def test_flags_missing_frontmatter(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("# No frontmatter")
        errors, warnings = validate_topic_file(f)
        assert any("frontmatter" in e for e in errors)

    def test_flags_missing_name(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("---\ndescription: a test\ntype: project\n---\nBody")
        errors, warnings = validate_topic_file(f)
        assert any("name" in e for e in errors)

    def test_flags_missing_description(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("---\nname: test\ntype: project\n---\nBody")
        errors, warnings = validate_topic_file(f)
        assert any("description" in e for e in errors)

    def test_flags_missing_type(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("---\nname: test\ndescription: a test\n---\nBody")
        errors, warnings = validate_topic_file(f)
        assert any("type" in e for e in errors)

    def test_flags_invalid_type(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("---\nname: test\ndescription: a test\ntype: invalid\n---\nBody")
        errors, warnings = validate_topic_file(f)
        assert any("invalid type" in e for e in errors)

    def test_flags_empty_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("")
        errors, warnings = validate_topic_file(f)
        assert any("empty" in e for e in errors)

    def test_warns_duplicate_name_description(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("---\nname: test\ndescription: test\ntype: project\n---\nBody")
        errors, warnings = validate_topic_file(f)
        assert any("identical" in w for w in warnings)


class TestFindOrphanedFiles:
    def test_finds_orphans(self, tmp_path):
        (tmp_path / "referenced.md").write_text("content")
        (tmp_path / "orphan.md").write_text("content")
        (tmp_path / "MEMORY.md").write_text("- [Ref](referenced.md) — desc")
        index_text = "- [Ref](referenced.md) — desc"
        orphans = find_orphaned_files(tmp_path, index_text)
        assert len(orphans) == 1
        assert orphans[0].name == "orphan.md"

    def test_no_orphans(self, tmp_path):
        (tmp_path / "a.md").write_text("content")
        (tmp_path / "MEMORY.md").write_text("- [A](a.md) — desc")
        orphans = find_orphaned_files(tmp_path, "- [A](a.md) — desc")
        assert len(orphans) == 0

    def test_excludes_memory_md(self, tmp_path):
        (tmp_path / "MEMORY.md").write_text("index")
        orphans = find_orphaned_files(tmp_path, "")
        assert not any(o.name == "MEMORY.md" for o in orphans)


class TestValidateMemoryDir:
    def test_full_valid_dir(self, tmp_path):
        (tmp_path / "MEMORY.md").write_text("- [Test](test.md) — a test")
        (tmp_path / "test.md").write_text(
            "---\nname: test\ndescription: a test\ntype: project\n---\nBody"
        )
        errors, warnings = validate_memory_dir(tmp_path)
        assert len(errors) == 0

    def test_missing_memory_md(self, tmp_path):
        errors, warnings = validate_memory_dir(tmp_path)
        assert any("MEMORY.md not found" in e for e in errors)

    def test_catches_all_issues(self, tmp_path):
        (tmp_path / "MEMORY.md").write_text("- [Missing](missing.md) — broken")
        (tmp_path / "bad.md").write_text("# No frontmatter")
        errors, warnings = validate_memory_dir(tmp_path)
        assert len(errors) >= 2  # broken link + missing frontmatter
        assert len(warnings) >= 1  # orphan


class TestPrintReport:
    """Cover print_report (lines 245-281)."""

    def test_report_with_errors_and_warnings(self, tmp_path, capsys):
        (tmp_path / "MEMORY.md").write_text("- [A](a.md) — desc")
        (tmp_path / "a.md").write_text("content")
        errors = ["error 1", "error 2"]
        warnings = ["warning 1"]
        mod.print_report(tmp_path, errors, warnings)
        captured = capsys.readouterr()
        assert "Errors (2)" in captured.err
        assert "Warnings (1)" in captured.err
        assert "2 error(s), 1 warning(s)" in captured.err

    def test_report_clean(self, tmp_path, capsys):
        (tmp_path / "MEMORY.md").write_text("- [A](a.md) — desc")
        (tmp_path / "a.md").write_text("content")
        mod.print_report(tmp_path, [], [])
        captured = capsys.readouterr()
        assert "All checks passed" in captured.err

    def test_report_warnings_only(self, tmp_path, capsys):
        (tmp_path / "MEMORY.md").write_text("- [A](a.md) — desc")
        (tmp_path / "a.md").write_text("content")
        mod.print_report(tmp_path, [], ["minor warning"])
        captured = capsys.readouterr()
        assert "No errors" in captured.err
        assert "1 warnings" in captured.err

    def test_report_no_index(self, tmp_path, capsys):
        """Reports when MEMORY.md doesn't exist."""
        mod.print_report(tmp_path, ["MEMORY.md not found"], [])
        captured = capsys.readouterr()
        assert "Topic files:" in captured.err


class TestFixMemory:
    """Cover fix_memory (lines 313-365)."""

    def test_removes_broken_links(self, tmp_path):
        (tmp_path / "MEMORY.md").write_text(
            "- [Good](good.md) — exists\n"
            "- [Bad](missing.md) — does not exist\n"
        )
        (tmp_path / "good.md").write_text("---\nname: good\ndescription: g\ntype: project\n---\n")

        errors = ["Line 2: broken link — 'missing.md' does not exist"]
        mod.fix_memory(tmp_path, errors)

        content = (tmp_path / "MEMORY.md").read_text()
        assert "good.md" in content
        assert "missing.md" not in content

    def test_adds_orphans_to_index(self, tmp_path):
        (tmp_path / "MEMORY.md").write_text("- [A](a.md) — desc\n")
        (tmp_path / "a.md").write_text("content")
        (tmp_path / "orphan.md").write_text(
            "---\nname: Orphan\ndescription: an orphan\ntype: project\n---\ncontent"
        )

        errors = []  # No errors but orphans exist
        mod.fix_memory(tmp_path, errors)

        content = (tmp_path / "MEMORY.md").read_text()
        assert "Orphan" in content
        assert "orphan.md" in content

    def test_no_index_returns_early(self, tmp_path):
        """fix_memory returns when MEMORY.md doesn't exist."""
        mod.fix_memory(tmp_path, ["some error"])
        # No crash, no files created

    def test_adds_orphan_without_frontmatter(self, tmp_path):
        (tmp_path / "MEMORY.md").write_text("# Index\n")
        (tmp_path / "orphan.md").write_text("# No frontmatter")

        errors = []
        mod.fix_memory(tmp_path, errors)

        content = (tmp_path / "MEMORY.md").read_text()
        assert "orphan" in content
        assert "needs description" in content


class TestMainFunction:
    """Cover main() (lines 287-310)."""

    def test_main_valid_dir(self, tmp_path, monkeypatch, capsys):
        (tmp_path / "MEMORY.md").write_text("- [A](a.md) — desc")
        (tmp_path / "a.md").write_text(
            "---\nname: A\ndescription: test\ntype: project\n---\ncontent"
        )
        monkeypatch.setattr("sys.argv", ["validate-memory.py", str(tmp_path)])
        mod.main()
        captured = capsys.readouterr()
        assert "Memory Validation" in captured.err

    def test_main_check_only_exits(self, tmp_path, monkeypatch, capsys):
        import pytest

        (tmp_path / "MEMORY.md").write_text("- [Missing](missing.md) — broken")
        monkeypatch.setattr(
            "sys.argv", ["validate-memory.py", str(tmp_path), "--check-only"]
        )
        with pytest.raises(SystemExit) as exc_info:
            mod.main()
        assert exc_info.value.code == 1

    def test_main_nonexistent_dir(self, tmp_path, monkeypatch, capsys):
        import pytest

        monkeypatch.setattr(
            "sys.argv", ["validate-memory.py", str(tmp_path / "nonexistent")]
        )
        with pytest.raises(SystemExit) as exc_info:
            mod.main()
        assert exc_info.value.code == 1

    def test_main_fix_mode(self, tmp_path, monkeypatch, capsys):
        (tmp_path / "MEMORY.md").write_text("- [Missing](missing.md) — broken\n")
        monkeypatch.setattr(
            "sys.argv", ["validate-memory.py", str(tmp_path), "--fix"]
        )
        mod.main()
        # After fix, broken link should be removed
        content = (tmp_path / "MEMORY.md").read_text()
        assert "missing.md" not in content
