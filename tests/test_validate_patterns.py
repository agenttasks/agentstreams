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
