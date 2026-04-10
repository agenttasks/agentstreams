"""Tests for src/cube_models.py — Cube.dev YAML data model generation."""

from __future__ import annotations

import yaml
import pytest

from src.cube_models import (
    CubeDefinition,
    CubeProjection,
    Dimension,
    Join,
    Measure,
    _classify_ontology_class,
    _property_to_column,
)
from src.projections import OntologyParser


@pytest.fixture
def parser():
    """Parse the real ontology file."""
    p = OntologyParser()
    p.parse()
    return p


@pytest.fixture
def cube_projection(parser):
    return CubeProjection(parser)


class TestPropertyToColumn:
    def test_camel_case(self):
        assert _property_to_column("skillName") == "skill_name"

    def test_multiple_words(self):
        assert _property_to_column("supportsThinking") == "supports_thinking"

    def test_single_word(self):
        assert _property_to_column("name") == "name"

    def test_id_suffix(self):
        assert _property_to_column("modelId") == "model_id"


class TestClassifyOntologyClass:
    def test_classify_with_parser(self, parser):
        """Verify classification works on real ontology classes."""
        for cls in parser.classes.values():
            result = _classify_ontology_class(cls)
            assert result in {
                "transaction_fact",
                "accumulating_snapshot",
                "dimension",
                "factless_fact",
            }


class TestCubeProjection:
    def test_generate_known_class(self, cube_projection, parser):
        """Generate a cube for a known ontology class."""
        # Pick any class that exists
        class_name = next(iter(parser.classes))
        cube = cube_projection.generate(class_name)
        assert isinstance(cube, CubeDefinition)
        assert cube.name
        assert cube.sql_table
        assert len(cube.dimensions) > 0
        assert len(cube.measures) > 0  # At least 'count'

    def test_generate_unknown_class_raises(self, cube_projection):
        with pytest.raises(ValueError, match="Unknown class"):
            cube_projection.generate("NonExistent")

    def test_generate_all(self, cube_projection, parser):
        cubes = cube_projection.generate_all()
        assert len(cubes) == len(parser.classes)
        for cube in cubes:
            assert isinstance(cube, CubeDefinition)

    def test_count_measure_always_present(self, cube_projection, parser):
        """Every cube gets a count measure."""
        for class_name in parser.classes:
            cube = cube_projection.generate(class_name)
            measure_names = {m.name for m in cube.measures}
            assert "count" in measure_names

    def test_kimball_type_assigned(self, cube_projection, parser):
        for class_name in parser.classes:
            cube = cube_projection.generate(class_name)
            assert cube.kimball_type in {
                "transaction_fact",
                "accumulating_snapshot",
                "dimension",
                "factless_fact",
            }

    def test_relationship_properties_become_joins(self, cube_projection, parser):
        """Classes with relationship properties should have joins."""
        for cls in parser.classes.values():
            has_relationships = any(p.is_relationship for p in cls.properties)
            if has_relationships:
                cube = cube_projection.generate(cls.name)
                assert len(cube.joins) > 0
                for join in cube.joins:
                    assert "{CUBE}" in join.sql
                break  # Just need one example


class TestCubeYAMLOutput:
    def test_to_yaml_valid(self, cube_projection, parser):
        class_name = next(iter(parser.classes))
        yaml_str = cube_projection.to_yaml(class_name)
        parsed = yaml.safe_load(yaml_str)
        assert "cubes" in parsed
        assert len(parsed["cubes"]) == 1

    def test_to_yaml_all_valid(self, cube_projection, parser):
        yaml_str = cube_projection.to_yaml_all()
        parsed = yaml.safe_load(yaml_str)
        assert "cubes" in parsed
        assert len(parsed["cubes"]) == len(parser.classes)

    def test_yaml_structure_matches_julia_models(self, cube_projection, parser):
        """Generated YAML should have the same keys as julia/models/*.yaml."""
        class_name = next(iter(parser.classes))
        yaml_str = cube_projection.to_yaml(class_name)
        parsed = yaml.safe_load(yaml_str)
        cube = parsed["cubes"][0]

        # Required keys per Cube.dev spec
        assert "name" in cube
        assert "sql" in cube

        # Optional but expected keys
        if "dimensions" in cube:
            for dim in cube["dimensions"]:
                assert "name" in dim
                assert "sql" in dim
                assert "type" in dim

        if "measures" in cube:
            for measure in cube["measures"]:
                assert "name" in measure
                assert "type" in measure

        if "joins" in cube:
            for join in cube["joins"]:
                assert "name" in join
                assert "relationship" in join
                assert "sql" in join

    def test_dimension_types_valid(self, cube_projection, parser):
        """All dimension types should be valid Cube.dev types."""
        valid_types = {"string", "number", "time", "boolean"}
        for class_name in parser.classes:
            cube = cube_projection.generate(class_name)
            for dim in cube.dimensions:
                assert dim.type in valid_types, f"Invalid type {dim.type} for {dim.name}"

    def test_measure_types_valid(self, cube_projection, parser):
        """All measure types should be valid Cube.dev aggregation types."""
        valid_types = {"count", "sum", "avg", "min", "max", "count_distinct"}
        for class_name in parser.classes:
            cube = cube_projection.generate(class_name)
            for measure in cube.measures:
                assert measure.type in valid_types, f"Invalid type {measure.type} for {measure.name}"
