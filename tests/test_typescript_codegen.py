"""Tests for src/typescript_codegen.py — TypeScript type codegen from GraphQL."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.graphql_toolkit import GraphQLSchemaParser
from src.typescript_codegen import TypeScriptCodegen, codegen_from_ontology, codegen_from_sdl


@pytest.fixture
def sample_sdl():
    schema_path = (
        Path(__file__).parent.parent
        / "evals"
        / "api-client"
        / "test_data"
        / "graphql_schema.graphql"
    )
    return schema_path.read_text()


@pytest.fixture
def parsed_types(sample_sdl):
    parser = GraphQLSchemaParser()
    return parser.parse(sample_sdl)


@pytest.fixture
def codegen(parsed_types):
    return TypeScriptCodegen(parsed_types)


class TestBrandedIds:
    def test_generates_brand_type(self, codegen):
        output = codegen.generate_branded_ids()
        assert "Brand<" in output
        assert "__brand" in output

    def test_user_id_branded(self, codegen):
        output = codegen.generate_branded_ids()
        assert "UserId" in output
        assert "Brand<string, 'UserId'>" in output

    def test_post_id_branded(self, codegen):
        output = codegen.generate_branded_ids()
        assert "PostId" in output


class TestEnumConsts:
    def test_generates_role_type(self, codegen):
        output = codegen.generate_enum_consts()
        assert "export type Role" in output
        assert "'ADMIN'" in output
        assert "'USER'" in output
        assert "'MODERATOR'" in output

    def test_generates_const_object(self, codegen):
        output = codegen.generate_enum_consts()
        assert "export const Role" in output
        assert "as const" in output

    def test_companion_object_pattern(self, codegen):
        """Both type and const should share the same name (Cherny p.140)."""
        output = codegen.generate_enum_consts()
        assert "export type Role" in output
        assert "export const Role" in output


class TestObjectTypes:
    def test_generates_user_interface(self, codegen):
        output = codegen.generate_types()
        assert "export interface User" in output

    def test_user_has_expected_fields(self, codegen):
        output = codegen.generate_types()
        assert "email" in output
        assert "name" in output
        assert "role" in output

    def test_branded_id_used_in_interface(self, codegen):
        output = codegen.generate_types()
        assert "UserId" in output

    def test_post_interface_generated(self, codegen):
        output = codegen.generate_types()
        assert "export interface Post" in output


class TestInputTypes:
    def test_generates_create_input(self, codegen):
        output = codegen.generate_input_types()
        assert "CreateUserInput" in output

    def test_generates_update_input(self, codegen):
        output = codegen.generate_input_types()
        assert "UpdateUserInput" in output


class TestDiscriminatedUnions:
    def test_generates_query_result(self, codegen):
        output = codegen.generate_discriminated_unions()
        assert "QueryResult<T>" in output
        assert "'success'" in output
        assert "'error'" in output

    def test_generates_graphql_error(self, codegen):
        output = codegen.generate_discriminated_unions()
        assert "GraphQLError" in output
        assert "message" in output


class TestQueryFunctions:
    def test_generates_query_function(self, codegen):
        output = codegen.generate_query_functions()
        assert "queryUser" in output
        assert "Promise<QueryResult<User>>" in output

    def test_query_takes_branded_id(self, codegen):
        output = codegen.generate_query_functions()
        assert "UserId" in output


class TestConnectionHelpers:
    def test_generates_page_info(self, codegen):
        output = codegen.generate_connection_helpers()
        assert "PageInfo" in output
        assert "hasNextPage" in output

    def test_generates_edge(self, codegen):
        output = codegen.generate_connection_helpers()
        assert "Edge<T>" in output

    def test_generates_connection(self, codegen):
        output = codegen.generate_connection_helpers()
        assert "Connection<T>" in output


class TestGenerateAll:
    def test_complete_output(self, codegen):
        output = codegen.generate_all()
        assert "Branded ID types" in output
        assert "Enum companion objects" in output
        assert "Object types" in output
        assert "QueryResult" in output

    def test_auto_generated_header(self, codegen):
        output = codegen.generate_all()
        assert "Auto-generated TypeScript types" in output


class TestCodegenFromSDL:
    def test_end_to_end(self, sample_sdl):
        output = codegen_from_sdl(sample_sdl)
        assert isinstance(output, str)
        assert len(output) > 100
        assert "export interface User" in output
        assert "UserId" in output
        assert "Role" in output


class TestCodegenFromOntology:
    def test_end_to_end(self):
        output = codegen_from_ontology()
        assert isinstance(output, str)
        assert len(output) > 0
        assert "Auto-generated" in output
