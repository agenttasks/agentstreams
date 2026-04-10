-- ═══════════════════════════════════════════════════════════
-- CaseHOLD Eval Schema — Kimball Transaction Fact
--
-- Data Warehouse Toolkit (Kimball, 3rd Ed) patterns:
--   Grain: one prediction per example per eval run
--   Conformed dims: model (shared with julia_cuad_eval_runs, julia_lexglue_results)
--   Degenerate dims: jurisdiction, confidence_bucket (embedded in fact)
--   Generated column: confidence_bucket (computed at insert, no ETL needed)
--
-- Neon Postgres extensions used:
--   pg_trgm: GIN index on citing_prompt for fuzzy grounding verification
--   pg_graphql: COMMENT ON annotations for auto-generated GraphQL API
--
-- Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
-- ═══════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS julia_casehold_eval_runs (
    id BIGSERIAL PRIMARY KEY,

    -- Run dimension (degenerate — no separate dim table)
    harness_run_id INTEGER,
    run_id TEXT NOT NULL,

    -- Grain: one prediction per example
    example_id TEXT NOT NULL,

    -- Fact measures
    predicted_idx SMALLINT NOT NULL CHECK (predicted_idx BETWEEN -1 AND 4),
    gold_idx SMALLINT NOT NULL CHECK (gold_idx BETWEEN 0 AND 4),
    correct BOOLEAN NOT NULL,
    confidence FLOAT NOT NULL CHECK (confidence BETWEEN 0.0 AND 1.0),

    -- Citation grounding measures
    supporting_quote TEXT,
    grounding_verified BOOLEAN NOT NULL DEFAULT false,

    -- Degenerate dimensions
    jurisdiction TEXT,
    confidence_bucket TEXT GENERATED ALWAYS AS (
        CASE
            WHEN confidence > 0.8 THEN 'high'
            WHEN confidence >= 0.5 THEN 'medium'
            ELSE 'low'
        END
    ) STORED,

    -- Context (for audit replay, not scoring)
    citing_prompt TEXT NOT NULL,
    holding_options JSONB NOT NULL,
    reasoning TEXT,

    -- Conformed dimension: model
    model TEXT NOT NULL,

    -- Additive facts (for cost analysis)
    input_tokens INTEGER,
    output_tokens INTEGER,
    duration_ms INTEGER,

    -- Audit
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_casehold_run
    ON julia_casehold_eval_runs(run_id);
CREATE INDEX IF NOT EXISTS idx_casehold_jurisdiction
    ON julia_casehold_eval_runs(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_casehold_bucket
    ON julia_casehold_eval_runs(confidence_bucket);
CREATE INDEX IF NOT EXISTS idx_casehold_correct
    ON julia_casehold_eval_runs(correct);

-- pg_trgm: fuzzy citation grounding verification in SQL
CREATE INDEX IF NOT EXISTS idx_casehold_citing_trgm
    ON julia_casehold_eval_runs
    USING gin (citing_prompt gin_trgm_ops);

-- pg_graphql annotations for auto-generated API
COMMENT ON TABLE julia_casehold_eval_runs IS
    'CaseHOLD benchmark results — Kimball transaction fact (grain: one prediction per example per run)';
COMMENT ON COLUMN julia_casehold_eval_runs.confidence_bucket IS
    'Degenerate dimension: high (>0.8), medium (0.5-0.8), low (<0.5)';
COMMENT ON COLUMN julia_casehold_eval_runs.jurisdiction IS
    'Degenerate dimension: court jurisdiction extracted from citing passage';
COMMENT ON COLUMN julia_casehold_eval_runs.grounding_verified IS
    'Citation audit: supporting_quote found in citing_prompt via pg_trgm';
COMMENT ON COLUMN julia_casehold_eval_runs.holding_options IS
    'JSONB array of 5 candidate holdings for audit replay';
