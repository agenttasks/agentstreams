# Python Stack Setup

## Installation (uv)

```bash
# Initialize project
uv init crawl-project && cd crawl-project

# Core Anthropic packages
uv add anthropic
uv add claude-agent-sdk
uv add mcp

# Web Crawling
uv add scrapy==2.14.2
uv add scrapy-playwright==0.0.46    # JS rendering support

# Bloom Filters
uv add pybloom-live==4.0.0
uv add bitarray==3.8.0              # High-performance bit arrays
uv add mmh3==5.2.1                  # MurmurHash3 (fast hashing)

# Programmatic Prompts
uv add dspy==3.1.3

# LSP (dev dependency)
uv add --dev python-lsp-server==1.14.0
uv add --dev pylsp-mypy==0.7.1
uv add --dev python-lsp-ruff==2.3.0
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | 0.86.0 | Official Python SDK — messages, streaming, tool use, structured outputs |
| `claude-agent-sdk` | 0.1.53 | Headless agent — `query()`, `ClaudeSDKClient` |
| `mcp` | 1.26.0 | Official MCP SDK — servers, clients, tools, resources (22k★) |
| `scrapy` | 2.14.2 | Web crawling framework — spiders, middleware, pipelines |
| `scrapy-playwright` | 0.0.46 | Playwright integration for JS-rendered pages |
| `pybloom-live` | 4.0.0 | Bloom filter implementation — `BloomFilter`, `ScalableBloomFilter` |
| `dspy` | 3.1.3 | Programmatic prompts — signatures, modules, optimizers |
| `python-lsp-server` | 1.14.0 | Python LSP for code intelligence |

## Quick Start: Scrapy + Claude + Bloom Filter

```python
import scrapy
import anthropic
from pybloom_live import ScalableBloomFilter

# Initialize
client = anthropic.Anthropic()
bloom = ScalableBloomFilter(
    initial_capacity=100_000,
    error_rate=0.01
)

class ProductSpider(scrapy.Spider):
    name = 'products'
    start_urls = ['https://example.com/products']

    def parse(self, response):
        # Bloom filter dedup
        if response.url in bloom:
            return
        bloom.add(response.url)

        # Extract with CSS selectors
        html = response.text

        # Claude extraction with structured output
        result = client.messages.create(
            model='claude-opus-4-6',
            max_tokens=1024,
            thinking={'type': 'adaptive'},
            messages=[{
                'role': 'user',
                'content': f'Extract product data from:\n{html[:50000]}'
            }],
        )

        yield {
            'url': response.url,
            'extracted': result.content,
            'timestamp': response.headers.get('Date', b'').decode(),
        }

        # Follow pagination and product links
        for href in response.css('a::attr(href)').getall():
            url = response.urljoin(href)
            if url not in bloom:
                yield scrapy.Request(url, callback=self.parse)
```

## Further Reading

- `python/scrapy-patterns.md` — Spider types, middleware, pipelines
- `python/sdk-integration.md` — Python SDK patterns, Agent SDK, tool use
- `python/dspy-integration.md` — DSPy with Claude — signatures, modules, optimizers
- `python/lsp-config.md` — Python LSP setup
- `shared/bloom-filters.md` — Bloom filter API and persistence
