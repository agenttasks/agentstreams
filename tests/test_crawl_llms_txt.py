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
