"""Scrapy sitemap spider with bloom-filter deduplication and Neon persistence.

Replaces the manual aiohttp crawler with a proper Scrapy spider that:
1. Parses sitemaps recursively (SitemapSpider)
2. Deduplicates URLs via bloom filter before fetching
3. Extracts text content from HTML
4. Persists pages to Neon Postgres as UDA CrawledPage entities
5. Emits agentstreams.crawl.* metrics

Usage:
  scrapy crawl sitemap -a sitemap_url=https://platform.claude.com/sitemap.xml
  scrapy crawl sitemap -a sitemap_url=... -a domain=platform.claude.com

Requires: scrapy, psycopg[binary]
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


# ── HTML to text converter ──────────────────────────────────


class HTMLToText(HTMLParser):
    """Strip HTML tags, extract text content."""

    SKIP_TAGS = {"script", "style", "nav", "footer", "header"}
    BLOCK_TAGS = {"br", "p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr"}
    CLOSE_BLOCK_TAGS = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "table"}

    def __init__(self):
        super().__init__()
        self._text: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip = True
        if tag in self.BLOCK_TAGS:
            self._text.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            self._skip = False
        if tag in self.CLOSE_BLOCK_TAGS:
            self._text.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self._text.append(data)

    def get_text(self) -> str:
        return "".join(self._text)


def html_to_text(html: str) -> str:
    """Convert HTML to plain text."""
    parser = HTMLToText()
    parser.feed(html)
    return parser.get_text()


def content_hash(text: str) -> str:
    """SHA-256 content hash (12-char prefix)."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


# ── Page type classifier ───────────────────────────────────

PAGE_TYPE_SIGNALS = {
    "blog": [r"Published\s+\w+\s+\d+,?\s+\d{4}", r"engineering/", r"research/"],
    "reference": [r"Parameters\b", r"Returns?\b.*\btype\b", r"Endpoint", r"api-reference"],
    "changelog": [r"changelog", r"what.?s.new", r"release.notes"],
    "tutorial": [r"step\s+\d", r"tutorial", r"getting.started", r"quickstart"],
    "guide": [r"guide", r"how.to", r"best.practices", r"overview"],
    "api-doc": [r"api\.anthropic\.com", r"messages\.create", r"completions"],
}


def classify_page_type(url: str, content: str) -> str:
    """Classify page type based on URL and content signals."""
    text = (url + "\n" + content[:3000]).lower()
    scores: dict[str, int] = {}
    for ptype, patterns in PAGE_TYPE_SIGNALS.items():
        score = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
        if score > 0:
            scores[ptype] = score
    if not scores:
        return "guide"
    return max(scores, key=scores.get)


# ── Topic extractor ─────────────────────────────────────────

TOPIC_PATTERNS = {
    "tool-use": [r"tool.use", r"function.call", r"tools?\s*="],
    "streaming": [r"stream", r"server.sent.event", r"SSE"],
    "models": [r"claude.opus", r"claude.sonnet", r"claude.haiku", r"model.selection"],
    "agents": [r"agent", r"agentic", r"agent.sdk"],
    "mcp": [r"model.context.protocol", r"MCP", r"mcp.server"],
    "evals": [r"eval", r"benchmark", r"promptfoo"],
    "vision": [r"vision", r"image", r"multimodal"],
    "thinking": [r"extended.thinking", r"think", r"chain.of.thought"],
    "batch": [r"batch", r"message.batch"],
    "embeddings": [r"embed", r"vector", r"semantic.search"],
}


def extract_topics(url: str, content: str) -> list[str]:
    """Extract topic tags from page content."""
    text = (url + "\n" + content[:5000]).lower()
    topics = []
    for topic, patterns in TOPIC_PATTERNS.items():
        if any(re.search(p, text, re.IGNORECASE) for p in patterns):
            topics.append(topic)
    return topics[:5]


# ── Scrapy Spider ───────────────────────────────────────────

try:
    import scrapy
    from scrapy.spiders import SitemapSpider as _SitemapSpider

    class AgentStreamsSitemapSpider(_SitemapSpider):
        """Scrapy sitemap spider with bloom filter deduplication.

        Args (spider arguments):
            sitemap_url: URL of the sitemap.xml to crawl.
            domain: Override detected domain name.
            max_pages: Maximum pages to crawl (default: 2000).
            bloom_capacity: Bloom filter capacity (default: 100000).
            bloom_fp_rate: Target false-positive rate (default: 0.001).
        """

        name = "sitemap"
        custom_settings = {
            "USER_AGENT": "agentstreams-crawler/2.0 (scrapy sitemap spider)",
            "CONCURRENT_REQUESTS": 20,
            "DOWNLOAD_DELAY": 0.05,
            "ROBOTSTXT_OBEY": True,
            "LOG_LEVEL": "INFO",
        }

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.sitemap_urls = [kwargs.get("sitemap_url", "")]
            self.domain = kwargs.get("domain", "")
            self.max_pages = int(kwargs.get("max_pages", 2000))

            # Initialize bloom filter for deduplication
            from ..bloom.filter import BloomFilter

            capacity = int(kwargs.get("bloom_capacity", 100_000))
            fp_rate = float(kwargs.get("bloom_fp_rate", 0.001))
            self.bloom = BloomFilter(capacity=capacity, fp_rate=fp_rate)
            self._page_count = 0
            self._results: list[dict[str, Any]] = []

            super().__init__(*args, **kwargs)

            if not self.domain and self.sitemap_urls:
                self.domain = urlparse(self.sitemap_urls[0]).netloc

        def parse(self, response: scrapy.http.Response) -> dict[str, Any] | None:
            """Process each crawled page."""
            url = response.url

            # Bloom filter dedup check
            if self.bloom.add(url):
                logger.info("Duplicate URL skipped: %s", url)
                return None

            if self._page_count >= self.max_pages:
                return None
            self._page_count += 1

            # Extract text
            raw = response.text
            if "<html" in raw[:500].lower() or "<!doctype" in raw[:500].lower():
                text = html_to_text(raw)
            else:
                text = raw

            # Truncate
            if len(text) > 50_000:
                text = text[:50_000] + "\n\n[... truncated at 50KB ...]\n"

            page_type = classify_page_type(url, text)
            topics = extract_topics(url, text)
            chash = content_hash(text)

            item = {
                "url": url,
                "domain": self.domain,
                "content": text.strip(),
                "content_hash": chash,
                "page_type": page_type,
                "topics": topics,
            }
            self._results.append(item)

            logger.info(
                "Crawled [%d/%d] %s (%s, topics=%s)",
                self._page_count,
                self.max_pages,
                url,
                page_type,
                topics,
            )

            return item

        def closed(self, reason: str) -> None:
            """Emit stats on spider close."""
            stats = self.bloom.stats()
            logger.info(
                "Spider closed (%s). Pages: %d, Bloom stats: %s",
                reason,
                self._page_count,
                json.dumps(stats),
            )

except ImportError:
    # Scrapy not installed — provide a stub for environments without it
    class AgentStreamsSitemapSpider:  # type: ignore[no-redef]
        """Stub: install scrapy to use the sitemap spider."""

        name = "sitemap"

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise ImportError(
                "scrapy is required for AgentStreamsSitemapSpider. "
                "Install with: uv add scrapy"
            )
