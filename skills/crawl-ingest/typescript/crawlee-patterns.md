# Crawlee Patterns

## Crawler Types

| Crawler | Use Case | JS Rendering | Speed |
|---------|----------|-------------|-------|
| `CheerioCrawler` | Static HTML, no JS needed | No | Fastest |
| `PlaywrightCrawler` | JS-rendered pages, SPAs | Yes | Slow |
| `PuppeteerCrawler` | JS-rendered (Chrome-only) | Yes | Slow |
| `HttpCrawler` | Raw HTTP, API endpoints | No | Fastest |
| `JSDOMCrawler` | Static HTML with DOM API | Partial | Medium |

**Default choice**: `CheerioCrawler` for static sites, `PlaywrightCrawler` for anything with JavaScript.

## Request Queue with Bloom Filter

```typescript
import { CheerioCrawler, RequestQueue } from 'crawlee';
import { BloomFilter } from 'bloom-filters';
import { readFileSync, writeFileSync, existsSync } from 'fs';

// Load or create bloom filter
const BLOOM_PATH = './data/bloom.json';
const bloom = existsSync(BLOOM_PATH)
  ? BloomFilter.fromJSON(JSON.parse(readFileSync(BLOOM_PATH, 'utf-8')))
  : BloomFilter.create(1_000_000, 0.01);

const crawler = new CheerioCrawler({
  maxRequestsPerMinute: 60,
  maxConcurrency: 5,

  async requestHandler({ request, $, enqueueLinks }) {
    const url = request.url;
    if (bloom.has(url)) return;
    bloom.add(url);

    // Extract with Cheerio selectors
    const title = $('title').text();
    const content = $('main').text() || $('body').text();

    // Store locally
    await Dataset.pushData({ url, title, content });

    // Enqueue discovered links (same domain only)
    await enqueueLinks({
      strategy: 'same-domain',
      transformRequestFunction: (req) => {
        if (bloom.has(req.url)) return false;
        return req;
      },
    });
  },

  async failedRequestHandler({ request }) {
    console.error(`Failed: ${request.url} (${request.errorMessages.join(', ')})`);
  },
});

// Run and save bloom filter
await crawler.run(['https://example.com']);
writeFileSync(BLOOM_PATH, JSON.stringify(bloom.saveAsJSON()));
```

## Storage Options

Crawlee has built-in storage:

```typescript
import { Dataset, KeyValueStore } from 'crawlee';

// Dataset — append-only structured data (JSON lines)
await Dataset.pushData({ url, title, content });

// KeyValueStore — key-value pairs (for state, configs)
const store = await KeyValueStore.open('crawl-state');
await store.setValue('bloom-filter', bloom.saveAsJSON());

// Export dataset to file
const dataset = await Dataset.open();
await dataset.exportToCSV('output.csv');
await dataset.exportToJSON('output.json');
```

## Auto-Scaling

```typescript
const crawler = new PlaywrightCrawler({
  // Auto-scaling adjusts concurrency based on system load
  autoscaledPoolOptions: {
    minConcurrency: 1,
    maxConcurrency: 10,
    desiredConcurrency: 5,
  },
  // Rate limiting
  maxRequestsPerMinute: 120,
  // Retry configuration
  maxRequestRetries: 3,
});
```

## Proxy Rotation

```typescript
import { ProxyConfiguration } from 'crawlee';

const proxyConfig = new ProxyConfiguration({
  proxyUrls: [
    'http://proxy1:8080',
    'http://proxy2:8080',
  ],
});

const crawler = new CheerioCrawler({
  proxyConfiguration: proxyConfig,
  // ...
});
```

## Session Management

```typescript
import { SessionPool } from 'crawlee';

const sessionPool = new SessionPool({
  maxPoolSize: 20,
  sessionOptions: {
    maxAgeSecs: 3600,
    maxUsageCount: 50,
  },
});
```
