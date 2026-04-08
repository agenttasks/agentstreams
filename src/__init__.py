"""AgentStreams — Unified Data Architecture modules.

Model Once, Represent Everywhere. Inspired by Netflix UDA.

Modules:
    bloom       — Probabilistic bloom filter with Neon Postgres persistence
    neon_db     — Async Neon Postgres 18 connection pool and data layer
    crawlers    — Scrapy-pattern web crawlers with DB persistence
    dspy_prompts — DSPy headless subagent prompting for structured extraction
    projections — UDA ontology projection generators (Avro, GraphQL, TTL)
    mcp_tools   — MCP SDK v2 tool server exposing src/ capabilities
    agent_tasks — Agent SDK v2 task orchestration
    harness     — GAN-inspired planner → generator → evaluator iterative loop
    embeddings  — LanceDB + Neon pgvector dual-backend vector store
    tracing     — OpenTelemetry distributed tracing
"""
