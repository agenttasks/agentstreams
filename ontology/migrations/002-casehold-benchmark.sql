-- ═══════════════════════════════════════════════════════════
-- Migration 002: CaseHOLD Legal Holdings Benchmark
--
-- Adds tables for storing CaseHOLD dataset (53K+ legal holdings)
-- and evaluation results. Uses pgvector for semantic search
-- and pg_trgm for fuzzy text matching on citing prompts.
--
-- Source: HuggingFace casehold/casehold
-- GitHub issue: https://github.com/agenttasks/agentstreams/issues/55
-- ═══════════════════════════════════════════════════════════

-- ── CaseHOLD Examples ──────────────────────────────────────

CREATE TABLE IF NOT EXISTS casehold_examples (
    id TEXT PRIMARY KEY,                    -- 'casehold_test_0'
    citing_prompt TEXT NOT NULL,            -- legal context with <HOLDING> placeholder
    holdings JSONB NOT NULL,               -- array of 5 candidate holdings
    label INTEGER NOT NULL CHECK (label BETWEEN 0 AND 4),  -- correct answer index
    jurisdiction TEXT NOT NULL DEFAULT '',  -- extracted: 'federal', 'delaware', etc.
    court TEXT NOT NULL DEFAULT '',         -- raw court name from citing context
    embedding vector(384),                 -- pgvector: hash_embedding of citing_prompt
    content_hash TEXT NOT NULL DEFAULT '',  -- SHA-256 for dedup
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE casehold_examples IS 'CaseHOLD benchmark: 53K+ legal holdings for citation quality evaluation';
COMMENT ON COLUMN casehold_examples.citing_prompt IS 'Legal context paragraph with <HOLDING> placeholder marking where the holding belongs';
COMMENT ON COLUMN casehold_examples.holdings IS 'Array of 5 candidate holding strings (JSON array)';
COMMENT ON COLUMN casehold_examples.label IS 'Index (0-4) of the correct holding in the holdings array';
COMMENT ON COLUMN casehold_examples.embedding IS '384-dim vector (hash_embedding of citing_prompt) for pgvector similarity search';
COMMENT ON COLUMN casehold_examples.jurisdiction IS 'Extracted jurisdiction: federal, delaware, california, etc.';

CREATE INDEX IF NOT EXISTS idx_casehold_vector ON casehold_examples
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_casehold_jurisdiction ON casehold_examples(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_casehold_hash ON casehold_examples(content_hash);
CREATE INDEX IF NOT EXISTS idx_casehold_text_trgm ON casehold_examples
    USING gin (citing_prompt gin_trgm_ops);

-- ── CaseHOLD Evaluation Results ────────────────────────────

CREATE TABLE IF NOT EXISTS casehold_eval_results (
    id BIGSERIAL PRIMARY KEY,
    run_id TEXT NOT NULL,                   -- eval run identifier (timestamp-based)
    example_id TEXT NOT NULL REFERENCES casehold_examples(id),
    model TEXT NOT NULL,                    -- 'claude-sonnet-4-6'
    selected_holding INTEGER NOT NULL CHECK (selected_holding BETWEEN -1 AND 4),
    correct BOOLEAN NOT NULL,
    confidence DOUBLE PRECISION NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    reasoning TEXT NOT NULL DEFAULT '',
    supporting_quote TEXT NOT NULL DEFAULT '',
    citation_grounded BOOLEAN,             -- does supporting_quote appear in context?
    duration_ms INTEGER NOT NULL DEFAULT 0,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    raw_output TEXT NOT NULL DEFAULT '',    -- full model response for debugging
    created_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE casehold_eval_results IS 'Per-example results from CaseHOLD benchmark evaluation runs';
COMMENT ON COLUMN casehold_eval_results.run_id IS 'Unique identifier for each eval run (ISO timestamp + model)';
COMMENT ON COLUMN casehold_eval_results.selected_holding IS 'Model-selected holding index (0-4), or -1 if model chose none';
COMMENT ON COLUMN casehold_eval_results.citation_grounded IS 'Whether supporting_quote appears in citing_prompt (fuzzy match via pg_trgm)';

CREATE INDEX IF NOT EXISTS idx_casehold_results_run ON casehold_eval_results(run_id);
CREATE INDEX IF NOT EXISTS idx_casehold_results_model ON casehold_eval_results(model);
CREATE INDEX IF NOT EXISTS idx_casehold_results_correct ON casehold_eval_results(correct);

-- ── Seed: Register eval suite ──────────────────────────────

INSERT INTO eval_suites (name, skill_name, config_path, test_count, assertion_count)
VALUES (
    'casehold-legal-holdings',
    NULL,
    'julia/evals/casehold/promptfooconfig.yaml',
    53000,
    53000
) ON CONFLICT (name) DO NOTHING;
