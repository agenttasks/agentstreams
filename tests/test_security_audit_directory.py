"""Tests for security-audit.py — scan_directory traversal and filtering."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("security-audit")
scan_directory = mod.scan_directory
scan_file = mod.scan_file
Finding = mod.Finding
print_report = mod.print_report


class TestScanDirectory:
    def test_scans_specific_paths(self, tmp_path):
        py_file = tmp_path / "scripts" / "bad.py"
        py_file.parent.mkdir(parents=True)
        py_file.write_text("os.system(cmd)")
        findings = scan_directory(tmp_path, ["scripts"])
        assert any(f.severity == Finding.CRITICAL for f in findings)

    def test_scans_single_file_path(self, tmp_path):
        (tmp_path / "check.py").write_text("import pickle\n")
        findings = scan_directory(tmp_path, ["check.py"])
        assert len(findings) == 1
        assert findings[0].category == "dependency-risk"

    @pytest.mark.parametrize(
        "skip_dir,file_content",
        [
            (".git/hooks", "os.system('echo hook')"),
            ("node_modules/pkg", "eval(user_input)"),
            ("__pycache__", "exec(code)"),
            ("src/node_modules/pkg", "eval(user_input)"),
        ],
    )
    def test_skips_excluded_directories(self, tmp_path, skip_dir, file_content):
        target = tmp_path / skip_dir
        target.mkdir(parents=True, exist_ok=True)
        (target / "file.py").write_text(file_content)
        assert scan_directory(tmp_path) == []

    @pytest.mark.parametrize("ext", [".exe", ".png", ".csv"])
    def test_skips_non_scan_extensions(self, tmp_path, ext):
        (tmp_path / f"file{ext}").write_text("os.system(cmd)")
        assert scan_directory(tmp_path) == []

    def test_full_project_scan_clean(self, tmp_path):
        sub = tmp_path / "src"
        sub.mkdir()
        (sub / "clean.py").write_text("import json\ndata = json.loads(text)")
        assert scan_directory(tmp_path) == []

    def test_crawled_content_dirs_skip_code_checks(self, tmp_path):
        taxonomy = tmp_path / "taxonomy"
        taxonomy.mkdir()
        (taxonomy / "crawled.py").write_text("os.system(cmd)\nimport pickle")
        findings = scan_directory(tmp_path)
        assert not any(f.category == "shell-injection" for f in findings)
        assert not any(f.category == "dependency-risk" for f in findings)

    def test_crawled_content_dirs_still_check_secrets(self, tmp_path):
        taxonomy = tmp_path / "taxonomy"
        taxonomy.mkdir()
        (taxonomy / "leak.py").write_text("key = 'sk-ant-abcdefghijklmnopqrst'")
        assert any(f.category == "secret-leakage" for f in scan_directory(tmp_path))

    def test_recursive_subdirectory_scan(self, tmp_path):
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        (deep / "deep.py").write_text("os.system(cmd)")
        assert len(scan_directory(tmp_path)) >= 1


class TestScanFile:
    def test_handles_unreadable_file(self, tmp_path):
        assert scan_file(tmp_path / "missing.py") == []

    def test_combines_multiple_check_findings(self, tmp_path):
        f = tmp_path / "multi.py"
        f.write_text("os.system(cmd)\nimport pickle\n")
        categories = {finding.category for finding in scan_file(f)}
        assert "shell-injection" in categories
        assert "dependency-risk" in categories


class TestPrintReport:
    def test_no_findings(self, capsys):
        print_report([])
        assert "PASS" in capsys.readouterr().err

    def test_groups_by_severity(self, capsys):
        findings = [
            Finding(Finding.CRITICAL, "test", Path("a.py"), 1, "critical issue"),
            Finding(Finding.LOW, "test", Path("b.py"), 2, "minor issue"),
        ]
        print_report(findings)
        err = capsys.readouterr().err
        assert "1 critical" in err
        assert "1 low" in err

    def test_summary_counts(self, capsys):
        findings = [
            Finding(Finding.HIGH, "a", Path("x.py"), 1, "msg"),
            Finding(Finding.HIGH, "b", Path("y.py"), 2, "msg"),
            Finding(Finding.MEDIUM, "c", Path("z.py"), 3, "msg"),
        ]
        print_report(findings)
        err = capsys.readouterr().err
        assert "2 high" in err
        assert "1 medium" in err
