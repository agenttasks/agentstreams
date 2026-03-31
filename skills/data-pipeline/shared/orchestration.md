# Orchestration Patterns

## DAG (Directed Acyclic Graph)

Pipelines are DAGs — each node is a task, edges are dependencies:

```
    extract_a ──┐
                ├──▶ transform ──▶ load ──▶ quality_check
    extract_b ──┘
```

### Key Properties

- **Idempotent**: Every task safe to re-run
- **Deterministic**: Same input → same output
- **Observable**: Every task emits metrics (duration, row count, errors)

## Scheduling

### Cron-Based

| Pattern | Schedule |
|---------|----------|
| `0 * * * *` | Hourly |
| `0 0 * * *` | Daily midnight |
| `0 6 * * 1` | Weekly Monday 6am |
| `*/5 * * * *` | Every 5 minutes |

### Event-Based

Trigger pipelines on:
- New file in storage (S3/GCS event)
- Database change (CDC)
- API webhook
- Message queue (Kafka/SQS)

## Temporal Workflow Pattern

Best for long-running, stateful pipelines:

```
@workflow.defn
class ETLWorkflow:
    @workflow.run
    async def run(self, config):
        data = await workflow.execute_activity(extract, config.source)
        transformed = await workflow.execute_activity(transform, data)
        await workflow.execute_activity(load, transformed, config.target)
        await workflow.execute_activity(quality_check, config.target)
```

Benefits:
- Automatic retry on failure
- Durable execution (survives process restarts)
- Built-in timeout handling
- Workflow versioning for zero-downtime deploys

## Prefect / Dagster Pattern

Best for data-team workflows:

```python
@flow
def etl_pipeline(source: str, target: str):
    raw = extract(source)
    clean = transform(raw)
    load(clean, target)
    validate(target)
```

Benefits:
- Python-native, low ceremony
- Built-in UI for monitoring
- Data lineage tracking
- Asset-based (Dagster) or task-based (Prefect)
