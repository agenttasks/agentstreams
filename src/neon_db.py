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


# ── Kimball dimensional operations ──────────────────────


async def upsert_dim_domain(
    conn,
    *,
    domain_name: str,
    tld: str,
    sitemap_url: str = "",
) -> int:
    """Upsert a domain dimension record (SCD Type 1). Returns domain_key."""
    row = await (
        await conn.execute(
            """INSERT INTO dim_domain (domain_name, tld, sitemap_url, last_crawled_at)
               VALUES (%s, %s, %s, now())
               ON CONFLICT (domain_name) DO UPDATE SET
                   last_crawled_at = now(),
                   sitemap_url = COALESCE(NULLIF(EXCLUDED.sitemap_url, ''), dim_domain.sitemap_url)
               RETURNING domain_key""",
            (domain_name, tld, sitemap_url),
        )
    ).fetchone()
    return row[0]


async def increment_domain_pages(conn, domain_key: int, discovered: int) -> None:
    """Increment total_pages_discovered for a domain."""
    await conn.execute(
        """UPDATE dim_domain SET total_pages_discovered = total_pages_discovered + %s
           WHERE domain_key = %s""",
        (discovered, domain_key),
    )


async def get_or_create_content_type(conn, content_type_code: str) -> int:
    """Get content_type_key, creating if needed. Returns content_type_key."""
    row = await (
        await conn.execute(
            "SELECT content_type_key FROM dim_content_type WHERE content_type_code = %s",
            (content_type_code,),
        )
    ).fetchone()
    if row:
        return row[0]
    row = await (
        await conn.execute(
            """INSERT INTO dim_content_type (content_type_code, content_type_label)
               VALUES (%s, %s) RETURNING content_type_key""",
            (content_type_code, content_type_code.replace("-", " ").title()),
        )
    ).fetchone()
    return row[0]


async def get_or_create_extraction(
    conn,
    *,
    model_name: str,
    pipeline_version: str,
    config_hash: str = "",
) -> int:
    """Get current extraction dimension key, creating if needed."""
    row = await (
        await conn.execute(
            """SELECT extraction_key FROM dim_extraction
               WHERE model_name = %s AND pipeline_version = %s AND is_current = true""",
            (model_name, pipeline_version),
        )
    ).fetchone()
    if row:
        return row[0]
    row = await (
        await conn.execute(
            """INSERT INTO dim_extraction (model_name, pipeline_version, config_hash)
               VALUES (%s, %s, %s) RETURNING extraction_key""",
            (model_name, pipeline_version, config_hash),
        )
    ).fetchone()
    return row[0]


async def create_crawl_session(
    conn,
    *,
    session_id: str,
    pipeline_name: str,
    config: dict | None = None,
) -> int:
    """Create a crawl session dimension record. Returns session_key."""
    row = await (
        await conn.execute(
            """INSERT INTO dim_crawl_session (session_id, pipeline_name, config)
               VALUES (%s, %s, %s) RETURNING session_key""",
            (session_id, pipeline_name, json.dumps(config or {})),
        )
    ).fetchone()
    return row[0]


async def complete_crawl_session(
    conn,
    session_key: int,
    *,
    total_urls: int,
    total_pages: int,
    total_new: int,
    total_errors: int,
    bloom_fp_rate: float = 0.0,
) -> None:
    """Mark a crawl session as completed with summary stats."""
    await conn.execute(
        """UPDATE dim_crawl_session SET
               ended_at = now(),
               total_urls_discovered = %s,
               total_pages_crawled = %s,
               total_pages_new = %s,
               total_errors = %s,
               bloom_fp_rate = %s
           WHERE session_key = %s""",
        (total_urls, total_pages, total_new, total_errors, bloom_fp_rate, session_key),
    )


async def insert_fact_crawl_event(
    conn,
    *,
    date_key: int,
    domain_key: int,
    content_type_key: int | None,
    extraction_key: int | None,
    session_key: int,
    url: str,
    content_hash: str = "",
    title: str = "",
    status_code: int = 200,
    response_time_ms: int | None = None,
    content_bytes: int = 0,
    markdown_bytes: int = 0,
    token_count: int = 0,
    chunk_count: int = 0,
    is_new_url: bool = True,
    is_duplicate_content: bool = False,
    is_error: bool = False,
    orjson_cache_path: str = "",
) -> int:
    """Insert a crawl event fact row. Returns crawl_event_id."""
    row = await (
        await conn.execute(
            """INSERT INTO fact_crawl_events (
                   date_key, domain_key, content_type_key, extraction_key,
                   session_key, url, content_hash, title, status_code,
                   response_time_ms, content_bytes, markdown_bytes,
                   token_count, chunk_count, is_new_url,
                   is_duplicate_content, is_error, orjson_cache_path)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING crawl_event_id""",
            (
                date_key, domain_key, content_type_key, extraction_key,
                session_key, url, content_hash, title, status_code,
                response_time_ms, content_bytes, markdown_bytes,
                token_count, chunk_count, is_new_url,
                is_duplicate_content, is_error, orjson_cache_path,
            ),
        )
    ).fetchone()
    return row[0]


async def upsert_fact_page_content(
    conn,
    *,
    date_key: int,
    domain_key: int,
    content_type_key: int | None,
    url: str,
    content_hash: str,
    title: str = "",
    markdown_bytes: int = 0,
    raw_html_bytes: int = 0,
    token_count: int = 0,
    heading_count: int = 0,
    link_count: int = 0,
    code_block_count: int = 0,
    image_count: int = 0,
    has_structured_data: bool = False,
    has_code_samples: bool = False,
    has_api_references: bool = False,
    embedding_wing: str = "docs",
    embedding_room: str = "",
    lance_record_count: int = 0,
) -> int:
    """Upsert a page content snapshot fact. Returns page_content_id."""
    row = await (
        await conn.execute(
            """INSERT INTO fact_page_content (
                   date_key, domain_key, content_type_key, url, content_hash,
                   title, markdown_bytes, raw_html_bytes, token_count,
                   heading_count, link_count, code_block_count, image_count,
                   has_structured_data, has_code_samples, has_api_references,
                   embedding_wing, embedding_room, lance_record_count)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (url) DO UPDATE SET
                   content_hash = EXCLUDED.content_hash,
                   title = EXCLUDED.title,
                   markdown_bytes = EXCLUDED.markdown_bytes,
                   token_count = EXCLUDED.token_count,
                   heading_count = EXCLUDED.heading_count,
                   link_count = EXCLUDED.link_count,
                   code_block_count = EXCLUDED.code_block_count,
                   image_count = EXCLUDED.image_count,
                   has_code_samples = EXCLUDED.has_code_samples,
                   has_api_references = EXCLUDED.has_api_references,
                   lance_record_count = EXCLUDED.lance_record_count,
                   last_updated_at = now()
               RETURNING page_content_id""",
            (
                date_key, domain_key, content_type_key, url, content_hash,
                title, markdown_bytes, raw_html_bytes, token_count,
                heading_count, link_count, code_block_count, image_count,
                has_structured_data, has_code_samples, has_api_references,
                embedding_wing, embedding_room, lance_record_count,
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
