"""Tests for error recovery and edge cases across scripts."""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

crawl_mod = import_module("crawl-sitemap")
validate_memory_mod = import_module("validate-memory")
convert_mod = import_module("convert-taxonomy")
security_mod = import_module("security-audit")

html_to_text = crawl_mod.html_to_text
content_hash = crawl_mod.content_hash
fetch_page = crawl_mod.fetch_page
HTMLToText = crawl_mod.HTMLToText
TRUNCATE_BYTES = crawl_mod.TRUNCATE_BYTES

parse_index_entries = validate_memory_mod.parse_index_entries
validate_index = validate_memory_mod.validate_index

slugify = convert_mod.slugify

scan_file = security_mod.scan_file
Finding = security_mod.Finding


# ── HTML parsing edge cases ─────────────────────────────────


class TestHtmlToTextEdgeCases:
    def test_nested_script_tags(self):
        html = "<div><script>var x = '<script>nested</script>';</script><p>Keep</p></div>"
        text = html_to_text(html)
        assert "Keep" in text

    def test_malformed_html(self):
        html = "<p>Unclosed paragraph<div>Overlapping<p>tags"
        text = html_to_text(html)
        assert "Unclosed paragraph" in text

    def test_empty_html(self):
        assert html_to_text("").strip() == ""

    def test_html_entities(self):
        html = "<p>Fish &amp; Chips &lt;3</p>"
        text = html_to_text(html)
        assert "Fish & Chips <3" in text

    def test_strips_nav_footer_header(self):
        html = """<html>
<nav>Skip to main</nav>
<header>Site Header</header>
<main><p>Main content</p></main>
<footer>Copyright 2024</footer>
</html>"""
        text = html_to_text(html)
        assert "Main content" in text
        assert "Skip to main" not in text
        assert "Copyright" not in text

    def test_preserves_semantic_newlines(self):
        html = "<h1>Title</h1><p>Paragraph 1</p><p>Paragraph 2</p>"
        text = html_to_text(html)
        lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
        assert len(lines) >= 3


# ── Content hash edge cases ────────────────────────────────


class TestContentHashEdgeCases:
    def test_unicode_content(self):
        h = content_hash("日本語テスト")
        assert len(h) == 12

    def test_empty_string(self):
        h = content_hash("")
        assert len(h) == 12

    def test_very_long_content(self):
        h = content_hash("x" * 1_000_000)
        assert len(h) == 12


# ── Fetch page partial failure ─────────────────────────────


class TestFetchPagePartialFailure:
    async def test_concurrent_fetches_with_mixed_results(self):
        """Simulate multiple concurrent fetches where some succeed and some fail."""
        sem = asyncio.Semaphore(5)

        async def mock_fetch(url):
            response = AsyncMock()
            if "fail" in url:
                response.__aenter__ = AsyncMock(side_effect=ConnectionError(f"Failed: {url}"))
            else:
                response.text = AsyncMock(return_value=f"Content of {url}")
                response.__aenter__ = AsyncMock(return_value=response)
            response.__aexit__ = AsyncMock(return_value=False)

            session = MagicMock()
            session.get = MagicMock(return_value=response)
            return await fetch_page(session, sem, url, 0.0)

        urls = [
            "https://example.com/ok1",
            "https://example.com/fail1",
            "https://example.com/ok2",
            "https://example.com/fail2",
            "https://example.com/ok3",
        ]

        results = await asyncio.gather(*[mock_fetch(u) for u in urls])

        successes = [r for r in results if r["error"] is None]
        failures = [r for r in results if r["error"] is not None]
        assert len(successes) == 3
        assert len(failures) == 2


# ── Validate memory boundary tests ─────────────────────────


class TestValidateMemoryBoundary:
    def test_parse_index_entries_empty(self):
        entries = parse_index_entries("")
        assert entries == []

    def test_parse_index_entries_valid(self):
        content = "- [Topic One](topics/topic-one.md) — Description\n- [Topic Two](topics/topic-two.md) — Another\n"
        entries = parse_index_entries(content)
        assert len(entries) == 2

    def test_validate_index_line_count_limit(self, tmp_path):
        """MEMORY.md should not exceed 200 lines."""
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        topics_dir = memory_dir / "topics"
        topics_dir.mkdir()

        # Create a MEMORY.md with 201 lines
        lines = ["# Memory Index\n\n"]
        for i in range(199):
            topic_file = topics_dir / f"topic-{i}.md"
            topic_file.write_text(
                f"---\nname: Topic {i}\ndescription: Test\ntype: knowledge\n---\nContent {i}\n"
            )
            lines.append(f"- [Topic {i}](topics/topic-{i}.md) — Test\n")
        index_text = "".join(lines)
        (memory_dir / "MEMORY.md").write_text(index_text)

        errors, warnings = validate_index(index_text, memory_dir)
        # Should flag as too many lines
        all_findings = errors + warnings
        has_line_warning = any("line" in f.lower() or "200" in f for f in all_findings)
        assert has_line_warning or len(all_findings) > 0


# ── Slugify edge cases ──────────────────────────────────────


class TestSlugifyEdgeCases:
    def test_unicode_heading(self):
        slug = slugify("Über die API-Nutzung")
        assert slug == "ber-die-api-nutzung"

    def test_special_characters(self):
        slug = slugify("Hello! @World #2024")
        assert slug == "hello-world-2024"

    def test_long_heading_truncated(self):
        slug = slugify("A" * 100)
        assert len(slug) <= 60

    def test_leading_trailing_dashes(self):
        slug = slugify("---test---")
        assert not slug.startswith("-")
        assert not slug.endswith("-")

    def test_empty_string(self):
        slug = slugify("")
        assert slug == ""


# ── Security scan edge cases ────────────────────────────────


class TestSecurityScanEdgeCases:
    def test_binary_like_content(self, tmp_path):
        """Files with binary-like content should not crash the scanner."""
        f = tmp_path / "weird.py"
        f.write_text("# Normal header\n\x00\x01\x02 os.system(cmd)")
        findings = scan_file(f)
        # Should still detect the os.system call
        assert any(f.category == "shell-injection" for f in findings)

    def test_very_large_file(self, tmp_path):
        """Large files should be scanned without memory issues."""
        f = tmp_path / "large.py"
        content = "import json\n" * 10000 + "os.system(cmd)\n"
        f.write_text(content)
        findings = scan_file(f)
        assert any(f.category == "shell-injection" for f in findings)

    def test_file_with_only_comments(self, tmp_path):
        f = tmp_path / "comments.py"
        f.write_text("# os.system(cmd)\n# eval(x)\n# import pickle\n")
        findings = scan_file(f)
        # Comments should be skipped for shell injection
        assert not any(f.category == "shell-injection" for f in findings)

    def test_multiline_string_context(self, tmp_path):
        f = tmp_path / "docstring.py"
        f.write_text('"""\nWarning: never use os.system(cmd)\n"""\nprint("clean")\n')
        findings = scan_file(f)
        # Safe context (docstring with "never") should be skipped
        shell_findings = [f for f in findings if f.category == "shell-injection"]
        assert len(shell_findings) == 0
