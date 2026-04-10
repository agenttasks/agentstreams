"""UDA ontology projection generators.

Reads the AgentStreams ontology (ontology/agentstreams.ttl) and generates
multiple format projections following Netflix UDA's "Model Once, Represent
Everywhere" pattern:

- Avro schemas (data pipeline serialization)
- GraphQL schemas (API layer via pg_graphql)
- TTL DataContainer definitions (data mesh source registration)
- TTL Mapping definitions (ontology → physical layer bridges)

Each projection is auto-generated from the single ontology source of truth,
ensuring consistency across all representations.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class OntologyClass:
    """Parsed ontology class from TTL."""

    name: str
    label: str = ""
    comment: str = ""
    parent: str = ""
    properties: list[OntologyProperty] = field(default_factory=list)
    key_property: str = ""  # Primary key field


@dataclass
class OntologyProperty:
    """Parsed ontology property from TTL."""

    name: str
    domain: str = ""
    range_type: str = ""  # xsd:string, xsd:integer, xsd:boolean, class ref
    label: str = ""
    comment: str = ""
    is_key: bool = False
    is_relationship: bool = False  # References another class vs literal


@dataclass
class OntologyEnum:
    """Parsed enumeration from TTL."""

    name: str
    values: list[str] = field(default_factory=list)


class OntologyParser:
    """Parse AgentStreams TTL ontology into structured class/property model.

    Reads the TTL file and extracts classes, properties, enumerations,
    and their relationships for projection generation.
    """

    def __init__(self, ttl_path: str | Path | None = None):
        self.ttl_path = (
            Path(ttl_path)
            if ttl_path
            else (Path(__file__).parent.parent / "ontology" / "agentstreams.ttl")
        )
        self.classes: dict[str, OntologyClass] = {}
        self.properties: dict[str, OntologyProperty] = {}
        self.enums: dict[str, OntologyEnum] = {}

    def parse(self) -> None:
        """Parse the TTL file into structured objects."""
        text = self.ttl_path.read_text()

        # Extract classes
        for match in re.finditer(
            r"as:(\w+)\s+a\s+rdfs:Class\s*;(.*?)(?=\n\nas:|\Z)",
            text,
            re.DOTALL,
        ):
            name = match.group(1)
            body = match.group(2)
            cls = OntologyClass(name=name)

            label_m = re.search(r'rdfs:label\s+"([^"]+)"', body)
            if label_m:
                cls.label = label_m.group(1)

            comment_m = re.search(r'rdfs:comment\s+"([^"]+)"', body)
            if comment_m:
                cls.comment = comment_m.group(1)

            self.classes[name] = cls

        # Extract properties
        for match in re.finditer(
            r"as:(\w+)\s+a\s+rdf:Property\s*;(.*?)(?=\n\nas:|\Z)",
            text,
            re.DOTALL,
        ):
            name = match.group(1)
            body = match.group(2)
            prop = OntologyProperty(name=name)

            domain_m = re.search(r"rdfs:domain\s+as:(\w+)", body)
            if domain_m:
                prop.domain = domain_m.group(1)

            range_m = re.search(r"rdfs:range\s+(xsd:\w+|as:\w+)", body)
            if range_m:
                prop.range_type = range_m.group(1)
                prop.is_relationship = prop.range_type.startswith("as:")

            comment_m = re.search(r'rdfs:comment\s+"([^"]+)"', body)
            if comment_m:
                prop.comment = comment_m.group(1)

            self.properties[name] = prop

            # Attach to class
            if prop.domain in self.classes:
                self.classes[prop.domain].properties.append(prop)

        # Extract enums (instances of enum classes)
        for match in re.finditer(
            r"as:(\w+)\s+a\s+as:(\w+)\s*;",
            text,
        ):
            instance = match.group(1)
            enum_cls = match.group(2)
            if enum_cls not in self.enums:
                self.enums[enum_cls] = OntologyEnum(name=enum_cls)
            self.enums[enum_cls].values.append(instance)


# ── Avro Schema Projection ─────────────────────────────────


class AvroProjection:
    """Generate Avro schemas from ontology classes.

    Follows the UDA pattern from Netflix's onepiece.avro:
    - Classes become Avro records
    - Properties become fields with udaUri annotations
    - Relationships become reference records with primary key only
    - Enums become Avro enums
    """

    TYPE_MAP = {
        "xsd:string": "string",
        "xsd:integer": "long",
        "xsd:boolean": "boolean",
        "xsd:float": "float",
        "xsd:double": "double",
        "xsd:anyURI": "string",
    }

    def __init__(self, parser: OntologyParser):
        self.parser = parser

    def generate(self, class_name: str) -> dict:
        """Generate Avro schema for an ontology class."""
        cls = self.parser.classes.get(class_name)
        if not cls:
            raise ValueError(f"Unknown class: {class_name}")

        fields = []
        for prop in cls.properties:
            avro_field = self._property_to_field(prop, class_name)
            if avro_field:
                fields.append(avro_field)

        return {
            "type": "record",
            "name": f"AS_{class_name}",
            "namespace": "dev.agentstreams",
            "doc": cls.comment or cls.label,
            "fields": fields,
            "udaUri": f"https://agentstreams.dev/ontology#{class_name}",
        }

    def _property_to_field(self, prop: OntologyProperty, parent: str) -> dict | None:
        if prop.is_relationship:
            ref_class = prop.range_type.replace("as:", "")
            return {
                "name": f"AS_{prop.name}",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": f"AS_{ref_class}_Reference",
                        "fields": [{"name": "id", "type": "string"}],
                    },
                ],
                "default": None,
                "udaUri": f"https://agentstreams.dev/ontology#{prop.name}",
            }

        avro_type = self.TYPE_MAP.get(prop.range_type, "string")
        return {
            "name": f"AS_{prop.name}",
            "type": avro_type,
            "udaUri": f"https://agentstreams.dev/ontology#{prop.name}",
        }

    def generate_all(self) -> list[dict]:
        """Generate Avro schemas for all ontology classes."""
        return [self.generate(name) for name in self.parser.classes]

    def to_json(self, class_name: str) -> str:
        """Render Avro schema as formatted JSON."""
        return json.dumps(self.generate(class_name), indent=2)


# ── GraphQL Schema Projection ──────────────────────────────


class GraphQLProjection:
    """Generate GraphQL schemas from ontology classes.

    Follows UDA pattern from Netflix's onepiece.graphqls:
    - Classes become GraphQL types with @key directives
    - Properties become typed fields with @udaUri directives
    - Enums become GraphQL enums
    - Relationships become object references
    """

    TYPE_MAP = {
        "xsd:string": "String",
        "xsd:integer": "Int",
        "xsd:boolean": "Boolean",
        "xsd:float": "Float",
        "xsd:double": "Float",
        "xsd:anyURI": "String",
    }

    def __init__(self, parser: OntologyParser):
        self.parser = parser

    def generate(self, class_name: str) -> str:
        """Generate GraphQL type definition for an ontology class."""
        cls = self.parser.classes.get(class_name)
        if not cls:
            raise ValueError(f"Unknown class: {class_name}")

        key_field = cls.key_property or (cls.properties[0].name if cls.properties else "id")
        lines = [
            f'type AS_{class_name} @key(fields: "as_{key_field}") '
            f'@udaUri(uri: "https://agentstreams.dev/ontology#{class_name}") {{',
        ]

        for prop in cls.properties:
            gql_type = self._property_type(prop)
            lines.append(
                f"  as_{prop.name}: {gql_type} "
                f'@udaUri(uri: "https://agentstreams.dev/ontology#{prop.name}")'
            )

        lines.append("}")
        return "\n".join(lines)

    def _property_type(self, prop: OntologyProperty) -> str:
        if prop.is_relationship:
            ref_class = prop.range_type.replace("as:", "")
            return f"AS_{ref_class}"
        return self.TYPE_MAP.get(prop.range_type, "String")

    def generate_enums(self) -> str:
        """Generate GraphQL enum definitions."""
        lines = []
        for enum_name, enum in self.parser.enums.items():
            lines.append(f"enum AS_{enum_name} {{")
            for value in enum.values:
                lines.append(f"  {value.upper()}")
            lines.append("}")
            lines.append("")
        return "\n".join(lines)

    def generate_input_types(self, class_name: str) -> str:
        """Generate Create and Update input types for a class."""
        cls = self.parser.classes.get(class_name)
        if not cls:
            return ""

        lines = []
        # Create input — all non-relationship fields
        create_fields = []
        update_fields = []
        for prop in cls.properties:
            if prop.is_relationship:
                continue
            gql_type = self.TYPE_MAP.get(prop.range_type, "String")
            create_fields.append(f"  as_{prop.name}: {gql_type}!")
            update_fields.append(f"  as_{prop.name}: {gql_type}")

        if create_fields:
            lines.append(f"input CreateAS_{class_name}Input {{")
            lines.extend(create_fields)
            lines.append("}")
            lines.append("")
            lines.append(f"input UpdateAS_{class_name}Input {{")
            lines.extend(update_fields)
            lines.append("}")
            lines.append("")

        return "\n".join(lines)

    def generate_connection_type(self, class_name: str) -> str:
        """Generate Relay-style connection types for pagination."""
        return "\n".join([
            f"type AS_{class_name}Connection {{",
            f"  edges: [AS_{class_name}Edge!]!",
            "  pageInfo: PageInfo!",
            "  totalCount: Int!",
            "}",
            "",
            f"type AS_{class_name}Edge {{",
            f"  node: AS_{class_name}!",
            "  cursor: String!",
            "}",
            "",
        ])

    def generate_all(self) -> str:
        """Generate complete GraphQL schema with queries, mutations, connections."""
        parts = [
            '"""AgentStreams UDA GraphQL Schema"""',
            '"""Auto-generated from ontology/agentstreams.ttl"""',
            "",
            "directive @key(fields: String!) on OBJECT",
            "directive @udaUri(uri: String!) on OBJECT | FIELD_DEFINITION",
            "",
            "scalar DateTime",
            "",
        ]

        # Enums first
        enum_defs = self.generate_enums()
        if enum_defs:
            parts.append(enum_defs)

        # PageInfo (Relay spec)
        parts.extend([
            "type PageInfo {",
            "  hasNextPage: Boolean!",
            "  hasPreviousPage: Boolean!",
            "  startCursor: String",
            "  endCursor: String",
            "}",
            "",
        ])

        # Types + connection types + input types
        for class_name in self.parser.classes:
            parts.append(self.generate(class_name))
            parts.append("")
            parts.append(self.generate_connection_type(class_name))
            parts.append(self.generate_input_types(class_name))

        # Query root type
        query_fields = []
        for class_name in self.parser.classes:
            lower = class_name[0].lower() + class_name[1:]
            query_fields.append(f"  as_{lower}(id: ID!): AS_{class_name}")
            query_fields.append(
                f"  as_{lower}s(limit: Int = 10, offset: Int = 0): AS_{class_name}Connection!"
            )
        parts.append("type Query {")
        parts.extend(query_fields)
        parts.append("}")
        parts.append("")

        # Mutation root type
        mutation_fields = []
        for class_name in self.parser.classes:
            lower = class_name[0].lower() + class_name[1:]
            mutation_fields.append(
                f"  createAS_{class_name}(input: CreateAS_{class_name}Input!): AS_{class_name}!"
            )
            mutation_fields.append(
                f"  updateAS_{class_name}(id: ID!, input: UpdateAS_{class_name}Input!): AS_{class_name}!"
            )
            mutation_fields.append(
                f"  deleteAS_{class_name}(id: ID!): Boolean!"
            )
        parts.append("type Mutation {")
        parts.extend(mutation_fields)
        parts.append("}")
        parts.append("")

        # Subscription root type
        sub_fields = []
        for class_name in self.parser.classes:
            sub_fields.append(
                f"  onAS_{class_name}Created: AS_{class_name}!"
            )
            sub_fields.append(
                f"  onAS_{class_name}Updated: AS_{class_name}!"
            )
        parts.append("type Subscription {")
        parts.extend(sub_fields)
        parts.append("}")
        parts.append("")

        return "\n".join(parts)


# ── TTL DataContainer Projection ───────────────────────────


class DataContainerProjection:
    """Generate TTL DataContainer definitions following UDA pattern.

    Follows Netflix's onepiece_character_data_container.ttl:
    - Each class gets a DataContainer (data mesh source registration)
    - Fields are projected as the Avro record schema
    - Relationships become foreign-key reference records
    """

    def __init__(self, parser: OntologyParser):
        self.parser = parser

    def generate(self, class_name: str, source_id: str = "auto") -> str:
        """Generate TTL DataContainer for an ontology class."""
        cls = self.parser.classes.get(class_name)
        if not cls:
            raise ValueError(f"Unknown class: {class_name}")

        lines = [
            "@prefix as: <https://agentstreams.dev/ontology#> .",
            "@prefix dc: <https://agentstreams.dev/datacontainer#> .",
            "@prefix datamesh: <https://agentstreams.dev/datamesh#> .",
            "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
            "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
            "",
            f"# DataContainer for as:{class_name}",
            "# Auto-generated from ontology — source of truth: ontology/agentstreams.ttl",
            "",
            f"dc:{class_name}_source a datamesh:Source ;",
            '    datamesh:sourceType "APPLICATION_PRODUCER" ;',
            f'    datamesh:sourceId "{source_id}" ;',
            f'    rdfs:label "{cls.label or class_name} Data Container" ;',
            f"    datamesh:projects as:{class_name} .",
            "",
        ]

        # Field projections
        for prop in cls.properties:
            if prop.is_relationship:
                ref_class = prop.range_type.replace("as:", "")
                lines.extend(
                    [
                        f"dc:{class_name}_{prop.name}_field a datamesh:Field ;",
                        f'    datamesh:fieldName "AS_{prop.name}" ;',
                        f"    datamesh:referencesClass as:{ref_class} ;",
                        f"    datamesh:sourceField dc:{class_name}_source .",
                        "",
                    ]
                )
            else:
                lines.extend(
                    [
                        f"dc:{class_name}_{prop.name}_field a datamesh:Field ;",
                        f'    datamesh:fieldName "AS_{prop.name}" ;',
                        f'    datamesh:fieldType "{prop.range_type}" ;',
                        f"    datamesh:sourceField dc:{class_name}_source .",
                        "",
                    ]
                )

        return "\n".join(lines)


# ── TTL Mapping Projection ─────────────────────────────────


class MappingProjection:
    """Generate TTL mapping definitions following UDA pattern.

    Follows Netflix's onepiece_character_mappings.ttl:
    - Links ontology concepts to physical data assets
    - Maps properties to data container fields
    - Handles relationship mappings with nested references
    """

    def __init__(self, parser: OntologyParser):
        self.parser = parser

    def generate(self, class_name: str, table_name: str = "") -> str:
        """Generate TTL mapping for an ontology class → Postgres table."""
        cls = self.parser.classes.get(class_name)
        if not cls:
            raise ValueError(f"Unknown class: {class_name}")

        target_table = table_name or class_name.lower() + "s"

        lines = [
            "@prefix as: <https://agentstreams.dev/ontology#> .",
            "@prefix map: <https://agentstreams.dev/mapping#> .",
            "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
            "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
            "",
            f"# Mapping: as:{class_name} → {target_table} table",
            "",
            f"map:{class_name.lower()}-table a map:Mapping ;",
            f"    map:ontologyClass as:{class_name} ;",
            f'    map:targetTable "{target_table}" ;',
            f'    rdfs:label "{class_name} → {target_table} table" .',
            "",
        ]

        for prop in cls.properties:
            col_name = self._property_to_column(prop.name)
            lines.extend(
                [
                    f"map:{class_name.lower()}-{prop.name} a map:Mapping ;",
                    f"    map:ontologyProperty as:{prop.name} ;",
                    f'    map:targetTable "{target_table}" ;',
                    f'    map:targetColumn "{col_name}" .',
                    "",
                ]
            )

        return "\n".join(lines)

    @staticmethod
    def _property_to_column(prop_name: str) -> str:
        """Convert camelCase property name to snake_case column name."""
        return re.sub(r"(?<=[a-z])([A-Z])", r"_\1", prop_name).lower()


# ── Convenience function ────────────────────────────────────


def generate_all_projections(
    ttl_path: str | Path | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, str]:
    """Generate all UDA projections from ontology.

    Returns dict mapping filename → content for each generated file.
    Formats: Avro, GraphQL, DataContainer, Mapping, Cube YAML, TypeScript.
    """
    parser = OntologyParser(ttl_path)
    parser.parse()

    results = {}

    # Avro schemas
    avro = AvroProjection(parser)
    for name in parser.classes:
        results[f"avro/{name}.avsc"] = json.dumps(avro.generate(name), indent=2)

    # GraphQL schema (enhanced with queries, mutations, connections)
    gql = GraphQLProjection(parser)
    results["graphql/schema.graphqls"] = gql.generate_all()

    # DataContainers
    dc = DataContainerProjection(parser)
    for name in parser.classes:
        results[f"datacontainers/{name}_data_container.ttl"] = dc.generate(name)

    # Mappings
    mp = MappingProjection(parser)
    for name in parser.classes:
        results[f"mappings/{name}_mappings.ttl"] = mp.generate(name)

    # Cube.dev YAML data models (Kimball dimensional modeling)
    from src.cube_models import CubeProjection

    cube = CubeProjection(parser)
    results["cube/models.yml"] = cube.to_yaml_all()

    # TypeScript types (from GraphQL schema)
    from src.typescript_codegen import codegen_from_ontology

    results["typescript/types.ts"] = codegen_from_ontology(parser)

    # Write to output directory if specified
    if output_dir:
        out = Path(output_dir)
        for filepath, content in results.items():
            full_path = out / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

    return results
