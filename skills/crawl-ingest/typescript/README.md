# TypeScript Stack Setup

## Installation

```bash
# Initialize project
mkdir crawl-project && cd crawl-project
npm init -y
npx tsc --init

# Core Anthropic packages
npm install @anthropic-ai/sdk
npm install @anthropic-ai/claude-agent-sdk
npm install @anthropic-ai/tokenizer@0.0.4

# Cloud provider SDKs (install as needed)
npm install @anthropic-ai/bedrock-sdk@0.26.4    # AWS Bedrock
npm install @anthropic-ai/vertex-sdk@0.14.4      # Google Vertex
npm install @anthropic-ai/foundry-sdk@0.2.3      # Anthropic Foundry

# MCP SDK (modelcontextprotocol)
npm install @modelcontextprotocol/sdk

# MCP Bundle Builder + Sandbox
npm install @anthropic-ai/mcpb@2.1.2
npm install @anthropic-ai/sandbox-runtime@0.0.44

# Web Crawling
npm install crawlee@3.16.0
npm install playwright                            # For PlaywrightCrawler

# Bloom Filters
npm install bloom-filters@3.0.4

# Programmatic Prompts
npm install @ts-dspy/core@0.4.2

# LSP (dev dependency)
npm install -D typescript-language-server@5.1.3
```

## All @anthropic-ai/* Packages

| Package | Version | Purpose |
|---------|---------|---------|
| `@anthropic-ai/sdk` | latest | Core Messages API client |
| `@anthropic-ai/claude-agent-sdk` | 0.2.88 | Headless agent orchestration (spawns Claude CLI) |
| `@anthropic-ai/claude-code` | 2.1.88 | Claude Code CLI (global install, not project dep) |
| `@anthropic-ai/bedrock-sdk` | 0.26.4 | AWS Bedrock variant of the SDK |
| `@anthropic-ai/vertex-sdk` | 0.14.4 | Google Vertex variant of the SDK |
| `@anthropic-ai/foundry-sdk` | 0.2.3 | Anthropic Foundry variant |
| `@anthropic-ai/tokenizer` | 0.0.4 | Token counting |
| `@modelcontextprotocol/sdk` | latest | Official MCP SDK — servers, clients, tools, resources |
| `@anthropic-ai/mcpb` | 2.1.2 | MCP Bundle builder |
| `@anthropic-ai/sandbox-runtime` | 0.0.44 | Security sandbox (seatbelt/bubblewrap) |

## Quick Start: Crawl + Extract + Store

```typescript
import Anthropic from '@anthropic-ai/sdk';
import { PlaywrightCrawler, Dataset } from 'crawlee';
import { BloomFilter } from 'bloom-filters';

const client = new Anthropic();
const bloom = BloomFilter.create(1_000_000, 0.01);

const crawler = new PlaywrightCrawler({
  maxRequestsPerMinute: 60,
  async requestHandler({ request, page, enqueueLinks }) {
    const url = request.url;

    // Bloom filter dedup
    if (bloom.has(url)) return;
    bloom.add(url);

    // Extract page content
    const html = await page.content();
    const title = await page.title();

    // Claude extraction
    const response = await client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 1024,
      thinking: { type: 'adaptive' },
      messages: [{
        role: 'user',
        content: `Extract structured data from this page:\n\nTitle: ${title}\nHTML: ${html.slice(0, 50000)}`
      }],
    });

    // Store result
    await Dataset.pushData({
      url,
      title,
      extracted: response.content,
      timestamp: new Date().toISOString(),
    });

    // Discover more links
    await enqueueLinks();
  },
});

await crawler.run(['https://example.com']);
```

## Further Reading

- `typescript/crawlee-patterns.md` — Crawler types, request queue, storage
- `typescript/sdk-integration.md` — SDK v2 patterns, streaming, tool use
- `typescript/lsp-config.md` — TypeScript LSP setup for code intelligence
- `shared/bloom-filters.md` — Bloom filter API and persistence
- `shared/programmatic-prompts.md` — @ts-dspy/core usage
