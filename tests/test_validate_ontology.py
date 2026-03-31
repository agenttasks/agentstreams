"""Tests for scripts/validate-ontology.py — UDA alignment checks."""

import sys
from pathlib import Path

# Add scripts to path so we can import functions
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


class TestParseOntologyClasses:
    def test_extracts_classes(self):
        from importlib import import_module

        mod = import_module("validate-ontology")
        ttl = """
as:Skill a rdfs:Class ;
    rdfs:label "Skill" .

as:Model a rdfs:Class ;
    rdfs:label "Model" .
"""
        classes = mod.parse_ontology_classes(ttl)
        assert classes == {"Skill", "Model"}

    def test_empty_ttl(self):
        from importlib import import_module

        mod = import_module("validate-ontology")
        assert mod.parse_ontology_classes("") == set()


class TestParseOntologyInstances:
    def test_extracts_instances(self):
        from importlib import import_module

        mod = import_module("validate-ontology")
        ttl = """
as:metric-api-requests a as:Metric ;
    as:metricName "agentstreams.api.requests" .

as:metric-api-tokens a as:Metric ;
    as:metricName "agentstreams.api.tokens" .

as:sdk-python a as:SDK ;
    as:sdkLanguage as:python .
"""
        instances = mod.parse_ontology_instances(ttl)
        assert len(instances["Metric"]) == 2
        assert "metric-api-requests" in instances["Metric"]
        assert len(instances["SDK"]) == 1


class TestParseMappingTables:
    def test_extracts_class_table_mapping(self):
        from importlib import import_module

        mod = import_module("validate-ontology")
        ttl = """
map:skill-table a map:Mapping ;
    map:ontologyClass as:Skill ;
    map:targetTable "skills" ;
    rdfs:label "Skill → skills table" .

map:model-table a map:Mapping ;
    map:ontologyClass as:Model ;
    map:targetTable "models" ;
    rdfs:label "Model → models table" .
"""
        mappings = mod.parse_mapping_tables(ttl)
        assert mappings["Skill"] == "skills"
        assert mappings["Model"] == "models"


class TestParseMappingColumns:
    def test_extracts_property_column_mapping(self):
        from importlib import import_module

        mod = import_module("validate-ontology")
        ttl = """
map:skill-name a map:Mapping ;
    map:ontologyProperty as:skillName ;
    map:targetTable "skills" ;
    map:targetColumn "name" .

map:model-id a map:Mapping ;
    map:ontologyProperty as:modelId ;
    map:targetTable "models" ;
    map:targetColumn "model_id" .
"""
        columns = mod.parse_mapping_columns(ttl)
        assert len(columns) == 2
        assert ("skillName", "skills", "name") in columns
        assert ("modelId", "models", "model_id") in columns


class TestParseSchemaTables:
    def test_extracts_tables_and_columns(self):
        from importlib import import_module

        mod = import_module("validate-ontology")
        sql = """
CREATE TABLE skills (
    name TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    trigger_pattern TEXT
);

CREATE TABLE models (
    model_id TEXT PRIMARY KEY,
    family TEXT NOT NULL,
    label TEXT NOT NULL
);
"""
        tables = mod.parse_schema_tables(sql)
        assert "skills" in tables
        assert "name" in tables["skills"]
        assert "description" in tables["skills"]
        assert "models" in tables
        assert "model_id" in tables["models"]

    def test_skips_constraints(self):
        from importlib import import_module

        mod = import_module("validate-ontology")
        sql = """
CREATE TABLE tasks (
    id BIGSERIAL PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'processing'))
);
"""
        tables = mod.parse_schema_tables(sql)
        assert "id" in tables["tasks"]
        assert "status" in tables["tasks"]
        assert "CHECK" not in tables["tasks"]


class TestParseSeedCounts:
    def test_counts_seed_rows(self):
        from importlib import import_module

        mod = import_module("validate-ontology")
        sql = """
INSERT INTO languages (id, label) VALUES
    ('typescript', 'TypeScript'),
    ('python', 'Python'),
    ('java', 'Java');

INSERT INTO models (model_id, family, label) VALUES
    ('claude-opus-4-6', 'Claude 4.6', 'Claude Opus 4.6'),
    ('claude-sonnet-4-6', 'Claude 4.6', 'Claude Sonnet 4.6');
"""
        counts = mod.parse_seed_counts(sql)
        assert counts["languages"] == 3
        assert counts["models"] == 2
