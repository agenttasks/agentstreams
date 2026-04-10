---
name: data-pipeline
description: "Data pipeline orchestration, ETL/ELT, streaming, and batch processing with Claude. TRIGGER when: user asks to build data pipelines, ETL/ELT workflows, stream processing, batch jobs, data transformation, workflow orchestration, or schedule recurring data tasks with Claude. Also triggers for CDC (change data capture), schema evolution, or data quality checks. DO NOT TRIGGER for: web crawling (use crawl-ingest), API client building (use api-client), or one-off data transformations."
---

# Data Pipeline: Multi-Language ETL/ELT & Streaming Skill

Build data pipelines with Claude-powered transformation, validation, and orchestration — batch ETL, streaming ELT, CDC, and workflow scheduling across TypeScript, Python, Java, Go, Ruby, C#, PHP, or shell.

## Defaults

- Default to batch processing unless the user specifies streaming
- Use `claude-sonnet-4-6` for data transformation, `claude-opus-4-6` with adaptive thinking for pipeline design decisions
- Use `claude-mythos-preview` for security-sensitive data pipeline auditing (partner-only)
- Always validate data quality between stages (null checks, schema conformance, row counts)
- Default to idempotent operations (safe to re-run)

---

## Language Detection

Before reading setup docs, determine which language stack the user needs:

1. **Look at project files** to infer the language:
   - `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` -> **TypeScript** -- read from `typescript/`
   - `*.py`, `pyproject.toml`, `requirements.txt`, `*.cfg` -> **Python** -- read from `python/`
   - `*.java`, `build.gradle`, `build.gradle.kts`, `pom.xml` -> **Java** -- read from `java/`
   - `*.go`, `go.mod` -> **Go** -- read from `go/`
   - `*.rb`, `Gemfile` -> **Ruby** -- read from `ruby/`
   - `*.cs`, `*.csproj` -> **C#** -- read from `csharp/`
   - `*.php`, `composer.json` -> **PHP** -- read from `php/`
   - Shell scripts, Makefiles, no source files -> **cURL** -- read from `curl/`

2. **If language can't be inferred**: Default to Python (richest data pipeline ecosystem).

---

## Core Capabilities by Language

### Tier 1: Full Stack (SDK + Orchestration + Streaming + Batch + Quality)

| Capability | TypeScript | Python |
|---|---|---|
| **Anthropic SDK** | `@anthropic-ai/sdk` 0.87.0 | `anthropic` 0.87.0 |
| **Orchestration** | Temporal SDK | Prefect 3.4 / Dagster 1.10 |
| **Streaming** | Node.js Streams / Kafka.js | Faust 0.11 / kafka-python |
| **Batch ETL** | Node.js worker_threads | Pandas 2.2 / Polars 1.27 |
| **Data Quality** | Custom + zod | Great Expectations 1.4 / Pandera |
| **Schema** | TypeBox / zod | Pydantic 2.11 / Pandera |

### Tier 2: SDK + Orchestration + Streaming

| Capability | Java | Go | C# |
|---|---|---|---|
| **Anthropic SDK** | `anthropic-sdk-java` | `anthropic-sdk-go` | `anthropic-sdk-csharp` |
| **Orchestration** | Temporal / Airflow (API) | Temporal Go SDK | .NET Aspire |
| **Streaming** | Kafka Streams / Flink | Sarama / confluent-kafka-go | Kafka .NET |
| **Batch ETL** | Spark / custom | concurrent pipelines | SSIS / custom |
| **Data Quality** | Deequ (Spark) | custom | custom |

### Tier 3: SDK + Basic Batch

| Capability | Ruby | PHP | Shell |
|---|---|---|---|
| **Anthropic SDK** | `anthropic-sdk-ruby` | `anthropic-sdk-php` | Raw HTTP |
| **Orchestration** | Sidekiq | Laravel Queue | cron |
| **Batch ETL** | Kiba ETL | Laravel Pipeline | awk/sed/jq |
| **Streaming** | -- | -- | tail -f / pipes |

---

## Pipeline Patterns

### 1. Batch ETL (Extract → Transform → Load)

```
┌──────────┐     ┌──────────────────┐     ┌──────────┐
│  Extract  │────▶│  Transform       │────▶│   Load    │
│  (source) │     │  (Claude + code) │     │  (target) │
└──────────┘     └──────────────────┘     └──────────┘
                        │
                  ┌─────┴─────┐
                  │  Quality   │
                  │  Check     │
                  └───────────┘
```

### 2. Streaming ELT (Extract → Load → Transform)

```
┌──────────┐     ┌──────────┐     ┌──────────────────┐
│  Source    │────▶│   Load    │────▶│  Transform       │
│  (stream) │     │  (raw)    │     │  (Claude + code) │
└──────────┘     └──────────┘     └──────────────────┘
```

### 3. CDC (Change Data Capture)

```
┌──────────┐     ┌──────────┐     ┌──────────────────┐
│  Source DB │────▶│  CDC Log  │────▶│  Apply Changes   │
│  (binlog)  │     │  (stream) │     │  (target)        │
└──────────┘     └──────────┘     └──────────────────┘
```

---

## Claude Integration Points

| Stage | Claude Role | Model |
|-------|------------|-------|
| **Schema inference** | Analyze sample data, generate schema | claude-opus-4-6 |
| **Transformation** | Complex field mapping, normalization | claude-sonnet-4-6 |
| **Validation** | Generate data quality rules from context | claude-sonnet-4-6 |
| **Error handling** | Classify and route failed records | claude-sonnet-4-6 |
| **Documentation** | Generate pipeline docs from code | claude-sonnet-4-6 |
| **Security audit** | Vulnerability scanning of pipeline code | claude-mythos-preview (partner-only) |
