# PHP Stack Setup

## Installation (Composer)

```json
{
    "require": {
        "anthropic-ai/anthropic": "^0.8",
        "symfony/dom-crawler": "^7.0",
        "symfony/http-client": "^7.0",
        "symfony/css-selector": "^7.0",
        "guzzlehttp/psr7": "^2.0",
        "pleonasm/bloom-filter": "^1.0"
    },
    "require-dev": {
        "phpactor/phpactor": "^2024.06"
    }
}
```

```bash
composer install
```

## Package Overview

| Package | Purpose |
|---------|---------|
| `anthropic-ai/anthropic` | Official PHP SDK — messages, streaming, tool use |
| `symfony/dom-crawler` | DOM traversal + CSS selectors |
| `symfony/http-client` | HTTP client for crawling |
| `pleonasm/bloom-filter` | Bloom filter implementation |
| `phpactor` | PHP LSP server |

**Note:** No Agent SDK for PHP. MCP SDK is available: `modelcontextprotocol/php-sdk` (maintained by PHP Foundation). Use BetaRunnableTool for tool use.

## Quick Start: Symfony Crawler + Claude + Bloom Filter

```php
<?php
require_once __DIR__ . '/vendor/autoload.php';

use Anthropic\Anthropic;
use Symfony\Component\DomCrawler\Crawler;
use Symfony\Component\HttpClient\HttpClient;

$client = Anthropic::client();
$http = HttpClient::create([
    'headers' => ['User-Agent' => 'MyCrawler/1.0'],
    'timeout' => 30,
]);

// Simple array-based bloom filter (or use pleonasm/bloom-filter)
$seen = [];
$queue = ['https://example.com'];

while (!empty($queue) && count($seen) < 1000) {
    $url = array_shift($queue);
    if (isset($seen[$url])) continue;
    $seen[$url] = true;

    try {
        $response = $http->request('GET', $url);
        $html = $response->getContent();
    } catch (\Exception $e) {
        echo "Error: {$url}: {$e->getMessage()}\n";
        continue;
    }

    $crawler = new Crawler($html, $url);
    $title = $crawler->filter('title')->count()
        ? $crawler->filter('title')->text()
        : '';

    // Claude extraction
    $result = $client->messages()->create([
        'model' => 'claude-sonnet-4-6',
        'max_tokens' => 1024,
        'messages' => [[
            'role' => 'user',
            'content' => "Extract data:\nTitle: {$title}\nHTML: " . substr($html, 0, 30000),
        ]],
    ]);

    echo "Extracted: {$url}\n";

    // Enqueue links (same domain)
    $crawler->filter('a[href]')->each(function (Crawler $node) use (&$queue, &$seen, $url) {
        $href = $node->attr('href');
        $absoluteUrl = (new \GuzzleHttp\Psr7\Uri($href))->withScheme('https')->__toString();
        if (!isset($seen[$absoluteUrl]) && str_starts_with($absoluteUrl, parse_url($url, PHP_URL_SCHEME) . '://' . parse_url($url, PHP_URL_HOST))) {
            $queue[] = $absoluteUrl;
        }
    });
}
```

## PHP LSP (Phpactor)

```bash
composer global require phpactor/phpactor
# Launch: phpactor language-server --stdio
```

Key features: completions, go-to-definition, find references, class generation.
