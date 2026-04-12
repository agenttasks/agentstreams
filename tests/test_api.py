"""Tests for src/api.py FastAPI endpoints.

Uses httpx.AsyncClient with mocked neon_db.connection_pool to avoid
requiring a live Neon database connection during testing.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient


@asynccontextmanager
async def mock_connection_pool(url=None):
    """Mock connection_pool that returns a mock connection."""
    conn = AsyncMock()
    yield conn


def _mock_cursor(rows, description=None):
    """Create a mock cursor with fetchall/fetchone."""
    cursor = AsyncMock()
    cursor.fetchall = AsyncMock(return_value=rows)
    cursor.fetchone = AsyncMock(return_value=rows[0] if rows else None)
    cursor.description = description
    return cursor


@pytest.fixture
def mock_pool():
    with (
        patch("src.api.connection_pool", mock_connection_pool),
        patch("src.neon_db.connection_pool", mock_connection_pool),
    ):
        yield


@pytest.fixture
async def client(mock_pool):
    from src.api import app

    # Patch lifespan to skip DB check
    @asynccontextmanager
    async def noop_lifespan(app):
        yield

    app.router.lifespan_context = noop_lifespan

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def test_health(client):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


async def test_get_metrics(client, mock_pool):
    with patch(
        "src.api.list_metrics",
        AsyncMock(
            return_value=[
                {
                    "name": "test.metric",
                    "type": "counter",
                    "unit": "ops",
                    "dimensions": ["model"],
                    "description": "Test metric",
                }
            ]
        ),
    ):
        resp = await client.get("/api/metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "test.metric"


async def test_get_tasks(client, mock_pool):
    with patch(
        "src.api.list_tasks",
        AsyncMock(
            return_value=[
                {
                    "id": 1,
                    "queue_name": "crawl",
                    "type": "knowledge_work",
                    "status": "queued",
                    "priority": 0,
                    "skill_name": None,
                    "model_id": None,
                    "plugin": None,
                    "attempts": 0,
                    "created_at": "2026-01-01T00:00:00",
                    "started_at": None,
                    "completed_at": None,
                }
            ]
        ),
    ):
        resp = await client.get("/api/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["status"] == "queued"


async def test_get_tasks_with_filters(client, mock_pool):
    with patch("src.api.list_tasks", AsyncMock(return_value=[])):
        resp = await client.get("/api/tasks?status=completed&type=code&limit=5")
        assert resp.status_code == 200


async def test_create_task(client, mock_pool):
    with patch("src.api.enqueue_task", AsyncMock(return_value=42)):
        resp = await client.post(
            "/api/tasks",
            json={
                "queue_name": "test-queue",
                "task_type": "code",
                "priority": 1,
            },
        )
        assert resp.status_code == 200
        assert resp.json()["id"] == 42


async def test_get_task_stats(client, mock_pool):
    with patch(
        "src.api.task_stats",
        AsyncMock(
            return_value=[
                {
                    "status": "completed",
                    "type": "code",
                    "queue_name": "test",
                    "count": 5,
                    "avg_duration_s": 1.5,
                }
            ]
        ),
    ):
        resp = await client.get("/api/tasks/stats")
        assert resp.status_code == 200


async def test_get_agents(client, mock_pool):
    with patch(
        "src.api.list_agents",
        AsyncMock(
            return_value=[
                {
                    "name": "code-generator",
                    "model_id": "claude-sonnet-4-6",
                    "allowed_tools": ["Read", "Write"],
                    "denied_tools": None,
                    "description": "Code gen agent",
                }
            ]
        ),
    ):
        resp = await client.get("/api/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert data[0]["name"] == "code-generator"


async def test_get_agent_not_found(client, mock_pool):
    with patch("src.api.get_agent", AsyncMock(return_value=None)):
        resp = await client.get("/api/agents/nonexistent")
        assert resp.status_code == 404


async def test_get_skills(client, mock_pool):
    with patch(
        "src.api.list_skills",
        AsyncMock(
            return_value=[
                {"name": "commit", "description": "Create git commit", "trigger_pattern": "/commit"}
            ]
        ),
    ):
        resp = await client.get("/api/skills")
        assert resp.status_code == 200


async def test_get_models(client, mock_pool):
    with patch(
        "src.api.list_models",
        AsyncMock(
            return_value=[
                {
                    "model_id": "claude-opus-4-6",
                    "family": "Claude 4.6",
                    "label": "Opus",
                    "supports_thinking": True,
                    "supports_tool_use": True,
                    "supports_vision": True,
                }
            ]
        ),
    ):
        resp = await client.get("/api/models")
        assert resp.status_code == 200
        data = resp.json()
        assert data[0]["supports_thinking"] is True


async def test_get_pipelines(client, mock_pool):
    with patch("src.api.list_pipelines", AsyncMock(return_value=[])):
        resp = await client.get("/api/pipelines")
        assert resp.status_code == 200


async def test_search_resources(client, mock_pool):
    with patch("src.api.fuzzy_search", AsyncMock(return_value=[{"label": "test", "sim": 0.8}])):
        resp = await client.get("/api/resources/search?q=test")
        assert resp.status_code == 200


async def test_search_resources_invalid_table(client, mock_pool):
    resp = await client.get("/api/resources/search?q=test&table=users")
    assert resp.status_code == 400


async def test_search_resources_missing_query(client, mock_pool):
    resp = await client.get("/api/resources/search")
    assert resp.status_code == 422


async def test_get_skill_registry(client, mock_pool):
    resp = await client.get("/api/skills/registry")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Verify schema: each entry has name, category, agent
    entry = data[0]
    assert "name" in entry
    assert "category" in entry
    assert "agent" in entry


async def test_get_skill_registry_contains_neon_skills(client, mock_pool):
    resp = await client.get("/api/skills/registry")
    assert resp.status_code == 200
    data = resp.json()
    neon_skills = [s for s in data if s["name"].startswith("neon-")]
    assert len(neon_skills) == 3
    neon_names = {s["name"] for s in neon_skills}
    assert neon_names == {"neon-api", "neon-dashboard", "neon-team-setup"}
    # All neon skills route to data-analyst via DATA category
    for skill in neon_skills:
        assert skill["category"] == "data"
        assert skill["agent"] == "data-analyst"


async def test_health_enriched(client, mock_pool):
    with patch("src.api.connection_pool", mock_connection_pool):
        # Mock the enriched health queries
        mock_conn = AsyncMock()
        mock_version_cursor = AsyncMock()
        mock_version_cursor.fetchone = AsyncMock(return_value=("PostgreSQL 18.0",))
        mock_branch_cursor = AsyncMock()
        mock_branch_cursor.fetchone = AsyncMock(return_value=("main",))
        mock_conn.execute = AsyncMock(side_effect=[mock_version_cursor, mock_branch_cursor])

        @asynccontextmanager
        async def mock_pool_enriched(url=None):
            yield mock_conn

        with patch("src.api.connection_pool", mock_pool_enriched):
            resp = await client.get("/api/health")
            assert resp.status_code == 200
            data = resp.json()
            assert data["status"] == "ok"
            assert "pg_version" in data
            assert "neon_branch" in data
            assert "skill_count" in data
            assert data["skill_count"] > 0
