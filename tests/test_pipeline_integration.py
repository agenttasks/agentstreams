"""Tests for run-pipeline.py — stage integration, caching, and reporting."""

import os
import sys
import time
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("run-pipeline")
is_fresh = mod.is_fresh
run_command = mod.run_command
run_pipeline = mod.run_pipeline
print_pipeline_report = mod.print_pipeline_report
ALL_STAGES = mod.ALL_STAGES
STAGE_RUNNERS = mod.STAGE_RUNNERS


class TestStageRunners:
    def test_all_stages_have_runners(self):
        for stage in ALL_STAGES:
            assert stage in STAGE_RUNNERS, f"Missing runner for stage: {stage}"

    def test_crawl_skip_reports_cached(self):
        """Crawl stage with skip=True should pass and report cached."""
        ok, messages = STAGE_RUNNERS["crawl"](skip=True)
        assert ok is True
        assert any("skip" in m.lower() or "cached" in m.lower() for m in messages)


class TestPipelineOrdering:
    def test_stages_execute_in_order(self):
        """Pipeline should execute stages in the order given."""
        execution_order = []

        def mock_runner_factory(name):
            def runner(**kwargs):
                execution_order.append(name)
                return True, [f"{name} done"]

            return runner

        with patch.dict(
            STAGE_RUNNERS,
            {s: mock_runner_factory(s) for s in ALL_STAGES},
        ):
            ok, results = run_pipeline(["crawl", "extract", "validate", "security"])

        assert execution_order == ["crawl", "extract", "validate", "security"]
        assert ok is True

    def test_pipeline_continues_after_stage_failure(self):
        """Pipeline should continue even if a stage fails."""

        def pass_stage(**kwargs):
            return True, ["passed"]

        def fail_stage(**kwargs):
            return False, ["failed"]

        with patch.dict(
            STAGE_RUNNERS,
            {
                "crawl": pass_stage,
                "extract": fail_stage,
                "validate": pass_stage,
                "security": pass_stage,
            },
        ):
            ok, results = run_pipeline(ALL_STAGES)

        assert ok is False  # overall should fail
        assert results["crawl"][0] is True
        assert results["extract"][0] is False
        assert results["validate"][0] is True

    def test_subset_of_stages(self):
        """Pipeline should only run requested stages."""

        def pass_stage(**kwargs):
            return True, ["ok"]

        with patch.dict(STAGE_RUNNERS, {s: pass_stage for s in ALL_STAGES}):
            ok, results = run_pipeline(["validate", "security"])

        assert "validate" in results
        assert "security" in results
        assert "crawl" not in results
        assert "extract" not in results


class TestIsFreshEdgeCases:
    def test_exact_boundary_age(self, tmp_path):
        f = tmp_path / "boundary.txt"
        f.write_text("data")
        # Set mtime to exactly max_age_hours ago
        boundary_time = time.time() - 24 * 3600
        os.utime(f, (boundary_time, boundary_time))
        # At exactly the boundary, should be stale
        assert is_fresh(f, max_age_hours=24) is False

    def test_just_under_boundary(self, tmp_path):
        f = tmp_path / "almost.txt"
        f.write_text("data")
        # 23 hours ago — still fresh
        recent_time = time.time() - 23 * 3600
        os.utime(f, (recent_time, recent_time))
        assert is_fresh(f, max_age_hours=24) is True

    def test_custom_max_age(self, tmp_path):
        f = tmp_path / "custom.txt"
        f.write_text("data")
        old_time = time.time() - 2 * 3600
        os.utime(f, (old_time, old_time))
        assert is_fresh(f, max_age_hours=1) is False
        assert is_fresh(f, max_age_hours=4) is True


class TestRunCommandEdgeCases:
    def test_command_with_output(self):
        ok, output = run_command(["echo", "test output"], "echo test")
        assert ok is True
        assert "test output" in output

    def test_command_stderr_captured(self):
        ok, output = run_command(
            ["python3", "-c", "import sys; sys.stderr.write('err msg')"],
            "stderr test",
        )
        assert ok is True
        assert "err msg" in output

    def test_nonzero_exit_code(self):
        ok, output = run_command(
            ["python3", "-c", "import sys; sys.exit(1)"],
            "exit 1 test",
        )
        assert ok is False


class TestPrintPipelineReport:
    def test_prints_pass_status(self, capsys):
        results = {
            "security": (True, ["No issues found"]),
        }
        print_pipeline_report(results)
        captured = capsys.readouterr()
        assert "PASS" in captured.out or "PASS" in captured.err

    def test_prints_fail_status(self, capsys):
        results = {
            "security": (False, ["3 critical findings"]),
        }
        print_pipeline_report(results)
        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "FAIL" in combined

    def test_prints_all_stages(self, capsys):
        results = {
            "crawl": (True, ["10 pages"]),
            "extract": (True, ["patterns ok"]),
            "validate": (False, ["2 issues"]),
            "security": (True, ["clean"]),
        }
        print_pipeline_report(results)
        captured = capsys.readouterr()
        combined = captured.out + captured.err
        for stage in ["crawl", "extract", "validate", "security"]:
            assert stage in combined.lower()
