---
name: uda-projector
description: Reusable instructions for the UDA ontology projection subagent. Generates Avro, GraphQL, DataContainer, and Mapping files from the ontology source of truth.
type: subagent
---

<subagent-instructions name="uda-projector">
  <purpose>
    Generate multiple format projections from the AgentStreams ontology
    following Netflix UDA's "Model Once, Represent Everywhere" pattern.
    The ontology (ontology/agentstreams.ttl) is the single source of truth;
    all other representations are auto-generated projections.
  </purpose>

  <tools>
    <tool module="src/projections.py" class="OntologyParser">
      Parses TTL ontology into structured class/property/enum model.
      Methods: parse() → populates classes, properties, enums dicts
    </tool>
    <tool module="src/projections.py" class="AvroProjection">
      Generate Avro record schemas with udaUri annotations.
      Methods: generate(class_name), generate_all(), to_json()
    </tool>
    <tool module="src/projections.py" class="GraphQLProjection">
      Generate GraphQL types with @key and @udaUri directives.
      Methods: generate(class_name), generate_enums(), generate_all()
    </tool>
    <tool module="src/projections.py" class="DataContainerProjection">
      Generate TTL DataContainer definitions (data mesh source registration).
      Methods: generate(class_name, source_id)
    </tool>
    <tool module="src/projections.py" class="MappingProjection">
      Generate TTL mapping definitions (ontology → physical layer bridges).
      Methods: generate(class_name, table_name)
    </tool>
    <tool module="src/projections.py" function="generate_all_projections">
      Convenience function generating all projections at once.
      Returns dict mapping filename → content.
    </tool>
  </tools>

  <uda-pattern>
    <principle>Ontology is the single source of truth</principle>
    <projection format="avro">
      Avro record schemas for data pipeline serialization.
      Each class becomes a record; relationships become reference records.
      Fields carry udaUri linking back to ontology properties.
    </projection>
    <projection format="graphql">
      GraphQL types for API layer (exposed via pg_graphql in Neon).
      Types have @key directives for federation, @udaUri for traceability.
      Enums map directly to ontology enumerations.
    </projection>
    <projection format="datacontainer">
      TTL DataContainer definitions for data mesh registration.
      Each class gets a datamesh:Source with field projections.
      Relationships become foreign-key reference records.
    </projection>
    <projection format="mapping">
      TTL mapping definitions bridging ontology → Postgres tables.
      Each class maps to a table; properties map to columns.
      camelCase properties auto-convert to snake_case columns.
    </projection>
  </uda-pattern>

  <constraints>
    <constraint>Never modify ontology/agentstreams.ttl — it is the source of truth</constraint>
    <constraint>Generated files must carry provenance comments</constraint>
    <constraint>Avro field names are prefixed AS_ (AgentStreams namespace)</constraint>
    <constraint>GraphQL type names are prefixed AS_</constraint>
    <constraint>Mapping column names use snake_case conversion</constraint>
  </constraints>

  <example>
    ```python
    from src.projections import generate_all_projections

    # Generate everything to output/ directory
    results = generate_all_projections(output_dir="output/projections")
    for filename in sorted(results):
        print(f"  Generated: {filename}")
    ```
  </example>
</subagent-instructions>
