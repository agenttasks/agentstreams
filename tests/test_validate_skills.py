"""Tests for scripts/validate-skills.py — skill validation checks."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Import using importlib since filename has hyphens
from importlib import import_module

mod = import_module("validate-skills")
ValidationResult = mod.ValidationResult
check_forbidden_patterns = mod.check_forbidden_patterns
check_model_names = mod.check_model_names
check_cross_references = mod.check_cross_references
check_skill_md = mod.check_skill_md


class TestValidationResult:
    def test_passes_with_no_errors(self):
        r = ValidationResult("test-skill")
        assert r.passed is True
        assert "PASS" in r.summary()

    def test_fails_with_errors(self):
        r = ValidationResult("test-skill")
        r.errors.append("something broke")
        assert r.passed is False
        assert "FAIL" in r.summary()
        assert "something broke" in r.summary()

    def test_summary_includes_warnings(self):
        r = ValidationResult("test-skill")
        r.warnings.append("minor issue")
        r.files_checked = 3
        summary = r.summary()
        assert "PASS" in summary
        assert "minor issue" in summary
        assert "3 files" in summary


class TestCheckForbiddenPatterns:
    def test_flags_api_key(self):
        content = 'export ANTHROPIC_API_KEY="sk-..."'
        errors = check_forbidden_patterns(content, Path("test.md"))
        assert len(errors) == 1
        assert "ANTHROPIC_API_KEY" in errors[0]

    def test_allows_never_use_context(self):
        content = "Never use ANTHROPIC_API_KEY in production"
        errors = check_forbidden_patterns(content, Path("test.md"))
        assert len(errors) == 0

    def test_allows_dont_use_context(self):
        content = "Don't use ANTHROPIC_API_KEY"
        errors = check_forbidden_patterns(content, Path("test.md"))
        assert len(errors) == 0

    def test_no_errors_clean_content(self):
        content = "Use CLAUDE_CODE_OAUTH_TOKEN for auth"
        errors = check_forbidden_patterns(content, Path("test.md"))
        assert len(errors) == 0


class TestCheckModelNames:
    def test_flags_dot_format(self):
        content = "Use claude.opus.4 for best results"
        warnings = check_model_names(content, Path("test.md"))
        assert len(warnings) == 1

    def test_flags_underscore_format(self):
        content = "Model: claude_sonnet_4"
        warnings = check_model_names(content, Path("test.md"))
        assert len(warnings) == 1

    def test_accepts_hyphen_format(self):
        content = "Use claude-opus-4-6 for best results"
        warnings = check_model_names(content, Path("test.md"))
        assert len(warnings) == 0


class TestCheckSkillMd:
    def test_valid_skill_md(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: test-skill\ndescription: A test\n---\n# Test Skill\n"
            )
            errors = check_skill_md(skill_dir)
            assert len(errors) == 0

    def test_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("# No frontmatter here\n")
            errors = check_skill_md(skill_dir)
            assert any("missing frontmatter" in e for e in errors)

    def test_missing_name(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("---\ndescription: A test\n---\n")
            errors = check_skill_md(skill_dir)
            assert any("name" in e for e in errors)

    def test_missing_description(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "SKILL.md").write_text("---\nname: test-skill\n---\n")
            errors = check_skill_md(skill_dir)
            assert any("description" in e for e in errors)


class TestCheckCrossReferences:
    def test_valid_reference(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            (skill_dir / "other.md").write_text("# Other")
            content = "See `other.md` for details"
            errors = check_cross_references(skill_dir, content, skill_dir / "README.md")
            assert len(errors) == 0

    def test_broken_reference(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            content = "See `nonexistent.md` for details"
            errors = check_cross_references(skill_dir, content, skill_dir / "README.md")
            assert len(errors) == 1
            assert "nonexistent.md" in errors[0]

    def test_skips_http_links(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            content = "See `https://example.com/doc.md` for details"
            errors = check_cross_references(skill_dir, content, skill_dir / "README.md")
            assert len(errors) == 0

    def test_skips_generic_refs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            content = "See the `README.md` for details"
            errors = check_cross_references(skill_dir, content, skill_dir / "test.md")
            assert len(errors) == 0
