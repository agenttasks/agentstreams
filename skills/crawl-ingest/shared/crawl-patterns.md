# Web Crawling Patterns

## Crawl Strategy Decision Tree

```
What are you crawling?
├── Single site, structured data → Focused crawl (sitemap + CSS selectors)
├── Single site, JS-rendered → Browser crawl (Playwright/Puppeteer)
├── Multiple sites, similar structure → Template crawl (shared selectors per domain)
├── Broad discovery across domains → BFS crawl with domain-level throttling
└── API endpoints, not HTML → HTTP crawl (no browser needed)
```

## Politeness Rules

CRITICAL: Always implement these unless explicitly told otherwise:

1. **Respect robots.txt** — check before crawling any domain
2. **Rate limiting** — 1-2 requests/second per domain (default)
3. **User-Agent** — identify your crawler honestly
4. **Retry with backoff** — exponential backoff on 429/503
5. **Session management** — maintain cookies when required

## Deduplication Strategy

```
URL arrives
├── Normalize URL (lowercase host, remove fragments, sort params)
├── Check bloom filter
│   ├── Not in filter → NEW: add to filter + enqueue
│   └── Might be in filter → SKIP (accept rare false positives)
└── For content dedup: hash page content (SimHash/MinHash for near-duplicates)
```

## Content Extraction Pipeline

```
Raw HTML/Response
├── Parse HTML (Cheerio/BeautifulSoup/JSoup)
├── Extract structured data (CSS selectors, XPath)
├── Claude SDK: classify/extract/summarize content
│   ├── Use structured outputs for schema enforcement
│   ├── Use batch API for bulk processing (50% cheaper)
│   └── Use programmatic tool calling for multi-step extraction
└── Store to local DB (SQLite) or cloud DW
```

## Error Handling

| Error | Action |
|-------|--------|
| 404 | Log and skip — mark URL as dead |
| 429 | Exponential backoff, respect Retry-After |
| 403 | Check robots.txt, try different User-Agent |
| 500/502/503 | Retry with backoff (max 3 retries) |
| Timeout | Retry once, then skip |
| SSL Error | Log warning, optionally skip |

## Storage Patterns

### Local-First (Default)

```
data/
├── crawl.db          # SQLite: URLs, metadata, status
├── pages/            # Raw HTML snapshots (gzipped)
├── extracted/        # Structured JSON per page
└── bloom.bin         # Serialized bloom filter
```

### Cloud Switchover

When local storage exceeds thresholds or you need shared access:
- See `shared/data-warehouse.md` for Kimball-modeled warehouse schema
- Fact table: `fact_crawl_events` (url, timestamp, status, content_hash)
- Dimensions: `dim_domain`, `dim_content_type`, `dim_extraction_result`
