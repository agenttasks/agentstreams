# AgentStreams Ontology — Unified Data Architecture

Inspired by [Netflix UDA](https://netflixtechblog.com/uda-unified-data-architecture-6a6aee261d8d): **Model Once, Represent Everywhere**.

## Architecture

```
agentstreams.ttl          ← Canonical ontology (Model Once)
       │
       ├── schema.sql     ← Neon Postgres DDL (Represent: relational + pg_graphql)
       ├── mappings.ttl   ← Ontology → physical table/column mappings
       └── atlas-chart/   ← Atlas PNG renderer (Represent: time-series visualization)
```

## Files

| File | Purpose |
|------|---------|
| `agentstreams.ttl` | RDF/TTL ontology — classes, properties, instances for skills, models, SDKs, metrics, resources |
| `mappings.ttl` | UDA mappings linking ontology concepts to Neon Postgres tables/columns |
| `schema.sql` | Postgres DDL with seed data — enables pg_graphql to auto-generate GraphQL API |

## How It Works

1. **Ontology** (`agentstreams.ttl`) defines the domain: `Skill`, `Model`, `SDK`, `Metric`, `Resource`, `Pipeline`
2. **Schema** (`schema.sql`) creates Postgres tables that mirror these classes, with seed data
3. **pg_graphql** (Postgres extension) introspects the schema and auto-generates a GraphQL API
4. **Mappings** (`mappings.ttl`) trace lineage from concept → table → column

## Neon Project

| Property | Value |
|----------|-------|
| **Project** | `agentstreams` |
| **Project ID** | `calm-paper-82059121` |
| **Branch** | `main` (ID: `br-shiny-haze-ajzux7we`) |
| **Database** | `neondb` |
| **Region** | `us-east-2` |

### Setup

Schema is deployed. To re-deploy or update:

```sql
-- Run via Neon MCP or psql
\i ontology/schema.sql
```

### pg_graphql Queries

```sql
-- List all skills
SELECT graphql.resolve($$ {
  skillsCollection { edges { node { name description trigger_pattern } } }
} $$);

-- List models with capabilities
SELECT graphql.resolve($$ {
  modelsCollection { edges { node { model_id family supports_thinking supports_tool_use } } }
} $$);

-- List SDKs with constructor patterns
SELECT graphql.resolve($$ {
  sdksCollection { edges { node { label language_id constructor_pattern github_stars } } }
} $$);

-- List metrics
SELECT graphql.resolve($$ {
  metricsCollection { edges { node { name type unit dimensions } } }
} $$);
```

## Metrics (Atlas/Spectator Pattern)

Metrics follow Netflix Atlas dimensional model:
- **Name**: dot-separated hierarchy (`agentstreams.api.requests`)
- **Type**: counter, timer, gauge, distribution_summary
- **Dimensions**: tag key-value pairs for slicing (`model=claude-opus-4-6`, `skill=crawl-ingest`)
- **Values**: stored in `metric_values` fact table with JSONB tags

## Atlas Chart Rendering

The `atlas-chart/` project reads `metric_values` from Neon and renders PNG charts:

```
metric_values (Neon) → JDBC → ArrayTimeSeq → TimeSeries → GraphDef → PNG
```

- Uses Netflix `atlas-chart` library (`DefaultGraphEngine.write()`)
- No Atlas server needed — standalone JVM rendering
- 7 metrics × 33 series, trailing 2 weeks at 5-minute step intervals

```bash
cd atlas-chart && ./render-charts.sh
```

## Claude Platform Resources

The ontology tracks Claude platform ingestion resources:
- `llms.txt` — 620-page documentation index
- `llms-full.txt` — complete docs in single file
- API Primer — concise API guide for LLM ingestion
- Model Cards — per-model safety and capability documentation
