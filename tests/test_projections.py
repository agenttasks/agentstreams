"""Tests for src/projections.py — UDA ontology projection generators."""

from __future__ import annotations

import json

import pytest

from src.projections import (
    AvroProjection,
    DataContainerProjection,
    GraphQLProjection,
    MappingProjection,
    OntologyParser,
)


@pytest.fixture
def parser():
    """Parse the real ontology file."""
    p = OntologyParser()
    p.parse()
    return p


class TestOntologyParser:
    def test_parses_classes(self, parser):
        assert len(parser.classes) > 0
        assert "Skill" in parser.classes
        assert "Model" in parser.classes

    def test_skill_class_has_properties(self, parser):
        skill = parser.classes.get("Skill")
        assert skill is not None
        prop_names = [p.name for p in skill.properties]
        assert "skillName" in prop_names

    def test_parses_properties(self, parser):
        assert len(parser.properties) > 0
        assert "skillName" in parser.properties
        assert "bloomName" in parser.properties

    def test_property_domain_and_range(self, parser):
        prop = parser.properties.get("skillName")
        assert prop is not None
        assert prop.domain == "Skill"
        assert prop.range_type == "xsd:string"
        assert prop.is_relationship is False

    def test_relationship_property(self, parser):
        # supportsLanguage should be a relationship
        prop = parser.properties.get("supportsLanguage")
        assert prop is not None
        assert prop.is_relationship is True
        assert prop.range_type == "as:Language"


class TestAvroProjection:
    def test_generates_valid_schema(self, parser):
        avro = AvroProjection(parser)
        schema = avro.generate("Skill")
        assert schema["type"] == "record"
        assert schema["name"] == "AS_Skill"
        assert schema["namespace"] == "dev.agentstreams"
        assert "udaUri" in schema

    def test_fields_have_uda_uri(self, parser):
        avro = AvroProjection(parser)
        schema = avro.generate("Skill")
        for field in schema["fields"]:
            assert "udaUri" in field
            assert field["udaUri"].startswith("https://agentstreams.dev/ontology#")

    def test_relationship_fields_are_nullable(self, parser):
        avro = AvroProjection(parser)
        schema = avro.generate("Skill")
        for field in schema["fields"]:
            if isinstance(field["type"], list) and len(field["type"]) == 2:
                assert field["type"][0] == "null"

    def test_to_json_produces_valid_json(self, parser):
        avro = AvroProjection(parser)
        json_str = avro.to_json("Skill")
        parsed = json.loads(json_str)
        assert parsed["name"] == "AS_Skill"

    def test_generate_all(self, parser):
        avro = AvroProjection(parser)
        schemas = avro.generate_all()
        assert len(schemas) == len(parser.classes)

    def test_unknown_class_raises(self, parser):
        avro = AvroProjection(parser)
        with pytest.raises(ValueError, match="Unknown class"):
            avro.generate("NonExistent")


class TestGraphQLProjection:
    def test_generates_type_with_directives(self, parser):
        gql = GraphQLProjection(parser)
        output = gql.generate("Skill")
        assert "type AS_Skill" in output
        assert "@key" in output
        assert "@udaUri" in output

    def test_generates_enums(self, parser):
        gql = GraphQLProjection(parser)
        enums = gql.generate_enums()
        # Should have at least the enum types from the ontology
        assert isinstance(enums, str)

    def test_generate_all_includes_directives(self, parser):
        gql = GraphQLProjection(parser)
        full = gql.generate_all()
        assert "directive @key" in full
        assert "directive @udaUri" in full

    def test_unknown_class_raises(self, parser):
        gql = GraphQLProjection(parser)
        with pytest.raises(ValueError, match="Unknown class"):
            gql.generate("NonExistent")


class TestDataContainerProjection:
    def test_generates_ttl(self, parser):
        dc = DataContainerProjection(parser)
        output = dc.generate("Skill")
        assert "@prefix as:" in output
        assert "datamesh:Source" in output
        assert "dc:Skill_source" in output

    def test_includes_field_projections(self, parser):
        dc = DataContainerProjection(parser)
        output = dc.generate("Skill")
        assert "datamesh:Field" in output

    def test_unknown_class_raises(self, parser):
        dc = DataContainerProjection(parser)
        with pytest.raises(ValueError, match="Unknown class"):
            dc.generate("NonExistent")


class TestMappingProjection:
    def test_generates_mapping_ttl(self, parser):
        mp = MappingProjection(parser)
        output = mp.generate("Skill", "skills")
        assert "map:skill-table" in output
        assert '"skills"' in output
        assert "map:Mapping" in output

    def test_snake_case_conversion(self):
        assert MappingProjection._property_to_column("skillName") == "skill_name"
        assert MappingProjection._property_to_column("modelId") == "model_id"
        assert MappingProjection._property_to_column("supportsThinking") == "supports_thinking"
        assert MappingProjection._property_to_column("name") == "name"

    def test_unknown_class_raises(self, parser):
        mp = MappingProjection(parser)
        with pytest.raises(ValueError, match="Unknown class"):
            mp.generate("NonExistent")
