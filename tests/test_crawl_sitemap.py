"""Tests for scripts/crawl-sitemap.py — async sitemap crawler."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("crawl-sitemap")
parse_sitemap_xml = mod.parse_sitemap_xml
HTMLToText = mod.HTMLToText
content_hash = mod.content_hash
html_to_text = mod.html_to_text
slug_from_url = mod.slug_from_url
write_taxonomy = mod.write_taxonomy


class TestParseSitemapXml:
    def test_extracts_urls_from_urlset(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/page1</loc></url>
  <url><loc>https://example.com/page2</loc></url>
  <url><loc>https://example.com/page3</loc></url>
</urlset>"""
        urls = parse_sitemap_xml(xml)
        assert len(urls) == 3
        assert "https://example.com/page1" in urls
        assert "https://example.com/page3" in urls

    def test_extracts_urls_from_sitemapindex(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://example.com/sitemap-pages.xml</loc></sitemap>
  <sitemap><loc>https://example.com/sitemap-blog.xml</loc></sitemap>
</sitemapindex>"""
        urls = parse_sitemap_xml(xml)
        assert len(urls) == 2
        assert "https://example.com/sitemap-pages.xml" in urls

    def test_handles_empty_sitemap(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</urlset>"""
        urls = parse_sitemap_xml(xml)
        assert urls == []

    def test_handles_invalid_xml(self):
        urls = parse_sitemap_xml("not valid xml <><>")
        assert urls == []

    def test_strips_whitespace_from_urls(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>  https://example.com/page  </loc></url>
</urlset>"""
        urls = parse_sitemap_xml(xml)
        assert urls[0] == "https://example.com/page"


class TestSlugFromUrl:
    def test_extracts_last_segment(self):
        assert slug_from_url("https://example.com/docs/en/tools-reference") == "tools-reference"

    def test_strips_trailing_slash(self):
        assert slug_from_url("https://example.com/docs/en/page/") == "page"

    def test_returns_index_for_root(self):
        assert slug_from_url("https://example.com/") == "index"

    def test_handles_deep_paths(self):
        assert slug_from_url("https://example.com/a/b/c/d/deep-page") == "deep-page"


class TestHtmlToText:
    def test_strips_html(self):
        assert "Hello" in html_to_text("<p>Hello</p>")

    def test_skips_script_and_style(self):
        html = "<script>var x=1;</script><style>.foo{}</style><p>Content</p>"
        text = html_to_text(html)
        assert "var x" not in text
        assert "Content" in text


class TestContentHash:
    def test_deterministic(self):
        assert content_hash("test") == content_hash("test")

    def test_different_inputs(self):
        assert content_hash("a") != content_hash("b")

    def test_length(self):
        assert len(content_hash("test")) == 12


class TestPriorityPattern:
    def test_english_pages_match(self):
        pattern = re.compile("/en/")
        assert pattern.search("https://platform.claude.com/docs/en/tool-use")
        assert pattern.search("https://code.claude.com/docs/en/sub-agents")

    def test_other_languages_dont_match(self):
        pattern = re.compile("/en/")
        assert not pattern.search("https://platform.claude.com/docs/ja/tool-use")
        assert not pattern.search("https://platform.claude.com/docs/de/overview")


class TestWriteTaxonomy:
    def test_writes_markdown_with_frontmatter(self, tmp_path):
        results = [
            {
                "url": "https://example.com/page1",
                "content": "Hello world",
                "hash": "abc123",
                "error": None,
            },
            {"url": "https://example.com/page2", "content": None, "hash": None, "error": "404"},
        ]
        output = str(tmp_path / "test.md")
        write_taxonomy(results, output, "https://example.com/sitemap.xml", "example.com")

        content = Path(output).read_text()
        assert "---" in content
        assert "domain: example.com" in content
        assert "page_count: 1" in content
        assert "error_count: 1" in content
        assert "### page1" in content
        assert "Hello world" in content
        assert "404" in content

    def test_handles_empty_results(self, tmp_path):
        output = str(tmp_path / "empty.md")
        write_taxonomy([], output, "https://example.com/sitemap.xml", "example.com")
        content = Path(output).read_text()
        assert "page_count: 0" in content
