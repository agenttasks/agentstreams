# Pipeline Patterns

## Idempotency

All pipeline stages should be idempotent — safe to re-run without side effects.

### Strategies

| Strategy | How | When to use |
|----------|-----|-------------|
| **Upsert** | INSERT ON CONFLICT UPDATE | Database loads |
| **Partition overwrite** | Delete + insert by partition key | Time-partitioned data |
| **Checkpoint** | Track last processed offset/timestamp | Streaming |
| **Dedup key** | Hash of business keys, skip if exists | Any |

## Backpressure

When producers outpace consumers:

```
Producer → Buffer (bounded) → Consumer
              │
              └─ When full: drop / block / sample
```

### Strategies

- **Block**: Producer waits. Simple, prevents data loss.
- **Drop**: Discard newest. Use when freshness matters more than completeness.
- **Sample**: Process every Nth record. Use for monitoring/analytics pipelines.
- **Spill to disk**: Write overflow to temp storage. Use for batch pipelines.

## Error Handling

### Dead Letter Queue (DLQ)

Records that fail processing go to a DLQ for later inspection:

```
Input → Process ─── success ──▶ Output
            │
            └── failure ──▶ DLQ
                              │
                              └── Retry / Manual review
```

### Retry Tiers

| Tier | Delay | Use case |
|------|-------|----------|
| Immediate | 0 | Transient network errors |
| Short | 1-5s | Rate limits, brief outages |
| Medium | 1-5m | Service restarts |
| Long | 1h+ | Upstream data not ready |

## Data Quality Checks

Run between pipeline stages:

| Check | What | Action on failure |
|-------|------|-------------------|
| **Null rate** | % of nulls per column < threshold | Warn or halt |
| **Row count** | Output rows within expected range | Halt |
| **Schema** | Output matches expected schema | Halt |
| **Freshness** | Data timestamp within SLA | Warn |
| **Uniqueness** | No duplicate primary keys | Halt |
| **Range** | Numeric values within bounds | Warn |
