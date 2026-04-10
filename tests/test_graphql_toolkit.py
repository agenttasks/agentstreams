"""Tests for src/graphql_toolkit.py — GraphQL schema parser and toolkit."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.graphql_toolkit import (
    GraphQLSchemaParser,
    validate_schema_against_ontology,
)


@pytest.fixture
def parser():
    return GraphQLSchemaParser()


@pytest.fixture
def sample_sdl():
    """Load the existing test GraphQL schema."""
    schema_path = (
        Path(__file__).parent.parent
        / "evals"
        / "api-client"
        / "test_data"
        / "graphql_schema.graphql"
    )
    return schema_path.read_text()


@pytest.fixture
def parsed_types(parser, sample_sdl):
    return parser.parse(sample_sdl)


class TestGraphQLSchemaParser:
    def test_parses_object_types(self, parsed_types):
        object_types = [t for t in parsed_types if t.kind == "OBJECT"]
        type_names = {t.name for t in object_types}
        assert "User" in type_names
        assert "Post" in type_names
        assert "Query" in type_names

    def test_parses_enum_types(self, parsed_types):
        enum_types = [t for t in parsed_types if t.kind == "ENUM"]
        assert len(enum_types) >= 1
        role_enum = next((t for t in enum_types if t.name == "Role"), None)
        assert role_enum is not None
        assert "ADMIN" in role_enum.enum_values
        assert "USER" in role_enum.enum_values
        assert "MODERATOR" in role_enum.enum_values

    def test_parses_scalar_types(self, parsed_types):
        scalar_types = [t for t in parsed_types if t.kind == "SCALAR"]
        scalar_names = {t.name for t in scalar_types}
        assert "DateTime" in scalar_names

    def test_parses_input_types(self, parsed_types):
        input_types = [t for t in parsed_types if t.kind == "INPUT"]
        input_names = {t.name for t in input_types}
        assert "CreateUserInput" in input_names
        assert "UpdateUserInput" in input_names

    def test_user_type_fields(self, parsed_types):
        user = next(t for t in parsed_types if t.name == "User")
        field_names = {f.name for f in user.fields}
        assert "id" in field_names
        assert "email" in field_names
        assert "name" in field_names
        assert "role" in field_names
        assert "posts" in field_names
        assert "createdAt" in field_names

    def test_field_types_resolved(self, parsed_types):
        user = next(t for t in parsed_types if t.name == "User")
        id_field = next(f for f in user.fields if f.name == "id")
        assert id_field.type_name == "ID"
        assert id_field.is_non_null is True

    def test_list_fields_detected(self, parsed_types):
        user = next(t for t in parsed_types if t.name == "User")
        posts_field = next(f for f in user.fields if f.name == "posts")
        assert posts_field.is_list is True

    def test_query_type_has_arguments(self, parsed_types):
        query = next(t for t in parsed_types if t.name == "Query")
        user_field = next(f for f in query.fields if f.name == "user")
        assert len(user_field.arguments) >= 1
        assert user_field.arguments[0].name == "id"

    def test_mutation_type_parsed(self, parsed_types):
        mutation = next((t for t in parsed_types if t.name == "Mutation"), None)
        assert mutation is not None
        field_names = {f.name for f in mutation.fields}
        assert "createUser" in field_names

    def test_connection_types_parsed(self, parsed_types):
        type_names = {t.name for t in parsed_types}
        assert "UserConnection" in type_names
        assert "UserEdge" in type_names
        assert "PageInfo" in type_names

    def test_parse_file(self, parser):
        schema_path = (
            Path(__file__).parent.parent
            / "evals"
            / "api-client"
            / "test_data"
            / "graphql_schema.graphql"
        )
        types = parser.parse_file(schema_path)
        assert len(types) > 0

    def test_parse_empty_schema(self, parser):
        types = parser.parse("")
        assert types == []

    def test_parse_minimal_schema(self, parser):
        sdl = """
        type Foo {
          id: ID!
          name: String
        }
        """
        types = parser.parse(sdl)
        assert len(types) == 1
        assert types[0].name == "Foo"
        assert types[0].kind == "OBJECT"
        assert len(types[0].fields) == 2


class TestValidateSchemaAgainstOntology:
    def test_detects_missing_ontology_class(self, parsed_types):
        # Provide empty ontology — all GraphQL types should be flagged
        warnings = validate_schema_against_ontology(parsed_types, {})
        assert len(warnings) > 0
        assert any("has no corresponding ontology class" in w for w in warnings)

    def test_detects_missing_graphql_type(self):
        # Provide ontology classes with no GraphQL representation
        ontology_classes = {"Skill": {}, "Model": {}}
        warnings = validate_schema_against_ontology([], ontology_classes)
        assert any("has no GraphQL type projection" in w for w in warnings)

    def test_standard_types_not_flagged(self, parsed_types):
        warnings = validate_schema_against_ontology(parsed_types, {})
        assert not any("Query" in w and "has no corresponding" in w for w in warnings)
        assert not any("Mutation" in w and "has no corresponding" in w for w in warnings)
