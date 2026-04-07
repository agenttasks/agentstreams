"""Scrapy-pattern web crawlers with Neon Postgres persistence.

Extends the spider hierarchy from scripts/spiders.py with proper
database persistence, bloom filter deduplication, and pipeline
integration following the UDA DataContainer pattern.

Each crawler:
1. Reads URLs from sitemap/feed/start_urls
2. Deduplicates via persistent BloomFilter (src/bloom.py)
3. Fetches and parses content (HTMLToText)
4. Persists results to Neon Postgres (src/neon_db.py)
5. Enqueues analysis tasks for downstream processing

UDA pattern: crawled pages are DataContainers. The crawler is a
data producer that writes to the crawl_pages projection. Downstream
consumers read from the same table via pg_graphql.
"""

from __future__ import annotations

import asyncio
import re

# Re-export shared utilities from scripts/spiders.py
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import aiohttp

from src.bloom import BloomFilter, NeonBloomStore
from src.neon_db import (
    connection_pool,
    enqueue_task,
    record_metric,
    upsert_crawl_page,
    upsert_resource,
)

_scripts_dir = str(Path(__file__).parent.parent / "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from spiders import content_hash, html_to_text  # noqa: E402


@dataclass
class CrawlResult:
    """Structured result from a single page crawl."""

    url: str
    domain: str
    title: str = ""
    content: str = ""
    content_hash: str = ""
    status_code: int = 0
    error: str = ""
    crawled_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return not self.error and self.status_code == 200


@dataclass
class CrawlConfig:
    """Configuration for a crawl pipeline."""

    name: str
    domains: list[str]
    sitemap_urls: list[str] = field(default_factory=list)
    start_urls: list[str] = field(default_factory=list)
    url_patterns: list[str] = field(default_factory=list)
    concurrency: int = 20
    rate_delay: float = 0.05
    max_pages: int = 10_000
    truncate_bytes: int = 50_000
    user_agent: str = "agentstreams-crawler/3.0 (UDA pipeline)"
    bloom_expected_items: int = 100_000
    bloom_fp_rate: float = 0.01
    neon_url: str = ""
    persist_content: bool = True
    enqueue_analysis: bool = True
    priority_patterns: list[str] = field(default_factory=list)


class UDACrawler:
    """Scrapy-pattern web crawler with UDA data persistence.

    Implements the full crawl pipeline:
    - Sitemap parsing → URL discovery
    - Bloom filter deduplication (persistent across sessions)
    - Concurrent HTTP fetching with rate limiting
    - HTML→text extraction
    - Neon Postgres persistence (crawl_pages + resources)
    - Task enqueueing for downstream analysis

    Args:
        config: CrawlConfig with all pipeline parameters.
    """

    def __init__(self, config: CrawlConfig):
        self.config = config
        self.bloom = BloomFilter(
            expected_items=config.bloom_expected_items,
            fp_rate=config.bloom_fp_rate,
        )
        self._results: list[CrawlResult] = []
        self._semaphore = asyncio.Semaphore(config.concurrency)
        self._url_filters = [re.compile(p) for p in config.url_patterns]

    def _should_crawl(self, url: str) -> bool:
        """Check if URL matches domain allowlist and pattern filters."""
        parsed = urlparse(url)
        if parsed.netloc not in self.config.domains:
            return False
        if self._url_filters:
            return any(f.search(url) for f in self._url_filters)
        return True

    async def _load_bloom(self, conn) -> None:
        """Load persistent bloom filter from Neon if available."""
        store = NeonBloomStore(conn)
        existing = await store.load(f"crawler:{self.config.name}")
        if existing:
            self.bloom = existing

    async def _save_bloom(self, conn) -> None:
        """Persist bloom filter state to Neon."""
        store = NeonBloomStore(conn)
        await store.save(
            f"crawler:{self.config.name}",
            self.bloom,
            domain=",".join(self.config.domains),
        )

    async def _parse_sitemap(self, session: aiohttp.ClientSession, url: str) -> list[str]:
        """Fetch and parse a sitemap XML, following sitemapindex entries."""
        urls: list[str] = []
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return urls
                xml_text = await resp.text()
        except (TimeoutError, aiohttp.ClientError):
            return urls

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return urls

        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"

        # Follow sub-sitemaps
        for sitemap in root.findall(f"{ns}sitemap"):
            loc = sitemap.find(f"{ns}loc")
            if loc is not None and loc.text:
                sub_urls = await self._parse_sitemap(session, loc.text.strip())
                urls.extend(sub_urls)

        # Extract page URLs
        for url_elem in root.findall(f"{ns}url"):
            loc = url_elem.find(f"{ns}loc")
            if loc is not None and loc.text:
                page_url = loc.text.strip()
                if self._should_crawl(page_url):
                    urls.append(page_url)

        return urls

    async def _fetch_page(
        self, session: aiohttp.ClientSession, url: str
    ) -> CrawlResult:
        """Fetch a single page with rate limiting and error handling."""
        domain = urlparse(url).netloc
        result = CrawlResult(url=url, domain=domain)

        async with self._semaphore:
            if self.config.rate_delay > 0:
                await asyncio.sleep(self.config.rate_delay)

            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    result.status_code = resp.status
                    if resp.status != 200:
                        result.error = f"HTTP {resp.status}"
                        return result

                    html = await resp.text()
                    text = html_to_text(html[: self.config.truncate_bytes])

                    # Extract title
                    title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
                    result.title = title_match.group(1).strip() if title_match else ""
                    result.content = text
                    result.content_hash = content_hash(text)
                    result.crawled_at = datetime.now(UTC).isoformat()

            except (TimeoutError, aiohttp.ClientError) as e:
                result.error = str(e)

        return result

    async def discover_urls(self, session: aiohttp.ClientSession) -> list[str]:
        """Discover all URLs from sitemaps and start_urls, deduplicating via bloom filter."""
        all_urls: list[str] = []

        # Parse sitemaps
        for sitemap_url in self.config.sitemap_urls:
            sitemap_urls = await self._parse_sitemap(session, sitemap_url)
            all_urls.extend(sitemap_urls)

        # Add start_urls
        all_urls.extend(u for u in self.config.start_urls if self._should_crawl(u))

        # Deduplicate via bloom filter
        unique_urls = [u for u in all_urls if self.bloom.is_new(u)]

        # Respect max_pages
        return unique_urls[: self.config.max_pages]

    async def crawl(self) -> list[CrawlResult]:
        """Execute the full crawl pipeline.

        Returns:
            List of CrawlResult objects for all pages.
        """
        headers = {"User-Agent": self.config.user_agent}

        async with aiohttp.ClientSession(headers=headers) as session:
            urls = await self.discover_urls(session)
            if not urls:
                return []

            # Fetch all pages concurrently
            tasks = [self._fetch_page(session, url) for url in urls]
            self._results = await asyncio.gather(*tasks)

        return self._results

    async def persist(self, neon_url: str | None = None) -> dict[str, int]:
        """Persist crawl results to Neon Postgres.

        Writes to:
        - crawl_pages: full page content and metadata
        - resources: URL registry with content hashes
        - tasks: analysis tasks for downstream processing
        - bloom_filters: updated bloom filter state
        - metric_values: crawl metrics

        Returns:
            Dict with counts of persisted records.
        """
        url = neon_url or self.config.neon_url
        if not url:
            return {"pages": 0, "resources": 0, "tasks": 0}

        counts = {"pages": 0, "resources": 0, "tasks": 0}
        priority_re = (
            re.compile("|".join(self.config.priority_patterns))
            if self.config.priority_patterns
            else None
        )

        async with connection_pool(url) as conn:
            # Load existing bloom state
            await self._load_bloom(conn)

            for result in self._results:
                if not result.is_success:
                    continue

                # Persist page content
                if self.config.persist_content:
                    await upsert_crawl_page(
                        conn,
                        url=result.url,
                        domain=result.domain,
                        content_hash=result.content_hash,
                        title=result.title,
                        content=result.content,
                        status_code=result.status_code,
                    )
                    counts["pages"] += 1

                # Upsert resource record
                await upsert_resource(
                    conn,
                    resource_type="crawled_page",
                    label=result.title or result.url.split("/")[-1],
                    url=result.url,
                    content_hash=result.content_hash,
                )
                counts["resources"] += 1

                # Enqueue analysis task
                if self.config.enqueue_analysis:
                    priority = (
                        1
                        if priority_re and priority_re.search(result.url)
                        else 0
                    )
                    await enqueue_task(
                        conn,
                        queue_name="crawl-analyze",
                        task_type="knowledge_work",
                        skill_name="crawl-ingest",
                        task_input={"url": result.url, "domain": result.domain},
                        priority=priority,
                    )
                    counts["tasks"] += 1

            # Record metrics
            success_count = sum(1 for r in self._results if r.is_success)
            error_count = sum(1 for r in self._results if r.error)
            await record_metric(
                conn,
                metric_name="agentstreams.crawl.pages",
                value=success_count,
                tags={"domain": self.config.domains[0] if self.config.domains else "", "status": "success"},
            )
            if error_count:
                await record_metric(
                    conn,
                    metric_name="agentstreams.crawl.pages",
                    value=error_count,
                    tags={"domain": self.config.domains[0] if self.config.domains else "", "status": "error"},
                )
            await record_metric(
                conn,
                metric_name="agentstreams.crawl.dedup",
                value=self.bloom.estimated_fp_rate,
                tags={"method": "bloom"},
            )

            # Save bloom filter state
            await self._save_bloom(conn)
            await conn.commit()

        return counts


class RSSCrawler(UDACrawler):
    """Crawler for RSS/Atom feeds following XMLFeedSpider pattern.

    Parses feed entries instead of sitemap URLs, then crawls each
    entry's link for full content.
    """

    async def _parse_feed(self, session: aiohttp.ClientSession, feed_url: str) -> list[dict]:
        """Parse an RSS/Atom feed into structured entries."""
        entries: list[dict] = []
        try:
            async with session.get(feed_url) as resp:
                if resp.status != 200:
                    return entries
                xml_text = await resp.text()
        except (TimeoutError, aiohttp.ClientError):
            return entries

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return entries

        # Handle RSS 2.0
        for item in root.iter("item"):
            entry = {}
            for child in ("title", "link", "description", "pubDate", "guid"):
                elem = item.find(child)
                if elem is not None and elem.text:
                    entry[child] = elem.text.strip()
            if "link" in entry:
                entries.append(entry)

        # Handle Atom
        ns = "{http://www.w3.org/2005/Atom}"
        for item in root.iter(f"{ns}entry"):
            entry = {}
            title = item.find(f"{ns}title")
            if title is not None and title.text:
                entry["title"] = title.text.strip()
            link = item.find(f"{ns}link")
            if link is not None:
                entry["link"] = link.get("href", "")
            if "link" in entry:
                entries.append(entry)

        return entries

    async def discover_urls(self, session: aiohttp.ClientSession) -> list[str]:
        """Discover URLs from RSS/Atom feeds."""
        all_urls: list[str] = []
        for feed_url in self.config.sitemap_urls:
            entries = await self._parse_feed(session, feed_url)
            for entry in entries:
                url = entry.get("link", "")
                if url and self._should_crawl(url):
                    all_urls.append(url)

        # Add start_urls
        all_urls.extend(u for u in self.config.start_urls if self._should_crawl(u))

        # Deduplicate via bloom filter
        unique_urls = [u for u in all_urls if self.bloom.is_new(u)]
        return unique_urls[: self.config.max_pages]


class ChangelogCrawler(UDACrawler):
    """Crawler for changelog/release pages with version extraction.

    Combines UDACrawler's persistence with ChangelogSpider's parsing
    to extract structured version/bullet data and persist to Neon.
    """

    VERSION_RE = re.compile(r"^#+\s*([\d.]+)\s*[-–—]\s*(.+)$", re.MULTILINE)
    BULLET_RE = re.compile(r"^\s*[\*\-]\s+(.+)$", re.MULTILINE)

    def _parse_changelog(self, text: str) -> list[dict]:
        """Parse changelog text into structured version entries."""
        entries = []
        sections = self.VERSION_RE.split(text)

        i = 1
        while i + 2 <= len(sections):
            version = sections[i].strip()
            date = sections[i + 1].strip()
            body = sections[i + 2] if i + 2 < len(sections) else ""

            bullets = []
            for match in self.BULLET_RE.finditer(body):
                bullet_text = match.group(1).strip()
                bullets.append({
                    "text": bullet_text,
                    "category": self._classify(bullet_text),
                    "hash": content_hash(f"{version}:{bullet_text}"),
                })

            if bullets:
                entries.append({"version": version, "date": date, "bullets": bullets})
            i += 3

        return entries

    @staticmethod
    def _classify(text: str) -> str:
        t = text.lower()
        if t.startswith(("added", "new ")):
            return "feat"
        if t.startswith("fixed"):
            return "fix"
        if t.startswith(("improved", "reduced", "optimized")):
            return "improve"
        if t.startswith(("removed", "changed", "deprecated")):
            return "remove"
        return "other"
