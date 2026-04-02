"""Tests for scripts/crawl-llms-txt.py — llms.txt crawler."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("crawl-llms-txt")
extract_urls = mod.extract_urls
content_hash = mod.content_hash
HTMLToText = mod.HTMLToText


class TestExtractUrls:
    def test_extracts_markdown_links(self):
        text = "- [Tools](https://code.claude.com/docs/en/tools-reference.md): Tool docs"
        urls = extract_urls(text, "https://code.claude.com/docs/llms.txt")
        assert "https://code.claude.com/docs/en/tools-reference.md" in urls

    def test_extracts_bare_urls(self):
        text = "https://example.com/page\nhttps://example.com/other"
        urls = extract_urls(text, "https://example.com/llms.txt")
        assert "https://example.com/page" in urls
        assert "https://example.com/other" in urls

    def test_resolves_relative_urls(self):
        text = "- [Tools](/docs/en/tools.md): Tool docs"
        urls = extract_urls(text, "https://code.claude.com/docs/llms.txt")
        assert "https://code.claude.com/docs/en/tools.md" in urls

    def test_empty_text(self):
        urls = extract_urls("", "https://example.com/llms.txt")
        assert urls == []

    def test_deduplicates(self):
        text = "https://example.com/page\nhttps://example.com/page"
        urls = extract_urls(text, "https://example.com/llms.txt")
        # First bare URL match, second skipped by dedup check
        assert urls.count("https://example.com/page") == 1


class TestContentHash:
    def test_deterministic(self):
        h1 = content_hash("hello world")
        h2 = content_hash("hello world")
        assert h1 == h2

    def test_different_content_different_hash(self):
        h1 = content_hash("hello")
        h2 = content_hash("world")
        assert h1 != h2

    def test_hash_length(self):
        h = content_hash("test")
        assert len(h) == 12  # sha256[:12]


class TestHTMLToText:
    def test_strips_tags(self):
        parser = HTMLToText()
        parser.feed("<p>Hello <b>world</b></p>")
        assert "Hello world" in parser.get_text()

    def test_skips_script(self):
        parser = HTMLToText()
        parser.feed("<script>var x = 1;</script><p>Content</p>")
        text = parser.get_text()
        assert "var x" not in text
        assert "Content" in text

    def test_skips_style(self):
        parser = HTMLToText()
        parser.feed("<style>.foo{color:red}</style><p>Content</p>")
        text = parser.get_text()
        assert "color" not in text
        assert "Content" in text

    def test_extracts_href(self):
        parser = HTMLToText()
        parser.feed('<a href="https://example.com">Click</a>')
        text = parser.get_text()
        assert "https://example.com" in text


class TestExtractUrlsAdvanced:
    """Cover additional branches in extract_urls (lines 80-110)."""

    def test_relative_bare_md_url(self):
        text = "/docs/en/getting-started.md"
        urls = extract_urls(text, "https://example.com/llms.txt")
        assert "https://example.com/docs/en/getting-started.md" in urls

    def test_absolute_bare_md_url(self):
        text = "https://example.com/docs/overview.md"
        urls = extract_urls(text, "https://example.com/llms.txt")
        assert "https://example.com/docs/overview.md" in urls

    def test_bare_url_takes_first_token(self):
        text = "https://example.com/page some trailing text"
        urls = extract_urls(text, "https://example.com/llms.txt")
        assert "https://example.com/page" in urls

    def test_relative_markdown_link(self):
        text = "- [Guide](/docs/guide.md): A guide"
        urls = extract_urls(text, "https://code.claude.com/llms.txt")
        assert "https://code.claude.com/docs/guide.md" in urls


class TestFetchUrl:
    """Cover fetch_url (lines 63-77) via monkeypatching."""

    def test_fetch_plain_text(self, monkeypatch):
        import io
        import urllib.request

        fetch_url = mod.fetch_url

        class FakeResp:
            def read(self):
                return b"Hello plain text content"

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        monkeypatch.setattr(urllib.request, "urlopen", lambda req, timeout=30: FakeResp())
        result = fetch_url("https://example.com/page.txt")
        assert result == "Hello plain text content"

    def test_fetch_html_strips_tags(self, monkeypatch):
        import urllib.request

        fetch_url = mod.fetch_url

        html = b"<!doctype html><html><body><p>Content here</p><script>bad</script></body></html>"

        class FakeResp:
            def read(self):
                return html

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        monkeypatch.setattr(urllib.request, "urlopen", lambda req, timeout=30: FakeResp())
        result = fetch_url("https://example.com/page.html")
        assert "Content here" in result
        assert "<p>" not in result


class TestMainFunction:
    """Cover main() (lines 117-210) via monkeypatching."""

    def test_main_success(self, tmp_path, monkeypatch, capsys):
        import urllib.request

        output_file = tmp_path / "output.md"

        # Mock fetch_url to return controlled content
        call_count = {"n": 0}

        def fake_fetch(url, timeout=30):
            call_count["n"] += 1
            if "llms.txt" in url:
                return "# Index\n- [Page](https://example.com/page)\nhttps://example.com/other"
            return f"Page content for {url}"

        monkeypatch.setattr(mod, "fetch_url", fake_fetch)
        monkeypatch.setattr(
            "sys.argv",
            ["crawl-llms-txt.py", "https://example.com/llms.txt", str(output_file)],
        )

        mod.main()

        content = output_file.read_text()
        assert "source: https://example.com/llms.txt" in content
        assert "domain: example.com" in content
        assert "## Pages" in content
        assert "Crawl complete" in content

    def test_main_with_specific_pages(self, tmp_path, monkeypatch, capsys):
        output_file = tmp_path / "output.md"

        def fake_fetch(url, timeout=30):
            return f"Content for {url}"

        monkeypatch.setattr(mod, "fetch_url", fake_fetch)
        monkeypatch.setattr(
            "sys.argv",
            [
                "crawl-llms-txt.py",
                "https://example.com/llms.txt",
                str(output_file),
                "--pages",
                "https://example.com/page1",
                "https://example.com/page2",
            ],
        )

        mod.main()
        content = output_file.read_text()
        assert "page_count: 2" in content

    def test_main_handles_page_errors(self, tmp_path, monkeypatch, capsys):
        output_file = tmp_path / "output.md"

        def fake_fetch(url, timeout=30):
            if "llms.txt" in url:
                return "# Index"
            raise ConnectionError("network down")

        monkeypatch.setattr(mod, "fetch_url", fake_fetch)
        monkeypatch.setattr(
            "sys.argv",
            [
                "crawl-llms-txt.py",
                "https://example.com/llms.txt",
                str(output_file),
                "--pages",
                "https://example.com/fail",
            ],
        )

        mod.main()
        content = output_file.read_text()
        assert "Error:" in content
        assert "0 pages fetched, 1 errors" in content

    def test_main_truncates_long_pages(self, tmp_path, monkeypatch, capsys):
        output_file = tmp_path / "output.md"

        def fake_fetch(url, timeout=30):
            if "llms.txt" in url:
                return "# Index"
            return "x" * 60000  # Exceeds 50KB limit

        monkeypatch.setattr(mod, "fetch_url", fake_fetch)
        monkeypatch.setattr(
            "sys.argv",
            [
                "crawl-llms-txt.py",
                "https://example.com/llms.txt",
                str(output_file),
                "--pages",
                "https://example.com/big",
            ],
        )

        mod.main()
        content = output_file.read_text()
        assert "truncated at 50KB" in content

    def test_main_fetch_error_exits(self, tmp_path, monkeypatch, capsys):
        import pytest
        import urllib.error

        output_file = tmp_path / "output.md"

        def fake_fetch(url, timeout=30):
            raise urllib.error.URLError("connection refused")

        monkeypatch.setattr(mod, "fetch_url", fake_fetch)
        monkeypatch.setattr(
            "sys.argv",
            ["crawl-llms-txt.py", "https://example.com/llms.txt", str(output_file)],
        )

        with pytest.raises(SystemExit) as exc_info:
            mod.main()
        assert exc_info.value.code == 1
