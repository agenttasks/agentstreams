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
        raise ValueError(
            "No database URL provided. Set NEON_DATABASE_URL or pass url parameter."
        )
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
