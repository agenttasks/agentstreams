-- ═══════════════════════════════════════════════════════════
-- Julia — Legal AI Agent Schema
-- Neon Postgres 18: pgvector, pg_graphql, pg_tiktoken, pg_cron
--
-- Kimball Dimensional Modeling patterns:
--   Transaction fact:        julia_audit_logs
--   Accumulating snapshot:   julia_vault_files
--   SCD Type 2 dimension:    julia_client_matters
--   SCD Type 1 dimension:    julia_vault_projects
--   Conformed dimensions:    models, skills (from ontology/schema.sql)
--
-- All tables annotated with COMMENT ON for pg_graphql auto-generation.
-- Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
-- ═══════════════════════════════════════════════════════════

-- Extensions already created in ontology/schema.sql:
--   pg_graphql, vector, pg_tiktoken, hll, pg_trgm,
--   pg_stat_statements, pg_cron

-- ── Client Matters (SCD Type 2 Dimension) ───────────────────
-- Billing attribution + access control per legal matter.
-- SCD Type 2: status changes add a new row with effective/expiration dates.
-- Kimball: natural key = id, surrogate key = (id, effective_date)

CREATE TABLE julia_client_matters (
    id TEXT NOT NULL,                  -- branded MatterId
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'closed', 'archived')),
    query_count INTEGER NOT NULL DEFAULT 0,
    token_count BIGINT NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    -- SCD Type 2 columns
    effective_date TIMESTAMPTZ NOT NULL DEFAULT now(),
    expiration_date TIMESTAMPTZ,       -- NULL = current row
    is_current BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,            -- soft delete
    PRIMARY KEY (id, effective_date)
);

CREATE INDEX idx_julia_matters_current ON julia_client_matters(id) WHERE is_current = true;
CREATE INDEX idx_julia_matters_status ON julia_client_matters(status) WHERE is_current = true;

COMMENT ON TABLE julia_client_matters IS 'Client matter billing and access control (SCD Type 2 dimension)';
COMMENT ON COLUMN julia_client_matters.id IS 'Branded MatterId — natural key across SCD versions';
COMMENT ON COLUMN julia_client_matters.effective_date IS 'SCD2: when this version became active';
COMMENT ON COLUMN julia_client_matters.expiration_date IS 'SCD2: when this version was superseded (NULL = current)';
COMMENT ON COLUMN julia_client_matters.is_current IS 'SCD2: true for the active version';
COMMENT ON COLUMN julia_client_matters.query_count IS 'Periodic snapshot: aggregated by pg_cron daily';
COMMENT ON COLUMN julia_client_matters.token_count IS 'Periodic snapshot: aggregated by pg_cron daily';

-- ── Vault Projects (SCD Type 1 Dimension) ───────────────────
-- Document collections. SCD Type 1: overwrites on rename (no history).

CREATE TABLE julia_vault_projects (
    id TEXT PRIMARY KEY,               -- branded ProjectId (UUID)
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    is_knowledge_base BOOLEAN NOT NULL DEFAULT false,
    owner_email TEXT NOT NULL,
    storage_bytes BIGINT NOT NULL DEFAULT 0,
    file_count INTEGER NOT NULL DEFAULT 0,
    client_matter_id TEXT,             -- FK to current matter row
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    archived_at TIMESTAMPTZ
);

CREATE INDEX idx_julia_projects_owner ON julia_vault_projects(owner_email);
CREATE INDEX idx_julia_projects_matter ON julia_vault_projects(client_matter_id);

COMMENT ON TABLE julia_vault_projects IS 'Vault document collections (SCD Type 1 dimension)';
COMMENT ON COLUMN julia_vault_projects.id IS 'Branded ProjectId';
COMMENT ON COLUMN julia_vault_projects.is_knowledge_base IS 'True for regional knowledge bases';
COMMENT ON COLUMN julia_vault_projects.client_matter_id IS 'FK to julia_client_matters.id (current row)';

-- ── Vault Files (Accumulating Snapshot Fact) ─────────────────
-- Kimball: milestones track processing pipeline progression.
-- uploaded_at → chunked_at → embedded_at → processed_at

CREATE TABLE julia_vault_files (
    id TEXT PRIMARY KEY,               -- branded FileId (UUID)
    project_id TEXT NOT NULL REFERENCES julia_vault_projects(id),
    filename TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT '',
    size_bytes BIGINT NOT NULL DEFAULT 0,
    content TEXT NOT NULL DEFAULT '',   -- extracted text for embedding
    content_hash TEXT NOT NULL,
    processing_status TEXT NOT NULL DEFAULT 'pending'
        CHECK (processing_status IN ('pending', 'processing', 'ready', 'failed')),
    chunk_count INTEGER NOT NULL DEFAULT 0,
    token_count INTEGER NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    -- Accumulating snapshot milestone dates
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    chunked_at TIMESTAMPTZ,            -- when text was chunked
    embedded_at TIMESTAMPTZ,           -- when embeddings were computed
    processed_at TIMESTAMPTZ,          -- when fully ready
    UNIQUE (project_id, filename)
);

CREATE INDEX idx_julia_files_project ON julia_vault_files(project_id);
CREATE INDEX idx_julia_files_status ON julia_vault_files(processing_status);
CREATE INDEX idx_julia_files_hash ON julia_vault_files(content_hash);

COMMENT ON TABLE julia_vault_files IS 'Vault documents (accumulating snapshot fact table)';
COMMENT ON COLUMN julia_vault_files.id IS 'Branded FileId';
COMMENT ON COLUMN julia_vault_files.processing_status IS 'Pipeline milestone: pending → processing → ready | failed';
COMMENT ON COLUMN julia_vault_files.uploaded_at IS 'Accumulating snapshot: upload milestone';
COMMENT ON COLUMN julia_vault_files.chunked_at IS 'Accumulating snapshot: chunking milestone';
COMMENT ON COLUMN julia_vault_files.embedded_at IS 'Accumulating snapshot: embedding milestone';
COMMENT ON COLUMN julia_vault_files.processed_at IS 'Accumulating snapshot: completion milestone';

-- ── Vault File Chunks (pgvector embeddings) ──────────────────

CREATE TABLE julia_vault_file_chunks (
    id TEXT PRIMARY KEY,               -- branded ChunkId
    file_id TEXT NOT NULL REFERENCES julia_vault_files(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    embedding vector(384),             -- pgvector: same dim as src/embeddings.py
    token_count INTEGER NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (file_id, chunk_index)
);

CREATE INDEX idx_julia_chunks_file ON julia_vault_file_chunks(file_id);
CREATE INDEX idx_julia_chunks_vector ON julia_vault_file_chunks
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_julia_chunks_text_trgm ON julia_vault_file_chunks
    USING gin (content gin_trgm_ops);

COMMENT ON TABLE julia_vault_file_chunks IS 'Chunked document text with pgvector embeddings for semantic search';
COMMENT ON COLUMN julia_vault_file_chunks.embedding IS '384-dim vector (hash_embedding or sentence-transformers)';

-- ── Review Tables ────────────────────────────────────────────

CREATE TABLE julia_review_tables (
    id TEXT PRIMARY KEY,               -- branded ReviewTableId
    project_id TEXT NOT NULL REFERENCES julia_vault_projects(id),
    title TEXT NOT NULL,
    columns JSONB NOT NULL,            -- [{name, type, description}]
    file_ids TEXT[] NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_julia_review_tables_project ON julia_review_tables(project_id);

COMMENT ON TABLE julia_review_tables IS 'Structured document review matrices (column extraction across files)';
COMMENT ON COLUMN julia_review_tables.columns IS 'Review column definitions: [{name: string, type: text|date|currency|boolean, description: string}]';

-- ── Review Rows ──────────────────────────────────────────────

CREATE TABLE julia_review_rows (
    id TEXT PRIMARY KEY,
    review_table_id TEXT NOT NULL REFERENCES julia_review_tables(id) ON DELETE CASCADE,
    file_id TEXT NOT NULL REFERENCES julia_vault_files(id),
    cells JSONB NOT NULL,              -- {column_name: extracted_value}
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'complete', 'error')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (review_table_id, file_id)
);

CREATE INDEX idx_julia_review_rows_table ON julia_review_rows(review_table_id);

COMMENT ON TABLE julia_review_rows IS 'Per-file extracted data for a review table';

-- ── Audit Logs (Transaction Fact Table) ──────────────────────
-- Kimball: grain = one event. FKs to dimension tables.
-- Degenerate dimension: event_type (no separate dim table needed).

CREATE TABLE julia_audit_logs (
    id BIGSERIAL PRIMARY KEY,          -- branded AuditLogId
    event_type TEXT NOT NULL,          -- degenerate dimension
    user_email TEXT,
    client_matter_id TEXT,             -- FK to matters natural key
    project_id TEXT,                   -- FK to projects
    input_summary TEXT,                -- truncated input (not full content)
    output_summary TEXT,
    model TEXT,                        -- conformed dimension: models.model_id
    input_tokens INTEGER,
    output_tokens INTEGER,
    duration_ms INTEGER,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_julia_audit_created ON julia_audit_logs(created_at);
CREATE INDEX idx_julia_audit_type ON julia_audit_logs(event_type);
CREATE INDEX idx_julia_audit_user ON julia_audit_logs(user_email);
CREATE INDEX idx_julia_audit_matter ON julia_audit_logs(client_matter_id);
CREATE INDEX idx_julia_audit_project ON julia_audit_logs(project_id);

COMMENT ON TABLE julia_audit_logs IS 'Full activity trail (Kimball transaction fact table)';
COMMENT ON COLUMN julia_audit_logs.event_type IS 'Degenerate dimension: vault.upload, completion, matter.create, etc.';
COMMENT ON COLUMN julia_audit_logs.model IS 'Conformed dimension FK to models.model_id';
COMMENT ON COLUMN julia_audit_logs.input_tokens IS 'Fact: input token count';
COMMENT ON COLUMN julia_audit_logs.output_tokens IS 'Fact: output token count';
COMMENT ON COLUMN julia_audit_logs.duration_ms IS 'Fact: operation duration in milliseconds';

-- ── pg_cron: Periodic Snapshot Aggregation ───────────────────
-- Aggregates daily usage stats into client matter dimension rows.

SELECT cron.schedule(
    'julia-daily-matter-stats',
    '0 1 * * *',
    $$
    UPDATE julia_client_matters SET
        query_count = sub.cnt,
        token_count = sub.tokens,
        updated_at = now()
    FROM (
        SELECT client_matter_id, count(*) AS cnt,
               coalesce(sum(input_tokens + output_tokens), 0) AS tokens
        FROM julia_audit_logs
        WHERE client_matter_id IS NOT NULL
        GROUP BY client_matter_id
    ) sub
    WHERE julia_client_matters.id = sub.client_matter_id
      AND julia_client_matters.is_current = true
    $$
);
