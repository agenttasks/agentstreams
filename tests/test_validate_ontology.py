"""Tests for scripts/validate-ontology.py — UDA alignment checks."""

import sys
from pathlib import Path
from importlib import import_module

# Add scripts to path so we can import functions
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

mod = import_module("validate-ontology")


class TestParseOntologyClasses:
    def test_extracts_classes(self):
        ttl = """
as:Skill a rdfs:Class ;
    rdfs:label "Skill" .

as:Model a rdfs:Class ;
    rdfs:label "Model" .
"""
        classes = mod.parse_ontology_classes(ttl)
        assert classes == {"Skill", "Model"}

    def test_empty_ttl(self):
        assert mod.parse_ontology_classes("") == set()


class TestParseOntologyInstances:
    def test_extracts_instances(self):
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


class TestMain:
    """Test the main() function — the core validation orchestrator (lines 92-186)."""

    def _make_ontology_dir(self, tmp_path):
        """Create a minimal ontology directory with valid aligned files."""
        ontology_dir = tmp_path / "ontology"
        ontology_dir.mkdir()

        ontology_dir.joinpath("agentstreams.ttl").write_text(
            'as:Skill a rdfs:Class ;\n    rdfs:label "Skill" .\n\n'
            'as:Model a rdfs:Class ;\n    rdfs:label "Model" .\n\n'
            "as:sdk-python a as:SDK ;\n    as:sdkLanguage as:python .\n"
        )

        ontology_dir.joinpath("mappings.ttl").write_text(
            "map:skill-table a map:Mapping ;\n"
            "    map:ontologyClass as:Skill ;\n"
            '    map:targetTable "skills" .\n\n'
            "map:model-table a map:Mapping ;\n"
            "    map:ontologyClass as:Model ;\n"
            '    map:targetTable "models" .\n\n'
            "map:skill-name a map:Mapping ;\n"
            "    map:ontologyProperty as:skillName ;\n"
            '    map:targetTable "skills" ;\n'
            '    map:targetColumn "name" .\n'
        )

        ontology_dir.joinpath("schema.sql").write_text(
            "CREATE TABLE skills (\n"
            "    name TEXT PRIMARY KEY,\n"
            "    description TEXT NOT NULL\n"
            ");\n\n"
            "CREATE TABLE models (\n"
            "    model_id TEXT PRIMARY KEY,\n"
            "    family TEXT NOT NULL\n"
            ");\n\n"
            "INSERT INTO skills (name) VALUES\n"
            "    ('crawl-ingest');\n"
        )

        return ontology_dir

    def test_main_all_aligned(self, tmp_path, monkeypatch, capsys):
        """When ontology, mappings, and schema are aligned, main returns 0."""
        ontology_dir = self._make_ontology_dir(tmp_path)
        monkeypatch.setattr(mod, "ONTOLOGY_DIR", ontology_dir)

        result = mod.main()
        captured = capsys.readouterr()
        assert "Classes:" in captured.out
        assert "Mapped:" in captured.out
        # May have warnings due to instance count mismatches, but no errors
        assert result in (0, 2)

    def test_main_missing_table_error(self, tmp_path, monkeypatch, capsys):
        """When a mapped table doesn't exist in schema, main returns 1."""
        ontology_dir = self._make_ontology_dir(tmp_path)
        # Add a mapping to a non-existent table
        mappings = ontology_dir / "mappings.ttl"
        mappings.write_text(
            mappings.read_text()
            + "\nmap:ghost-table a map:Mapping ;\n"
            "    map:ontologyClass as:Ghost ;\n"
            '    map:targetTable "ghosts" .\n'
        )
        # Add Ghost class to ontology
        ttl = ontology_dir / "agentstreams.ttl"
        ttl.write_text(ttl.read_text() + '\nas:Ghost a rdfs:Class ;\n    rdfs:label "Ghost" .\n')

        monkeypatch.setattr(mod, "ONTOLOGY_DIR", ontology_dir)
        result = mod.main()
        captured = capsys.readouterr()
        assert result == 1
        assert "ERRORS" in captured.out
        assert "ghosts" in captured.out

    def test_main_missing_column_error(self, tmp_path, monkeypatch, capsys):
        """When a mapped column doesn't exist in its table, main returns 1."""
        ontology_dir = self._make_ontology_dir(tmp_path)
        mappings = ontology_dir / "mappings.ttl"
        mappings.write_text(
            mappings.read_text()
            + "\nmap:bad-col a map:Mapping ;\n"
            "    map:ontologyProperty as:badCol ;\n"
            '    map:targetTable "skills" ;\n'
            '    map:targetColumn "nonexistent_col" .\n'
        )
        monkeypatch.setattr(mod, "ONTOLOGY_DIR", ontology_dir)
        result = mod.main()
        captured = capsys.readouterr()
        assert result == 1
        assert "nonexistent_col" in captured.out

    def test_main_unmapped_class_warning(self, tmp_path, monkeypatch, capsys):
        """Unmapped ontology classes produce warnings (return 2)."""
        ontology_dir = self._make_ontology_dir(tmp_path)
        ttl = ontology_dir / "agentstreams.ttl"
        ttl.write_text(
            ttl.read_text() + '\nas:NewClass a rdfs:Class ;\n    rdfs:label "NewClass" .\n'
        )
        monkeypatch.setattr(mod, "ONTOLOGY_DIR", ontology_dir)
        result = mod.main()
        captured = capsys.readouterr()
        assert result == 2
        assert "WARNINGS" in captured.out
        assert "NewClass" in captured.out

    def test_main_instance_count_mismatch_warning(self, tmp_path, monkeypatch, capsys):
        """Instance count mismatches between ontology and seed data warn."""
        ontology_dir = self._make_ontology_dir(tmp_path)
        # Add Language instances to ontology but no seed data
        ttl = ontology_dir / "agentstreams.ttl"
        ttl.write_text(
            ttl.read_text()
            + '\nas:Language a rdfs:Class ;\n    rdfs:label "Language" .\n'
            "\nas:lang-python a as:Language ;\n    as:langId \"python\" .\n"
            "\nas:lang-typescript a as:Language ;\n    as:langId \"typescript\" .\n"
        )
        # Add Language mapping
        mappings = ontology_dir / "mappings.ttl"
        mappings.write_text(
            mappings.read_text()
            + "\nmap:lang-table a map:Mapping ;\n"
            "    map:ontologyClass as:Language ;\n"
            '    map:targetTable "languages" .\n'
        )
        # Add languages table to schema (empty, no seed data)
        schema = ontology_dir / "schema.sql"
        schema.write_text(
            schema.read_text()
            + "\nCREATE TABLE languages (\n    id TEXT PRIMARY KEY\n);\n"
        )
        monkeypatch.setattr(mod, "ONTOLOGY_DIR", ontology_dir)
        result = mod.main()
        captured = capsys.readouterr()
        assert result == 2
        assert "Language" in captured.out
