"""UDA codegen — generate Avro schemas, GraphQL types, and TTL from the registry.

Netflix UDA principle: the ontology is the single source of truth.
This module generates all derivative representations from the Python
schema registry, ensuring they never drift.

Usage:
  uv run -c "from agentstreams.uda.codegen import generate_all; generate_all('build/')"
"""

from __future__ import annotations

import json
from pathlib import Path

from .schema_registry import (
    list_entities,
    to_avro_schema,
    to_graphql_type,
    get_entity_class,
    get_table_name,
    get_ontology_uri,
)


def generate_avro_schemas(output_dir: str | Path) -> list[Path]:
    """Generate Avro .avsc files for all registered entities."""
    out = Path(output_dir) / "avro"
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in list_entities():
        schema = to_avro_schema(name)
        path = out / f"{name}.avsc"
        path.write_text(json.dumps(schema, indent=2) + "\n")
        paths.append(path)
    return paths


def generate_graphql_schema(output_dir: str | Path) -> Path:
    """Generate a unified GraphQL schema from all registered entities."""
    out = Path(output_dir) / "graphql"
    out.mkdir(parents=True, exist_ok=True)

    lines = [
        '"""AgentStreams UDA GraphQL Schema',
        "",
        "Auto-generated from the Python schema registry.",
        "Served by Neon pg_graphql in production.",
        '"""',
        "",
        "scalar DateTime",
        "scalar JSON",
        "",
    ]

    for name in list_entities():
        lines.append(to_graphql_type(name))
        lines.append("")

    # Query root
    lines.append("type Query {")
    for name in list_entities():
        table = get_table_name(name)
        lines.append(f"  {table}(limit: Int = 20, offset: Int = 0): [{name}!]!")
        # Singular lookup
        lines.append(f"  {table}_by_pk(id: ID!): {name}")
    lines.append("}")
    lines.append("")

    path = out / "schema.graphqls"
    path.write_text("\n".join(lines) + "\n")
    return path


def generate_ttl_instances(output_dir: str | Path) -> Path:
    """Generate TTL instance data from the registry (entity definitions only)."""
    out = Path(output_dir) / "ttl"
    out.mkdir(parents=True, exist_ok=True)

    lines = [
        "@prefix as: <https://agentstreams.dev/ontology#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "",
        "# Auto-generated UDA entity registry",
        "",
    ]

    for name in list_entities():
        uri = get_ontology_uri(name)
        table = get_table_name(name)
        cls = get_entity_class(name)
        doc = (cls.__doc__ or "").strip().split("\n")[0]
        lines.append(f"# {name} → {table}")
        lines.append(f'as:entity-{name.lower()} a {uri} ;')
        lines.append(f'    rdfs:label "{name}" ;')
        lines.append(f'    rdfs:comment "{doc}" .')
        lines.append("")

    path = out / "entities.ttl"
    path.write_text("\n".join(lines) + "\n")
    return path


def generate_all(output_dir: str | Path = "build") -> dict[str, list[str]]:
    """Generate all UDA representations. Returns paths by format."""
    avro_paths = generate_avro_schemas(output_dir)
    graphql_path = generate_graphql_schema(output_dir)
    ttl_path = generate_ttl_instances(output_dir)

    return {
        "avro": [str(p) for p in avro_paths],
        "graphql": [str(graphql_path)],
        "ttl": [str(ttl_path)],
    }
