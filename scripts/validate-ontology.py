#!/usr/bin/env python3
"""Validate UDA alignment: ontology classes ↔ schema tables ↔ mappings.

Checks:
1. Every ontology class has a mapping to a target table
2. Every mapped table exists in schema.sql
3. Every mapped column exists in its target table
4. Seed data instance counts match between ontology and schema
"""

import re
import sys
from pathlib import Path

ONTOLOGY_DIR = Path(__file__).parent.parent / "ontology"


def parse_ontology_classes(ttl: str) -> set[str]:
    """Extract class names from ontology (as:Foo a rdfs:Class)."""
    return set(re.findall(r"as:(\w+)\s+a\s+rdfs:Class", ttl))


def parse_ontology_instances(ttl: str) -> dict[str, list[str]]:
    """Extract instances grouped by class (as:foo a as:Bar)."""
    instances: dict[str, list[str]] = {}
    for name, cls in re.findall(r"as:([\w-]+)\s+a\s+as:(\w+)\s", ttl):
        instances.setdefault(cls, []).append(name)
    return instances


def parse_mapping_tables(ttl: str) -> dict[str, str]:
    """Extract class → table mappings."""
    mappings = {}
    # Find blocks like: map:X a map:Mapping ; map:ontologyClass as:Y ; map:targetTable "z"
    blocks = re.split(r"\n(?=map:\S+\s+a\s+map:Mapping)", ttl)
    for block in blocks:
        cls_match = re.search(r"map:ontologyClass\s+as:(\w+)", block)
        table_match = re.search(r'map:targetTable\s+"(\w+)"', block)
        if cls_match and table_match:
            mappings[cls_match.group(1)] = table_match.group(1)
    return mappings


def parse_mapping_columns(ttl: str) -> list[tuple[str, str, str]]:
    """Extract (property, table, column) triples."""
    columns = []
    blocks = re.split(r"\n(?=map:\S+\s+a\s+map:Mapping)", ttl)
    for block in blocks:
        prop_match = re.search(r"map:ontologyProperty\s+as:(\w+)", block)
        table_match = re.search(r'map:targetTable\s+"(\w+)"', block)
        col_match = re.search(r'map:targetColumn\s+"(\w+)"', block)
        if prop_match and table_match and col_match:
            columns.append((prop_match.group(1), table_match.group(1), col_match.group(1)))
    return columns


def parse_schema_tables(sql: str) -> dict[str, list[str]]:
    """Extract table → columns from CREATE TABLE statements."""
    tables: dict[str, list[str]] = {}
    for match in re.finditer(r"CREATE TABLE (\w+)\s*\((.*?)\);", sql, re.DOTALL):
        table_name = match.group(1)
        body = match.group(2)
        cols = []
        for line in body.split("\n"):
            line = line.strip().rstrip(",")
            col_match = re.match(r"^(\w+)\s+", line)
            if col_match:
                col = col_match.group(1)
                # Skip constraints
                if col.upper() not in ("PRIMARY", "UNIQUE", "CHECK", "FOREIGN", "CONSTRAINT"):
                    cols.append(col)
        tables[table_name] = cols
    return tables


def parse_seed_counts(sql: str) -> dict[str, int]:
    """Count seed data rows per table."""
    counts: dict[str, int] = {}
    for match in re.finditer(r"INSERT INTO (\w+)\s.*?VALUES\s*(.*?);", sql, re.DOTALL):
        table = match.group(1)
        values_block = match.group(2)
        # Count rows by lines starting with whitespace + open paren
        row_count = sum(
            1
            for line in values_block.strip().split("\n")
            if line.strip().startswith("('") or line.strip().startswith("(")
        )
        counts[table] = counts.get(table, 0) + row_count
    return counts


def main():
    ontology = (ONTOLOGY_DIR / "agentstreams.ttl").read_text()
    mappings = (ONTOLOGY_DIR / "mappings.ttl").read_text()
    schema = (ONTOLOGY_DIR / "schema.sql").read_text()

    classes = parse_ontology_classes(ontology)
    instances = parse_ontology_instances(ontology)
    class_table_map = parse_mapping_tables(mappings)
    column_mappings = parse_mapping_columns(mappings)
    schema_tables = parse_schema_tables(schema)
    seed_counts = parse_seed_counts(schema)

    errors = []
    warnings = []

    # Check 1: Every ontology class should have a mapping
    mapped_classes = set(class_table_map.keys())
    # Skip enum/type classes
    skip_classes = {
        "LanguageTier",
        "MetricType",
        "ResourceType",
        "Tier1",
        "Tier2",
        "Tier3",
        "Counter",
        "Timer",
        "Gauge",
        "DistributionSummary",
        "ModelCard",
        "APIPrimer",
        "LLMsIndex",
        "Cookbook",
    }
    unmapped = classes - mapped_classes - skip_classes
    for cls in sorted(unmapped):
        warnings.append(f"Ontology class as:{cls} has no mapping to a table")

    # Check 2: Every mapped table exists in schema
    for cls, table in sorted(class_table_map.items()):
        if table not in schema_tables:
            errors.append(f"Mapping {cls} → {table}: table not found in schema.sql")

    # Check 3: Every mapped column exists in its table
    for prop, table, col in column_mappings:
        if table in schema_tables:
            if col not in schema_tables[table]:
                errors.append(f"Mapping {prop} → {table}.{col}: column not found")

    # Check 4: Instance counts
    class_to_table = {
        "Language": "languages",
        "Model": "models",
        "Skill": "skills",
        "SDK": "sdks",
        "Metric": "metrics",
    }
    for cls, table in class_to_table.items():
        ont_count = len(instances.get(cls, []))
        seed_count = seed_counts.get(table, 0)
        if ont_count != seed_count and ont_count > 0:
            warnings.append(
                f"{cls}: ontology has {ont_count} instances, schema has {seed_count} seed rows"
            )

    # Report
    print("UDA Ontology ↔ Schema Validation")
    print("=" * 40)
    print(f"Classes: {len(classes)}")
    print(f"Mapped:  {len(mapped_classes)} classes → {len(set(class_table_map.values()))} tables")
    print(f"Columns: {len(column_mappings)} property → column mappings")
    print(f"Tables:  {len(schema_tables)} in schema.sql")
    print()

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ❌ {e}")
        print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠️  {w}")
        print()

    if not errors and not warnings:
        print("✅ All checks passed — ontology, mappings, and schema are aligned.")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
