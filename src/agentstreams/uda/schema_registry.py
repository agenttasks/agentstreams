"""UDA Schema Registry — single source of truth for all entity schemas.

Netflix UDA principle: "Model once, represent everywhere." Each entity is defined
once as a Python dataclass, then projected into Avro, GraphQL, TTL, and SQL
representations via the registry.

Entities map 1:1 to ontology classes in ontology/agentstreams.ttl and physical
tables in ontology/schema.sql.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, fields
from datetime import datetime
from enum import Enum
from typing import Any


# ── Enumerations ────────────────────────────────────────────


class LanguageTier(str, Enum):
    TIER1 = "tier1"
    TIER2 = "tier2"
    TIER3 = "tier3"


class MetricType(str, Enum):
    COUNTER = "counter"
    TIMER = "timer"
    GAUGE = "gauge"
    DISTRIBUTION_SUMMARY = "distribution_summary"


class TaskType(str, Enum):
    CODE = "code"
    KNOWLEDGE_WORK = "knowledge_work"
    FINANCIAL = "financial"


class TaskStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PipelineStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class ResourceType(str, Enum):
    MODEL_CARD = "model_card"
    API_PRIMER = "api_primer"
    LLMS_INDEX = "llms_index"
    COOKBOOK = "cookbook"
    CRAWLED_PAGE = "crawled_page"


# ── Core Entities (UDA canonical model) ─────────────────────


@dataclass
class Language:
    """Programming language supported by the skill system."""

    id: str
    label: str
    tier: LanguageTier | None = None


@dataclass
class Model:
    """Claude model version with specific capabilities."""

    model_id: str
    family: str
    label: str
    supports_thinking: bool = False
    supports_tool_use: bool = False
    supports_vision: bool = False
    created_at: datetime | None = None


@dataclass
class Skill:
    """Multi-language capability package."""

    name: str
    description: str
    trigger_pattern: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class SDK:
    """Anthropic SDK for a specific language."""

    id: str
    language_id: str
    label: str
    constructor_pattern: str
    github_stars: int | None = None
    repo_url: str | None = None


@dataclass
class MCPServer:
    """Model Context Protocol server."""

    id: str
    name: str
    version: str | None = None
    transport: str | None = None
    description: str | None = None
    created_at: datetime | None = None


@dataclass
class Package:
    """Third-party library used within a skill."""

    id: int | None = None
    name: str = ""
    version: str | None = None
    language_id: str = ""
    skill_name: str = ""
    purpose: str | None = None


@dataclass
class Metric:
    """Dimensional time-series metric (Atlas/Spectator pattern)."""

    name: str
    type: MetricType
    unit: str | None = None
    dimensions: list[str] = field(default_factory=list)
    description: str | None = None


@dataclass
class MetricValue:
    """Single metric observation — fact table grain."""

    id: int | None = None
    metric_name: str = ""
    value: float = 0.0
    tags: dict[str, str] = field(default_factory=dict)
    recorded_at: datetime | None = None


@dataclass
class Pipeline:
    """Data processing pipeline instance."""

    id: int | None = None
    name: str = ""
    skill_name: str | None = None
    model_id: str | None = None
    config: dict[str, Any] = field(default_factory=dict)
    status: PipelineStatus = PipelineStatus.ACTIVE
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Resource:
    """External documentation or reference resource."""

    id: int | None = None
    type: ResourceType = ResourceType.CRAWLED_PAGE
    label: str = ""
    url: str = ""
    related_model_id: str | None = None
    description: str | None = None
    fetched_at: datetime | None = None
    content_hash: str | None = None


@dataclass
class Task:
    """Queued unit of work — code, knowledge-work, or financial."""

    id: int | None = None
    queue_name: str = ""
    type: TaskType = TaskType.CODE
    status: TaskStatus = TaskStatus.QUEUED
    priority: int = 0
    skill_name: str | None = None
    model_id: str | None = None
    plugin: str | None = None
    input: dict[str, Any] = field(default_factory=dict)
    config: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] | None = None
    error: str | None = None
    attempts: int = 0
    max_attempts: int = 3
    execute_after: datetime | None = None
    created_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


@dataclass
class CrawledPage:
    """A page fetched by a crawler — extends Resource with crawl metadata."""

    url: str = ""
    domain: str = ""
    content: str = ""
    content_hash: str = ""
    page_type: str = "guide"
    topics: list[str] = field(default_factory=list)
    is_duplicate: bool = False
    crawled_at: datetime | None = None


# ── Schema Registry ─────────────────────────────────────────

# Maps entity name → (dataclass, table_name, ontology_class_uri)
_REGISTRY: dict[str, tuple[type, str, str]] = {
    "Language": (Language, "languages", "as:Language"),
    "Model": (Model, "models", "as:Model"),
    "Skill": (Skill, "skills", "as:Skill"),
    "SDK": (SDK, "sdks", "as:SDK"),
    "MCPServer": (MCPServer, "mcp_servers", "as:MCPServer"),
    "Package": (Package, "packages", "as:Package"),
    "Metric": (Metric, "metrics", "as:Metric"),
    "MetricValue": (MetricValue, "metric_values", "as:Metric"),
    "Pipeline": (Pipeline, "pipelines", "as:Pipeline"),
    "Resource": (Resource, "resources", "as:Resource"),
    "Task": (Task, "tasks", "as:Task"),
    "CrawledPage": (CrawledPage, "resources", "as:Resource"),
}


def get_entity_class(name: str) -> type:
    """Look up entity dataclass by name."""
    return _REGISTRY[name][0]


def get_table_name(name: str) -> str:
    """Look up physical table for an entity."""
    return _REGISTRY[name][1]


def get_ontology_uri(name: str) -> str:
    """Look up ontology class URI for an entity."""
    return _REGISTRY[name][2]


def list_entities() -> list[str]:
    """List all registered entity names."""
    return list(_REGISTRY.keys())


def to_avro_schema(entity_name: str) -> dict[str, Any]:
    """Generate Avro schema from a registered entity.

    Netflix UDA uses Avro as the canonical serialization format.
    """
    cls = get_entity_class(entity_name)
    avro_fields = []
    for f in fields(cls):
        avro_type = _python_type_to_avro(f.type, f.name)
        avro_fields.append({"name": f.name, "type": avro_type})

    return {
        "type": "record",
        "name": entity_name,
        "namespace": "dev.agentstreams",
        "doc": cls.__doc__ or "",
        "fields": avro_fields,
    }


def to_graphql_type(entity_name: str) -> str:
    """Generate GraphQL type definition from a registered entity.

    Netflix UDA exposes entities via GraphQL for API consumption.
    """
    cls = get_entity_class(entity_name)
    lines = [f"type {entity_name} {{"]
    for f in fields(cls):
        gql_type = _python_type_to_graphql(f.type, f.name)
        lines.append(f"  {f.name}: {gql_type}")
    lines.append("}")
    return "\n".join(lines)


def to_dict(instance: Any) -> dict[str, Any]:
    """Serialize a dataclass instance to a dict suitable for JSON/DB insertion."""
    result = {}
    for f in fields(instance):
        val = getattr(instance, f.name)
        if isinstance(val, Enum):
            val = val.value
        elif isinstance(val, datetime):
            val = val.isoformat()
        elif isinstance(val, (dict, list)):
            val = json.dumps(val) if not isinstance(val, str) else val
        result[f.name] = val
    return result


# ── Type mapping helpers ────────────────────────────────────


def _python_type_to_avro(type_hint: Any, field_name: str) -> Any:
    """Map Python type hints to Avro types."""
    type_str = str(type_hint)
    if "int" in type_str:
        if field_name == "id":
            return ["null", "long"]
        return "int" if "None" not in type_str else ["null", "int"]
    if "float" in type_str:
        return "double" if "None" not in type_str else ["null", "double"]
    if "bool" in type_str:
        return "boolean" if "None" not in type_str else ["null", "boolean"]
    if "datetime" in type_str:
        return ["null", {"type": "long", "logicalType": "timestamp-millis"}]
    if "list" in type_str:
        return {"type": "array", "items": "string"}
    if "dict" in type_str:
        return ["null", {"type": "map", "values": "string"}]
    # Default to string
    return "string" if "None" not in type_str else ["null", "string"]


def _python_type_to_graphql(type_hint: Any, field_name: str) -> str:
    """Map Python type hints to GraphQL types."""
    type_str = str(type_hint)
    nullable = "None" in type_str
    suffix = "" if nullable else "!"

    if "int" in type_str:
        base = "Int"
    elif "float" in type_str:
        base = "Float"
    elif "bool" in type_str:
        base = "Boolean"
    elif "datetime" in type_str:
        base = "DateTime"
    elif "list" in type_str:
        base = "[String]"
    elif "dict" in type_str:
        base = "JSON"
    else:
        base = "String"

    if field_name == "id" and "int" in type_str:
        return "ID"

    return f"{base}{suffix}"
