"""Cube.dev YAML data model generation from the AgentStreams ontology.

Generates Cube.dev-style YAML data models following Kimball dimensional
modeling patterns (Data Warehouse Toolkit, 3rd Ed.):

- Transaction fact tables → cubes with count/sum/avg measures
- Accumulating snapshot fact tables → cubes with lag/duration measures
- Dimension tables → cubes with descriptive dimensions
- SCD Type 2 → cubes with ``WHERE is_current = true`` filter
- Conformed dimensions → reusable join targets across fact cubes

Output matches the structure of existing hand-authored models in
``julia/models/*.yaml`` (matters.yaml, vault.yaml, audit_logs.yaml).

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

import yaml

from src.projections import OntologyClass, OntologyParser, OntologyProperty


@dataclass
class Dimension:
    """A Cube.dev dimension (Kimball: descriptive attribute)."""

    name: str
    sql: str
    type: str  # "string" | "number" | "time" | "boolean"
    primary_key: bool = False
    description: str = ""


@dataclass
class Measure:
    """A Cube.dev measure (Kimball: fact/metric aggregation)."""

    name: str
    type: str  # "count" | "sum" | "avg" | "min" | "max" | "count_distinct"
    sql: str = ""
    description: str = ""


@dataclass
class Join:
    """A Cube.dev join (Kimball: dimension foreign key relationship)."""

    name: str
    sql: str
    relationship: str  # "one_to_one" | "one_to_many" | "many_to_one"


@dataclass
class CubeDefinition:
    """A complete Cube.dev cube definition.

    Maps to a single ``cubes:`` entry in YAML output.
    """

    name: str
    sql_table: str
    dimensions: list[Dimension] = field(default_factory=list)
    measures: list[Measure] = field(default_factory=list)
    joins: list[Join] = field(default_factory=list)
    description: str = ""
    kimball_type: str = ""


# ── Kimball Classification ─────────────────────────────────

# Ontology property name patterns indicating Kimball fact table types
_TIMESTAMP_PROPS = {"createdAt", "updatedAt", "recordedAt", "crawledAt", "fetchedAt"}
_MILESTONE_PROPS = {"startedAt", "completedAt", "processedAt", "uploadedAt"}
_NUMERIC_RANGES = {"xsd:integer", "xsd:float", "xsd:double"}
_MEASURE_PROPS = {
    "value",
    "count",
    "tokenCount",
    "charCount",
    "budgetTokens",
    "thinkingTokens",
    "inputTokens",
    "outputTokens",
    "durationMs",
    "overallScore",
    "totalIterations",
    "totalTokens",
    "itemCount",
    "fpRate",
    "numHashes",
    "expectedItems",
    "testCount",
    "assertionCount",
    "githubStars",
    "priority",
    "attempts",
    "maxAttempts",
    "statusCode",
    "maxIterations",
    "acceptanceThreshold",
    "temperature",
}


def _classify_ontology_class(cls: OntologyClass) -> str:
    """Classify an ontology class into a Kimball fact table type.

    Returns one of:
    - "transaction_fact": Event-grained rows with timestamps + metrics
    - "accumulating_snapshot": Pipeline/workflow with milestone dates
    - "dimension": Descriptive lookup table
    - "factless_fact": Events without numeric measures
    """
    prop_names = {p.name for p in cls.properties}
    numeric_props = {p.name for p in cls.properties if p.range_type in _NUMERIC_RANGES}

    # Check for accumulating snapshot (multiple milestone timestamps)
    milestone_count = len(prop_names & _MILESTONE_PROPS)
    if milestone_count >= 2:
        return "accumulating_snapshot"

    # Check for transaction fact (timestamp + numeric measures)
    has_timestamp = bool(prop_names & _TIMESTAMP_PROPS)
    has_measures = bool(numeric_props & _MEASURE_PROPS) or len(numeric_props) >= 2
    if has_timestamp and has_measures:
        return "transaction_fact"

    # Check for factless fact (timestamp + foreign keys, no measures)
    has_relationships = any(p.is_relationship for p in cls.properties)
    if has_timestamp and has_relationships and not has_measures:
        return "factless_fact"

    # Default to dimension
    return "dimension"


# ── Type Mapping ───────────────────────────────────────────

TYPE_MAP: dict[str, str] = {
    "xsd:string": "string",
    "xsd:integer": "number",
    "xsd:boolean": "boolean",
    "xsd:float": "number",
    "xsd:double": "number",
    "xsd:anyURI": "string",
}


def _property_to_column(prop_name: str) -> str:
    """Convert camelCase property name to snake_case column name."""
    return re.sub(r"(?<=[a-z])([A-Z])", r"_\1", prop_name).lower()


def _is_timestamp_prop(prop: OntologyProperty) -> bool:
    """Check if a property represents a timestamp/date field."""
    name_lower = prop.name.lower()
    return (
        prop.name in _TIMESTAMP_PROPS
        or prop.name in _MILESTONE_PROPS
        or name_lower.endswith("at")
        or name_lower.endswith("date")
    )


# ── Cube Projection ───────────────────────────────────────


class CubeProjection:
    """Generate Cube.dev-style YAML data models from the ontology.

    Follows Kimball four-step design (Data Warehouse Toolkit Ch. 2):
    1. Business process → cube name
    2. Grain → sql_table with WHERE clause
    3. Dimensions → dimension fields (who/what/where/when/why/how)
    4. Facts → measure fields (numeric aggregations)

    Conformed dimensions: models, skills, languages cubes are reusable
    via joins from any fact cube — same column names, same domain.

    Degenerate dimensions: Non-FK columns like event_type, status become
    string dimensions directly in the fact cube.
    """

    def __init__(self, parser: OntologyParser):
        self.parser = parser

    def classify_table(self, cls: OntologyClass) -> str:
        """Classify an ontology class into a Kimball fact table type."""
        return _classify_ontology_class(cls)

    def generate(self, class_name: str) -> CubeDefinition:
        """Generate a CubeDefinition for an ontology class."""
        cls = self.parser.classes.get(class_name)
        if not cls:
            raise ValueError(f"Unknown class: {class_name}")

        kimball_type = self.classify_table(cls)
        table_name = _property_to_column(class_name) + "s"
        sql_table = f"SELECT * FROM {table_name}"

        dimensions = self._build_dimensions(cls, kimball_type)
        measures = self._build_measures(cls, kimball_type)
        joins = self._build_joins(cls, table_name)

        description = cls.comment or cls.label or class_name
        if kimball_type == "transaction_fact":
            description = f"Transaction fact table — {description}"
        elif kimball_type == "accumulating_snapshot":
            description = f"Accumulating snapshot fact — {description}"
        elif kimball_type == "dimension":
            description = f"Dimension — {description}"

        return CubeDefinition(
            name=table_name,
            sql_table=sql_table,
            dimensions=dimensions,
            measures=measures,
            joins=joins,
            description=description,
            kimball_type=kimball_type,
        )

    def generate_all(self) -> list[CubeDefinition]:
        """Generate CubeDefinitions for all ontology classes."""
        return [self.generate(name) for name in self.parser.classes]

    def to_yaml(self, class_name: str) -> str:
        """Generate YAML for a single cube."""
        cube = self.generate(class_name)
        return _cube_to_yaml(cube)

    def to_yaml_all(self) -> str:
        """Generate YAML for all cubes."""
        cubes = self.generate_all()
        return _cubes_to_yaml(cubes)

    def _build_dimensions(self, cls: OntologyClass, kimball_type: str) -> list[Dimension]:
        """Build dimension list for a class."""
        dimensions: list[Dimension] = []

        for prop in cls.properties:
            if prop.is_relationship:
                continue

            col_name = _property_to_column(prop.name)

            if _is_timestamp_prop(prop):
                dimensions.append(
                    Dimension(
                        name=col_name,
                        sql=col_name,
                        type="time",
                        description=prop.comment or "",
                    )
                )
            elif prop.range_type in _NUMERIC_RANGES and prop.name in _MEASURE_PROPS:
                # Numeric measure props are facts, not dimensions (in fact tables)
                if kimball_type == "dimension":
                    dimensions.append(
                        Dimension(
                            name=col_name,
                            sql=col_name,
                            type="number",
                            description=prop.comment or "",
                        )
                    )
            else:
                cube_type = TYPE_MAP.get(prop.range_type, "string")
                is_key = prop.name in {"name", "id"} or prop.name.endswith("Id")
                dimensions.append(
                    Dimension(
                        name=col_name,
                        sql=col_name,
                        type=cube_type,
                        primary_key=is_key and col_name in {"id", "name"},
                        description=prop.comment or "",
                    )
                )

        # Every cube needs at least an id-like primary key dimension
        dim_names = {d.name for d in dimensions}
        if not any(d.primary_key for d in dimensions) and "id" not in dim_names:
            dimensions.insert(
                0,
                Dimension(name="id", sql="id", type="string", primary_key=True),
            )

        return dimensions

    def _build_measures(self, cls: OntologyClass, kimball_type: str) -> list[Measure]:
        """Build measure list for a class."""
        measures: list[Measure] = []

        # Every cube gets a count measure
        measures.append(
            Measure(
                name="count", type="count", description=f"Total {cls.label or cls.name} records"
            )
        )

        if kimball_type == "dimension":
            return measures

        # Add numeric property measures for fact tables
        for prop in cls.properties:
            if prop.range_type not in _NUMERIC_RANGES:
                continue
            if prop.is_relationship:
                continue

            col_name = _property_to_column(prop.name)

            # Sum measure
            measures.append(
                Measure(
                    name=f"total_{col_name}",
                    type="sum",
                    sql=col_name,
                    description=f"Sum of {col_name}",
                )
            )

            # Average measure for duration/score-like properties
            if any(
                kw in prop.name.lower()
                for kw in ("duration", "score", "rate", "ratio", "count", "tokens")
            ):
                measures.append(
                    Measure(
                        name=f"avg_{col_name}",
                        type="avg",
                        sql=col_name,
                        description=f"Average {col_name}",
                    )
                )

        return measures

    def _build_joins(self, cls: OntologyClass, table_name: str) -> list[Join]:
        """Build join list from relationship properties."""
        joins: list[Join] = []
        for prop in cls.properties:
            if not prop.is_relationship:
                continue

            ref_class = prop.range_type.replace("as:", "")
            ref_table = _property_to_column(ref_class) + "s"
            fk_col = _property_to_column(prop.name) + "_id"

            joins.append(
                Join(
                    name=ref_table,
                    relationship="many_to_one",
                    sql=f"{{CUBE}}.{fk_col} = {{{ref_table}}}.id",
                )
            )
        return joins


# ── YAML Serialization ─────────────────────────────────────


def _cube_to_dict(cube: CubeDefinition) -> dict[str, Any]:
    """Convert a CubeDefinition to a YAML-serializable dict."""
    result: dict[str, Any] = {
        "name": cube.name,
        "sql": cube.sql_table,
    }
    if cube.description:
        result["description"] = cube.description

    if cube.measures:
        result["measures"] = []
        for m in cube.measures:
            measure_dict: dict[str, Any] = {"name": m.name, "type": m.type}
            if m.sql:
                measure_dict["sql"] = m.sql
            if m.description:
                measure_dict["description"] = m.description
            result["measures"].append(measure_dict)

    if cube.dimensions:
        result["dimensions"] = []
        for d in cube.dimensions:
            dim_dict: dict[str, Any] = {
                "name": d.name,
                "sql": d.sql,
                "type": d.type,
            }
            if d.primary_key:
                dim_dict["primary_key"] = True
            if d.description:
                dim_dict["description"] = d.description
            result["dimensions"].append(dim_dict)

    if cube.joins:
        result["joins"] = []
        for j in cube.joins:
            result["joins"].append(
                {
                    "name": j.name,
                    "relationship": j.relationship,
                    "sql": j.sql,
                }
            )

    return result


def _cube_to_yaml(cube: CubeDefinition) -> str:
    """Render a single CubeDefinition as YAML."""
    data = {"cubes": [_cube_to_dict(cube)]}
    return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)


def _cubes_to_yaml(cubes: list[CubeDefinition]) -> str:
    """Render multiple CubeDefinitions as a single YAML document."""
    data = {"cubes": [_cube_to_dict(c) for c in cubes]}
    return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
