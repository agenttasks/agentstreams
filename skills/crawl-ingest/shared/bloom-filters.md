# Bloom Filters for URL Deduplication

## Concept

A bloom filter is a space-efficient probabilistic data structure that tests set membership. It can produce false positives (says "maybe in set" when not) but never false negatives (if it says "not in set", it's definitely not).

For web crawling, this means: a URL that passes the bloom filter check is guaranteed to be new. A URL that fails might have been seen before (with configurable probability).

## Parameters

- **Expected insertions (n)**: How many URLs you expect to crawl
- **False positive rate (fpp)**: Probability of a false positive (default: 0.01 = 1%)
- **Bit array size**: Calculated automatically from n and fpp
- **Hash functions (k)**: Calculated automatically (optimal k = (m/n) * ln(2))

## Sizing Guide

| URLs | FPP | Memory |
|------|-----|--------|
| 100K | 1% | ~117 KB |
| 1M | 1% | ~1.14 MB |
| 10M | 1% | ~11.4 MB |
| 100M | 1% | ~114 MB |
| 1B | 0.1% | ~1.72 GB |

## API by Language

### TypeScript (`bloom-filters` 3.0.4)

```typescript
import { BloomFilter } from 'bloom-filters';

// Create with expected size and error rate
const filter = BloomFilter.create(1_000_000, 0.01);

// Add URL
filter.add('https://example.com/page1');

// Check membership
if (!filter.has(url)) {
  // Definitely new — crawl it
  filter.add(url);
  await crawler.addRequest({ url });
}

// Also available: CuckooFilter (supports deletion), CountMinSketch, HyperLogLog
```

### Python (`pybloom-live` 4.0.0)

```python
from pybloom_live import BloomFilter, ScalableBloomFilter

# Fixed-size bloom filter
bf = BloomFilter(capacity=1_000_000, error_rate=0.01)

bf.add('https://example.com/page1')
if 'https://example.com/page2' not in bf:
    # Definitely new
    bf.add('https://example.com/page2')

# Auto-scaling bloom filter (grows as needed)
sbf = ScalableBloomFilter(
    initial_capacity=100_000,
    error_rate=0.01,
    mode=ScalableBloomFilter.SMALL_SET_GROWTH
)
```

### Java (Guava `BloomFilter`)

```java
import com.google.common.hash.BloomFilter;
import com.google.common.hash.Funnels;

// Create bloom filter for strings
BloomFilter<String> filter = BloomFilter.create(
    Funnels.unencodedCharsFunnel(),
    1_000_000,  // expected insertions
    0.01        // false positive probability
);

filter.put("https://example.com/page1");
if (!filter.mightContain(url)) {
    // Definitely new
    filter.put(url);
    crawlQueue.add(url);
}

// Check current FPP
double currentFpp = filter.expectedFpp();
```

## Persistence

Bloom filters should be saved to disk between crawl sessions:

- **TypeScript**: `JSON.stringify(filter.saveAsJSON())` / `BloomFilter.fromJSON(data)`
- **Python**: `pickle.dump(bf, file)` / `pickle.load(file)` — or use `pybloomfiltermmap3` for mmap-backed persistence
- **Java**: `filter.writeTo(outputStream)` / `BloomFilter.readFrom(inputStream, funnel)`

## When to Use Scalable vs Fixed

- **Fixed**: You know the approximate URL count upfront. Better memory efficiency.
- **Scalable**: URL count unknown or growing indefinitely. Slightly higher memory overhead. Python's `ScalableBloomFilter` handles this automatically.
