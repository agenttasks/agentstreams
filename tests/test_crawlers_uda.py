"""Tests for src/crawlers.py — UDA Scrapy-pattern crawlers."""

from __future__ import annotations

from src.crawlers import (
    ChangelogCrawler,
    CrawlConfig,
    CrawlResult,
    RSSCrawler,
    UDACrawler,
)


class TestCrawlConfig:
    def test_defaults(self):
        config = CrawlConfig(name="test", domains=["example.com"])
        assert config.concurrency == 20
        assert config.rate_delay == 0.05
        assert config.max_pages == 10_000
        assert config.bloom_expected_items == 100_000
        assert config.bloom_fp_rate == 0.01

    def test_custom_values(self):
        config = CrawlConfig(
            name="custom",
            domains=["a.com", "b.com"],
            concurrency=5,
            max_pages=100,
        )
        assert config.concurrency == 5
        assert config.max_pages == 100
        assert len(config.domains) == 2


class TestCrawlResult:
    def test_success_result(self):
        r = CrawlResult(
            url="https://example.com",
            domain="example.com",
            content="hello",
            status_code=200,
        )
        assert r.is_success is True

    def test_error_result(self):
        r = CrawlResult(
            url="https://example.com",
            domain="example.com",
            error="timeout",
            status_code=0,
        )
        assert r.is_success is False

    def test_non_200_result(self):
        r = CrawlResult(
            url="https://example.com",
            domain="example.com",
            status_code=404,
        )
        assert r.is_success is False


class TestUDACrawler:
    def test_should_crawl_allowed_domain(self):
        config = CrawlConfig(name="t", domains=["example.com"])
        crawler = UDACrawler(config)
        assert crawler._should_crawl("https://example.com/page") is True
        assert crawler._should_crawl("https://other.com/page") is False

    def test_should_crawl_with_url_patterns(self):
        config = CrawlConfig(
            name="t",
            domains=["example.com"],
            url_patterns=[r"/docs/", r"/api/"],
        )
        crawler = UDACrawler(config)
        assert crawler._should_crawl("https://example.com/docs/intro") is True
        assert crawler._should_crawl("https://example.com/api/v2") is True
        assert crawler._should_crawl("https://example.com/about") is False

    def test_bloom_filter_initialized(self):
        config = CrawlConfig(
            name="t",
            domains=["example.com"],
            bloom_expected_items=500,
            bloom_fp_rate=0.05,
        )
        crawler = UDACrawler(config)
        assert crawler.bloom.expected_items == 500
        assert crawler.bloom.fp_rate == 0.05


class TestChangelogCrawler:
    def test_parse_changelog(self):
        config = CrawlConfig(name="cl", domains=["example.com"])
        crawler = ChangelogCrawler(config)

        changelog = """
# 1.2.0 - 2024-01-15

- Added new bloom filter persistence
- Fixed memory leak in crawler
- Improved sitemap parsing performance

# 1.1.0 - 2024-01-01

- Added initial crawler
- Changed config format
"""
        entries = crawler._parse_changelog(changelog)
        assert len(entries) == 2
        assert entries[0]["version"] == "1.2.0"
        assert len(entries[0]["bullets"]) == 3

    def test_classify(self):
        assert ChangelogCrawler._classify("Added new feature") == "feat"
        assert ChangelogCrawler._classify("Fixed bug in parser") == "fix"
        assert ChangelogCrawler._classify("Improved performance") == "improve"
        assert ChangelogCrawler._classify("Removed old code") == "remove"
        assert ChangelogCrawler._classify("Updated docs") == "other"


class TestRSSCrawler:
    def test_inherits_from_uda_crawler(self):
        config = CrawlConfig(name="rss", domains=["example.com"])
        crawler = RSSCrawler(config)
        assert isinstance(crawler, UDACrawler)
        assert hasattr(crawler, "_parse_feed")
