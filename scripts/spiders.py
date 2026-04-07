"""Scrapy-inspired spider class hierarchy for agentstreams crawlers.

Provides shared utilities (HTMLToText, content_hash, BloomDedup) and a
base class hierarchy (BaseSpider → SitemapSpider, XMLFeedSpider) that
consolidates patterns from crawl-sitemap.py, crawl_changelog.py, and
crawl-llms-txt.py.

These are lightweight, async-compatible Python classes — not actual Scrapy
spiders — but they follow the same structural patterns: start_urls,
parse(), parse_node(), adapt_response(), sitemap_filter(), etc.
"""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# ── HTML Parser ──────────────────────────────────────────────


class HTMLToText(HTMLParser):
    """Strip HTML tags, extract text content.

    Unified implementation consolidating three prior versions:
    - crawl-sitemap.py: block-element newlines on start + end tags
    - crawl-llms-txt.py: + href extraction via extract_links flag
    - crawl_changelog.py: start-tag newlines only (subset)

    Args:
        extract_links: If True, emit ``[href]`` for ``<a>`` tags.
    """

    def __init__(self, *, extract_links: bool = False):
        super().__init__()
        self._text: list[str] = []
        self._skip = False
        self._skip_tags = {"script", "style", "nav", "footer", "header"}
        self._extract_links = extract_links

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True
        if tag in ("br", "p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr"):
            self._text.append("\n")
        if self._extract_links and tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self._text.append(f" [{value}] ")

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False
        if tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "table"):
            self._text.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self._text.append(data)

    def get_text(self) -> str:
        return "".join(self._text)


def html_to_text(html: str, *, extract_links: bool = False) -> str:
    """Convert HTML to plain text, optionally extracting link hrefs."""
    parser = HTMLToText(extract_links=extract_links)
    parser.feed(html)
    return parser.get_text()


# ── Content Hashing ──────────────────────────────────────────


def content_hash(text: str, *, length: int = 12) -> str:
    """SHA-256 content hash with configurable truncation.

    Default length=12 matches crawl-sitemap.py and crawl-llms-txt.py.
    Use length=16 for crawl_changelog.py.
    """
    return hashlib.sha256(text.encode()).hexdigest()[:length]


# ── Bloom Filter Dedup ───────────────────────────────────────


class BloomDedup:
    """Set-backed content deduplication with bloom-filter-style API.

    Uses a set of content hashes. No false negatives, no false positives
    (unlike a true bloom filter), but sufficient for the project's scale.
    For a real bloom filter, swap in pybloom-live per
    skills/crawl-ingest/shared/bloom-filters.md.
    """

    def __init__(self, *, hash_length: int = 16):
        self._seen: set[str] = set()
        self._hash_length = hash_length

    def is_new(self, text: str) -> bool:
        """Return True if text hasn't been seen. Adds it if new."""
        h = content_hash(text, length=self._hash_length)
        if h in self._seen:
            return False
        self._seen.add(h)
        return True

    def add(self, text: str) -> None:
        """Mark text as seen."""
        self._seen.add(content_hash(text, length=self._hash_length))

    def __contains__(self, text: str) -> bool:
        return content_hash(text, length=self._hash_length) in self._seen

    def clear(self) -> None:
        self._seen.clear()

    def __len__(self) -> int:
        return len(self._seen)


# ── Base Spider ──────────────────────────────────────────────


class BaseSpider:
    """Base spider class inspired by scrapy.Spider.

    Attributes:
        name: Spider identifier (must be unique).
        allowed_domains: Optional domain allowlist.
        start_urls: Initial URLs to crawl.
        custom_settings: Per-spider settings overrides.
        user_agent: HTTP User-Agent string.
        concurrency: Max parallel requests.
        rate_delay: Delay between requests in seconds.
        truncate_bytes: Max content size per page.
        hash_length: Content hash truncation length.
    """

    name: str = ""
    allowed_domains: list[str] = []
    start_urls: list[str] = []
    custom_settings: dict = {}

    user_agent: str = "agentstreams-crawler/2.0"
    concurrency: int = 20
    rate_delay: float = 0.05
    truncate_bytes: int = 50_000
    hash_length: int = 12

    def __init__(self, **kwargs):
        self.dedup = BloomDedup(hash_length=self.hash_length)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def content_hash(self, text: str) -> str:
        return content_hash(text, length=self.hash_length)

    def html_to_text(self, html: str) -> str:
        return html_to_text(html)

    def start(self) -> list[str]:
        """Return initial URLs to crawl."""
        return list(self.start_urls)

    def parse(self, url: str, content: str) -> dict:
        """Process a fetched page. Override in subclasses."""
        raise NotImplementedError


# ── Sitemap Spider ───────────────────────────────────────────


class SitemapSpider(BaseSpider):
    """Spider for sitemap-based crawling, inspired by scrapy.SitemapSpider.

    Attributes:
        sitemap_urls: URLs pointing to sitemaps or robots.txt.
        sitemap_rules: List of (regex, callback_name) tuples.
        sitemap_follow: Regex patterns for sub-sitemaps to follow.
    """

    sitemap_urls: list[str] = []
    sitemap_rules: list[tuple[str, str]] = []
    sitemap_follow: list[str] = [""]

    def parse_sitemap_xml(self, xml_text: str) -> list[str]:
        """Extract URLs from sitemap XML (handles urlset and sitemapindex)."""
        urls: list[str] = []
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return urls

        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"

        for sitemap in root.findall(f"{ns}sitemap"):
            loc = sitemap.find(f"{ns}loc")
            if loc is not None and loc.text:
                urls.append(loc.text.strip())

        for url_elem in root.findall(f"{ns}url"):
            loc = url_elem.find(f"{ns}loc")
            if loc is not None and loc.text:
                urls.append(loc.text.strip())

        return urls

    def sitemap_filter(self, entries: list[str]) -> list[str]:
        """Filter sitemap entries. Override for custom filtering."""
        return entries

    def start(self) -> list[str]:
        """Return sitemap URLs as start points."""
        return list(self.sitemap_urls) if self.sitemap_urls else super().start()


# ── XML Feed Spider ─────────────────────────────────────────


class XMLFeedSpider(BaseSpider):
    """Spider for XML/RSS feeds, inspired by scrapy.XMLFeedSpider.

    Attributes:
        iterator: Parser type — 'iternodes' (regex), 'xml' (DOM), 'html' (DOM).
        itertag: XML element name to iterate over.
    """

    iterator: str = "iternodes"
    itertag: str = "item"

    def adapt_response(self, text: str) -> str:
        """Pre-process response before parsing. Override for HTML→text."""
        return text

    def parse_node(self, node: dict) -> dict | None:
        """Process a single node. Override in subclasses."""
        raise NotImplementedError

    def process_results(self, results: list[dict]) -> list[dict]:
        """Post-process results. Override for filtering/transformation."""
        return results


# ── Changelog Spider ─────────────────────────────────────────


VERSION_RE = re.compile(r"^#+\s*([\d.]+)\s*[-–—]\s*(.+)$", re.MULTILINE)
BULLET_RE = re.compile(r"^\s*[\*\-]\s+(.+)$", re.MULTILINE)


class ChangelogSpider(XMLFeedSpider):
    """Spider for changelog markdown, combining XMLFeedSpider patterns with
    bullet classification and task decomposition.

    Parses version headers as itertag boundaries, then extracts and classifies
    bullet points within each version section.
    """

    name = "changelog"
    itertag = "version"
    hash_length = 16

    def adapt_response(self, text: str) -> str:
        """Convert HTML to plain text if needed."""
        if "<html" in text[:500].lower() or "<!doctype" in text[:500].lower():
            return html_to_text(text)
        return text

    def parse_node(self, node: dict) -> dict | None:
        """Classify a changelog bullet point.

        Args:
            node: dict with 'version', 'date', 'text' keys.

        Returns:
            dict with added 'category' and 'priority' keys, or None if duplicate.
        """
        text = node.get("text", "")
        key = f"{node.get('version', '')}:{text}"
        if not self.dedup.is_new(key):
            return None

        node["category"] = self._classify(text)
        node["priority"] = self._priority(text)
        node["hash"] = content_hash(key, length=self.hash_length)
        return node

    @staticmethod
    def _classify(text: str) -> str:
        t = text.lower()
        if t.startswith("added") or t.startswith("new "):
            return "feat"
        if t.startswith("fixed"):
            return "fix"
        if t.startswith("improved") or t.startswith("reduced") or t.startswith("optimized"):
            return "improve"
        if t.startswith("removed") or t.startswith("changed") or t.startswith("deprecated"):
            return "remove"
        return "other"

    @staticmethod
    def _priority(text: str) -> str:
        t = text.lower()
        if any(kw in t for kw in ["security", "crash", "oom", "critical", "breaking"]):
            return "high"
        if any(kw in t for kw in ["performance", "fixed", "regression", "leak"]):
            return "medium"
        return "low"

    def parse_changelog(self, text: str) -> list[dict]:
        """Parse markdown changelog into structured entries.

        Returns list of dicts with 'version', 'date', 'bullets' keys.
        Each bullet has 'version', 'date', 'text', 'category', 'priority', 'hash'.
        """
        adapted = self.adapt_response(text)
        entries = []
        sections = VERSION_RE.split(adapted)

        i = 1
        while i + 2 <= len(sections):
            version = sections[i].strip()
            date = sections[i + 1].strip()
            body = sections[i + 2] if i + 2 < len(sections) else ""

            bullets = []
            for match in BULLET_RE.finditer(body):
                bullet_text = match.group(1).strip()
                node = {"version": version, "date": date, "text": bullet_text}
                result = self.parse_node(node)
                if result is not None:
                    bullets.append(result)

            if bullets:
                entries.append({"version": version, "date": date, "bullets": bullets})
            i += 3

        return self.process_results(entries)
