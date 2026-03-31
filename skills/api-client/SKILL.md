---
name: api-client
description: "API client generation, testing, and integration using Anthropic SDKs. TRIGGER when: user asks to build API clients, generate SDKs from OpenAPI specs, test REST/GraphQL APIs, mock API responses, handle auth flows (OAuth, API keys), implement retry/backoff, or build API wrappers with Claude. Also triggers for API documentation generation or contract testing. DO NOT TRIGGER for: web crawling (use crawl-ingest), simple curl one-liners, or static file processing."
---

# API Client: Multi-Language API Client Generation & Testing Skill

Build type-safe API clients from OpenAPI/GraphQL schemas, test APIs with Claude-powered assertion generation, and implement production-ready patterns (retry, auth, rate limiting) — in TypeScript, Python, Java, Go, Ruby, C#, PHP, or cURL.

## Defaults

- Generate clients from OpenAPI 3.x specs when available
- Use `claude-sonnet-4-6` for code generation, `claude-opus-4-6` with adaptive thinking for architecture decisions
- Always include retry with exponential backoff (3 retries, 1s base)
- Generate type-safe request/response models from schemas
- Include rate limiting middleware by default

---

## Language Detection

Before reading setup docs, determine which language stack the user needs:

1. **Look at project files** to infer the language:
   - `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` -> **TypeScript** -- read from `typescript/`
   - `*.py`, `pyproject.toml`, `requirements.txt` -> **Python** -- read from `python/`
   - `*.java`, `build.gradle`, `build.gradle.kts`, `pom.xml` -> **Java** -- read from `java/`
   - `*.go`, `go.mod` -> **Go** -- read from `go/`
   - `*.rb`, `Gemfile` -> **Ruby** -- read from `ruby/`
   - `*.cs`, `*.csproj` -> **C#** -- read from `csharp/`
   - `*.php`, `composer.json` -> **PHP** -- read from `php/`
   - Shell scripts, Makefiles, no source files -> **cURL** -- read from `curl/`

2. **If multiple languages detected**: Check which language the user's current file relates to. If ambiguous, ask.

3. **If language can't be inferred**: Default to TypeScript (strongest HTTP client ecosystem).

---

## Core Capabilities by Language

### Tier 1: Full Stack (SDK + OpenAPI + Testing + Auth + Rate Limiting)

| Capability | TypeScript | Python |
|---|---|---|
| **Anthropic SDK** | `anthropic-sdk-typescript` (1.8k★) | `anthropic-sdk-python` (3.1k★) |
| **HTTP Client** | `axios` 1.9 / native `fetch` | `httpx` 0.28 / `aiohttp` 3.11 |
| **OpenAPI Codegen** | `openapi-typescript` 7.8 | `openapi-python-client` 0.24 |
| **API Testing** | `vitest` 3.1 + `msw` 2.7 | `pytest` 8.4 + `respx` 0.22 |
| **Auth** | `openid-client` 6.4 | `authlib` 1.5 |
| **Rate Limiting** | `bottleneck` 2.19 | `ratelimit` 2.2 |
| **Validation** | `zod` 3.24 | `pydantic` 2.11 |

### Tier 2: SDK + OpenAPI + Testing + Auth

| Capability | Java/Kotlin | Go | C# |
|---|---|---|---|
| **Anthropic SDK** | `anthropic-sdk-java` (271★) | `anthropic-sdk-go` (943★) | `anthropic-sdk-csharp` (212★) |
| **HTTP Client** | OkHttp 4.12 / Retrofit 2.11 | `net/http` + `resty` v2 | `HttpClient` / RestSharp 112 |
| **OpenAPI Codegen** | openapi-generator (Java) | oapi-codegen 2.4 | NSwag 14 / Kiota |
| **API Testing** | JUnit 5 + WireMock 3.12 | `net/http/httptest` | xUnit + WireMock.Net 1.6 |
| **Auth** | Spring Security OAuth2 | `golang.org/x/oauth2` | `Microsoft.Identity.Client` |
| **Validation** | Jakarta Validation 3.1 | `go-playground/validator` | FluentValidation 11 |

### Tier 3: SDK + Basic HTTP + Testing

| Capability | Ruby | PHP | cURL |
|---|---|---|---|
| **Anthropic SDK** | `anthropic-sdk-ruby` (312★) | `anthropic-sdk-php` (128★) | Raw HTTP |
| **HTTP Client** | Faraday 2.12 | Guzzle 7.9 | curl |
| **OpenAPI Codegen** | openapi-generator (Ruby) | openapi-generator (PHP) | N/A |
| **API Testing** | RSpec 3.13 + WebMock 3.24 | PHPUnit 11 + MockHandler | Shell assertions |
| **Auth** | OmniAuth 2.1 | `league/oauth2-client` 2.8 | `-H "Authorization: ..."` |

---

## Workflow

### 1. Schema-First Client Generation

```
OpenAPI/GraphQL Schema
        │
        ▼
┌─────────────────┐
│  Claude Analyzes │ ← Understands API structure, auth, pagination
│  Schema          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate Client │ ← Type-safe models, endpoints, auth handlers
│  Code            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate Tests  │ ← Mock responses, edge cases, error scenarios
│                  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Document API    │ ← Usage examples, auth setup, error handling
│                  │
└─────────────────┘
```

### 2. Exploration-First (No Schema)

```
API Base URL / Docs
        │
        ▼
┌─────────────────┐
│  Claude Explores │ ← Probes endpoints, infers types from responses
│  API             │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Infer Schema    │ ← Generates OpenAPI spec from observed behavior
│                  │
└────────┬────────┘
         │
         ▼
  (continues as schema-first flow)
```

---

## Common Patterns

### Retry with Exponential Backoff

All generated clients include retry logic:
- 3 retries by default
- Exponential backoff: 1s, 2s, 4s
- Retry on: 429 (rate limit), 500, 502, 503, 504
- Respect `Retry-After` header when present

### Rate Limiting

- Token bucket or sliding window
- Configurable requests per second/minute
- Queue overflow strategy: drop or backpressure

### Auth Patterns

- API Key (header, query param, or cookie)
- OAuth 2.0 (authorization code, client credentials, refresh token)
- JWT bearer tokens
- Mutual TLS (mTLS)

### Error Handling

- Typed error responses per status code
- Distinguish retryable vs terminal errors
- Structured error logging with request context
