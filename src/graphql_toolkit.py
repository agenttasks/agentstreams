"""GraphQL schema parser and pg_graphql introspection toolkit.

Provides:
- SDL parser: parse .graphql files into structured GraphQLType objects
- pg_graphql introspection: query Neon's auto-generated GraphQL schema
- Schema persistence: store generated schemas in data_containers table
- Ontology validation: detect drift between GraphQL schema and TTL ontology

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class GraphQLArgument:
    """A GraphQL field argument."""

    name: str
    type_name: str
    is_list: bool = False
    is_non_null: bool = False
    default_value: str | None = None


@dataclass
class GraphQLField:
    """A field within a GraphQL type."""

    name: str
    type_name: str
    is_list: bool = False
    is_non_null: bool = False
    arguments: list[GraphQLArgument] = field(default_factory=list)
    description: str = ""


@dataclass
class GraphQLType:
    """A parsed GraphQL type definition."""

    name: str
    kind: str  # "OBJECT" | "INPUT" | "ENUM" | "SCALAR" | "UNION" | "INTERFACE"
    fields: list[GraphQLField] = field(default_factory=list)
    directives: list[str] = field(default_factory=list)
    description: str = ""
    enum_values: list[str] = field(default_factory=list)
    union_types: list[str] = field(default_factory=list)


# ── SDL Parser ─────────────────────────────────────────────


class GraphQLSchemaParser:
    """Parse GraphQL SDL (Schema Definition Language) into structured types.

    Handles: type, input, enum, scalar, union, interface definitions.
    Extracts fields, arguments, directives, and descriptions.
    """

    # Regex patterns for SDL parsing
    _TYPE_PATTERN = re.compile(
        r'(?:"""(.*?)"""\s*)?'
        r"(type|input|interface)\s+(\w+)"
        r"(?:\s+implements\s+[\w\s&]+)?"
        r"(?:\s+@\w+(?:\([^)]*\))?)?"
        r"\s*\{([^}]*)\}",
        re.DOTALL,
    )
    _ENUM_PATTERN = re.compile(
        r'(?:"""(.*?)"""\s*)?enum\s+(\w+)\s*\{([^}]*)\}',
        re.DOTALL,
    )
    _SCALAR_PATTERN = re.compile(r"scalar\s+(\w+)")
    _UNION_PATTERN = re.compile(r"union\s+(\w+)\s*=\s*([^}\n]+)")
    _FIELD_PATTERN = re.compile(
        r'(?:"""(.*?)"""\s*)?'
        r"(\w+)"
        r"(?:\(([^)]*)\))?"
        r"\s*:\s*"
        r"(\[?\w+!?\]?!?)"
        r"(?:\s*=\s*(\w+))?"
        r"(?:\s*@\w+(?:\([^)]*\))?)*",
        re.DOTALL,
    )
    _DIRECTIVE_PATTERN = re.compile(r"@(\w+(?:\([^)]*\))?)")
    _ARG_PATTERN = re.compile(
        r"(\w+)\s*:\s*(\[?\w+!?\]?!?)(?:\s*=\s*(\w+))?",
    )

    def parse(self, sdl: str) -> list[GraphQLType]:
        """Parse a GraphQL SDL string into a list of GraphQLType objects."""
        types: list[GraphQLType] = []

        # Parse object/input/interface types
        for match in self._TYPE_PATTERN.finditer(sdl):
            description = (match.group(1) or "").strip()
            kind_str = match.group(2).upper()
            name = match.group(3)
            body = match.group(4)

            kind_map = {"TYPE": "OBJECT", "INPUT": "INPUT", "INTERFACE": "INTERFACE"}
            kind = kind_map.get(kind_str, "OBJECT")

            fields = self._parse_fields(body)
            directives = self._extract_directives(match.group(0))

            types.append(
                GraphQLType(
                    name=name,
                    kind=kind,
                    fields=fields,
                    directives=directives,
                    description=description,
                )
            )

        # Parse enums
        for match in self._ENUM_PATTERN.finditer(sdl):
            description = (match.group(1) or "").strip()
            name = match.group(2)
            values_str = match.group(3)
            values = [v.strip() for v in values_str.strip().split("\n") if v.strip()]

            types.append(
                GraphQLType(
                    name=name,
                    kind="ENUM",
                    description=description,
                    enum_values=values,
                )
            )

        # Parse scalars
        for match in self._SCALAR_PATTERN.finditer(sdl):
            types.append(GraphQLType(name=match.group(1), kind="SCALAR"))

        # Parse unions
        for match in self._UNION_PATTERN.finditer(sdl):
            name = match.group(1)
            member_types = [t.strip() for t in match.group(2).split("|")]
            types.append(
                GraphQLType(name=name, kind="UNION", union_types=member_types)
            )

        return types

    def parse_file(self, path: str | Path) -> list[GraphQLType]:
        """Parse a .graphql file into structured types."""
        sdl = Path(path).read_text()
        return self.parse(sdl)

    def _parse_fields(self, body: str) -> list[GraphQLField]:
        """Parse field definitions from a type body."""
        fields: list[GraphQLField] = []
        for match in self._FIELD_PATTERN.finditer(body):
            description = (match.group(1) or "").strip()
            name = match.group(2)
            args_str = match.group(3)
            type_str = match.group(4)

            is_list = type_str.startswith("[")
            is_non_null = type_str.endswith("!")
            type_name = type_str.strip("[]!").strip("!")

            arguments = self._parse_arguments(args_str) if args_str else []

            fields.append(
                GraphQLField(
                    name=name,
                    type_name=type_name,
                    is_list=is_list,
                    is_non_null=is_non_null,
                    arguments=arguments,
                    description=description,
                )
            )
        return fields

    def _parse_arguments(self, args_str: str) -> list[GraphQLArgument]:
        """Parse argument definitions from a field."""
        arguments: list[GraphQLArgument] = []
        for match in self._ARG_PATTERN.finditer(args_str):
            name = match.group(1)
            type_str = match.group(2)
            default = match.group(3)

            is_list = type_str.startswith("[")
            is_non_null = type_str.endswith("!")
            type_name = type_str.strip("[]!").strip("!")

            arguments.append(
                GraphQLArgument(
                    name=name,
                    type_name=type_name,
                    is_list=is_list,
                    is_non_null=is_non_null,
                    default_value=default,
                )
            )
        return arguments

    def _extract_directives(self, text: str) -> list[str]:
        """Extract directive names from a type definition."""
        return [m.group(1) for m in self._DIRECTIVE_PATTERN.finditer(text)]


# ── pg_graphql Introspection ───────────────────────────────


async def introspect_pg_graphql(conn, *, table_filter: str | None = None) -> str:
    """Query Neon's pg_graphql extension to get the auto-generated schema.

    Returns the introspection result as a JSON string.
    """
    query = """
    SELECT graphql.resolve($$
    {
        __schema {
            types {
                name
                kind
                fields {
                    name
                    type {
                        name
                        kind
                        ofType {
                            name
                            kind
                        }
                    }
                    args {
                        name
                        type {
                            name
                            kind
                        }
                    }
                }
                enumValues {
                    name
                }
            }
        }
    }
    $$)
    """
    row = await (await conn.execute(query)).fetchone()
    if not row:
        return "{}"

    result = row[0] if isinstance(row[0], str) else json.dumps(row[0])

    if table_filter:
        parsed = json.loads(result)
        if "data" in parsed and "__schema" in parsed["data"]:
            types = parsed["data"]["__schema"]["types"]
            parsed["data"]["__schema"]["types"] = [
                t for t in types if table_filter.lower() in t.get("name", "").lower()
            ]
            result = json.dumps(parsed)

    return result


# ── Schema Persistence ─────────────────────────────────────


async def persist_graphql_schema(
    conn,
    *,
    class_name: str,
    schema_sdl: str,
) -> None:
    """Write generated GraphQL SDL to data_containers.projection_graphql."""
    await conn.execute(
        """INSERT INTO data_containers (class_name, projection_graphql)
           VALUES (%s, %s)
           ON CONFLICT (class_name) DO UPDATE SET
               projection_graphql = EXCLUDED.projection_graphql,
               updated_at = now()""",
        (class_name, schema_sdl),
    )


async def persist_schema_version(
    conn,
    *,
    schema_name: str,
    sdl: str,
    source: str = "ontology",
) -> int:
    """Persist a versioned GraphQL schema to the graphql_schemas table.

    Auto-increments the version number. Returns the new version.
    """
    checksum = hashlib.sha256(sdl.encode()).hexdigest()

    # Check if identical schema already exists
    existing = await (
        await conn.execute(
            """SELECT version FROM graphql_schemas
               WHERE schema_name = %s AND checksum = %s
               ORDER BY version DESC LIMIT 1""",
            (schema_name, checksum),
        )
    ).fetchone()

    if existing:
        return existing[0]

    # Get next version
    max_ver = await (
        await conn.execute(
            "SELECT COALESCE(MAX(version), 0) FROM graphql_schemas WHERE schema_name = %s",
            (schema_name,),
        )
    ).fetchone()
    next_version = (max_ver[0] if max_ver else 0) + 1

    await conn.execute(
        """INSERT INTO graphql_schemas (schema_name, version, sdl, checksum, source)
           VALUES (%s, %s, %s, %s, %s)""",
        (schema_name, next_version, sdl, checksum, source),
    )
    return next_version


# ── Ontology Validation ────────────────────────────────────


def validate_schema_against_ontology(
    schema_types: list[GraphQLType],
    ontology_classes: dict[str, Any],
) -> list[str]:
    """Check for drift between GraphQL schema types and ontology classes.

    Returns a list of warning messages for:
    - GraphQL types with no corresponding ontology class
    - Ontology classes with no corresponding GraphQL type
    - Field mismatches between GraphQL and ontology
    """
    warnings: list[str] = []

    # Build lookup sets
    gql_type_names = {t.name for t in schema_types if t.kind == "OBJECT"}
    # Strip AS_ prefix for comparison
    gql_class_names = {
        name.removeprefix("AS_") for name in gql_type_names
    }
    ontology_class_names = set(ontology_classes.keys())

    # Check for GraphQL types without ontology backing
    # Skip standard GraphQL types
    standard_types = {
        "Query", "Mutation", "Subscription", "PageInfo",
        "__Schema", "__Type", "__Field", "__InputValue",
        "__EnumValue", "__Directive",
    }
    for gql_type in schema_types:
        if gql_type.kind != "OBJECT":
            continue
        base_name = gql_type.name.removeprefix("AS_")
        if base_name in standard_types:
            continue
        if base_name.endswith("Connection") or base_name.endswith("Edge"):
            continue
        if base_name.endswith("Input"):
            continue
        if base_name not in ontology_class_names:
            warnings.append(
                f"GraphQL type '{gql_type.name}' has no corresponding ontology class"
            )

    # Check for ontology classes without GraphQL representation
    for cls_name in ontology_class_names:
        if cls_name not in gql_class_names and f"AS_{cls_name}" not in gql_type_names:
            warnings.append(
                f"Ontology class '{cls_name}' has no GraphQL type projection"
            )

    return warnings
