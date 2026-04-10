-- ═══════════════════════════════════════════════════════════
-- LexGLUE Benchmark Schema — Neon Postgres 18
-- pgvector, pg_graphql, pg_trgm
--
-- Kimball patterns:
--   Transaction fact: julia_lexglue_samples, julia_lexglue_results
--   Degenerate dimension: task (no separate dim table)
--
-- All tables annotated with COMMENT ON for pg_graphql auto-generation.
-- Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
-- ═══════════════════════════════════════════════════════════

-- Extensions already created in ontology/schema.sql:
--   pg_graphql, vector, pg_tiktoken, hll, pg_trgm,
--   pg_stat_statements, pg_cron

-- ── LexGLUE Samples (Transaction Fact) ──────────────────────
-- Grain: one benchmark sample. Task is degenerate dimension.
-- Source: HuggingFace lex_glue dataset (8 tasks).

CREATE TABLE IF NOT EXISTS julia_lexglue_samples (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    task TEXT NOT NULL CHECK (task IN (
        'ledgar', 'unfair_tos', 'scotus', 'ecthr_a', 'ecthr_b',
        'eurlex', 'contract_nli', 'casehold'
    )),
    hf_index INTEGER NOT NULL,           -- HuggingFace dataset index
    text TEXT NOT NULL,                   -- document/premise text
    -- CaseHOLD-specific: multiple-choice holdings
    holdings JSONB,                      -- array of 5 candidate holdings
    -- Labels
    label TEXT,                          -- single-label (LEDGAR, SCOTUS, ContractNLI, CaseHOLD)
    labels JSONB,                        -- multi-label (UNFAIR-ToS, ECtHR-A/B, EUR-Lex)
    label_set JSONB NOT NULL,            -- valid label vocabulary for this task
    -- Metadata
    split TEXT NOT NULL DEFAULT 'test',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    content_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (task, hf_index, split)
);

CREATE INDEX IF NOT EXISTS idx_lexglue_task ON julia_lexglue_samples(task);
CREATE INDEX IF NOT EXISTS idx_lexglue_split ON julia_lexglue_samples(split);
CREATE INDEX IF NOT EXISTS idx_lexglue_hash ON julia_lexglue_samples(content_hash);

COMMENT ON TABLE julia_lexglue_samples IS
    'LexGLUE benchmark samples from HuggingFace lex_glue dataset';
COMMENT ON COLUMN julia_lexglue_samples.task IS
    'LexGLUE task: ledgar, unfair_tos, scotus, ecthr_a, ecthr_b, eurlex, contract_nli, casehold';
COMMENT ON COLUMN julia_lexglue_samples.hf_index IS
    'Original index in the HuggingFace dataset split';
COMMENT ON COLUMN julia_lexglue_samples.holdings IS
    'CaseHOLD: 5 candidate holdings (JSON array of strings)';
COMMENT ON COLUMN julia_lexglue_samples.label IS
    'Ground truth for single-label tasks (LEDGAR, SCOTUS, ContractNLI, CaseHOLD)';
COMMENT ON COLUMN julia_lexglue_samples.labels IS
    'Ground truth for multi-label tasks (UNFAIR-ToS types, ECtHR-A/B articles, EUR-Lex concepts)';
COMMENT ON COLUMN julia_lexglue_samples.label_set IS
    'Valid label vocabulary for this task (JSON array)';

-- ── LexGLUE Embeddings (pgvector) ───────────────────────────
-- Chunks of sample texts with 384-dim embeddings for retrieval.
-- Follows julia_vault_file_chunks pattern.

CREATE TABLE IF NOT EXISTS julia_lexglue_embeddings (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    sample_id TEXT NOT NULL REFERENCES julia_lexglue_samples(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    embedding vector(384),               -- pgvector: same dim as src/embeddings.py
    token_count INTEGER NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (sample_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_lexglue_emb_sample ON julia_lexglue_embeddings(sample_id);
CREATE INDEX IF NOT EXISTS idx_lexglue_emb_vector ON julia_lexglue_embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_lexglue_emb_trgm ON julia_lexglue_embeddings
    USING gin (content gin_trgm_ops);

COMMENT ON TABLE julia_lexglue_embeddings IS
    'pgvector embeddings for LexGLUE sample chunks (384-dim, IVFFlat)';
COMMENT ON COLUMN julia_lexglue_embeddings.embedding IS
    '384-dim vector (hash_embedding from src/embeddings.py)';

-- ── LexGLUE Results (Transaction Fact) ──────────────────────
-- Stores eval run results for tracking Julia performance over time.
-- Grain: one prediction per sample per run.

CREATE TABLE IF NOT EXISTS julia_lexglue_results (
    id BIGSERIAL PRIMARY KEY,
    run_id TEXT NOT NULL,                -- groups results by eval run
    sample_id TEXT NOT NULL REFERENCES julia_lexglue_samples(id),
    task TEXT NOT NULL,
    predicted_label TEXT,                -- single-label prediction
    predicted_labels JSONB,              -- multi-label prediction
    gold_label TEXT,                     -- ground truth (single)
    gold_labels JSONB,                   -- ground truth (multi)
    is_correct BOOLEAN,
    confidence FLOAT,
    model TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    latency_ms INTEGER,
    raw_output TEXT,                     -- full model response
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_lexglue_results_run ON julia_lexglue_results(run_id);
CREATE INDEX IF NOT EXISTS idx_lexglue_results_task ON julia_lexglue_results(task);
CREATE INDEX IF NOT EXISTS idx_lexglue_results_sample ON julia_lexglue_results(sample_id);

COMMENT ON TABLE julia_lexglue_results IS
    'LexGLUE eval run results (Kimball transaction fact)';
COMMENT ON COLUMN julia_lexglue_results.run_id IS
    'Eval run identifier — groups all predictions in a single benchmark run';
COMMENT ON COLUMN julia_lexglue_results.is_correct IS
    'Whether predicted label(s) match gold label(s)';
COMMENT ON COLUMN julia_lexglue_results.confidence IS
    'Model-reported confidence score (0.0-1.0)';
