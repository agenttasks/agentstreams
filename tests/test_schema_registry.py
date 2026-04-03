"""Tests for the UDA schema registry."""

from agentstreams.uda.schema_registry import (
    CrawledPage,
    Language,
    LanguageTier,
    Metric,
    MetricType,
    Model,
    Skill,
    Task,
    TaskStatus,
    TaskType,
    get_entity_class,
    get_ontology_uri,
    get_table_name,
    list_entities,
    to_avro_schema,
    to_dict,
    to_graphql_type,
)


def test_list_entities():
    entities = list_entities()
    assert "Language" in entities
    assert "Model" in entities
    assert "Skill" in entities
    assert "Task" in entities
    assert "CrawledPage" in entities


def test_get_entity_class():
    assert get_entity_class("Language") is Language
    assert get_entity_class("Model") is Model
    assert get_entity_class("Task") is Task


def test_get_table_name():
    assert get_table_name("Language") == "languages"
    assert get_table_name("Model") == "models"
    assert get_table_name("Task") == "tasks"


def test_get_ontology_uri():
    assert get_ontology_uri("Skill") == "as:Skill"
    assert get_ontology_uri("Metric") == "as:Metric"


def test_to_avro_schema():
    schema = to_avro_schema("Language")
    assert schema["type"] == "record"
    assert schema["name"] == "Language"
    assert schema["namespace"] == "dev.agentstreams"
    field_names = [f["name"] for f in schema["fields"]]
    assert "id" in field_names
    assert "label" in field_names


def test_to_graphql_type():
    gql = to_graphql_type("Language")
    assert "type Language {" in gql
    assert "id:" in gql
    assert "label:" in gql


def test_to_dict():
    lang = Language(id="python", label="Python", tier=LanguageTier.TIER1)
    d = to_dict(lang)
    assert d["id"] == "python"
    assert d["label"] == "Python"
    assert d["tier"] == "tier1"


def test_to_dict_task():
    task = Task(
        queue_name="crawl-analyze",
        type=TaskType.KNOWLEDGE_WORK,
        status=TaskStatus.QUEUED,
        input={"url": "https://example.com"},
    )
    d = to_dict(task)
    assert d["queue_name"] == "crawl-analyze"
    assert d["type"] == "knowledge_work"
    assert d["status"] == "queued"


def test_avro_schema_all_entities():
    """Every registered entity should produce a valid Avro schema."""
    for name in list_entities():
        schema = to_avro_schema(name)
        assert schema["type"] == "record"
        assert schema["name"] == name
        assert len(schema["fields"]) > 0


def test_graphql_type_all_entities():
    """Every registered entity should produce a valid GraphQL type."""
    for name in list_entities():
        gql = to_graphql_type(name)
        assert f"type {name} {{" in gql


def test_model_entity():
    m = Model(
        model_id="claude-opus-4-6",
        family="Claude 4.6",
        label="Claude Opus 4.6",
        supports_thinking=True,
        supports_tool_use=True,
        supports_vision=True,
    )
    d = to_dict(m)
    assert d["model_id"] == "claude-opus-4-6"
    assert d["supports_thinking"] is True


def test_crawled_page_entity():
    page = CrawledPage(
        url="https://example.com/page",
        domain="example.com",
        content="Hello world",
        content_hash="abc123",
        page_type="guide",
        topics=["agents", "mcp"],
    )
    assert page.url == "https://example.com/page"
    assert page.topics == ["agents", "mcp"]


def test_metric_entity():
    m = Metric(
        name="agentstreams.crawl.pages",
        type=MetricType.COUNTER,
        unit="pages",
        dimensions=["domain", "status", "is_new"],
    )
    d = to_dict(m)
    assert d["name"] == "agentstreams.crawl.pages"
    assert d["type"] == "counter"
