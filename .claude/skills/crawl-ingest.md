---
name: crawl-ingest
description: "Web crawling, deduplication, and data ingestion using Anthropic SDKs"
trigger: "user asks to crawl websites, build scrapers, deduplicate URLs with bloom filters, ingest data, or use Crawlee/Scrapy/crawler4j with Claude"
---

Read `skills/crawl-ingest/SKILL.md` for the full skill definition, then follow the language detection rules to load the appropriate language README.

## UDA Programmatic Tools (src/)

For Python implementations, prefer the unified src/ modules over inline code:

| Module | Class/Function | Purpose |
|--------|---------------|---------|
| `src/bloom.py` | `BloomFilter`, `NeonBloomStore` | Persistent bloom filter deduplication |
| `src/crawlers.py` | `UDACrawler`, `RSSCrawler`, `CrawlConfig` | Scrapy-pattern crawlers with Neon persistence |
| `src/neon_db.py` | `upsert_crawl_page`, `enqueue_task` | Typed Neon Postgres data access |
| `src/embeddings.py` | `EmbeddingPipeline`, `LanceStore` | Vector embeddings for crawled content |
| `src/dspy_prompts.py` | `EXTRACT_ENTITIES`, `CLASSIFY_CONTENT` | DSPy extraction on crawled pages |

See `.claude/subagents/uda-crawler.md` for structured execution instructions.
