"""Tests for security-audit.py — scan_directory traversal and filtering."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("security-audit")
scan_directory = mod.scan_directory
scan_file = mod.scan_file
Finding = mod.Finding
SKIP_DIRS = mod.SKIP_DIRS
SCAN_EXTENSIONS = mod.SCAN_EXTENSIONS
CRAWLED_CONTENT_DIRS = mod.CRAWLED_CONTENT_DIRS
print_report = mod.print_report


class TestScanDirectory:
    def test_scans_specific_paths(self, tmp_path):
        # Create a file with a known finding
        py_file = tmp_path / "scripts" / "bad.py"
        py_file.parent.mkdir(parents=True)
        py_file.write_text("os.system(cmd)")

        findings = scan_directory(tmp_path, ["scripts"])
        assert len(findings) >= 1
        assert any(f.severity == Finding.CRITICAL for f in findings)

    def test_scans_single_file_path(self, tmp_path):
        py_file = tmp_path / "check.py"
        py_file.write_text("import pickle\n")

        findings = scan_directory(tmp_path, ["check.py"])
        assert len(findings) == 1
        assert findings[0].category == "dependency-risk"

    def test_skips_git_directory(self, tmp_path):
        git_dir = tmp_path / ".git" / "hooks"
        git_dir.mkdir(parents=True)
        (git_dir / "pre-commit.py").write_text("os.system('echo hook')")

        findings = scan_directory(tmp_path)
        assert len(findings) == 0

    def test_skips_node_modules(self, tmp_path):
        nm_dir = tmp_path / "node_modules" / "pkg"
        nm_dir.mkdir(parents=True)
        (nm_dir / "index.py").write_text("eval(user_input)")

        findings = scan_directory(tmp_path)
        assert len(findings) == 0

    def test_skips_pycache(self, tmp_path):
        cache_dir = tmp_path / "__pycache__"
        cache_dir.mkdir()
        (cache_dir / "module.py").write_text("exec(code)")

        findings = scan_directory(tmp_path)
        assert len(findings) == 0

    def test_skips_non_scan_extensions(self, tmp_path):
        (tmp_path / "binary.exe").write_text("os.system(cmd)")
        (tmp_path / "image.png").write_text("eval(x)")
        (tmp_path / "data.csv").write_text("exec(y)")

        findings = scan_directory(tmp_path)
        assert len(findings) == 0

    def test_scans_all_valid_extensions(self, tmp_path):
        for ext in [".py", ".md", ".yml", ".yaml", ".sh", ".toml", ".txt", ".json"]:
            (tmp_path / f"file{ext}").write_text("normal content here")

        # Should not crash — all extensions scanned without error
        findings = scan_directory(tmp_path)
        assert isinstance(findings, list)

    def test_full_project_scan_no_paths(self, tmp_path):
        sub = tmp_path / "src"
        sub.mkdir()
        (sub / "clean.py").write_text("import json\ndata = json.loads(text)")
        (sub / "notes.md").write_text("# Documentation\nNormal content.")

        findings = scan_directory(tmp_path)
        assert len(findings) == 0

    def test_crawled_content_dirs_skip_code_checks(self, tmp_path):
        taxonomy = tmp_path / "taxonomy"
        taxonomy.mkdir()
        # This has shell injection patterns but is in taxonomy/ — code checks skipped
        (taxonomy / "crawled.py").write_text("os.system(cmd)\nimport pickle")

        findings = scan_directory(tmp_path)
        # Code-level checks (shell injection, dependency risks) should be skipped
        # Only non-code checks should run (secret leakage, agent boundaries, crawled content)
        assert not any(f.category == "shell-injection" for f in findings)
        assert not any(f.category == "dependency-risk" for f in findings)

    def test_crawled_content_dirs_still_check_secrets(self, tmp_path):
        taxonomy = tmp_path / "taxonomy"
        taxonomy.mkdir()
        (taxonomy / "leak.py").write_text("key = 'sk-ant-abcdefghijklmnopqrst'")

        findings = scan_directory(tmp_path)
        assert any(f.category == "secret-leakage" for f in findings)

    def test_recursive_subdirectory_scan(self, tmp_path):
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        (deep / "deep.py").write_text("os.system(cmd)")

        findings = scan_directory(tmp_path)
        assert len(findings) >= 1

    def test_skip_dirs_in_subdirectory_paths(self, tmp_path):
        # SKIP_DIRS should work at any depth
        nested = tmp_path / "src" / "node_modules" / "pkg"
        nested.mkdir(parents=True)
        (nested / "index.py").write_text("eval(user_input)")

        findings = scan_directory(tmp_path)
        assert len(findings) == 0


class TestScanFile:
    def test_handles_unreadable_file(self, tmp_path):
        f = tmp_path / "missing.py"
        # scan_file reads the file — if it doesn't exist, should return empty
        findings = scan_file(f)
        assert findings == []

    def test_combines_multiple_check_findings(self, tmp_path):
        f = tmp_path / "multi.py"
        f.write_text("os.system(cmd)\nimport pickle\n")

        findings = scan_file(f)
        categories = {f.category for f in findings}
        assert "shell-injection" in categories
        assert "dependency-risk" in categories


class TestPrintReport:
    def test_no_findings(self, capsys):
        print_report([])
        captured = capsys.readouterr()
        assert "PASS" in captured.err

    def test_groups_by_severity(self, capsys):
        findings = [
            Finding(Finding.CRITICAL, "test", Path("a.py"), 1, "critical issue"),
            Finding(Finding.LOW, "test", Path("b.py"), 2, "minor issue"),
        ]
        print_report(findings)
        captured = capsys.readouterr()
        assert "CRITICAL" in captured.err
        assert "LOW" in captured.err
        assert "1 critical" in captured.err
        assert "1 low" in captured.err

    def test_summary_counts(self, capsys):
        findings = [
            Finding(Finding.HIGH, "a", Path("x.py"), 1, "msg"),
            Finding(Finding.HIGH, "b", Path("y.py"), 2, "msg"),
            Finding(Finding.MEDIUM, "c", Path("z.py"), 3, "msg"),
        ]
        print_report(findings)
        captured = capsys.readouterr()
        assert "2 high" in captured.err
        assert "1 medium" in captured.err
