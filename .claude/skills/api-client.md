---
name: api-client
description: "Build API clients with retry, auth, rate limiting, and OpenAPI code generation"
trigger: "user asks to build API clients, generate SDKs, test REST/GraphQL APIs, mock responses, handle OAuth, implement retry/backoff, or wrap APIs with Claude"
---

Read `skills/api-client/SKILL.md` for the full skill definition, then follow the language detection rules to load the appropriate language README.

## UDA Programmatic Tools (src/)

For Python API clients, use the unified src/ modules:

| Module | Class/Function | Purpose |
|--------|---------------|---------|
| `src/mcp_tools.py` | `MCPToolHandler` | MCP SDK v2 tool server for API integration |
| `src/agent_tasks.py` | `AgentRunner`, `AgentConfig` | Agent SDK v2 client orchestration |
| `src/neon_db.py` | `record_metric` | API call metrics to dimensional fact table |
| `src/dspy_prompts.py` | `EXTRACT_API_PATTERNS` | Extract API patterns from documentation |
| `src/graphql_toolkit.py` | `GraphQLSchemaParser`, `introspect_pg_graphql` | Parse GraphQL SDL, introspect pg_graphql |
| `src/typescript_codegen.py` | `TypeScriptCodegen`, `codegen_from_sdl` | Generate TypeScript types from GraphQL |
| `src/cube_models.py` | `CubeProjection` | Cube.dev YAML data model generation |
