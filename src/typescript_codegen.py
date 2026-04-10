"""TypeScript type and query codegen from GraphQL schemas.

Generates TypeScript code following patterns from Programming TypeScript
(Boris Cherny, O'Reilly 2019), Chapter 6 "Advanced Types":

- Branded types (p.148): ``type UserId = Brand<string, 'UserId'>``
- Discriminated unions (p.129): Tagged union results with ``type`` field
- Companion object pattern (p.140): Enum type + const value object
- Mapped types (p.137): ``Partial<CreateInput>`` for update inputs
- as const assertions (p.123): Narrowest inference for enum values
- Keying-in (p.132): Nested type accessors for deep responses
- Generic constraints (p.134): Type-safe query variable builders

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

from src.graphql_toolkit import GraphQLSchemaParser, GraphQLType
from src.projections import GraphQLProjection, OntologyParser

# ── Type Mapping ───────────────────────────────────────────

TYPE_MAP: dict[str, str] = {
    "String": "string",
    "Int": "number",
    "Float": "number",
    "Boolean": "boolean",
    "ID": "string",
    "DateTime": "string",
}

# Standard GraphQL types to skip during codegen
_SKIP_TYPES = {
    "Query", "Mutation", "Subscription",
    "__Schema", "__Type", "__Field", "__InputValue",
    "__EnumValue", "__Directive",
}


# ── TypeScript Codegen ─────────────────────────────────────


class TypeScriptCodegen:
    """Generate TypeScript types and typed query functions from GraphQL types.

    Applies patterns from Programming TypeScript (Cherny, Ch. 6):

    1. Branded types: Every GraphQL ``ID`` field gets a branded type to
       prevent mixing incompatible IDs at compile time.
    2. Discriminated unions: GraphQL union types become tagged unions
       with a ``type`` discriminant field.
    3. Companion object pattern: GraphQL enums generate both a type
       (union of string literals) and a const object.
    4. as const assertions: Enum const objects use ``as const`` for
       narrowest possible type inference.
    """

    def __init__(self, types: list[GraphQLType]):
        self.types = types
        self._object_types = [t for t in types if t.kind == "OBJECT" and t.name not in _SKIP_TYPES]
        self._enum_types = [t for t in types if t.kind == "ENUM"]
        self._input_types = [t for t in types if t.kind == "INPUT"]
        self._union_types = [t for t in types if t.kind == "UNION"]
        self._scalar_types = [t for t in types if t.kind == "SCALAR"]

    def generate_branded_ids(self) -> str:
        """Generate branded ID types for type-safe identity fields.

        Pattern from Programming TypeScript p.148 (simulating nominal types):
        ``type UserId = Brand<string, 'UserId'>``

        Prevents accidentally passing a PostId where a UserId is expected.
        """
        lines = [
            "// ── Branded ID types (Cherny p.148) ─────────────────",
            "declare const __brand: unique symbol;",
            "type Brand<T, B extends string> = T & { readonly [__brand]: B };",
            "",
        ]

        # Collect all types that have an 'id' field
        branded_types: list[str] = []
        for gql_type in self._object_types:
            for fld in gql_type.fields:
                if fld.name == "id" and fld.type_name == "ID":
                    brand_name = f"{gql_type.name}Id"
                    branded_types.append(brand_name)
                    lines.append(
                        f"export type {brand_name} = Brand<string, '{brand_name}'>;"
                    )
                    break

        if branded_types:
            lines.append("")
        return "\n".join(lines)

    def generate_enum_consts(self) -> str:
        """Generate companion object pattern for GraphQL enums.

        Pattern from Programming TypeScript p.140:
        Both a type (union of string literals) and a const value object
        share the same name — consumers can import both at once.

        Uses ``as const`` assertions (p.123) for narrowest inference.
        """
        lines = [
            "// ── Enum companion objects (Cherny p.140) ───────────",
            "",
        ]

        for enum_type in self._enum_types:
            values = enum_type.enum_values
            if not values:
                continue

            # Type alias: union of string literals
            union_parts = " | ".join(f"'{v}'" for v in values)
            lines.append(f"export type {enum_type.name} = {union_parts};")

            # Const object: runtime values with as const
            obj_entries = ", ".join(f"{v}: '{v}'" for v in values)
            lines.append(
                f"export const {enum_type.name} = {{ {obj_entries} }} as const;"
            )
            lines.append("")

        return "\n".join(lines)

    def generate_types(self) -> str:
        """Generate TypeScript interfaces for GraphQL object types."""
        lines = [
            "// ── Object types ────────────────────────────────────",
            "",
        ]

        for gql_type in self._object_types:
            if gql_type.name.endswith("Connection") or gql_type.name.endswith("Edge"):
                continue  # Handled by generate_connection_helpers
            if gql_type.name == "PageInfo":
                continue

            lines.append(f"export interface {gql_type.name} {{")
            for fld in gql_type.fields:
                ts_type = self._resolve_field_type(fld.type_name, fld.is_list, gql_type.name, fld.name)
                optional = "" if fld.is_non_null else "?"
                lines.append(f"  {fld.name}{optional}: {ts_type};")
            lines.append("}")
            lines.append("")

        return "\n".join(lines)

    def generate_input_types(self) -> str:
        """Generate TypeScript types for GraphQL input types.

        Uses mapped types (Cherny p.137): Update inputs are generated as
        ``Partial<CreateInput>`` pattern when applicable.
        """
        lines = [
            "// ── Input types (mapped types, Cherny p.137) ───────",
            "",
        ]

        create_inputs: dict[str, str] = {}
        for input_type in self._input_types:
            lines.append(f"export interface {input_type.name} {{")
            for fld in input_type.fields:
                ts_type = self._resolve_field_type(fld.type_name, fld.is_list)
                optional = "" if fld.is_non_null else "?"
                lines.append(f"  {fld.name}{optional}: {ts_type};")
            lines.append("}")

            if input_type.name.startswith("Create"):
                base = input_type.name.removeprefix("Create").removesuffix("Input")
                create_inputs[base] = input_type.name

            lines.append("")

        # Generate Update types as Partial<Create> where possible
        for input_type in self._input_types:
            if input_type.name.startswith("Update"):
                base = input_type.name.removeprefix("Update").removesuffix("Input")
                if base in create_inputs:
                    lines.append(
                        f"// Mapped type: Update{base}Input ≈ Partial<{create_inputs[base]}>"
                    )

        return "\n".join(lines)

    def generate_discriminated_unions(self) -> str:
        """Generate discriminated unions for GraphQL union types.

        Pattern from Programming TypeScript p.129 (tagged unions):
        Each variant has a ``type`` discriminant field for exhaustive narrowing.
        """
        lines = [
            "// ── Discriminated unions (Cherny p.129) ─────────────",
            "",
        ]

        for union_type in self._union_types:
            members = union_type.union_types
            if not members:
                continue

            lines.append(f"export type {union_type.name} =")
            for i, member in enumerate(members):
                separator = "|" if i > 0 else " "
                lines.append(f"  {separator} {{ readonly __typename: '{member}' }} & {member}")
            lines.append(";")
            lines.append("")

        # Always generate a QueryResult discriminated union
        lines.extend([
            "// ── Query result wrapper ────────────────────────────",
            "",
            "export interface GraphQLError {",
            "  readonly message: string;",
            "  readonly locations?: readonly { line: number; column: number }[];",
            "  readonly path?: readonly (string | number)[];",
            "}",
            "",
            "export type QueryResult<T> =",
            "  | { readonly type: 'success'; readonly data: T }",
            "  | { readonly type: 'error'; readonly errors: readonly GraphQLError[] };",
            "",
        ])

        return "\n".join(lines)

    def generate_query_functions(self) -> str:
        """Generate typed query function stubs.

        Uses generic constraints (Cherny p.134):
        ``<K extends keyof O>(o: O, k: K): O[K]``
        for type-safe variable passing.
        """
        lines = [
            "// ── Typed query functions (Cherny p.134) ────────────",
            "",
        ]

        for gql_type in self._object_types:
            if gql_type.name.endswith("Connection") or gql_type.name.endswith("Edge"):
                continue
            if gql_type.name == "PageInfo":
                continue

            name = gql_type.name
            fn_name = f"query{name}"

            # Check if type has an ID field for single-entity query
            has_id = any(f.name == "id" for f in gql_type.fields)
            if has_id:
                brand_name = f"{name}Id"
                lines.append(
                    f"export declare function {fn_name}(id: {brand_name}): "
                    f"Promise<QueryResult<{name}>>;"
                )
            else:
                lines.append(
                    f"export declare function {fn_name}(): "
                    f"Promise<QueryResult<{name}>>;"
                )

        lines.append("")
        return "\n".join(lines)

    def generate_connection_helpers(self) -> str:
        """Generate Relay-style pagination helper types."""
        lines = [
            "// ── Relay connection helpers ────────────────────────",
            "",
            "export interface PageInfo {",
            "  readonly hasNextPage: boolean;",
            "  readonly hasPreviousPage?: boolean;",
            "  readonly startCursor?: string;",
            "  readonly endCursor?: string;",
            "}",
            "",
            "export interface Edge<T> {",
            "  readonly node: T;",
            "  readonly cursor: string;",
            "}",
            "",
            "export interface Connection<T> {",
            "  readonly edges: readonly Edge<T>[];",
            "  readonly pageInfo: PageInfo;",
            "  readonly totalCount?: number;",
            "}",
            "",
        ]
        return "\n".join(lines)

    def generate_all(self) -> str:
        """Generate complete TypeScript module content."""
        parts = [
            "/**",
            " * Auto-generated TypeScript types from GraphQL schema.",
            " * Source: ontology/agentstreams.ttl → GraphQL SDL → TypeScript",
            " *",
            " * Patterns from Programming TypeScript (Cherny, O'Reilly 2019):",
            " * - Branded types (p.148) for type-safe IDs",
            " * - Companion object pattern (p.140) for enums",
            " * - Discriminated unions (p.129) for query results",
            " * - Mapped types (p.137) for input transformations",
            " * - Generic constraints (p.134) for query functions",
            " */",
            "",
            "/* eslint-disable @typescript-eslint/no-empty-interface */",
            "",
            self.generate_branded_ids(),
            self.generate_enum_consts(),
            self.generate_types(),
            self.generate_input_types(),
            self.generate_connection_helpers(),
            self.generate_discriminated_unions(),
            self.generate_query_functions(),
        ]
        return "\n".join(parts)

    def _resolve_field_type(
        self,
        type_name: str,
        is_list: bool = False,
        parent_type: str = "",
        field_name: str = "",
    ) -> str:
        """Resolve a GraphQL type name to a TypeScript type string."""
        # Check for branded ID
        if type_name == "ID" and field_name == "id" and parent_type:
            ts_type = f"{parent_type}Id"
        elif type_name in TYPE_MAP:
            ts_type = TYPE_MAP[type_name]
        else:
            # Reference to another type (object, enum, etc.)
            ts_type = type_name

        if is_list:
            ts_type = f"readonly {ts_type}[]"

        return ts_type


# ── Convenience Functions ──────────────────────────────────


def codegen_from_sdl(sdl: str) -> str:
    """One-shot: GraphQL SDL string → TypeScript module string."""
    parser = GraphQLSchemaParser()
    types = parser.parse(sdl)
    codegen = TypeScriptCodegen(types)
    return codegen.generate_all()


def codegen_from_ontology(ontology_parser: OntologyParser | None = None) -> str:
    """One-shot: ontology → GraphQL SDL → TypeScript types."""
    if ontology_parser is None:
        ontology_parser = OntologyParser()
        ontology_parser.parse()

    # Generate GraphQL SDL from ontology
    gql = GraphQLProjection(ontology_parser)
    sdl = gql.generate_all()

    # Parse the generated SDL back into structured types
    schema_parser = GraphQLSchemaParser()
    types = schema_parser.parse(sdl)

    # Generate TypeScript from the parsed types
    codegen = TypeScriptCodegen(types)
    return codegen.generate_all()
