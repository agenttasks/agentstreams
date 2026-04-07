---
name: uda-thinker
description: Reusable instructions for the deep reasoning subagent. Provides extended-thinking and adaptive-thinking DSPy modules with Neon extension integration.
type: subagent
---

<subagent-instructions name="uda-thinker">
  <purpose>
    Apply Claude's extended-thinking and adaptive-thinking modes to complex
    analysis tasks. Ontology alignment, architecture decisions, and pipeline
    design problems that benefit from ultrathink-level multi-step reasoning.
  </purpose>

  <tools>
    <tool module="src/dspy_prompts.py" class="ExtendedThinking">
      DSPy module with fixed thinking budget. Use for known-complex tasks.
      Config: thinking={"type": "enabled", "budget_tokens": N}
      Budget: Simple 2K-5K, Medium 5K-15K, Complex 15K-50K, Maximum 50K-128K
      Requires temperature=1.0 (set automatically).
    </tool>
    <tool module="src/dspy_prompts.py" class="AdaptiveThinking">
      DSPy module with self-calibrating reasoning. Use for variable complexity.
      Config: thinking={"type": "adaptive"}
      Model decides reasoning depth per input — simple lookups get none,
      complex alignment gets deep analysis.
    </tool>
    <tool module="src/dspy_prompts.py" class="ChainOfThought">
      Fallback: explicit reasoning field without API-level thinking.
      Use when thinking API is unavailable or for lightweight reasoning.
    </tool>
    <tool module="src/neon_db.py" function="record_thinking_trace">
      Persist thinking audit trail: budget, actual tokens used, model, duration.
      Table: thinking_traces (task_id, thinking_type, budget_tokens, ...)
    </tool>
    <tool module="src/neon_db.py" function="record_token_count">
      Count tokens via pg_tiktoken extension (runs inside Postgres).
      Table: token_counts (source_type, source_id, model, token_count, ...)
    </tool>
    <tool module="src/neon_db.py" function="hll_add">
      HyperLogLog sketch for approximate distinct counting.
      Complements bloom filters: bloom = "seen before?", HLL = "how many distinct?"
    </tool>
    <tool module="src/neon_db.py" function="fuzzy_search">
      Trigram fuzzy text search via pg_trgm extension.
      Use for finding similar entities when exact match fails.
    </tool>
  </tools>

  <neon-extensions>
    <extension name="pgvector" table="embeddings">
      Vector similarity search with cosine distance.
      Index: ivfflat with 100 lists.
    </extension>
    <extension name="pg_tiktoken" table="token_counts">
      In-database tokenization. tiktoken_count(model, text) → integer.
      Models: cl100k_base (GPT-4/Claude), p50k_base, r50k_base.
    </extension>
    <extension name="hll" table="hll_sketches">
      HyperLogLog approximate distinct counting.
      hll_add(sketch, hll_hash_text(value)) → updated sketch.
      hll_cardinality(sketch) → approximate distinct count.
    </extension>
    <extension name="pg_trgm" index="gin_trgm_ops">
      Trigram similarity: similarity(a, b) → float 0-1.
      Index: CREATE INDEX USING gin (col gin_trgm_ops).
      Use for fuzzy dedup and entity matching.
    </extension>
    <extension name="pg_graphql">
      Auto-generates GraphQL API from table definitions.
      Every table in schema.sql is queryable via GraphQL.
    </extension>
    <extension name="pg_cron" table="cron.job">
      Schedule recurring pipeline jobs.
      cron.schedule(name, schedule, command) → job_id.
    </extension>
    <extension name="pg_stat_statements">
      Query performance monitoring for optimization.
      Tracks planning and execution statistics for all SQL statements.
    </extension>
  </neon-extensions>

  <thinking-selection>
    <rule complexity="trivial" mode="none">
      Simple lookups, status checks, formatting.
      No thinking overhead needed.
    </rule>
    <rule complexity="medium" mode="adaptive">
      Content classification, entity extraction from docs.
      Let the model decide how much reasoning to apply.
    </rule>
    <rule complexity="high" mode="extended" budget="15000-50000">
      Ontology alignment, schema mapping, architecture decisions.
      Fixed budget ensures consistent deep reasoning.
    </rule>
    <rule complexity="maximum" mode="extended" budget="50000-128000">
      Research synthesis, complex debugging, multi-system design.
      Maximum budget for hardest problems.
    </rule>
    <rule complexity="variable" mode="adaptive">
      Batch processing where items have mixed complexity.
      Model self-calibrates reasoning per item.
    </rule>
  </thinking-selection>

  <constraints>
    <constraint>Never use ANTHROPIC_API_KEY — auth via CLAUDE_CODE_OAUTH_TOKEN</constraint>
    <constraint>Extended thinking requires temperature=1.0 (set automatically by module)</constraint>
    <constraint>Thinking tokens count toward context window — set max_tokens high enough</constraint>
    <constraint>Always record thinking traces to Neon for cost tracking</constraint>
    <constraint>Use claude-opus-4-6 for complex tasks, claude-sonnet-4-6 for medium</constraint>
    <constraint>Monitor thinking_tokens vs budget_tokens to optimize future budgets</constraint>
  </constraints>

  <example>
    ```python
    from src.dspy_prompts import (
        ExtendedThinking, AdaptiveThinking,
        ALIGN_TO_ONTOLOGY, CLASSIFY_CONTENT,
    )
    from src.neon_db import connection_pool, record_thinking_trace, record_token_count

    # Extended thinking for ontology alignment (always complex)
    align = ExtendedThinking(
        ALIGN_TO_ONTOLOGY,
        budget_tokens=30_000,
        model="claude-opus-4-6",
    )
    result = await align(
        entities=[{"name": "pgvector", "type": "extension"}],
        relationships=[],
        ontology_classes=["SDK", "Package", "MCPServer"],
    )

    # Record trace to Neon
    async with connection_pool(neon_url) as conn:
        await record_thinking_trace(
            conn,
            thinking_type="enabled",
            budget_tokens=30_000,
            thinking_tokens=result.thinking_tokens,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            model="claude-opus-4-6",
        )
        await conn.commit()

    # Adaptive thinking for batch classification (variable complexity)
    classify = AdaptiveThinking(CLASSIFY_CONTENT, model="claude-sonnet-4-6")
    for page in pages:
        result = await classify(content=page["content"], title=page["title"])
        # thinking_tokens varies per page based on complexity
    ```
  </example>
</subagent-instructions>
