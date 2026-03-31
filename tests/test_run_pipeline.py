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
