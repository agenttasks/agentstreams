"""Pydantic v2 request/response models for the AgentStreams API.

Maps directly to ontology/schema.sql table definitions. Used by both
src/api.py (FastAPI) and src/tui.py (Textual dashboard).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

# ── Metrics ────────────────────────────────────────────────


class MetricOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    type: str
    unit: str | None = None
    dimensions: list[str] | None = None
    description: str | None = None


class MetricValueOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    recorded_at: str | None = None
    value: float
    tags: dict[str, str] | None = None


class MetricSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    group_key: str | None = None
    count: int
    avg: float
    min: float
    max: float
    p50: float
    p99: float


# ── Tasks ──────────────────────────────────────────────────


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    queue_name: str
    type: str
    status: str
    priority: int
    skill_name: str | None = None
    model_id: str | None = None
    plugin: str | None = None
    attempts: int | None = None
    created_at: str | None = None
    started_at: str | None = None
    completed_at: str | None = None


class TaskCreateIn(BaseModel):
    queue_name: str
    task_type: str = "knowledge_work"
    skill_name: str | None = None
    model_id: str | None = None
    plugin: str | None = None
    task_input: dict | None = None
    config: dict | None = None
    priority: int = 0


class TaskStatsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    type: str
    queue_name: str | None = None
    count: int
    avg_duration_s: float | None = None


# ── Agents ─────────────────────────────────────────────────


class AgentManifestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    model_id: str | None = None
    allowed_tools: list[str] | None = None
    denied_tools: list[str] | None = None
    description: str | None = None


# ── Skills ─────────────────────────────────────────────────


class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None
    trigger_pattern: str | None = None


# ── Models ─────────────────────────────────────────────────


class ModelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    model_id: str
    family: str
    label: str
    supports_thinking: bool = False
    supports_tool_use: bool = False
    supports_vision: bool = False


# ── Pipelines ──────────────────────────────────────────────


class PipelineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    skill_name: str
    model_id: str | None = None
    config: dict | None = None
    status: str
    created_at: str | None = None
    updated_at: str | None = None


# ── Resources ──────────────────────────────────────────────


class ResourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None
    type: str
    label: str
    url: str
    content_hash: str | None = None
    description: str | None = None


class SearchResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sim: float | None = None


# ── Skill Registry ────────────────────────────────────────


class SkillRegistryOut(BaseModel):
    """Skill catalog entry with category routing metadata."""

    name: str
    category: str
    agent: str
