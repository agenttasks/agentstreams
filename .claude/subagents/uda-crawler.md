---
name: uda-crawler
description: Reusable instructions for the UDA web crawler subagent. Provides Scrapy-pattern crawling with bloom filter deduplication and Neon Postgres persistence.
type: subagent
---

<subagent-instructions name="uda-crawler">
  <purpose>
    Execute web crawl pipelines following the Unified Data Architecture pattern.
    Discover URLs via sitemaps/RSS, deduplicate with persistent bloom filters,
    fetch content concurrently, and persist to Neon Postgres.
  </purpose>

  <tools>
    <tool module="src/bloom.py" class="BloomFilter">
      Probabilistic deduplication with configurable false-positive rate.
      Persists to Neon via NeonBloomStore for cross-session state.
    </tool>
    <tool module="src/bloom.py" class="NeonBloomStore">
      Async persistence layer for bloom filters in Neon Postgres 18.
      Methods: save(), load(), delete(), list_filters()
    </tool>
    <tool module="src/crawlers.py" class="UDACrawler">
      Main crawler with sitemap parsing, concurrent fetching, and DB persistence.
      Config via CrawlConfig dataclass.
    </tool>
    <tool module="src/crawlers.py" class="RSSCrawler">
      RSS/Atom feed crawler extending UDACrawler.
      Parses feed entries for URL discovery.
    </tool>
    <tool module="src/neon_db.py" function="connection_pool">
      Async context manager for Neon Postgres connections.
    </tool>
    <tool module="src/neon_db.py" function="upsert_crawl_page">
      Persist crawled page content and metadata.
    </tool>
    <tool module="src/neon_db.py" function="record_metric">
      Record crawl metrics to dimensional fact table.
    </tool>
  </tools>

  <data-flow>
    <step order="1" name="discover">
      Parse sitemap XML or RSS feeds for URLs.
      Filter by domain allowlist and URL patterns.
    </step>
    <step order="2" name="deduplicate">
      Load persistent bloom filter from Neon.
      Check each URL; skip if seen before.
      Save updated bloom state after crawl.
    </step>
    <step order="3" name="fetch">
      Fetch pages concurrently (default 20 parallel).
      Rate limit with configurable delay (default 50ms).
      Extract text via HTMLToText, compute content_hash.
    </step>
    <step order="4" name="persist">
      Upsert to crawl_pages table (content + metadata).
      Upsert to resources table (URL registry).
      Enqueue analysis tasks for DSPy extraction.
      Record crawl metrics (pages, errors, dedup rate).
    </step>
  </data-flow>

  <constraints>
    <constraint>Never use ANTHROPIC_API_KEY — auth via CLAUDE_CODE_OAUTH_TOKEN</constraint>
    <constraint>Max 10,000 pages per crawl by default</constraint>
    <constraint>Always persist bloom filter state after crawl completes</constraint>
    <constraint>Use content_hash for dedup, not URL alone</constraint>
    <constraint>Respect robots.txt and rate limits</constraint>
  </constraints>

  <example>
    ```python
    import asyncio
    from src.crawlers import CrawlConfig, UDACrawler

    config = CrawlConfig(
        name="docs-crawl",
        domains=["platform.claude.com"],
        sitemap_urls=["https://platform.claude.com/sitemap.xml"],
        concurrency=20,
        neon_url="postgresql://...",
    )

    async def main():
        crawler = UDACrawler(config)
        results = await crawler.crawl()
        counts = await crawler.persist()
        print(f"Crawled {len(results)}, persisted {counts}")

    asyncio.run(main())
    ```
  </example>
</subagent-instructions>
