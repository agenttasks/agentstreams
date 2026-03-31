# Scrapy Patterns

## Spider Types

| Spider | Use Case |
|--------|----------|
| `scrapy.Spider` | General-purpose, manual link following |
| `scrapy.CrawlSpider` | Rule-based automatic link following |
| `scrapy.SitemapSpider` | Crawl from sitemap.xml |
| `scrapy.XMLFeedSpider` | Parse XML/RSS feeds |

## CrawlSpider with Rules

```python
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SiteCrawler(CrawlSpider):
    name = 'site'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com']

    rules = (
        Rule(LinkExtractor(allow=r'/products/'), callback='parse_product'),
        Rule(LinkExtractor(allow=r'/category/')),  # follow but don't parse
    )

    def parse_product(self, response):
        yield {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'price': response.css('.price::text').get(),
        }
```

## Middleware: Bloom Filter Dedup

```python
# middlewares.py
from pybloom_live import ScalableBloomFilter
import pickle
import os

class BloomFilterMiddleware:
    BLOOM_PATH = './data/bloom.pickle'

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def __init__(self):
        if os.path.exists(self.BLOOM_PATH):
            with open(self.BLOOM_PATH, 'rb') as f:
                self.bloom = pickle.load(f)
        else:
            self.bloom = ScalableBloomFilter(
                initial_capacity=100_000, error_rate=0.01
            )

    def process_request(self, request, spider):
        if request.url in self.bloom:
            from scrapy.exceptions import IgnoreRequest
            raise IgnoreRequest(f'Bloom filter: {request.url}')
        return None

    def process_response(self, request, response, spider):
        self.bloom.add(request.url)
        return response

    def close_spider(self, spider):
        os.makedirs(os.path.dirname(self.BLOOM_PATH), exist_ok=True)
        with open(self.BLOOM_PATH, 'wb') as f:
            pickle.dump(self.bloom, f)
```

Enable in `settings.py`:

```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.BloomFilterMiddleware': 543,
}
```

## Pipeline: Claude Extraction

```python
# pipelines.py
import anthropic

class ClaudeExtractionPipeline:
    def open_spider(self, spider):
        self.client = anthropic.Anthropic()

    def process_item(self, item, spider):
        response = self.client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=1024,
            messages=[{
                'role': 'user',
                'content': f'Extract structured data:\n{item.get("html", "")[:30000]}'
            }],
        )
        item['claude_extraction'] = response.content[0].text
        return item
```

## Playwright Integration (JS Rendering)

```python
# settings.py
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# In spider
def start_requests(self):
    yield scrapy.Request(
        'https://spa-example.com',
        meta={'playwright': True, 'playwright_include_page': True},
    )

async def parse(self, response):
    page = response.meta['playwright_page']
    await page.wait_for_selector('.loaded')
    content = await page.content()
    await page.close()
    yield {'html': content, 'url': response.url}
```

## Settings Reference

```python
# settings.py
BOT_NAME = 'crawl_project'
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS_PER_DOMAIN = 8
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0
HTTPCACHE_ENABLED = True
LOG_LEVEL = 'INFO'
FEEDS = {
    'data/output.jsonl': {'format': 'jsonlines'},
}
```
