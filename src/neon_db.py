"""Async Neon Postgres 18 connection pool and data layer.

Provides a connection pool factory, schema bootstrap, and typed data access
functions for the AgentStreams UDA physical layer.

UDA pattern: this module IS the physical data layer. Every function maps
to an ontology class via the mappings.ttl definitions.

Environment:
    NEON_DATABASE_URL: Neon connection string (required for live operations)
"""

from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager
from typing import Any


async def get_connection(url: str | None = None):
    """Create an async connection to Neon Postgres 18.

    Args:
        url: Connection string. Falls back to NEON_DATABASE_URL env var.
    """
    import psycopg

    neon_url = url or os.environ.get("NEON_DATABASE_URL", "")
    if not neon_url:
        raise ValueError("No database URL provided. Set NEON_DATABASE_URL or pass url parameter.")
    return await psycopg.AsyncConnection.connect(neon_url)


@asynccontextmanager
async def connection_pool(url: str | None = None):
    """Async context manager for Neon connections.

    Usage:
        async with connection_pool() as conn:
            await conn.execute("SELECT 1")
    """
    conn = await get_connection(url)
    try:
        yield conn
    finally:
        await conn.close()


async def bootstrap_schema(conn) -> None:
    """Apply the UDA physical schema to a fresh Neon database.

    Reads ontology/schema.sql and executes it. Idempotent via
    CREATE TABLE IF NOT EXISTS and ON CONFLICT.
    """
    from pathlib import Path

    schema_path = Path(__file__).parent.parent / "ontology" / "schema.sql"
    sql = schema_path.read_text()
    await conn.execute(sql)
    await conn.commit()


# ── Resource operations (as:Resource → resources table) ──────


async def upsert_resource(
    conn,
    *,
    resource_type: str,
    label: str,
    url: str,
    content_hash: str | None = None,
    description: str | None = None,
    related_model_id: str | None = None,
) -> int:
    """Upsert a resource record. Returns the resource ID."""
    row = await (
        await conn.execute(
            """INSERT INTO resources (type, label, url, content_hash, description,
                   related_model_id, fetched_at)
               VALUES (%s, %s, %s, %s, %s, %s, now())
               ON CONFLICT (url) DO UPDATE SET
                   content_hash = EXCLUDED.content_hash,
                   fetched_at = now()
               RETURNING id""",
            (resource_type, label, url, content_hash, description, related_model_id),
        )
    ).fetchone()
    return row[0]


# ── Task operations (as:Task → tasks table) ─────────────────


async def enqueue_task(
    conn,
    *,
    queue_name: str,
    task_type: str = "knowledge_work",
    skill_name: str | None = None,
    model_id: str | None = None,
    plugin: str | None = None,
    task_input: dict | None = None,
    config: dict | None = None,
    priority: int = 0,
) -> int:
    """Enqueue a task for processing. Returns the task ID."""
    row = await (
        await conn.execute(
            """INSERT INTO tasks (queue_name, type, status, priority,
                   skill_name, model_id, plugin, input, config)
               VALUES (%s, %s, 'queued', %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                queue_name,
                task_type,
                priority,
                skill_name,
                model_id,
                plugin,
                json.dumps(task_input or {}),
                json.dumps(config or {}),
            ),
        )
    ).fetchone()
    return row[0]


async def complete_task(conn, task_id: int, *, output: dict | None = None) -> None:
    """Mark a task as completed with output."""
    await conn.execute(
        """UPDATE tasks SET status = 'completed', output = %s,
               completed_at = now() WHERE id = %s""",
        (json.dumps(output or {}), task_id),
    )


async def fail_task(conn, task_id: int, *, error: str) -> None:
    """Mark a task as failed with error message."""
    await conn.execute(
        """UPDATE tasks SET status = 'failed', error = %s,
               completed_at = now() WHERE id = %s""",
        (error, task_id),
    )


# ── Pipeline operations (as:Pipeline → pipelines table) ──────


async def upsert_pipeline(
    conn,
    *,
    name: str,
    skill_name: str,
    model_id: str | None = None,
    config: dict | None = None,
    status: str = "active",
) -> int:
    """Upsert a pipeline record. Returns pipeline ID."""
    row = await (
        await conn.execute(
            """INSERT INTO pipelines (name, skill_name, model_id, config, status)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (name) DO UPDATE SET
                   config = EXCLUDED.config,
                   status = EXCLUDED.status,
                   updated_at = now()
               RETURNING id""",
            (name, skill_name, model_id, json.dumps(config or {}), status),
        )
    ).fetchone()
    return row[0]


# ── Metric operations (as:Metric → metric_values fact table) ─


async def record_metric(
    conn,
    *,
    metric_name: str,
    value: float,
    tags: dict[str, str] | None = None,
) -> None:
    """Record a metric observation to the dimensional fact table."""
    await conn.execute(
        """INSERT INTO metric_values (metric_name, value, tags)
           VALUES (%s, %s, %s)""",
        (metric_name, value, json.dumps(tags or {})),
    )


# ── Crawl data operations ───────────────────────────────────


async def upsert_crawl_page(
    conn,
    *,
    url: str,
    domain: str,
    content_hash: str,
    title: str = "",
    content: str = "",
    status_code: int = 200,
) -> int:
    """Persist a crawled page to the crawl_pages table. Returns page ID."""
    row = await (
        await conn.execute(
            """INSERT INTO crawl_pages (url, domain, content_hash, title,
                   content, status_code, crawled_at)
               VALUES (%s, %s, %s, %s, %s, %s, now())
               ON CONFLICT (url) DO UPDATE SET
                   content_hash = EXCLUDED.content_hash,
                   title = EXCLUDED.title,
                   content = EXCLUDED.content,
                   status_code = EXCLUDED.status_code,
                   crawled_at = now()
               RETURNING id""",
            (url, domain, content_hash, title, content, status_code),
        )
    ).fetchone()
    return row[0]


async def get_crawl_stats(conn, domain: str | None = None) -> dict[str, Any]:
    """Get crawl statistics, optionally filtered by domain."""
    where = "WHERE domain = %s" if domain else ""
    params: tuple = (domain,) if domain else ()

    row = await (
        await conn.execute(
            f"""SELECT COUNT(*), COUNT(DISTINCT domain),
                       MAX(crawled_at)
                FROM crawl_pages {where}""",
            params,
        )
    ).fetchone()

    return {
        "total_pages": row[0],
        "domains": row[1],
        "last_crawl": row[2].isoformat() if row[2] else None,
    }


# ── HyperLogLog operations (hll extension) ───────────────


async def hll_add(conn, *, sketch_name: str, value: str, domain: str = "") -> None:
    """Add a value to a HyperLogLog sketch for approximate distinct counting.

    HLL sketches complement bloom filters: bloom tells you "seen before?",
    HLL tells you "how many distinct items total?"
    """
    await conn.execute(
        """INSERT INTO hll_sketches (name, domain, sketch, updated_at)
           VALUES (%s, %s, hll_add(hll_empty(), hll_hash_text(%s)), now())
           ON CONFLICT (name) DO UPDATE SET
               sketch = hll_add(hll_sketches.sketch, hll_hash_text(%s)),
               updated_at = now()""",
        (sketch_name, domain, value, value),
    )


async def hll_count(conn, sketch_name: str) -> int:
    """Get approximate distinct count from an HLL sketch."""
    row = await (
        await conn.execute(
            "SELECT hll_cardinality(sketch)::bigint FROM hll_sketches WHERE name = %s",
            (sketch_name,),
        )
    ).fetchone()
    return row[0] if row else 0


# ── Token counting (pg_tiktoken extension) ───────────────


async def count_tokens(conn, *, text: str, model: str = "cl100k_base") -> int:
    """Count tokens using pg_tiktoken (runs inside Postgres, no Python dep).

    Uses tiktoken_count() function from the pg_tiktoken extension.
    """
    row = await (
        await conn.execute(
            "SELECT tiktoken_count(%s, %s)",
            (model, text),
        )
    ).fetchone()
    return row[0]


async def record_token_count(
    conn,
    *,
    source_type: str,
    source_id: str,
    text: str,
    model: str = "cl100k_base",
) -> dict[str, int]:
    """Count tokens and persist to token_counts table."""
    row = await (
        await conn.execute(
            """INSERT INTO token_counts (source_type, source_id, model,
                   token_count, char_count)
               VALUES (%s, %s, %s, tiktoken_count(%s, %s), length(%s))
               RETURNING token_count, char_count""",
            (source_type, source_id, model, model, text, text),
        )
    ).fetchone()
    return {"token_count": row[0], "char_count": row[1]}


# ── Trigram similarity search (pg_trgm extension) ────────


async def fuzzy_search(
    conn, *, table: str, column: str, query: str, threshold: float = 0.3, limit: int = 10
) -> list[dict]:
    """Fuzzy text search using pg_trgm trigram similarity.

    Returns rows where similarity(column, query) >= threshold,
    ordered by similarity descending.
    """
    rows = await (
        await conn.execute(
            f"""SELECT *, similarity({column}, %s) AS sim
                FROM {table}
                WHERE similarity({column}, %s) >= %s
                ORDER BY sim DESC LIMIT %s""",
            (query, query, threshold, limit),
        )
    ).fetchall()
    return [dict(r._mapping) if hasattr(r, "_mapping") else r for r in rows]


# ── Thinking trace operations ────────────────────────────


# ── Read-only query functions (shared by API + TUI) ────────


async def list_metrics(conn) -> list[dict]:
    """List all metric definitions with type, unit, and dimensions."""
    rows = await (
        await conn.execute(
            "SELECT name, type, unit, dimensions, description FROM metrics ORDER BY name"
        )
    ).fetchall()
    return [
        {
            "name": r[0],
            "type": r[1],
            "unit": r[2],
            "dimensions": r[3],
            "description": r[4],
        }
        for r in rows
    ]


async def query_metric_values(
    conn,
    *,
    metric_name: str,
    hours: int = 24,
    tags_filter: dict[str, str] | None = None,
    limit: int = 1000,
) -> list[dict]:
    """Query raw time-series data for a specific metric."""
    params: list[Any] = [metric_name, hours]
    tag_clause = ""
    if tags_filter:
        tag_conditions = []
        for key, value in tags_filter.items():
            params.append(value)
            tag_conditions.append(f"tags->>'{key}' = %s")
        tag_clause = "AND " + " AND ".join(tag_conditions)

    params.append(limit)
    rows = await (
        await conn.execute(
            f"""SELECT recorded_at, value, tags
                FROM metric_values
                WHERE metric_name = %s
                  AND recorded_at > now() - interval '1 hour' * %s
                  {tag_clause}
                ORDER BY recorded_at DESC
                LIMIT %s""",
            tuple(params),
        )
    ).fetchall()
    return [
        {
            "recorded_at": r[0].isoformat() if r[0] else None,
            "value": float(r[1]),
            "tags": json.loads(r[2]) if isinstance(r[2], str) else r[2],
        }
        for r in rows
    ]


async def metric_summary(
    conn,
    *,
    metric_name: str,
    hours: int = 168,
    group_by_tag: str | None = None,
) -> list[dict]:
    """Statistical summary (count, avg, min, max, p50, p99) for a metric."""
    params: tuple = (metric_name, hours)

    if group_by_tag:
        query = f"""
            SELECT
                tags->>'{group_by_tag}' AS group_key,
                COUNT(*) AS count,
                ROUND(AVG(value)::numeric, 4) AS avg,
                ROUND(MIN(value)::numeric, 4) AS min,
                ROUND(MAX(value)::numeric, 4) AS max,
                ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value)::numeric, 4) AS p50,
                ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY value)::numeric, 4) AS p99
            FROM metric_values
            WHERE metric_name = %s
              AND recorded_at > now() - interval '1 hour' * %s
            GROUP BY group_key
            ORDER BY avg DESC
        """
    else:
        query = """
            SELECT
                COUNT(*) AS count,
                ROUND(AVG(value)::numeric, 4) AS avg,
                ROUND(MIN(value)::numeric, 4) AS min,
                ROUND(MAX(value)::numeric, 4) AS max,
                ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value)::numeric, 4) AS p50,
                ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY value)::numeric, 4) AS p99
            FROM metric_values
            WHERE metric_name = %s
              AND recorded_at > now() - interval '1 hour' * %s
        """

    rows = await (await conn.execute(query, params)).fetchall()
    if group_by_tag:
        return [
            {
                "group_key": r[0],
                "count": r[1],
                "avg": float(r[2] or 0),
                "min": float(r[3] or 0),
                "max": float(r[4] or 0),
                "p50": float(r[5] or 0),
                "p99": float(r[6] or 0),
            }
            for r in rows
        ]
    row = rows[0] if rows else None
    if not row:
        return []
    return [
        {
            "count": row[0],
            "avg": float(row[1] or 0),
            "min": float(row[2] or 0),
            "max": float(row[3] or 0),
            "p50": float(row[4] or 0),
            "p99": float(row[5] or 0),
        }
    ]


async def list_tasks(
    conn,
    *,
    status: str | None = None,
    task_type: str | None = None,
    queue_name: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """List tasks with optional filters."""
    conditions: list[str] = []
    params: list[Any] = []

    if status:
        params.append(status)
        conditions.append("status = %s")
    if task_type:
        params.append(task_type)
        conditions.append("type = %s")
    if queue_name:
        params.append(queue_name)
        conditions.append("queue_name = %s")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    params.append(limit)

    rows = await (
        await conn.execute(
            f"""SELECT id, queue_name, type, status, priority, skill_name,
                       model_id, plugin, attempts, created_at, started_at, completed_at
                FROM tasks {where}
                ORDER BY created_at DESC
                LIMIT %s""",
            tuple(params),
        )
    ).fetchall()
    return [
        {
            "id": r[0],
            "queue_name": r[1],
            "type": r[2],
            "status": r[3],
            "priority": r[4],
            "skill_name": r[5],
            "model_id": r[6],
            "plugin": r[7],
            "attempts": r[8],
            "created_at": r[9].isoformat() if r[9] else None,
            "started_at": r[10].isoformat() if r[10] else None,
            "completed_at": r[11].isoformat() if r[11] else None,
        }
        for r in rows
    ]


async def task_stats(conn, *, hours: int = 24) -> list[dict]:
    """Task queue statistics — counts by status, type, and queue."""
    rows = await (
        await conn.execute(
            """SELECT status, type, queue_name, COUNT(*) as count,
                      ROUND(AVG(EXTRACT(EPOCH FROM (completed_at - started_at)))::numeric, 2) as avg_duration_s
               FROM tasks
               WHERE created_at > now() - interval '1 hour' * %s
               GROUP BY status, type, queue_name
               ORDER BY count DESC""",
            (hours,),
        )
    ).fetchall()
    return [
        {
            "status": r[0],
            "type": r[1],
            "queue_name": r[2],
            "count": r[3],
            "avg_duration_s": float(r[4]) if r[4] else None,
        }
        for r in rows
    ]


async def list_agents(conn) -> list[dict]:
    """List all agent manifests with tool grants and model assignments."""
    rows = await (
        await conn.execute(
            """SELECT name, model_id, allowed_tools, denied_tools, description
               FROM agent_manifests
               ORDER BY name"""
        )
    ).fetchall()
    return [
        {
            "name": r[0],
            "model_id": r[1],
            "allowed_tools": r[2],
            "denied_tools": r[3],
            "description": r[4],
        }
        for r in rows
    ]


async def get_agent(conn, name: str) -> dict | None:
    """Get a single agent manifest by name."""
    row = await (
        await conn.execute(
            """SELECT name, model_id, allowed_tools, denied_tools, description
               FROM agent_manifests WHERE name = %s""",
            (name,),
        )
    ).fetchone()
    if not row:
        return None
    return {
        "name": row[0],
        "model_id": row[1],
        "allowed_tools": row[2],
        "denied_tools": row[3],
        "description": row[4],
    }


async def list_skills(conn) -> list[dict]:
    """List all registered skills."""
    rows = await (
        await conn.execute("SELECT name, description, trigger_pattern FROM skills ORDER BY name")
    ).fetchall()
    return [{"name": r[0], "description": r[1], "trigger_pattern": r[2]} for r in rows]


async def list_models(conn) -> list[dict]:
    """List Claude models with capabilities."""
    rows = await (
        await conn.execute(
            """SELECT model_id, family, label, supports_thinking,
                      supports_tool_use, supports_vision
               FROM models ORDER BY family DESC, model_id"""
        )
    ).fetchall()
    return [
        {
            "model_id": r[0],
            "family": r[1],
            "label": r[2],
            "supports_thinking": r[3],
            "supports_tool_use": r[4],
            "supports_vision": r[5],
        }
        for r in rows
    ]


async def list_pipelines(conn) -> list[dict]:
    """List all pipelines with config and status."""
    rows = await (
        await conn.execute(
            """SELECT id, name, skill_name, model_id, config, status, created_at, updated_at
               FROM pipelines ORDER BY name"""
        )
    ).fetchall()
    return [
        {
            "id": r[0],
            "name": r[1],
            "skill_name": r[2],
            "model_id": r[3],
            "config": json.loads(r[4]) if isinstance(r[4], str) else r[4],
            "status": r[5],
            "created_at": r[6].isoformat() if r[6] else None,
            "updated_at": r[7].isoformat() if r[7] else None,
        }
        for r in rows
    ]


# ── Thinking trace operations ────────────────────────────


async def record_thinking_trace(
    conn,
    *,
    task_id: int | None = None,
    thinking_type: str,
    budget_tokens: int | None = None,
    thinking_tokens: int = 0,
    input_tokens: int = 0,
    output_tokens: int = 0,
    model: str,
    duration_ms: int | None = None,
) -> int:
    """Record an extended/adaptive thinking trace for audit and optimization."""
    row = await (
        await conn.execute(
            """INSERT INTO thinking_traces (task_id, thinking_type, budget_tokens,
                   thinking_tokens, input_tokens, output_tokens, model, duration_ms)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                task_id,
                thinking_type,
                budget_tokens,
                thinking_tokens,
                input_tokens,
                output_tokens,
                model,
                duration_ms,
            ),
        )
    ).fetchone()
    return row[0]


# ── Harness run operations ───────────────────────────────


async def create_harness_run(
    conn,
    *,
    harness_name: str,
    sprint_id: str,
    objective: str,
    criteria: list[dict],
    max_iterations: int = 5,
    acceptance_threshold: float = 0.7,
) -> int:
    """Create a harness run record. Returns the run ID."""
    row = await (
        await conn.execute(
            """INSERT INTO harness_runs (harness_name, sprint_id, objective,
                   criteria, max_iterations, acceptance_threshold)
               VALUES (%s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                harness_name,
                sprint_id,
                objective,
                json.dumps(criteria),
                max_iterations,
                acceptance_threshold,
            ),
        )
    ).fetchone()
    return row[0]


async def record_evaluation_result(
    conn,
    *,
    harness_run_id: int,
    iteration: int,
    scores: list[dict],
    overall_score: float,
    passed: bool,
    summary: str,
    strategy_recommendation: str = "",
) -> int:
    """Record an evaluation iteration result. Returns the result ID."""
    row = await (
        await conn.execute(
            """INSERT INTO evaluation_results (harness_run_id, iteration, scores,
                   overall_score, passed, summary, strategy_recommendation)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                harness_run_id,
                iteration,
                json.dumps(scores),
                overall_score,
                passed,
                summary,
                strategy_recommendation,
            ),
        )
    ).fetchone()
    return row[0]


async def complete_harness_run(
    conn,
    run_id: int,
    *,
    final_status: str,
    total_iterations: int,
    total_tokens: int,
) -> None:
    """Mark a harness run as completed."""
    await conn.execute(
        """UPDATE harness_runs SET final_status = %s, total_iterations = %s,
               total_tokens = %s, completed_at = now()
           WHERE id = %s""",
        (final_status, total_iterations, total_tokens, run_id),
    )
