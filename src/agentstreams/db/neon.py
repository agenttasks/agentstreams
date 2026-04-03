"""Neon Postgres async persistence for UDA entities.

Handles connection pooling, entity CRUD, bloom filter persistence, and
crawled page upserts. All operations use parameterized queries.

Connection string sourced from NEON_DATABASE_URL environment variable.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any

import psycopg

from ..bloom.filter import BloomFilter
from ..uda.schema_registry import (
    CrawledPage,
    MetricValue,
    Resource,
    ResourceType,
    Task,
    TaskStatus,
    TaskType,
    to_dict,
)


def _get_neon_url() -> str:
    """Get Neon connection string from environment."""
    url = os.environ.get("NEON_DATABASE_URL", "")
    if not url:
        raise RuntimeError("NEON_DATABASE_URL environment variable is required")
    return url


# ── Resource / CrawledPage persistence ──────────────────────


async def upsert_crawled_page(
    conn: psycopg.AsyncConnection,
    page: CrawledPage,
) -> int:
    """Upsert a crawled page as a resource. Returns resource ID."""
    result = await conn.execute(
        """INSERT INTO resources (type, label, url, content_hash, fetched_at, description)
           VALUES (%s, %s, %s, %s, %s, %s)
           ON CONFLICT (url) DO UPDATE
           SET content_hash = EXCLUDED.content_hash,
               fetched_at = EXCLUDED.fetched_at,
               description = EXCLUDED.description
           RETURNING id""",
        (
            ResourceType.CRAWLED_PAGE.value,
            page.domain,
            page.url,
            page.content_hash,
            page.crawled_at or datetime.now(UTC),
            json.dumps({"page_type": page.page_type, "topics": page.topics}),
        ),
    )
    row = await result.fetchone()
    return row[0] if row else 0


async def upsert_crawled_pages(
    conn: psycopg.AsyncConnection,
    pages: list[CrawledPage],
) -> int:
    """Batch upsert crawled pages. Returns count of upserted rows."""
    count = 0
    for page in pages:
        if page.url and page.content_hash:
            await upsert_crawled_page(conn, page)
            count += 1
    await conn.commit()
    return count


# ── Task persistence ────────────────────────────────────────


async def create_task(
    conn: psycopg.AsyncConnection,
    queue_name: str,
    task_type: TaskType,
    input_data: dict[str, Any],
    *,
    skill_name: str | None = None,
    model_id: str | None = None,
    plugin: str | None = None,
    priority: int = 0,
    config: dict[str, Any] | None = None,
) -> int:
    """Create a new task in the queue. Returns task ID."""
    result = await conn.execute(
        """INSERT INTO tasks (queue_name, type, input, config, skill_name, model_id, plugin, priority)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
           RETURNING id""",
        (
            queue_name,
            task_type.value,
            json.dumps(input_data),
            json.dumps(config or {}),
            skill_name,
            model_id,
            plugin,
            priority,
        ),
    )
    row = await result.fetchone()
    await conn.commit()
    return row[0] if row else 0


async def update_task_status(
    conn: psycopg.AsyncConnection,
    task_id: int,
    status: TaskStatus,
    *,
    output: dict[str, Any] | None = None,
    error: str | None = None,
) -> None:
    """Update task status and optionally set output/error."""
    now = datetime.now(UTC)
    if status == TaskStatus.PROCESSING:
        await conn.execute(
            "UPDATE tasks SET status = %s, started_at = %s, attempts = attempts + 1 WHERE id = %s",
            (status.value, now, task_id),
        )
    elif status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
        await conn.execute(
            "UPDATE tasks SET status = %s, completed_at = %s, output = %s, error = %s WHERE id = %s",
            (status.value, now, json.dumps(output) if output else None, error, task_id),
        )
    else:
        await conn.execute(
            "UPDATE tasks SET status = %s WHERE id = %s",
            (status.value, task_id),
        )
    await conn.commit()


async def fetch_queued_tasks(
    conn: psycopg.AsyncConnection,
    queue_name: str,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Fetch queued tasks for processing, ordered by priority DESC."""
    result = await conn.execute(
        """SELECT id, queue_name, type, input, config, skill_name, model_id, plugin, priority
           FROM tasks
           WHERE queue_name = %s AND status = 'queued'
             AND (execute_after IS NULL OR execute_after <= now())
           ORDER BY priority DESC, created_at ASC
           LIMIT %s""",
        (queue_name, limit),
    )
    rows = await result.fetchall()
    columns = [desc.name for desc in result.description] if result.description else []
    return [dict(zip(columns, row)) for row in rows]


# ── Metric persistence ──────────────────────────────────────


async def record_metric(
    conn: psycopg.AsyncConnection,
    metric_name: str,
    value: float,
    tags: dict[str, str],
) -> None:
    """Record a single metric observation."""
    await conn.execute(
        "INSERT INTO metric_values (metric_name, value, tags) VALUES (%s, %s, %s)",
        (metric_name, value, json.dumps(tags)),
    )
    await conn.commit()


# ── Bloom filter persistence ────────────────────────────────


async def save_bloom_filter(
    conn: psycopg.AsyncConnection,
    filter_name: str,
    bloom: BloomFilter,
) -> None:
    """Persist bloom filter state to Neon for cross-session deduplication.

    Stores in a dedicated bloom_filters table (created if missing).
    """
    await conn.execute(
        """CREATE TABLE IF NOT EXISTS bloom_filters (
               name TEXT PRIMARY KEY,
               data BYTEA NOT NULL,
               capacity INTEGER NOT NULL,
               item_count INTEGER NOT NULL,
               fp_rate DOUBLE PRECISION NOT NULL,
               updated_at TIMESTAMPTZ DEFAULT now()
           )"""
    )
    data = bloom.to_bytes()
    await conn.execute(
        """INSERT INTO bloom_filters (name, data, capacity, item_count, fp_rate)
           VALUES (%s, %s, %s, %s, %s)
           ON CONFLICT (name) DO UPDATE
           SET data = EXCLUDED.data,
               item_count = EXCLUDED.item_count,
               updated_at = now()""",
        (filter_name, data, bloom.capacity, bloom.count, bloom.fp_rate),
    )
    await conn.commit()


async def load_bloom_filter(
    conn: psycopg.AsyncConnection,
    filter_name: str,
) -> BloomFilter | None:
    """Load a persisted bloom filter from Neon. Returns None if not found."""
    result = await conn.execute(
        "SELECT data FROM bloom_filters WHERE name = %s",
        (filter_name,),
    )
    row = await result.fetchone()
    if row and row[0]:
        return BloomFilter.from_bytes(bytes(row[0]))
    return None


# ── Connection helper ───────────────────────────────────────


async def connect() -> psycopg.AsyncConnection:
    """Open an async connection to Neon Postgres."""
    return await psycopg.AsyncConnection.connect(_get_neon_url())
