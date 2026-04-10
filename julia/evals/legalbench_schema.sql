-- ═══════════════════════════════════════════════════════════
-- LegalBench Benchmark Schema — Neon Postgres 18
-- pgvector 0.8.1, pg_graphql 1.5.12, pg_trgm 1.6,
-- pg_tiktoken 0.0.1, hll 2.19, pg_cron 1.6
--
-- Kimball patterns (per "The Data Warehouse Toolkit", 3rd Ed.):
--   Transaction fact: julia_legalbench_samples, julia_legalbench_results
--   Degenerate dimension: task, category (no separate dim table —
--     162 tasks × 22 categories is low cardinality, Ch.3 p.47)
--   Conformed dimension: model (FK to ontology models table)
--   Additive measures: input_tokens, output_tokens, duration_ms,
--     citation_score (can be summed/averaged across any dimension)
--   Periodic snapshot: julia_legalbench_category_stats (pg_cron daily)
--
-- All tables annotated with COMMENT ON for pg_graphql 1.5.12 auto-generation.
-- Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
-- ═══════════════════════════════════════════════════════════

-- Extensions already created in ontology/schema.sql:
--   pg_graphql, vector, pg_tiktoken, hll, pg_trgm,
--   pg_stat_statements, pg_cron

-- ── LegalBench Samples (Transaction Fact) ──────────────────────
-- Grain: one benchmark sample per task per split.
-- Source: HuggingFace nguha/legalbench dataset (162 tasks, 22 categories).
-- Kimball: task + category are degenerate dimensions.

CREATE TABLE IF NOT EXISTS julia_legalbench_samples (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    task TEXT NOT NULL,                    -- Degenerate dimension (162 tasks)
    category TEXT NOT NULL,                -- Degenerate dimension (22 categories)
    hf_index INTEGER NOT NULL,            -- HuggingFace dataset index
    text TEXT NOT NULL,                    -- Document/premise text (may be concatenation of multiple fields)
    context TEXT,                          -- Additional context (sara statutes, corporate lobbying descriptions, etc.)
    answer TEXT,                           -- Ground truth answer
    answer_type TEXT NOT NULL              -- binary, multiple_choice, classification, extraction
        CHECK (answer_type IN ('binary', 'multiple_choice', 'classification', 'extraction')),
    label_names JSONB,                     -- Valid label vocabulary for this task
    split TEXT NOT NULL DEFAULT 'test',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    content_hash TEXT NOT NULL,
    -- Approximate word-count token estimate for prompt budgeting
    token_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (task, hf_index, split)
);

CREATE INDEX IF NOT EXISTS idx_legalbench_task ON julia_legalbench_samples(task);
CREATE INDEX IF NOT EXISTS idx_legalbench_category ON julia_legalbench_samples(category);
CREATE INDEX IF NOT EXISTS idx_legalbench_split ON julia_legalbench_samples(split);
CREATE INDEX IF NOT EXISTS idx_legalbench_hash ON julia_legalbench_samples(content_hash);
-- pg_trgm 1.6: fuzzy text search on sample content
CREATE INDEX IF NOT EXISTS idx_legalbench_text_trgm ON julia_legalbench_samples
    USING gin (text gin_trgm_ops);

COMMENT ON TABLE julia_legalbench_samples IS
    'LegalBench benchmark samples from HuggingFace nguha/legalbench (162 tasks)';
COMMENT ON COLUMN julia_legalbench_samples.task IS
    'Degenerate dimension: one of 162 LegalBench tasks (e.g. contract_nli_explicit_identification)';
COMMENT ON COLUMN julia_legalbench_samples.category IS
    'Degenerate dimension: task category (contract_nli, cuad, maud, learned_hands, etc.)';
COMMENT ON COLUMN julia_legalbench_samples.hf_index IS
    'Original index in the HuggingFace dataset split';
COMMENT ON COLUMN julia_legalbench_samples.context IS
    'Additional context fields (sara statutes, corporate lobbying company descriptions, etc.)';
COMMENT ON COLUMN julia_legalbench_samples.answer IS
    'Ground truth answer (exact match target)';
COMMENT ON COLUMN julia_legalbench_samples.answer_type IS
    'binary (Yes/No), multiple_choice (A/B/C/D), classification (fixed labels), extraction (free text)';
COMMENT ON COLUMN julia_legalbench_samples.label_names IS
    'Valid label vocabulary for this task (JSON array)';
COMMENT ON COLUMN julia_legalbench_samples.token_count IS
    'Approximate word-count token estimate for prompt budgeting (whitespace split)';

-- ── LegalBench Embeddings (pgvector 0.8.1) ─────────────────────
-- Chunks of sample texts with 384-dim embeddings for retrieval.
-- Follows julia_vault_file_chunks pattern.

CREATE TABLE IF NOT EXISTS julia_legalbench_embeddings (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    sample_id TEXT NOT NULL REFERENCES julia_legalbench_samples(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    embedding vector(384),                 -- pgvector 0.8.1: same dim as src/embeddings.py
    token_count INTEGER NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (sample_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_legalbench_emb_sample ON julia_legalbench_embeddings(sample_id);
CREATE INDEX IF NOT EXISTS idx_legalbench_emb_vector ON julia_legalbench_embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_legalbench_emb_trgm ON julia_legalbench_embeddings
    USING gin (content gin_trgm_ops);

COMMENT ON TABLE julia_legalbench_embeddings IS
    'pgvector 0.8.1 embeddings for LegalBench sample chunks (384-dim, IVFFlat)';
COMMENT ON COLUMN julia_legalbench_embeddings.embedding IS
    '384-dim vector (hash_embedding from src/embeddings.py)';

-- ── LegalBench Results (Transaction Fact) ──────────────────────
-- Stores eval run results for tracking Julia performance over time.
-- Grain: one prediction per sample per run.
-- Kimball: additive measures — input_tokens, output_tokens, duration_ms,
--   citation_score can be summed/averaged across any dimension combination.

CREATE TABLE IF NOT EXISTS julia_legalbench_results (
    id BIGSERIAL PRIMARY KEY,
    run_id TEXT NOT NULL,                  -- Groups results by eval run
    sample_id TEXT REFERENCES julia_legalbench_samples(id),  -- NULL when running from JSON without Neon ingest
    task TEXT NOT NULL,                    -- Degenerate dimension
    category TEXT NOT NULL,                -- Degenerate dimension
    predicted_answer TEXT,                 -- Model prediction
    gold_answer TEXT,                      -- Ground truth
    is_correct BOOLEAN,
    confidence FLOAT,                      -- Model-reported confidence (0.0-1.0)
    reasoning TEXT,                         -- Chain-of-thought output
    quotes_used JSONB,                     -- Citation grounding evidence (array of strings)
    citation_score FLOAT,                  -- Source verification score (0.0-1.0)
    best_of_n_count INTEGER DEFAULT 1,     -- How many attempts in Best-of-N
    best_of_n_agreement FLOAT DEFAULT 1.0, -- Majority vote agreement ratio
    model TEXT NOT NULL,                   -- Conformed dimension (FK to models)
    input_tokens INTEGER,                  -- Additive measure
    output_tokens INTEGER,                 -- Additive measure
    duration_ms INTEGER,                   -- Additive measure
    raw_output TEXT,                        -- Full model response (truncated to 4000 chars)
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_legalbench_results_run ON julia_legalbench_results(run_id);
CREATE INDEX IF NOT EXISTS idx_legalbench_results_task ON julia_legalbench_results(task);
CREATE INDEX IF NOT EXISTS idx_legalbench_results_category ON julia_legalbench_results(category);
CREATE INDEX IF NOT EXISTS idx_legalbench_results_sample ON julia_legalbench_results(sample_id);

COMMENT ON TABLE julia_legalbench_results IS
    'LegalBench eval run results (Kimball transaction fact, grain = one prediction per sample per run)';
COMMENT ON COLUMN julia_legalbench_results.run_id IS
    'Eval run identifier — groups all predictions in a single benchmark run';
COMMENT ON COLUMN julia_legalbench_results.is_correct IS
    'Whether predicted answer matches gold answer (exact match after normalization)';
COMMENT ON COLUMN julia_legalbench_results.confidence IS
    'Model-reported confidence score (0.0-1.0)';
COMMENT ON COLUMN julia_legalbench_results.quotes_used IS
    'Direct quotes extracted from source document before analysis (anti-hallucination grounding)';
COMMENT ON COLUMN julia_legalbench_results.citation_score IS
    'Source verification score: fraction of quotes_used verified in source text (0.0-1.0)';
COMMENT ON COLUMN julia_legalbench_results.best_of_n_count IS
    'Number of completions used in Best-of-N verification (1 = single pass)';
COMMENT ON COLUMN julia_legalbench_results.best_of_n_agreement IS
    'Majority vote agreement ratio for Best-of-N (1.0 = unanimous)';

-- ── LegalBench Category Stats (Periodic Snapshot) ──────────────
-- Daily category-level accuracy rollup for dashboard queries.
-- Kimball: periodic snapshot fact, grain = one category per day.

CREATE TABLE IF NOT EXISTS julia_legalbench_category_stats (
    category TEXT NOT NULL,
    date DATE NOT NULL,
    accuracy FLOAT,                        -- Mean accuracy across all tasks in category
    sample_count INTEGER,                  -- Number of predictions
    avg_citation_score FLOAT,              -- Mean source verification score
    avg_confidence FLOAT,                  -- Mean model confidence
    avg_latency_ms INTEGER,                -- Mean latency
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (category, date)
);

COMMENT ON TABLE julia_legalbench_category_stats IS
    'Periodic snapshot: daily category-level accuracy rollup (pg_cron at 2 AM UTC)';

-- ── pg_cron: Daily Aggregation ─────────────────────────────────
-- Per julia/schema.sql:315-336 pattern (julia-daily-matter-stats).

SELECT cron.schedule(
    'julia-daily-legalbench-stats',
    '0 2 * * *',
    $$
    INSERT INTO julia_legalbench_category_stats
        (category, date, accuracy, sample_count, avg_citation_score, avg_confidence, avg_latency_ms)
    SELECT
        category,
        CURRENT_DATE,
        AVG(CASE WHEN is_correct THEN 1.0 ELSE 0.0 END),
        COUNT(*),
        AVG(citation_score),
        AVG(confidence),
        AVG(duration_ms)::integer
    FROM julia_legalbench_results
    WHERE created_at >= CURRENT_DATE - INTERVAL '1 day'
      AND created_at < CURRENT_DATE
    GROUP BY category
    ON CONFLICT (category, date) DO UPDATE SET
        accuracy = EXCLUDED.accuracy,
        sample_count = EXCLUDED.sample_count,
        avg_citation_score = EXCLUDED.avg_citation_score,
        avg_confidence = EXCLUDED.avg_confidence,
        avg_latency_ms = EXCLUDED.avg_latency_ms,
        updated_at = now()
    $$
);
