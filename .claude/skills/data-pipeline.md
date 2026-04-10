---
name: data-pipeline
description: "Data pipeline orchestration, ETL/ELT, streaming, and batch processing with Claude"
trigger: "user asks to build data pipelines, ETL/ELT workflows, stream processing, batch jobs, data transformation, workflow orchestration, or CDC"
context: fork
---

Read `skills/data-pipeline/SKILL.md` for the full skill definition, then follow the language detection rules to load the appropriate language README.

## UDA Programmatic Tools (src/)

For Python pipelines, use the unified src/ modules:

| Module | Class/Function | Purpose |
|--------|---------------|---------|
| `src/neon_db.py` | `connection_pool`, `upsert_pipeline` | Neon Postgres data access |
| `src/neon_db.py` | `record_metric`, `enqueue_task` | Metrics and task queuing |
| `src/projections.py` | `generate_all_projections` | UDA schema projections (Avro, GraphQL) |
| `src/embeddings.py` | `EmbeddingPipeline` | Vector embedding pipeline |
| `src/agent_tasks.py` | `AgentRunner`, `TaskSpec` | Agent SDK v2 task orchestration |

See `.claude/subagents/uda-projector.md` for ontology projection instructions.
