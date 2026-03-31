# Cross-Language Package Equivalence Matrix

## Anthropic SDK (github.com/anthropics)

| Capability | TypeScript | Python | Java/Kotlin | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Messages API** | `anthropic-sdk-typescript` (1.8k★) | `anthropic-sdk-python` (3.1k★) | `anthropic-sdk-java` Kotlin (271★) | `anthropic-sdk-go` (943★) | `anthropic-sdk-ruby` (312★) | `anthropic-sdk-csharp` (212★) | `anthropic-sdk-php` (128★) | Raw HTTP |
| **Agent SDK** | `claude-agent-sdk-typescript` (1.2k★) | `claude-agent-sdk-python` (6k★) | -- | -- | -- | -- | -- | -- |
| **Bedrock** | `@anthropic-ai/bedrock-sdk` | via `anthropic` | via AWS SDK | via AWS SDK | -- | -- | -- | -- |
| **Vertex** | `@anthropic-ai/vertex-sdk` | via `anthropic` | via Google SDK | via Google SDK | -- | -- | -- | -- |
| **Tokenizer** | `@anthropic-ai/tokenizer` | -- | -- | -- | -- | -- | -- | -- |

## MCP SDK (github.com/modelcontextprotocol)

| Language | Repo | Stars | Maintained by |
|---|---|---|---|
| **Python** | `python-sdk` | 22k★ | Anthropic |
| **TypeScript** | `typescript-sdk` | 12k★ | Anthropic |
| **Go** | `go-sdk` | 4.3k★ | Google |
| **C#** | `csharp-sdk` | 4.2k★ | Microsoft |
| **Java** | `java-sdk` | 3.3k★ | Spring AI |
| **Rust** | `rust-sdk` | 3.2k★ | Community |
| **Kotlin** | `kotlin-sdk` | 1.3k★ | JetBrains |
| **Swift** | `swift-sdk` | 1.3k★ | Community |
| **Ruby** | `ruby-sdk` | 758★ | Community |
| **PHP** | `php-sdk` | 125★ | PHP Foundation |

Also: `ext-apps` (2k★) — MCP Apps protocol for embedded AI chatbot UIs.

## Web Crawling

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Framework** | Crawlee 3.16.0 | Scrapy 2.14.2 | crawler4j 4.4.0 | Colly v2 | Mechanize | Abot 5.1.0 | Symfony HttpClient | wget |
| **HTML Parser** | Cheerio (built-in) | Scrapy Selectors | JSoup 1.17.2 | goquery | Nokogiri | AngleSharp 1.1.2 | DomCrawler | pup |
| **JS Rendering** | PlaywrightCrawler | scrapy-playwright | -- | -- | -- | -- | -- | -- |
| **Robots.txt** | Built-in | Built-in | Built-in | Built-in | Built-in | Built-in | Manual | wget respects |
| **Async** | Native | Twisted reactor | Thread pool | Goroutines | Threads | async/await | -- | GNU Parallel |

## Bloom Filters

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Package** | `bloom-filters` 3.0.4 | `pybloom-live` 4.0.0 | Guava 33.x | `bits-and-blooms/bloom` v3 | `bloomer` | `BloomFilter.NetCore` | `pleonasm/bloom-filter` | sort -u / sqlite |
| **Scalable** | CuckooFilter | ScalableBloomFilter | Apache Commons | -- | Scalable mode | -- | -- | -- |
| **Persistence** | JSON | pickle | writeTo/readFrom | WriteTo/ReadFrom | Marshal | Serialize | -- | File-based |

## LSP / Code Intelligence

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP |
|---|---|---|---|---|---|---|---|
| **Server** | typescript-language-server 5.1.3 | python-lsp-server 1.14.0 | Eclipse JDT LS | gopls | Solargraph | OmniSharp | Phpactor |
| **Protocol Lib** | vscode-languageserver | pygls | LSP4J 0.23.1 | (built-in) | -- | -- | -- |
| **Type Checking** | TypeScript compiler | pylsp-mypy | JDT (built-in) | go vet | Sorbet | Roslyn | PHPStan |
| **Linting** | ESLint | python-lsp-ruff | Checkstyle | golangci-lint | RuboCop | Roslyn | PHP_CodeSniffer |

## Programmatic Prompts

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Framework** | `@ts-dspy/core` 0.4.2 | `dspy` 3.1.3 | LangChain4j 1.0 | -- | -- | Semantic Kernel | -- | -- |
| **Signatures** | Yes | Yes | Prompt templates | -- | -- | Prompt templates | -- | -- |
| **Optimizers** | Limited | Full (MIPROv2) | No | -- | -- | No | -- | -- |
| **Claude Support** | Via provider | Native | Via adapter | -- | -- | Via adapter | -- | -- |

## Evals

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Universal** | promptfoo 0.121.3 | promptfoo (CLI) | promptfoo (CLI) | promptfoo (CLI) | promptfoo (CLI) | promptfoo (CLI) | promptfoo (CLI) | promptfoo (CLI) |
| **Native** | promptfoo (TS-native) | deepeval 3.9.4 | -- | -- | -- | AgentEval (.NET) | -- | -- |
| **RAG-specific** | -- | ragas 0.4.3 | -- | -- | -- | -- | -- | -- |
| **Gov/Research** | -- | inspect-ai 0.3.201 | -- | -- | -- | -- | -- | -- |
| **Observability** | -- | arize-phoenix 13.20.0 | -- | -- | -- | -- | -- | -- |
| **Red-teaming** | promptfoo redteam | promptfoo redteam | promptfoo redteam | promptfoo redteam | promptfoo redteam | promptfoo redteam | promptfoo redteam | promptfoo redteam |
| **Anthropic Safety** | anthropics/evals (JSONL datasets — sycophancy, AI risk, persona, bias) | same | same | same | same | same | same | same |

## Feature Completeness Score

Now scored across 7 dimensions (/35 total). SDK score includes Anthropic SDK + Agent SDK + MCP SDK availability.

| Language | SDK+Agent+MCP | Crawling | Bloom | LSP | Prompts | Evals | **Total** |
|---|---|---|---|---|---|---|---|
| **Python** | 5/5 (SDK+Agent+MCP) | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | **30/30** |
| **TypeScript** | 5/5 (SDK+Agent+MCP) | 5/5 | 4/5 | 5/5 | 3/5 | 5/5 | **27/30** |
| **Java/Kotlin** | 4/5 (SDK+MCP+MCP-Kotlin) | 4/5 | 5/5 | 4/5 | 2/5 | 3/5 | **22/30** |
| **Go** | 4/5 (SDK+MCP) | 4/5 | 4/5 | 5/5 | 0/5 | 3/5 | **20/30** |
| **C#** | 4/5 (SDK+MCP) | 3/5 | 3/5 | 4/5 | 1/5 | 4/5 | **19/30** |
| **Ruby** | 4/5 (SDK+MCP) | 3/5 | 3/5 | 3/5 | 0/5 | 3/5 | **16/30** |
| **PHP** | 4/5 (SDK+MCP) | 3/5 | 2/5 | 3/5 | 0/5 | 3/5 | **15/30** |
| **cURL** | 2/5 (Raw HTTP) | 2/5 | 1/5 | 0/5 | 0/5 | 3/5 | **8/30** |

**Key change:** MCP SDK availability across all 7 languages (maintained by Anthropic, Google, Microsoft, JetBrains, Spring AI, PHP Foundation) lifts Tier 2/3 SDK scores from 3/5 to 4/5. Agent SDK remains TypeScript+Python only.
