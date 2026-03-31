# Python Stack Setup

## Installation (uv)

```bash
uv init data-pipeline && cd data-pipeline

# Core Anthropic
uv add anthropic

# Orchestration (pick one)
uv add prefect==3.4.5
# uv add dagster==1.10.7 dagster-webserver==1.10.7

# Data Processing
uv add polars==1.27.0          # Fast DataFrames (Rust-backed)
uv add pandas==2.2.3           # Classic DataFrames
uv add pyarrow==19.0.1         # Columnar format, Parquet I/O

# Streaming
uv add confluent-kafka==2.8.0  # Kafka client
uv add faust-streaming==0.11.0 # Stream processing

# Data Quality
uv add great-expectations==1.4.1
uv add pandera==0.22.1         # DataFrame schema validation

# Testing
uv add --dev pytest==8.4.0
uv add --dev pytest-asyncio==0.25.3
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | 0.86.0 | Official Python SDK |
| `prefect` | 3.4.5 | Workflow orchestration — flows, tasks, scheduling, UI |
| `polars` | 1.27.0 | Fast DataFrames — lazy evaluation, streaming, parallel |
| `pyarrow` | 19.0.1 | Columnar format — Parquet read/write, zero-copy |
| `confluent-kafka` | 2.8.0 | Kafka producer/consumer — high throughput |
| `great-expectations` | 1.4.1 | Data quality — expectations, validation, docs |
| `pandera` | 0.22.1 | DataFrame schema validation — type checking, constraints |

## Quick Start: Prefect + Claude + Polars

```python
import anthropic
import polars as pl
from prefect import flow, task

client = anthropic.Anthropic()


@task(retries=3, retry_delay_seconds=10)
def extract(source_path: str) -> pl.DataFrame:
    """Extract data from CSV/Parquet."""
    if source_path.endswith(".parquet"):
        return pl.read_parquet(source_path)
    return pl.read_csv(source_path)


@task
def transform(df: pl.DataFrame) -> pl.DataFrame:
    """Clean and transform data."""
    return (
        df.drop_nulls(subset=["id"])
        .with_columns(
            pl.col("name").str.strip_chars().alias("name"),
            pl.col("created_at").cast(pl.Datetime).alias("created_at"),
        )
        .unique(subset=["id"])
    )


@task
def enrich_with_claude(df: pl.DataFrame, column: str) -> pl.DataFrame:
    """Use Claude to classify or enrich a text column."""
    texts = df[column].to_list()

    # Batch for efficiency
    batch_size = 50
    categories = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        result = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Classify each item into a category. "
                        f"Return one category per line, no numbering.\n\n"
                        + "\n".join(batch)
                    ),
                }
            ],
        )
        batch_categories = result.content[0].text.strip().split("\n")
        categories.extend(batch_categories[: len(batch)])

    return df.with_columns(pl.Series("category", categories[: len(df)]))


@task
def quality_check(df: pl.DataFrame) -> None:
    """Validate data quality."""
    assert df.height > 0, "DataFrame is empty"
    assert df["id"].null_count() == 0, "Null IDs found"
    assert df["id"].is_unique().all(), "Duplicate IDs found"


@task
def load(df: pl.DataFrame, target_path: str) -> None:
    """Load to Parquet."""
    df.write_parquet(target_path)


@flow(name="etl-pipeline")
def etl_pipeline(source: str, target: str, enrich_col: str | None = None):
    raw = extract(source)
    clean = transform(raw)
    if enrich_col:
        clean = enrich_with_claude(clean, enrich_col)
    quality_check(clean)
    load(clean, target)
    return {"rows": clean.height, "columns": clean.width}
```

## Further Reading

- `shared/pipeline-patterns.md` — Idempotency, backpressure, DLQ, data quality
- `shared/orchestration.md` — DAGs, scheduling, Temporal/Prefect patterns
