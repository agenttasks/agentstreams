-- ═══════════════════════════════════════════════════════════
-- AgentStreams — Neon Postgres Schema (pg_graphql auto-exposes)
-- UDA physical layer: each table maps to an ontology class
-- ═══════════════════════════════════════════════════════════

-- Enable pg_graphql
CREATE EXTENSION IF NOT EXISTS pg_graphql;

-- ── Languages ────────────────────────────────────────────

CREATE TABLE languages (
    id TEXT PRIMARY KEY,           -- 'typescript', 'python', etc.
    label TEXT NOT NULL,
    tier TEXT CHECK (tier IN ('tier1', 'tier2', 'tier3'))
);

-- ── Models ───────────────────────────────────────────────

CREATE TABLE models (
    model_id TEXT PRIMARY KEY,     -- 'claude-opus-4-6'
    family TEXT NOT NULL,          -- 'Claude 4.6'
    label TEXT NOT NULL,
    supports_thinking BOOLEAN DEFAULT false,
    supports_tool_use BOOLEAN DEFAULT false,
    supports_vision BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Skills ───────────────────────────────────────────────

CREATE TABLE skills (
    name TEXT PRIMARY KEY,         -- 'crawl-ingest'
    description TEXT NOT NULL,
    trigger_pattern TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE skill_languages (
    skill_name TEXT REFERENCES skills(name),
    language_id TEXT REFERENCES languages(id),
    tier TEXT CHECK (tier IN ('tier1', 'tier2', 'tier3')),
    PRIMARY KEY (skill_name, language_id)
);

-- ── SDKs ─────────────────────────────────────────────────

CREATE TABLE sdks (
    id TEXT PRIMARY KEY,           -- 'sdk-typescript'
    language_id TEXT REFERENCES languages(id),
    label TEXT NOT NULL,
    github_stars INTEGER,
    constructor_pattern TEXT NOT NULL,
    repo_url TEXT
);

-- ── Packages ─────────────────────────────────────────────

CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT,
    language_id TEXT REFERENCES languages(id),
    skill_name TEXT REFERENCES skills(name),
    purpose TEXT,
    UNIQUE (name, language_id, skill_name)
);

-- ── Metrics (Atlas/Spectator dimensional model) ──────────

CREATE TABLE metrics (
    name TEXT PRIMARY KEY,         -- 'agentstreams.pipeline.duration'
    type TEXT NOT NULL CHECK (type IN ('counter', 'timer', 'gauge', 'distribution_summary')),
    unit TEXT,
    dimensions TEXT[],             -- ['skill', 'language', 'stage']
    description TEXT
);

-- Fact table: one row per metric observation
CREATE TABLE metric_values (
    id BIGSERIAL PRIMARY KEY,
    metric_name TEXT REFERENCES metrics(name),
    value DOUBLE PRECISION NOT NULL,
    tags JSONB NOT NULL DEFAULT '{}',   -- dimensional tags
    recorded_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_metric_values_name ON metric_values(metric_name);
CREATE INDEX idx_metric_values_time ON metric_values(recorded_at);
CREATE INDEX idx_metric_values_tags ON metric_values USING GIN (tags);

-- ── Pipelines ────────────────────────────────────────────

CREATE TABLE pipelines (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    skill_name TEXT REFERENCES skills(name),
    model_id TEXT REFERENCES models(model_id),
    config JSONB DEFAULT '{}',
    status TEXT CHECK (status IN ('active', 'paused', 'completed', 'failed')),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ── Resources (Claude Platform + external) ───────────────

CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,             -- 'model_card', 'api_primer', 'llms_index', 'cookbook'
    label TEXT NOT NULL,
    url TEXT NOT NULL,
    related_model_id TEXT REFERENCES models(model_id),
    description TEXT,
    fetched_at TIMESTAMPTZ,
    content_hash TEXT               -- track changes
);

-- ── Eval Suites ──────────────────────────────────────────

CREATE TABLE eval_suites (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    skill_name TEXT REFERENCES skills(name),
    config_path TEXT,              -- path to promptfooconfig.yaml
    test_count INTEGER,
    assertion_count INTEGER,
    last_run_at TIMESTAMPTZ,
    last_run_pass_rate DOUBLE PRECISION
);

-- ── Tasks (pgqueuer-compatible) ──────────────────────────

CREATE TABLE tasks (
    id BIGSERIAL PRIMARY KEY,
    queue_name TEXT NOT NULL,          -- pgqueuer entrypoint name
    type TEXT NOT NULL CHECK (type IN ('code', 'knowledge_work', 'financial')),
    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'cancelled')),
    priority INTEGER NOT NULL DEFAULT 0,
    skill_name TEXT REFERENCES skills(name),
    model_id TEXT REFERENCES models(model_id),
    plugin TEXT,                       -- knowledge-work plugin identifier
    input JSONB NOT NULL DEFAULT '{}',
    config JSONB NOT NULL DEFAULT '{}',
    output JSONB,
    error TEXT,
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    execute_after TIMESTAMPTZ,         -- deferred execution (pgqueuer)
    created_at TIMESTAMPTZ DEFAULT now(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_tasks_status ON tasks(status) WHERE status IN ('queued', 'processing');
CREATE INDEX idx_tasks_queue ON tasks(queue_name, status, priority DESC);
CREATE INDEX idx_tasks_created ON tasks(created_at);
CREATE INDEX idx_tasks_type ON tasks(type);

-- ── Seed data ────────────────────────────────────────────

INSERT INTO languages (id, label) VALUES
    ('typescript', 'TypeScript'),
    ('python', 'Python'),
    ('java', 'Java'),
    ('go', 'Go'),
    ('ruby', 'Ruby'),
    ('csharp', 'C#'),
    ('php', 'PHP'),
    ('shell', 'Shell/cURL');

INSERT INTO models (model_id, family, label, supports_thinking, supports_tool_use, supports_vision) VALUES
    ('claude-opus-4-6', 'Claude 4.6', 'Claude Opus 4.6', true, true, true),
    ('claude-sonnet-4-6', 'Claude 4.6', 'Claude Sonnet 4.6', true, true, true),
    ('claude-haiku-4-5-20251001', 'Claude 4.5', 'Claude Haiku 4.5', false, true, true);

INSERT INTO skills (name, description, trigger_pattern) VALUES
    ('crawl-ingest', 'Web crawling, deduplication, and data ingestion using Anthropic SDKs', 'crawl websites, build scrapers, deduplicate URLs, bloom filters, ingest data'),
    ('api-client', 'API client generation, testing, and integration using Anthropic SDKs', 'build API clients, generate SDKs, test REST/GraphQL APIs, OAuth, retry/backoff'),
    ('data-pipeline', 'Data pipeline orchestration, ETL/ELT, streaming, and batch processing', 'build data pipelines, ETL/ELT workflows, stream processing, batch jobs, CDC');

INSERT INTO sdks (id, language_id, label, github_stars, constructor_pattern) VALUES
    ('sdk-typescript', 'typescript', 'anthropic-sdk-typescript', 1800, 'new Anthropic()'),
    ('sdk-python', 'python', 'anthropic-sdk-python', 3100, 'anthropic.Anthropic()'),
    ('sdk-java', 'java', 'anthropic-sdk-java', 271, 'AnthropicClient.builder().build()'),
    ('sdk-go', 'go', 'anthropic-sdk-go', 943, 'anthropic.NewClient()'),
    ('sdk-ruby', 'ruby', 'anthropic-sdk-ruby', 312, 'Anthropic::Client.new'),
    ('sdk-csharp', 'csharp', 'anthropic-sdk-csharp', 212, 'new AnthropicClient()'),
    ('sdk-php', 'php', 'anthropic-sdk-php', 128, 'Anthropic::client()');

INSERT INTO metrics (name, type, unit, dimensions, description) VALUES
    ('agentstreams.pipeline.duration', 'timer', 'seconds', ARRAY['skill', 'language', 'stage'], 'Pipeline stage duration'),
    ('agentstreams.api.requests', 'counter', 'requests', ARRAY['model', 'skill', 'status'], 'Claude API request count'),
    ('agentstreams.api.tokens', 'counter', 'tokens', ARRAY['model', 'skill', 'direction'], 'Token usage (input/output)'),
    ('agentstreams.api.cost', 'distribution_summary', 'USD', ARRAY['model', 'skill'], 'API cost per request'),
    ('agentstreams.eval.score', 'gauge', 'ratio', ARRAY['skill', 'eval_suite', 'assertion_type'], 'Eval pass rate'),
    ('agentstreams.crawl.pages', 'counter', 'pages', ARRAY['domain', 'status', 'is_new'], 'Pages crawled'),
    ('agentstreams.crawl.dedup', 'gauge', 'ratio', ARRAY['method'], 'Bloom filter false positive rate'),
    ('agentstreams.tasks.throughput', 'counter', 'tasks', ARRAY['queue', 'type', 'status'], 'Task completion count'),
    ('agentstreams.tasks.duration', 'timer', 'seconds', ARRAY['queue', 'type'], 'Task processing duration'),
    ('agentstreams.tasks.queue_depth', 'gauge', 'tasks', ARRAY['queue', 'type'], 'Current queue depth (queued + processing)');

INSERT INTO resources (type, label, url, description) VALUES
    ('api_primer', 'API Primer for Claude Ingestion', 'https://platform.claude.com/docs/en/claude_api_primer', 'Concise API guide for LLM ingestion'),
    ('llms_index', 'llms.txt', 'https://platform.claude.com/llms.txt', 'Documentation index — 620 pages'),
    ('llms_index', 'llms-full.txt', 'https://platform.claude.com/llms-full.txt', 'Complete docs in single file');

INSERT INTO resources (type, label, url, related_model_id, description) VALUES
    ('model_card', 'Claude Opus 4.6 System Card', 'https://www.anthropic.com/claude-opus-4-6-system-card', 'claude-opus-4-6', 'Safety and capability documentation'),
    ('model_card', 'Claude Sonnet 4.6 System Card', 'https://www.anthropic.com/claude-sonnet-4-6-system-card', 'claude-sonnet-4-6', 'Safety and capability documentation');

INSERT INTO eval_suites (name, skill_name, config_path, test_count, assertion_count) VALUES
    ('crawl-ingest-extraction', 'crawl-ingest', 'evals/crawl-ingest/promptfooconfig.yaml', 6, 16),
    ('api-client-generation', 'api-client', 'evals/api-client/promptfooconfig.yaml', 6, 18);
