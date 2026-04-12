---
name: neon-api
description: "Start and query the AgentStreams FastAPI REST API over Neon Postgres. TRIGGER when: user asks to start the data API server, query metrics/tasks/agents via HTTP, or build integrations against the REST endpoints. Also triggers for curl testing API endpoints. DO NOT TRIGGER for: TUI dashboard (use neon-dashboard), raw SQL (use sql-queries), or team setup (use neon-team-setup)."
argument-hint: "[endpoint: health|metrics|tasks|agents|skills|models|pipelines|search]"
---

# /neon-api - FastAPI Data API for Neon Postgres

> Connector: `~~data warehouse` = Neon Postgres 18 (via `NEON_DATABASE_URL` env var).
> Pattern: SRE Incident Response Agent cookbook (FastAPI + Postgres health checks, OpenAPI tags).

Thin REST layer over `src/neon_db.py` async functions. Uses the existing psycopg 3.2+ connection pattern -- one connection per request via `connection_pool()`. No SQLAlchemy.

## Usage

```
/neon-api [endpoint]
```

Start the server:

```bash
make dev-api                                    # via Makefile (with --reload)
uv run uvicorn src.api:app --reload --port 8000 # explicit
```

## Endpoints

### Health

```bash
curl http://localhost:8000/api/health
# {"status": "ok", "neon_branch": "main", "skill_count": 167, "pg_version": "PostgreSQL 18..."}
```

### Metrics

```bash
# List all metric definitions
curl http://localhost:8000/api/metrics

# Query time-series values for a metric (last 24h, up to 1000 points)
curl "http://localhost:8000/api/metrics/api.latency/values?hours=24&limit=1000"

# Statistical summary (count, avg, min, max, p50, p99)
curl "http://localhost:8000/api/metrics/api.latency/summary?hours=168&group_by=model"
```

### Tasks

```bash
# List tasks with optional filters
curl "http://localhost:8000/api/tasks?status=queued&type=code&limit=20"

# Create a new task
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"queue_name": "crawl", "task_type": "knowledge_work", "priority": 1}'

# Task queue statistics (last 24h)
curl "http://localhost:8000/api/tasks/stats?hours=24"
```

### Agents

```bash
# List all agent manifests
curl http://localhost:8000/api/agents

# Get a specific agent
curl http://localhost:8000/api/agents/code-generator
# Returns 404 if not found
```

### Skills, Models, Pipelines

```bash
curl http://localhost:8000/api/skills          # Registered skills from DB
curl http://localhost:8000/api/skills/registry  # Skill catalog with category + agent routing
curl http://localhost:8000/api/models           # Claude model registry
curl http://localhost:8000/api/pipelines        # Pipeline definitions
```

### Resource Search

```bash
# Fuzzy search using pg_trgm trigram similarity
curl "http://localhost:8000/api/resources/search?q=crawler&table=resources&column=label&threshold=0.3&limit=10"
# Allowed tables: resources, skills, crawl_pages
# Allowed columns: label, name, title, description, url
```

## Pydantic Models

All response models use `ConfigDict(from_attributes=True)` for direct mapping from psycopg row dicts:

| Model | Fields |
|-------|--------|
| `MetricOut` | name, type, unit, dimensions, description |
| `MetricValueOut` | recorded_at, value, tags |
| `MetricSummaryOut` | group_key, count, avg, min, max, p50, p99 |
| `TaskOut` | id, queue_name, type, status, priority, skill_name, model_id, plugin, attempts, created_at, started_at, completed_at |
| `TaskCreateIn` | queue_name, task_type, skill_name, model_id, plugin, task_input, config, priority |
| `TaskStatsOut` | status, type, queue_name, count, avg_duration_s |
| `AgentManifestOut` | name, model_id, allowed_tools, denied_tools, description |
| `SkillOut` | name, description, trigger_pattern |
| `SkillRegistryOut` | name, category, agent |
| `ModelOut` | model_id, family, label, supports_thinking, supports_tool_use, supports_vision |
| `PipelineOut` | id, name, skill_name, model_id, config, status, created_at, updated_at |

## Architecture

- **Data layer**: `src/neon_db.py` -- 10+ async query functions shared with TUI
- **Models**: `src/models.py` -- Pydantic v2 request/response schemas
- **CORS**: All origins allowed (team-internal use)
- **Lifespan**: Validates database connectivity on startup via `SELECT 1`
- **SQL injection protection**: Allowlisted tables/columns for fuzzy search endpoint

## Extending

To add a new endpoint:

1. Add a query function to `src/neon_db.py`:
   ```python
   async def my_query(conn, *, param: str) -> list[dict]:
       rows = await (await conn.execute("SELECT ... WHERE col = %s", (param,))).fetchall()
       return [dict(r._mapping) for r in rows]
   ```

2. Add a Pydantic model to `src/models.py`:
   ```python
   class MyOut(BaseModel):
       model_config = ConfigDict(from_attributes=True)
       field: str
   ```

3. Add the endpoint to `src/api.py`:
   ```python
   @app.get("/api/my-resource", response_model=list[MyOut], tags=["my-tag"])
   async def get_my_resource():
       async with connection_pool() as conn:
           return await my_query(conn)
   ```

4. Add a test to `tests/test_api.py` mocking the query function.

## Implementation

| File | Purpose |
|------|---------|
| `src/api.py` | FastAPI application with 14 endpoints |
| `src/neon_db.py` | Shared async query functions |
| `src/models.py` | Pydantic v2 request/response models |
| `tests/test_api.py` | httpx.AsyncClient tests with mocked DB |
| `Makefile` | `make dev-api` target |

## Cross-References

- For terminal dashboard over the same data: use the `neon-dashboard` skill
- For team branch setup: use the `neon-team-setup` skill
- For SQL query patterns: use the `sql-queries` skill
- For data visualization: use the `build-dashboard` or `data-visualization` skill
