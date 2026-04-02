"""Tests for scripts/run-pipeline.py — unified quality pipeline runner."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("run-pipeline")
is_fresh = mod.is_fresh
run_command = mod.run_command
run_pipeline = mod.run_pipeline
ALL_STAGES = mod.ALL_STAGES


class TestIsFresh:
    def test_fresh_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("content")
        assert is_fresh(f, max_age_hours=1) is True

    def test_missing_file(self, tmp_path):
        assert is_fresh(tmp_path / "missing.txt") is False

    def test_stale_file(self, tmp_path):
        f = tmp_path / "old.txt"
        f.write_text("content")
        # Set mtime to 48 hours ago
        old_time = time.time() - 48 * 3600
        import os

        os.utime(f, (old_time, old_time))
        assert is_fresh(f, max_age_hours=24) is False


class TestRunCommand:
    def test_successful_command(self):
        ok, output = run_command(["echo", "hello"], "test echo")
        assert ok is True
        assert "hello" in output

    def test_failing_command(self):
        ok, output = run_command(["false"], "test false")
        assert ok is False

    def test_missing_command(self):
        ok, output = run_command(["nonexistent_command_xyz"], "test missing")
        assert ok is False
        assert "not found" in output.lower() or "Command not found" in output


class TestRunPipeline:
    def test_security_stage_passes(self):
        """Security audit on our own codebase should pass."""
        all_ok, results = run_pipeline(["security"])
        assert "security" in results
        assert results["security"][0] is True

    def test_unknown_stage(self):
        all_ok, results = run_pipeline(["nonexistent"])
        assert all_ok is False
        assert results["nonexistent"][0] is False

    def test_crawl_with_skip(self):
        all_ok, results = run_pipeline(["crawl"], skip_crawl=True)
        assert "crawl" in results
        # Should pass — just reports cached status
        assert results["crawl"][0] is True

    def test_all_stages_defined(self):
        assert "crawl" in ALL_STAGES
        assert "extract" in ALL_STAGES
        assert "validate" in ALL_STAGES
        assert "security" in ALL_STAGES

    def test_multiple_stages(self):
        """Run security + crawl(skip) together."""
        all_ok, results = run_pipeline(["crawl", "security"], skip_crawl=True)
        assert "crawl" in results
        assert "security" in results
        # Each result has timing info
        for stage, (ok, messages) in results.items():
            assert any("⏱" in m for m in messages)


class TestStageCrawl:
    """Cover stage_crawl (lines 84-122)."""

    def test_skip_uses_cache(self):
        ok, messages = mod.stage_crawl(skip=True)
        assert ok is True
        assert all("cached" in m or "✓" in m for m in messages)


class TestStageExtract:
    """Cover stage_extract (lines 125-166)."""

    def test_extract_no_taxonomy_skips(self, tmp_path, monkeypatch):
        """When taxonomy files don't exist, extract skips gracefully."""
        monkeypatch.setattr(mod, "PROJECT_ROOT", tmp_path)
        monkeypatch.setattr(mod, "PATTERNS_DIR", tmp_path / "patterns")
        ok, messages = mod.stage_extract()
        assert ok is True
        assert any("skipping" in m or "cached" in m or "✓" in m or "⊘" in m for m in messages)


class TestStageValidate:
    """Cover stage_validate (lines 169-210)."""

    def test_validate_no_skills_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr(mod, "SKILLS_DIR", tmp_path / "nonexistent")
        monkeypatch.setattr(mod, "PATTERNS_DIR", tmp_path / "patterns")
        ok, messages = mod.stage_validate()
        assert ok is True
        assert any("skipping" in m or "⊘" in m for m in messages)

    def test_validate_no_pattern_files(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        patterns_dir = tmp_path / "patterns"
        patterns_dir.mkdir()
        monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
        monkeypatch.setattr(mod, "PATTERNS_DIR", patterns_dir)
        ok, messages = mod.stage_validate()
        assert ok is True
        assert any("skipping" in m or "⊘" in m for m in messages)


class TestStageSecurity:
    """Cover stage_security (lines 213-238)."""

    def test_security_passes(self):
        ok, messages = mod.stage_security()
        assert ok is True
        assert any("Security audit passed" in m or "✓" in m for m in messages)


class TestPrintPipelineReport:
    """Cover print_pipeline_report (lines 282-297)."""

    def test_report_all_pass(self, capsys):
        results = {
            "crawl": (True, ["  ✓ cached", "  ⏱ 0.1s"]),
            "security": (True, ["  ✓ passed", "  ⏱ 0.2s"]),
        }
        mod.print_pipeline_report(results)
        captured = capsys.readouterr()
        assert "PASS" in captured.err
        assert "Pipeline: PASS" in captured.err

    def test_report_with_failure(self, capsys):
        results = {
            "crawl": (False, ["  ✗ failed", "  ⏱ 0.1s"]),
        }
        mod.print_pipeline_report(results)
        captured = capsys.readouterr()
        assert "FAIL" in captured.err
        assert "Pipeline: FAIL" in captured.err


class TestMainFunction:
    """Cover main() (lines 303-324)."""

    def test_main_defaults(self, monkeypatch, capsys):
        """Main runs with default stages (skip crawl for speed)."""
        monkeypatch.setattr("sys.argv", ["run-pipeline.py", "--skip-crawl"])
        # main() may call sys.exit, so catch it
        try:
            mod.main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "Pipeline:" in captured.err

    def test_main_check_only_exits_on_failure(self, monkeypatch, capsys):
        import pytest

        monkeypatch.setattr(
            "sys.argv",
            ["run-pipeline.py", "--stages", "nonexistent_stage_xyz"],
        )
        # This should fail due to argparse choices validation
        with pytest.raises(SystemExit):
            mod.main()
