---
name: crawl-ingest
description: "Web crawling, deduplication, and data ingestion using Anthropic SDKs. TRIGGER when: user asks to crawl websites, build web scrapers, deduplicate URLs with bloom filters, ingest data into a warehouse, or use Crawlee/Scrapy/crawler4j with Claude. Also triggers for programmatic prompts (DSPy), LSP code intelligence setup, or multi-language SDK scaffolding. DO NOT TRIGGER for: general API usage (use claude-api), simple HTTP requests, or static file processing."
---

# Crawl-Ingest: Multi-Language Web Crawling & Data Ingestion Skill

Build web crawlers with bloom filter deduplication, Anthropic SDK integration, programmatic prompts, and LSP code intelligence — in TypeScript, Python, Java, Go, Ruby, C#, PHP, or cURL.

## Defaults

- Default to local storage (SQLite, filesystem) until the user explicitly requests cloud DW
- Use `claude-opus-4-6` with adaptive thinking for crawl strategy decisions
- Use `claude-mythos-preview` for security-focused crawl analysis (partner-only)
- Always enable bloom filter deduplication by default (configurable false positive rate: 0.01)
- Respect robots.txt and implement polite crawling (1-2 req/sec default)

---

## Language Detection

Before reading setup docs, determine which language stack the user needs:

1. **Look at project files** to infer the language:
   - `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` -> **TypeScript** -- read from `typescript/`
   - `*.py`, `pyproject.toml`, `requirements.txt`, `scrapy.cfg` -> **Python** -- read from `python/`
   - `*.java`, `build.gradle`, `build.gradle.kts`, `pom.xml` -> **Java** -- read from `java/`
   - `*.go`, `go.mod` -> **Go** -- read from `go/`
   - `*.rb`, `Gemfile` -> **Ruby** -- read from `ruby/`
   - `*.cs`, `*.csproj` -> **C#** -- read from `csharp/`
   - `*.php`, `composer.json` -> **PHP** -- read from `php/`
   - Shell scripts, Makefiles, no source files -> **cURL** -- read from `curl/`

2. **If multiple languages detected**: Check which language the user's current file relates to. If ambiguous, ask.

3. **If language can't be inferred**: Default to Python (most mature ecosystem for crawling + DSPy).

---

## Core Capabilities by Language

### Tier 1: Full Stack (SDK + Agent SDK + MCP + Crawling + Bloom + LSP + DSPy + Evals)

| Capability | TypeScript | Python |
|---|---|---|
| **Anthropic SDK** | `anthropic-sdk-typescript` | `anthropic-sdk-python` |
| **Agent SDK** | `claude-agent-sdk-typescript` 0.2.88 | `claude-agent-sdk-python` 0.1.53 |
| **MCP SDK** | `@modelcontextprotocol/sdk` 1.29.0 | `mcp` 1.26.0 |
| **Web Crawler** | Crawlee 3.16.0 | Scrapy 2.14.2 |
| **Bloom Filter** | `bloom-filters` 3.0.4 | `pybloom-live` 4.0.0 |
| **LSP** | `typescript-language-server` 5.1.3 | `python-lsp-server` 1.14.0 |
| **Programmatic Prompts** | `@ts-dspy/core` 0.4.2 | `dspy` 3.1.3 |
| **Evals** | promptfoo 0.121.3 (native TS) | deepeval 3.9.4 + promptfoo |

### Tier 2: SDK + MCP + Crawling + Bloom + LSP (No Agent SDK, limited DSPy)

| Capability | Java/Kotlin | Go | C# |
|---|---|---|---|
| **Anthropic SDK** | `anthropic-sdk-java` Kotlin | `anthropic-sdk-go` | `anthropic-sdk-csharp` |
| **MCP SDK** | `mcp/java-sdk` + `mcp/kotlin-sdk` | `mcp/go-sdk` | `mcp/csharp-sdk` |
| **Web Crawler** | crawler4j + JSoup | Colly v2 + goquery | Abot + AngleSharp |
| **Bloom Filter** | Guava `BloomFilter` | `bits-and-blooms/bloom` | `BloomFilter.NetCore` |
| **LSP** | Eclipse JDT LS + LSP4J | gopls | OmniSharp |
| **Prompts** | LangChain4j (templates only) | -- | Semantic Kernel (templates) |
| **Evals** | promptfoo (CLI) | promptfoo (CLI) | AgentEval (.NET) + promptfoo |

### Tier 3: SDK + MCP + Basic Crawling

| Capability | Ruby | PHP | cURL |
|---|---|---|---|
| **Anthropic SDK** | `anthropic-sdk-ruby` | `anthropic-sdk-php` | Raw HTTP |
| **MCP SDK** | `mcp/ruby-sdk` | `mcp/php-sdk` | N/A |
| **Web Crawler** | Mechanize + Nokogiri | Symfony HttpClient + DomCrawler | wget / curl |
| **Bloom Filter** | `bloomer` | `pleonasm/bloom-filter` | sort -u / sqlite |
| **LSP** | Solargraph | Phpactor | N/A |
| **Evals** | promptfoo (CLI) | promptfoo (CLI) | promptfoo (CLI) |

See `references/package-matrix.md` for the full equivalence table with scores.

---

## Workflow: Problem-First Approach

When the user describes a crawling/ingestion problem:

### Phase 1: Crawl Setup
1. Read the language-specific `README.md` for installation
2. Read `shared/crawl-patterns.md` for crawling strategy
3. Set up the crawler with bloom filter dedup (read `shared/bloom-filters.md`)

### Phase 2: SDK Integration
1. Read the language-specific `sdk-integration.md` for Claude API patterns
2. Configure content extraction and classification using the SDK
3. Set up programmatic prompts if complex extraction needed (read `shared/programmatic-prompts.md`)

### Phase 3: Data Storage
1. Start with local storage (SQLite/filesystem)
2. When ready to scale, read `shared/data-warehouse.md` for cloud switchover
3. Apply Kimball dimensional modeling for warehouse schema design

### Phase 4: Code Intelligence
1. Read the language-specific `lsp-config.md` for LSP setup
2. Configure LSP for navigation, completions, and diagnostics in the crawl codebase

### Phase 5: Evals
1. Read `shared/evals.md` for the eval framework landscape
2. Set up promptfoo (all languages) for extraction quality, robustness, and safety evals
3. For Python: add deepeval metrics (faithfulness, hallucination, GEval)
4. Run red-teaming: `promptfoo redteam generate --purpose "web content extraction"`
5. Integrate evals into CI/CD with promptfoo GitHub Action

---

## CRITICAL: Auth

**Never use `ANTHROPIC_API_KEY`** in this workspace. All auth flows through `CLAUDE_CODE_OAUTH_TOKEN`.

For programmatic SDK usage in scripts, use:
- TypeScript: `new Anthropic()` (reads env automatically)
- Python: `anthropic.Anthropic()` (reads env automatically)
- Java: `AnthropicClient.builder().build()` (reads env automatically)
- Go: `anthropic.NewClient()` (reads env automatically)
- Ruby: `Anthropic::Client.new` (reads env automatically)
- C#: `new AnthropicClient()` (reads env automatically)
- PHP: `Anthropic::client()` (reads env automatically)
- cURL: `-H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN"`

---

## Cross-References

- For Claude API details beyond crawl-ingest scope: use the `claude-api` skill
- Kimball taxonomy: `agentstreams/taxonomy/kimball-dw-toolkit.md` (5,355 lines)
- Platform API taxonomy: `agentstreams/taxonomy/live-sources.md` (1,240+ lines)
