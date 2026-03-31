# Atlas Chart Renderer

Renders PNG charts from Neon `metric_values` data using Netflix's [atlas-chart](https://github.com/Netflix/atlas) library.

## Data Flow

```
metric_values (Neon) → JDBC → ArrayTimeSeq → TimeSeries → GraphDef → DefaultGraphEngine → PNG
```

## Quick Start

```bash
# Ensure Java 17+ is installed
java -version

# Render all 7 metric charts
./render-charts.sh

# Custom output directory
./render-charts.sh /path/to/output
```

## Charts

| File | Metric | Series | Type |
|------|--------|--------|------|
| `agentstreams-api-requests.png` | API request rates | 5 | counter |
| `agentstreams-api-tokens.png` | Token usage rates | 6 | counter |
| `agentstreams-api-cost.png` | Cost per request | 3 | distribution_summary |
| `agentstreams-pipeline-duration.png` | Pipeline stage duration | 8 | timer |
| `agentstreams-crawl-pages.png` | Pages crawled | 5 | counter |
| `agentstreams-crawl-dedup.png` | Bloom filter FPR | 3 | gauge |
| `agentstreams-eval-score.png` | Eval pass rate | 3 | gauge |

## Atlas Data Model Alignment

```
Neon metric_values          Atlas Model
─────────────────           ───────────
recorded_at (5min step) →   ArrayTimeSeq(DsType, startMillis, stepMillis=300000, Array[Double])
value                   →   data array values
tags (JSONB)            →   TimeSeries tag Map[String,String]
metrics.type            →   DsType.Rate (counter/timer) or DsType.Gauge
```

## Configuration

Set `NEON_JDBC_URL` to override the default Neon connection:

```bash
export NEON_JDBC_URL="jdbc:postgresql://host/db?user=...&password=...&sslmode=require"
./render-charts.sh
```

## Dependencies

- `com.netflix.atlas_v1:atlas-chart_2.13:1.7.0-rc.22` — chart rendering (DefaultGraphEngine)
- `org.postgresql:postgresql:42.7.4` — JDBC driver for Neon
- `org.scala-lang:scala-library:2.13.15` — Scala runtime
