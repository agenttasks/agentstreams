"""Tests for the shared spider base module."""

from __future__ import annotations

from xml.etree import ElementTree

import pytest

from spiders import (
    BaseSpider,
    BloomDedup,
    ChangelogSpider,
    HTMLToText,
    SitemapSpider,
    XMLFeedSpider,
    content_hash,
    html_to_text,
)


class TestHTMLToText:
    def test_strips_tags(self):
        result = html_to_text("<p>Hello <b>world</b></p>")
        assert "Hello" in result
        assert "world" in result
        assert "<b>" not in result

    def test_skips_script_style(self):
        result = html_to_text("<p>text</p><script>bad</script><style>css</style><p>more</p>")
        assert "text" in result
        assert "more" in result
        assert "bad" not in result
        assert "css" not in result

    def test_block_element_newlines(self):
        result = html_to_text("<p>one</p><p>two</p>")
        assert "\n" in result

    def test_no_links_by_default(self):
        result = html_to_text('<a href="http://example.com">link</a>')
        assert "link" in result
        assert "http://example.com" not in result

    def test_extract_links(self):
        result = html_to_text('<a href="http://example.com">link</a>', extract_links=True)
        assert "link" in result
        assert "http://example.com" in result

    def test_class_extract_links_flag(self):
        parser = HTMLToText(extract_links=True)
        parser.feed('<a href="http://test.com">hi</a>')
        assert "http://test.com" in parser.get_text()

    def test_class_no_links_default(self):
        parser = HTMLToText()
        parser.feed('<a href="http://test.com">hi</a>')
        assert "http://test.com" not in parser.get_text()
        assert "hi" in parser.get_text()

    def test_empty_input(self):
        assert html_to_text("") == ""

    def test_skip_nav_footer_header(self):
        result = html_to_text("<nav>nav</nav><footer>foot</footer><header>head</header><p>ok</p>")
        assert "ok" in result
        assert "nav" not in result


class TestContentHash:
    def test_default_length_12(self):
        h = content_hash("test")
        assert len(h) == 12

    def test_custom_length_16(self):
        h = content_hash("test", length=16)
        assert len(h) == 16

    def test_deterministic(self):
        assert content_hash("hello") == content_hash("hello")

    def test_different_inputs(self):
        assert content_hash("a") != content_hash("b")

    def test_hex_chars(self):
        h = content_hash("test")
        assert all(c in "0123456789abcdef" for c in h)


class TestBloomDedup:
    def test_is_new_first_time(self):
        d = BloomDedup()
        assert d.is_new("hello") is True

    def test_is_new_second_time(self):
        d = BloomDedup()
        d.is_new("hello")
        assert d.is_new("hello") is False

    def test_contains(self):
        d = BloomDedup()
        d.add("hello")
        assert "hello" in d

    def test_not_contains(self):
        d = BloomDedup()
        assert "hello" not in d

    def test_clear(self):
        d = BloomDedup()
        d.add("hello")
        d.clear()
        assert "hello" not in d
        assert len(d) == 0

    def test_len(self):
        d = BloomDedup()
        d.add("a")
        d.add("b")
        assert len(d) == 2

    def test_custom_hash_length(self):
        d = BloomDedup(hash_length=8)
        assert d.is_new("test") is True
        assert d.is_new("test") is False


class TestBaseSpider:
    def test_construction(self):
        spider = BaseSpider(name="test")
        assert spider.name == "test"

    def test_content_hash(self):
        spider = BaseSpider()
        h = spider.content_hash("test")
        assert len(h) == 12

    def test_custom_hash_length(self):
        spider = BaseSpider(hash_length=16)
        h = spider.content_hash("test")
        assert len(h) == 16

    def test_start_urls(self):
        spider = BaseSpider(start_urls=["http://a.com", "http://b.com"])
        assert spider.start() == ["http://a.com", "http://b.com"]

    def test_html_to_text(self):
        spider = BaseSpider()
        assert "hello" in spider.html_to_text("<p>hello</p>")

    def test_dedup_initialized(self):
        spider = BaseSpider()
        assert isinstance(spider.dedup, BloomDedup)

    def test_parse_not_implemented(self):
        spider = BaseSpider()
        with pytest.raises(NotImplementedError):
            spider.parse("http://test.com", "content")


class TestSitemapSpider:
    SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>http://example.com/page1</loc></url>
        <url><loc>http://example.com/page2</loc></url>
    </urlset>"""

    INDEX_XML = """<?xml version="1.0" encoding="UTF-8"?>
    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <sitemap><loc>http://example.com/sitemap1.xml</loc></sitemap>
    </sitemapindex>"""

    def test_parse_urlset(self):
        spider = SitemapSpider()
        urls = spider.parse_sitemap_xml(self.SITEMAP_XML)
        assert len(urls) == 2
        assert "http://example.com/page1" in urls

    def test_parse_sitemapindex(self):
        spider = SitemapSpider()
        urls = spider.parse_sitemap_xml(self.INDEX_XML)
        assert len(urls) == 1
        assert "sitemap1.xml" in urls[0]

    def test_invalid_xml(self):
        spider = SitemapSpider()
        assert spider.parse_sitemap_xml("not xml") == []

    def test_empty_sitemap(self):
        spider = SitemapSpider()
        xml = '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"/>'
        assert spider.parse_sitemap_xml(xml) == []

    def test_sitemap_filter_default(self):
        spider = SitemapSpider()
        urls = ["http://a.com", "http://b.com"]
        assert spider.sitemap_filter(urls) == urls

    def test_start_from_sitemap_urls(self):
        spider = SitemapSpider(sitemap_urls=["http://example.com/sitemap.xml"])
        assert spider.start() == ["http://example.com/sitemap.xml"]


class TestXMLFeedSpider:
    def test_adapt_response_passthrough(self):
        spider = XMLFeedSpider()
        assert spider.adapt_response("raw text") == "raw text"

    def test_process_results_passthrough(self):
        spider = XMLFeedSpider()
        results = [{"a": 1}, {"b": 2}]
        assert spider.process_results(results) == results

    def test_parse_node_not_implemented(self):
        spider = XMLFeedSpider()
        with pytest.raises(NotImplementedError):
            spider.parse_node({"text": "test"})

    def test_defaults(self):
        spider = XMLFeedSpider()
        assert spider.iterator == "iternodes"
        assert spider.itertag == "item"


class TestChangelogSpider:
    SAMPLE = """# Changelog

## 2.1.92 - April 4, 2026
* Added new feature X
* Fixed crash in module Y
* Improved performance of Z
* Removed deprecated API
"""

    def test_parse_changelog(self):
        spider = ChangelogSpider()
        entries = spider.parse_changelog(self.SAMPLE)
        assert len(entries) == 1
        assert entries[0]["version"] == "2.1.92"
        assert len(entries[0]["bullets"]) == 4

    def test_classifies_bullets(self):
        spider = ChangelogSpider()
        entries = spider.parse_changelog(self.SAMPLE)
        cats = [b["category"] for b in entries[0]["bullets"]]
        assert cats == ["feat", "fix", "improve", "remove"]

    def test_assigns_priority(self):
        spider = ChangelogSpider()
        entries = spider.parse_changelog(self.SAMPLE)
        priorities = [b["priority"] for b in entries[0]["bullets"]]
        assert "medium" in priorities  # "Fixed" → medium

    def test_deduplicates(self):
        spider = ChangelogSpider()
        entries1 = spider.parse_changelog(self.SAMPLE)
        # Second parse with same spider should dedup
        entries2 = spider.parse_changelog(self.SAMPLE)
        assert entries2 == []  # all bullets already seen

    def test_adapt_response_html(self):
        spider = ChangelogSpider()
        result = spider.adapt_response("<html><body><p>text</p></body></html>")
        assert "<html" not in result
        assert "text" in result

    def test_adapt_response_text(self):
        spider = ChangelogSpider()
        result = spider.adapt_response("# plain markdown")
        assert result == "# plain markdown"

    def test_hash_length_16(self):
        spider = ChangelogSpider()
        h = spider.content_hash("test")
        assert len(h) == 16

    def test_name(self):
        spider = ChangelogSpider()
        assert spider.name == "changelog"
