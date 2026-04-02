"""Tests for scripts/validate-patterns.py — pattern-driven skill validation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("validate-patterns")
load_patterns = mod.load_patterns
aggregate_patterns = mod.aggregate_patterns
scan_skill_files = mod.scan_skill_files
check_model_ids = mod.check_model_ids
check_sdk_constructors = mod.check_sdk_constructors
check_topic_coverage = mod.check_topic_coverage
check_language_coverage = mod.check_language_coverage


class TestLoadPatterns:
    def test_loads_jsonl(self, tmp_path):
        f = tmp_path / "patterns.jsonl"
        f.write_text('{"url": "a", "topics": ["mcp"]}\n{"url": "b", "topics": ["agents"]}\n')
        patterns = load_patterns(str(f))
        assert len(patterns) == 2
        assert patterns[0]["topics"] == ["mcp"]

    def test_skips_empty_lines(self, tmp_path):
        f = tmp_path / "patterns.jsonl"
        f.write_text('{"url": "a"}\n\n{"url": "b"}\n')
        patterns = load_patterns(str(f))
        assert len(patterns) == 2


class TestAggregatePatterns:
    def test_collects_model_ids(self):
        patterns = [
            {
                "api_surface": ["claude-opus-4-6", "client.messages.create"],
                "sdk_patterns": [],
                "topics": [],
                "code_langs": [],
            },
        ]
        agg = aggregate_patterns(patterns)
        assert "claude-opus-4-6" in agg["model_ids"]
        assert "client.messages.create" in agg["api_methods"]

    def test_collects_topics(self):
        patterns = [
            {"api_surface": [], "sdk_patterns": [], "topics": ["mcp", "agents"], "code_langs": []},
            {"api_surface": [], "sdk_patterns": [], "topics": ["mcp"], "code_langs": []},
        ]
        agg = aggregate_patterns(patterns)
        assert agg["topics"]["mcp"] == 2
        assert agg["topics"]["agents"] == 1

    def test_collects_sdk_patterns(self):
        patterns = [
            {
                "api_surface": [],
                "sdk_patterns": ["anthropic.Anthropic()"],
                "topics": [],
                "code_langs": [],
            },
        ]
        agg = aggregate_patterns(patterns)
        assert "anthropic.Anthropic()" in agg["sdk_patterns"]


class TestCheckModelIds:
    def test_passes_known_models(self):
        doc = {"claude-opus-4-6", "claude-sonnet-4-6"}
        skill = {"claude-opus-4-6"}
        findings = check_model_ids(doc, skill)
        assert len(findings) == 0

    def test_flags_unknown_model(self):
        doc = {"claude-opus-4-6", "claude-sonnet-4-6"}
        skill = {"claude-old-model-1"}
        findings = check_model_ids(doc, skill)
        assert len(findings) == 1
        assert findings[0]["severity"] == "medium"

    def test_handles_date_suffix(self):
        doc = {"claude-sonnet-4-6", "claude-sonnet-4-5-20250929"}
        skill = {"claude-sonnet-4-5-20250929"}
        findings = check_model_ids(doc, skill)
        assert len(findings) == 0

    def test_empty_docs_skips(self):
        findings = check_model_ids(set(), {"claude-opus-4-6"})
        assert len(findings) == 0


class TestCheckSdkConstructors:
    def test_passes_matching_patterns(self):
        doc = {"anthropic.Anthropic()", "new Anthropic()"}
        skill = {"anthropic.Anthropic()"}
        findings = check_sdk_constructors(doc, skill)
        assert len(findings) == 0

    def test_flags_unknown_pattern(self):
        doc = {"anthropic.Anthropic()"}
        skill = {"custom.Client()"}
        findings = check_sdk_constructors(doc, skill)
        assert len(findings) == 1
        assert findings[0]["severity"] == "low"

    def test_empty_docs_skips(self):
        findings = check_sdk_constructors(set(), {"anthropic.Anthropic()"})
        assert len(findings) == 0


class TestCheckTopicCoverage:
    def test_finds_missing_topic(self, tmp_path):
        skill_dir = tmp_path / "skills"
        skill_dir.mkdir()
        (skill_dir / "README.md").write_text("# A skill about agents")
        topics = {"vision": 50, "agents": 30}
        findings = check_topic_coverage(topics, skill_dir)
        assert any("vision" in f["message"] for f in findings)

    def test_passes_covered_topic(self, tmp_path):
        skill_dir = tmp_path / "skills"
        skill_dir.mkdir()
        (skill_dir / "README.md").write_text("# Tool use and function calling guide")
        topics = {"tool-use": 50}
        findings = check_topic_coverage(topics, skill_dir)
        assert len(findings) == 0

    def test_skips_low_count_topics(self, tmp_path):
        skill_dir = tmp_path / "skills"
        skill_dir.mkdir()
        (skill_dir / "README.md").write_text("# Nothing here")
        topics = {"rare-topic": 3}
        findings = check_topic_coverage(topics, skill_dir)
        assert len(findings) == 0


class TestCheckLanguageCoverage:
    def test_finds_missing_language(self):
        doc_langs = {"python": 100, "typescript": 80, "rust": 20}
        skill_langs = {"python", "typescript"}
        findings = check_language_coverage(doc_langs, skill_langs)
        # rust has 20 pages but isn't in the lang_map, so no finding
        assert len(findings) == 0

    def test_flags_missing_known_language(self):
        doc_langs = {"python": 100, "go": 30}
        skill_langs = {"python"}
        findings = check_language_coverage(doc_langs, skill_langs)
        assert any("go" in f["message"] for f in findings)

    def test_skips_low_count_languages(self):
        doc_langs = {"python": 100, "go": 3}
        skill_langs = {"python"}
        findings = check_language_coverage(doc_langs, skill_langs)
        assert len(findings) == 0


class TestScanSkillFiles:
    def test_extracts_model_ids(self, tmp_path):
        skills = tmp_path / "skills"
        skills.mkdir()
        (skills / "test.md").write_text("Use claude-opus-4-6 for generation")
        result = scan_skill_files(skills)
        assert "claude-opus-4-6" in result["model_ids"]

    def test_extracts_sdk_patterns(self, tmp_path):
        skills = tmp_path / "skills"
        skills.mkdir()
        (skills / "test.md").write_text("client = anthropic.Anthropic()\nresponse = client.messages")
        result = scan_skill_files(skills)
        assert "anthropic.Anthropic()" in result["sdk_patterns"]

    def test_extracts_api_refs(self, tmp_path):
        skills = tmp_path / "skills"
        skills.mkdir()
        (skills / "test.md").write_text("Call client.messages.create to send")
        result = scan_skill_files(skills)
        assert "client.messages.create" in result["api_refs"]

    def test_detects_language_dirs(self, tmp_path):
        skills = tmp_path / "skills"
        (skills / "topic" / "python").mkdir(parents=True)
        (skills / "topic" / "python" / "guide.md").write_text("# Python Guide")
        result = scan_skill_files(skills)
        assert "python" in result["languages"]

    def test_skips_unreadable_files(self, tmp_path):
        skills = tmp_path / "skills"
        skills.mkdir()
        # Binary content that causes UnicodeDecodeError is handled
        (skills / "binary.md").write_bytes(b"\x80\x81\x82\x83")
        result = scan_skill_files(skills)
        assert isinstance(result["model_ids"], set)

    def test_empty_dir(self, tmp_path):
        skills = tmp_path / "skills"
        skills.mkdir()
        result = scan_skill_files(skills)
        assert result["model_ids"] == set()
        assert result["sdk_patterns"] == set()
        assert result["api_refs"] == set()
        assert result["languages"] == set()


class TestPrintReport:
    """Test print_report covers lines 268-308."""

    def test_no_findings(self, capsys):
        doc = {"model_ids": {"a"}, "sdk_patterns": {"b"}, "api_methods": {"c"},
               "topics": {"t": 1}, "code_langs": {"python": 5}}
        skill = {"model_ids": {"a"}, "sdk_patterns": {"b"}, "api_refs": {"c"},
                 "languages": {"python"}}
        mod.print_report(doc, skill, [])
        captured = capsys.readouterr()
        assert "No issues found" in captured.err

    def test_with_findings(self, capsys):
        doc = {"model_ids": set(), "sdk_patterns": set(), "api_methods": set(),
               "topics": {}, "code_langs": {}}
        skill = {"model_ids": set(), "sdk_patterns": set(), "api_refs": set(),
                 "languages": set()}
        findings = [
            {"severity": "high", "category": "test", "message": "high issue"},
            {"severity": "medium", "category": "test", "message": "medium issue"},
            {"severity": "low", "category": "test", "message": "low issue"},
            {"severity": "info", "category": "test", "message": "info issue"},
        ]
        mod.print_report(doc, skill, findings)
        captured = capsys.readouterr()
        assert "HIGH (1)" in captured.err
        assert "MEDIUM (1)" in captured.err
        assert "LOW (1)" in captured.err
        assert "INFO (1)" in captured.err
        assert "4 findings (2 actionable)" in captured.err


class TestMain:
    """Test the main() function (lines 314-347)."""

    def test_main_with_patterns_and_skills(self, tmp_path, monkeypatch, capsys):
        # Create a patterns JSONL file
        patterns_file = tmp_path / "patterns.jsonl"
        patterns_file.write_text(
            '{"api_surface": ["claude-opus-4-6"], "sdk_patterns": [], "topics": ["mcp"], "code_langs": ["python"]}\n'
        )
        # Create a skills dir
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        (skills_dir / "test.md").write_text("# MCP skill using claude-opus-4-6\nanthropic.Anthropic()")

        monkeypatch.setattr("sys.argv", [
            "validate-patterns.py",
            str(patterns_file),
            str(skills_dir),
        ])
        # main() doesn't sys.exit unless --check-only, so it returns None
        mod.main()
        captured = capsys.readouterr()
        assert "Pattern-Driven Skill Validation" in captured.err

    def test_main_check_only_exits_on_medium(self, tmp_path, monkeypatch, capsys):
        import pytest

        patterns_file = tmp_path / "patterns.jsonl"
        patterns_file.write_text(
            '{"api_surface": ["claude-opus-4-6"], "sdk_patterns": [], "topics": [], "code_langs": []}\n'
        )
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        # Skill references a model not in docs — triggers medium finding
        (skills_dir / "test.md").write_text("Use claude-haiku-99-obsolete for best results")

        monkeypatch.setattr("sys.argv", [
            "validate-patterns.py",
            str(patterns_file),
            str(skills_dir),
            "--check-only",
        ])
        with pytest.raises(SystemExit) as exc_info:
            mod.main()
        assert exc_info.value.code == 1
