"""AgentStreams FastAPI data API.

Thin REST layer over src/neon_db.py async functions. Uses the existing
psycopg 3.2+ connection pattern — one connection per request via
connection_pool(). No SQLAlchemy.

Refactored to follow Anthropic skills standard (SKILL.md format) and
cookbook patterns (SRE Incident Response Agent: enriched health, OpenAPI tags).

Skills: neon-api, neon-dashboard, neon-team-setup (registered in SKILL_CATALOG)
Cookbooks: platform.claude.com/cookbooks/sre-incident-response-agent

Run: uvicorn src.api:app --reload --port 8000
"""

from __future__ import annotations

import importlib.metadata
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.knowledge_agents import CATEGORY_AGENTS, SKILL_CATALOG
from src.models import (
    AgentManifestOut,
    MetricOut,
    MetricSummaryOut,
    MetricValueOut,
    ModelOut,
    PipelineOut,
    SkillOut,
    SkillRegistryOut,
    TaskCreateIn,
    TaskOut,
    TaskStatsOut,
)
from src.neon_db import (
    connection_pool,
    enqueue_task,
    fuzzy_search,
    get_agent,
    list_agents,
    list_metrics,
    list_models,
    list_pipelines,
    list_skills,
    list_tasks,
    metric_summary,
    query_metric_values,
    task_stats,
)

# ── OpenAPI Tags (SRE cookbook pattern) ────────────────────

tags_metadata = [
    {"name": "health", "description": "System health and diagnostics"},
    {"name": "metrics", "description": "Metric catalog and time-series data"},
    {"name": "tasks", "description": "Task queue management"},
    {"name": "agents", "description": "Agent manifest registry"},
    {"name": "skills", "description": "Skill catalog and registry"},
    {"name": "models", "description": "Claude model registry"},
    {"name": "pipelines", "description": "Pipeline definitions"},
    {"name": "resources", "description": "Resource search via pg_trgm"},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate database connectivity on startup."""
    async with connection_pool() as conn:
        await conn.execute("SELECT 1")
    yield


app = FastAPI(
    title="AgentStreams",
    version=importlib.metadata.version("agentstreams"),
    description="REST API for AgentStreams multi-agent orchestration data. "
    "Skills: neon-api, neon-dashboard, neon-team-setup.",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ─────────────────────────────────────────────────


@app.get("/api/health", tags=["health"])
async def health():
    """Health check with Neon diagnostics (SRE cookbook pattern)."""
    async with connection_pool() as conn:
        row = await (await conn.execute("SELECT version()")).fetchone()
        pg_version = row[0] if row else "unknown"
        branch_row = await (
            await conn.execute("SELECT setting FROM pg_settings WHERE name = 'neon.branch_name'")
        ).fetchone()
        neon_branch = branch_row[0] if branch_row else "unknown"
    return {
        "status": "ok",
        "pg_version": pg_version,
        "neon_branch": neon_branch,
        "skill_count": len(SKILL_CATALOG),
    }


# ── Metrics ────────────────────────────────────────────────


@app.get("/api/metrics", response_model=list[MetricOut], tags=["metrics"])
async def get_metrics():
    """List all metric definitions."""
    async with connection_pool() as conn:
        return await list_metrics(conn)


@app.get("/api/metrics/{name}/values", response_model=list[MetricValueOut], tags=["metrics"])
async def get_metric_values(
    name: str,
    hours: int = Query(24, ge=1, le=8760),
    limit: int = Query(1000, ge=1, le=10000),
):
    """Query time-series data for a specific metric."""
    async with connection_pool() as conn:
        return await query_metric_values(conn, metric_name=name, hours=hours, limit=limit)


@app.get("/api/metrics/{name}/summary", response_model=list[MetricSummaryOut], tags=["metrics"])
async def get_metric_summary(
    name: str,
    hours: int = Query(168, ge=1, le=8760),
    group_by: str | None = Query(None),
):
    """Statistical summary (count, avg, min, max, p50, p99) for a metric."""
    async with connection_pool() as conn:
        return await metric_summary(conn, metric_name=name, hours=hours, group_by_tag=group_by)


# ── Tasks ──────────────────────────────────────────────────


@app.get("/api/tasks", response_model=list[TaskOut], tags=["tasks"])
async def get_tasks(
    status: str | None = Query(None),
    type: str | None = Query(None),
    queue: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
):
    """List tasks with optional filters."""
    async with connection_pool() as conn:
        return await list_tasks(conn, status=status, task_type=type, queue_name=queue, limit=limit)


@app.post("/api/tasks", response_model=dict, tags=["tasks"])
async def create_task(task: TaskCreateIn):
    """Create a new task in the queue."""
    async with connection_pool() as conn:
        task_id = await enqueue_task(
            conn,
            queue_name=task.queue_name,
            task_type=task.task_type,
            skill_name=task.skill_name,
            model_id=task.model_id,
            plugin=task.plugin,
            task_input=task.task_input,
            config=task.config,
            priority=task.priority,
        )
        await conn.commit()
    return {"id": task_id, "status": "queued"}


@app.get("/api/tasks/stats", response_model=list[TaskStatsOut], tags=["tasks"])
async def get_task_stats(hours: int = Query(24, ge=1, le=8760)):
    """Task queue statistics by status, type, and queue."""
    async with connection_pool() as conn:
        return await task_stats(conn, hours=hours)


# ── Agents ─────────────────────────────────────────────────


@app.get("/api/agents", response_model=list[AgentManifestOut], tags=["agents"])
async def get_agents():
    """List all agent manifests."""
    async with connection_pool() as conn:
        return await list_agents(conn)


@app.get("/api/agents/{name}", response_model=AgentManifestOut, tags=["agents"])
async def get_agent_by_name(name: str):
    """Get a single agent manifest by name."""
    async with connection_pool() as conn:
        agent = await get_agent(conn, name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")
    return agent


# ── Skills ─────────────────────────────────────────────────


@app.get("/api/skills", response_model=list[SkillOut], tags=["skills"])
async def get_skills():
    """List all registered skills from the database."""
    async with connection_pool() as conn:
        return await list_skills(conn)


@app.get("/api/skills/registry", response_model=list[SkillRegistryOut], tags=["skills"])
async def get_skill_registry():
    """Skill catalog with category and agent routing metadata.

    Returns all skills from SKILL_CATALOG (knowledge-work-plugins +
    local skills) with their category and the agent that handles them.
    """
    return [
        SkillRegistryOut(
            name=meta.name,
            category=meta.category.value,
            agent=CATEGORY_AGENTS[meta.category],
        )
        for meta in sorted(SKILL_CATALOG.values(), key=lambda m: m.name)
    ]


# ── Models ─────────────────────────────────────────────────


@app.get("/api/models", response_model=list[ModelOut], tags=["models"])
async def get_models():
    """List Claude models with capabilities."""
    async with connection_pool() as conn:
        return await list_models(conn)


# ── Pipelines ──────────────────────────────────────────────


@app.get("/api/pipelines", response_model=list[PipelineOut], tags=["pipelines"])
async def get_pipelines():
    """List all pipelines."""
    async with connection_pool() as conn:
        return await list_pipelines(conn)


# ── Resources ──────────────────────────────────────────────


@app.get("/api/resources/search", tags=["resources"])
async def search_resources(
    q: str = Query(..., min_length=1),
    table: str = Query("resources"),
    column: str = Query("label"),
    threshold: float = Query(0.3, ge=0.0, le=1.0),
    limit: int = Query(10, ge=1, le=100),
):
    """Fuzzy search resources using pg_trgm trigram similarity."""
    allowed_tables = {"resources", "skills", "crawl_pages"}
    if table not in allowed_tables:
        raise HTTPException(status_code=400, detail=f"Table must be one of: {allowed_tables}")
    allowed_columns = {"label", "name", "title", "description", "url"}
    if column not in allowed_columns:
        raise HTTPException(status_code=400, detail=f"Column must be one of: {allowed_columns}")
    async with connection_pool() as conn:
        return await fuzzy_search(
            conn, table=table, column=column, query=q, threshold=threshold, limit=limit
        )
