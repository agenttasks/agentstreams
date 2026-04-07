-- ═══════════════════════════════════════════════════════════
-- AgentStreams — Neon Postgres 18 Schema
-- UDA physical layer: each table maps to an ontology class
-- Extensions: pgvector, pgrag, pg_tiktoken, hll, bloom,
--   pg_trgm, pg_graphql, pg_cron, pg_stat_statements
-- ═══════════════════════════════════════════════════════════

-- ── Extensions (Neon Postgres 18) ───────────────────────
CREATE EXTENSION IF NOT EXISTS pg_graphql;       -- GraphQL API layer
CREATE EXTENSION IF NOT EXISTS vector;           -- pgvector: embeddings + similarity search
CREATE EXTENSION IF NOT EXISTS pg_tiktoken;      -- tokenize text using OpenAI tiktoken
CREATE EXTENSION IF NOT EXISTS hll;              -- HyperLogLog: approximate distinct counting
CREATE EXTENSION IF NOT EXISTS pg_trgm;          -- trigram similarity search
CREATE EXTENSION IF NOT EXISTS pg_stat_statements; -- query performance monitoring
CREATE EXTENSION IF NOT EXISTS pg_cron;          -- scheduled jobs for pipeline automation

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

-- ── MCP Servers ─────────────────────────────────────────

CREATE TABLE mcp_servers (
    id TEXT PRIMARY KEY,             -- 'agentstreams'
    name TEXT NOT NULL,
    version TEXT,
    transport TEXT CHECK (transport IN ('stdio', 'http')),
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
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
    url TEXT NOT NULL UNIQUE,       -- ON CONFLICT (url) requires unique constraint
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

-- ── Prompts (agentic prompt patterns) ────────────────────

CREATE TABLE prompts (
    id TEXT PRIMARY KEY,              -- '01', '02', ..., '30'
    name TEXT NOT NULL UNIQUE,        -- 'verification-agent'
    prompt_type TEXT NOT NULL CHECK (prompt_type IN ('system', 'agent', 'tool', 'skill')),
    purpose TEXT NOT NULL,
    source_file TEXT,
    skill_name TEXT REFERENCES skills(name),
    tags TEXT[],
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Agent Manifests ─────────────────────────────────────

CREATE TABLE agent_manifests (
    name TEXT PRIMARY KEY,            -- 'coordinator'
    model_override TEXT,              -- 'haiku' or NULL for default
    allowed_tools TEXT[],
    denied_tools TEXT[],
    derived_from_prompt TEXT REFERENCES prompts(id),
    manifest_path TEXT,               -- '.claude/agents/coordinator.md'
    created_at TIMESTAMPTZ DEFAULT now()
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

-- ── Bloom Filters (UDA: persistent deduplication) ────────

CREATE TABLE bloom_filters (
    name TEXT PRIMARY KEY,              -- 'crawler:docs', 'crawler:blog'
    domain TEXT NOT NULL DEFAULT '',
    bit_array BYTEA NOT NULL,           -- serialized bloom filter bit array
    expected_items INTEGER NOT NULL DEFAULT 100000,
    fp_rate DOUBLE PRECISION NOT NULL DEFAULT 0.01,
    num_hashes INTEGER NOT NULL,
    item_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ── Crawl Pages (UDA DataContainer: crawled web content) ─

CREATE TABLE crawl_pages (
    id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    domain TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    status_code INTEGER NOT NULL DEFAULT 200,
    crawled_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_crawl_pages_domain ON crawl_pages(domain);
CREATE INDEX idx_crawl_pages_hash ON crawl_pages(content_hash);
CREATE INDEX idx_crawl_pages_crawled ON crawl_pages(crawled_at);

-- ── DSPy Signatures (UDA: typed I/O contracts) ──────────

CREATE TABLE dspy_signatures (
    name TEXT PRIMARY KEY,              -- 'ExtractEntities'
    doc TEXT NOT NULL,
    input_fields JSONB NOT NULL DEFAULT '[]',
    output_fields JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── DSPy Modules (UDA: prompt modules with execution) ───

CREATE TABLE dspy_modules (
    name TEXT PRIMARY KEY,              -- 'extract-entities'
    signature_name TEXT REFERENCES dspy_signatures(name),
    model_id TEXT REFERENCES models(model_id),
    module_type TEXT NOT NULL CHECK (module_type IN ('module', 'chain_of_thought')),
    system_prompt TEXT,
    temperature DOUBLE PRECISION DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Subagents (UDA: headless pipeline runners) ──────────

CREATE TABLE subagents (
    name TEXT PRIMARY KEY,              -- 'uda-crawler'
    description TEXT,
    pipeline_modules TEXT[],            -- ordered module names
    neon_persist BOOLEAN DEFAULT true,
    manifest_path TEXT,                 -- '.claude/subagents/uda-crawler.md'
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Data Containers (UDA: data mesh source registrations)

CREATE TABLE data_containers (
    id SERIAL PRIMARY KEY,
    class_name TEXT NOT NULL UNIQUE,    -- ontology class name
    source_type TEXT NOT NULL DEFAULT 'APPLICATION_PRODUCER',
    source_id TEXT,
    projection_avro JSONB,             -- generated Avro schema
    projection_graphql TEXT,           -- generated GraphQL type
    projection_ttl TEXT,               -- generated TTL DataContainer
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ── Embeddings (pgvector: semantic search) ──────────────

CREATE TABLE embeddings (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    embedding vector(384) NOT NULL,     -- 384-dim (MiniLM / hash_embedding)
    wing TEXT NOT NULL DEFAULT '',       -- mempalace domain: ontology, skills, docs
    room TEXT NOT NULL DEFAULT '',       -- mempalace topic: tool-use, streaming, mcp
    source_url TEXT NOT NULL DEFAULT '',
    content_hash TEXT NOT NULL DEFAULT '',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_embeddings_vector ON embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_embeddings_wing ON embeddings(wing);
CREATE INDEX idx_embeddings_room ON embeddings(room);
-- pg_trgm index for fuzzy text search on embedded chunks
CREATE INDEX idx_embeddings_text_trgm ON embeddings
    USING gin (text gin_trgm_ops);

-- ── Token Counts (pg_tiktoken: tokenization tracking) ───

CREATE TABLE token_counts (
    id BIGSERIAL PRIMARY KEY,
    source_type TEXT NOT NULL,           -- 'crawl_page', 'dspy_input', 'dspy_output', 'embedding'
    source_id TEXT NOT NULL,             -- URL, task ID, or embedding ID
    model TEXT NOT NULL DEFAULT 'cl100k_base',  -- tiktoken encoding name
    token_count INTEGER NOT NULL,
    char_count INTEGER NOT NULL,
    token_ratio DOUBLE PRECISION GENERATED ALWAYS AS (
        CASE WHEN char_count > 0 THEN token_count::double precision / char_count ELSE 0 END
    ) STORED,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_token_counts_source ON token_counts(source_type, source_id);

-- ── HyperLogLog Sketches (hll: approximate distinct counts) ─

CREATE TABLE hll_sketches (
    name TEXT PRIMARY KEY,               -- 'crawl:urls:example.com', 'embeddings:docs'
    domain TEXT NOT NULL DEFAULT '',
    sketch hll NOT NULL DEFAULT hll_empty(),
    description TEXT,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ── Thinking Traces (extended-thinking audit log) ───────

CREATE TABLE thinking_traces (
    id BIGSERIAL PRIMARY KEY,
    task_id BIGINT REFERENCES tasks(id),
    thinking_type TEXT NOT NULL CHECK (thinking_type IN ('enabled', 'adaptive')),
    budget_tokens INTEGER,               -- requested budget
    thinking_tokens INTEGER,             -- actual tokens used
    input_tokens INTEGER,
    output_tokens INTEGER,
    model TEXT NOT NULL,
    duration_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_thinking_model ON thinking_traces(model);
CREATE INDEX idx_thinking_task ON thinking_traces(task_id);

-- ── Scheduled Pipelines (pg_cron: automated jobs) ───────
-- NOTE: pg_cron jobs are registered via SQL, not DDL.
-- Example: SELECT cron.schedule('nightly-crawl', '0 2 * * *',
--   $$SELECT net.http_post(...)$$);
-- Jobs are stored in cron.job (managed by pg_cron extension).

-- ── Harness Runs (GAN-inspired iterative evaluation) ────

CREATE TABLE harness_runs (
    id BIGSERIAL PRIMARY KEY,
    harness_name TEXT NOT NULL,
    sprint_id TEXT NOT NULL UNIQUE,
    objective TEXT NOT NULL,
    criteria JSONB NOT NULL DEFAULT '[]',
    max_iterations INTEGER NOT NULL DEFAULT 5,
    acceptance_threshold DOUBLE PRECISION NOT NULL DEFAULT 0.7,
    final_status TEXT NOT NULL DEFAULT 'running'
        CHECK (final_status IN ('running', 'accepted', 'max_iterations', 'failed')),
    total_iterations INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_harness_runs_status ON harness_runs(final_status);
CREATE INDEX idx_harness_runs_name ON harness_runs(harness_name);

-- ── Evaluation Results (per-iteration grades) ───────────

CREATE TABLE evaluation_results (
    id BIGSERIAL PRIMARY KEY,
    harness_run_id BIGINT REFERENCES harness_runs(id),
    iteration INTEGER NOT NULL,
    scores JSONB NOT NULL DEFAULT '[]',
    overall_score DOUBLE PRECISION NOT NULL,
    passed BOOLEAN NOT NULL DEFAULT false,
    summary TEXT NOT NULL DEFAULT '',
    strategy_recommendation TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_eval_results_run ON evaluation_results(harness_run_id);

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
    ('data-pipeline', 'Data pipeline orchestration, ETL/ELT, streaming, and batch processing', 'build data pipelines, ETL/ELT workflows, stream processing, batch jobs, CDC'),
    ('agentic-prompts', 'Structured prompt engineering patterns from multi-agent AI architectures', 'prompt patterns, agent design, XML tasks, verification, coordination'),
    ('video-generation', 'Video generation with Google Veo models via the Gemini Cloud API', 'generate video, Veo, Gemini video, YouTube content, TikTok content, video pipeline'),
    ('frontend-design', 'Frontend design with React/Vite/Tailwind using GAN-inspired iterative evaluation', 'frontend design, React component, UI design, Tailwind, Vite, design system');

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
    ('api-client-generation', 'api-client', 'evals/api-client/promptfooconfig.yaml', 6, 18),
    ('agentic-prompts-validation', 'agentic-prompts', 'evals/agentic-prompts/promptfooconfig.yaml', 5, 12);

-- ── Seed: Prompts (representative subset of 30) ─────────

INSERT INTO prompts (id, name, prompt_type, purpose, source_file, skill_name, tags) VALUES
    ('05', 'coordinator', 'agent', 'Multi-worker orchestration with synthesis phases', '05_coordinator_system_prompt.md', 'agentic-prompts', ARRAY['orchestration', 'parallel', 'synthesis']),
    ('07', 'verification-agent', 'agent', 'Adversarial testing specialist', '07_verification_agent.md', 'agentic-prompts', ARRAY['verification', 'adversarial', 'read-only']),
    ('08', 'explore-agent', 'agent', 'Fast read-only codebase search', '08_explore_agent.md', 'agentic-prompts', ARRAY['exploration', 'search', 'read-only']),
    ('12', 'auto-mode-classifier', 'system', '2-stage security classification for tool approval', '12_yolo_auto_mode_classifier.md', 'agentic-prompts', ARRAY['security', 'classifier']),
    ('19', 'simplify-skill', 'skill', '3-agent parallel code review', '19_simplify_skill.md', 'agentic-prompts', ARRAY['review', 'parallel', 'cleanup']);

-- ── Seed: Agent Manifests ────────────────────────────────

INSERT INTO agent_manifests (name, model_override, allowed_tools, denied_tools, derived_from_prompt, manifest_path) VALUES
    ('coordinator', NULL, ARRAY['Agent', 'SendMessage', 'TaskStop', 'Read', 'Glob', 'Grep', 'Bash'], NULL, '05', '.claude/agents/coordinator.md'),
    ('verification', NULL, ARRAY['Read', 'Glob', 'Grep', 'Bash'], ARRAY['Edit', 'Write', 'Agent', 'NotebookEdit'], '07', '.claude/agents/verification.md'),
    ('explore', 'haiku', ARRAY['Read', 'Glob', 'Grep', 'Bash'], ARRAY['Edit', 'Write', 'Agent', 'NotebookEdit'], '08', '.claude/agents/explore.md'),
    ('video-generator', NULL, ARRAY['Read', 'Glob', 'Grep', 'Bash', 'Write'], NULL, NULL, '.claude/agents/video-generator.md'),
    ('uda-crawler', NULL, ARRAY['Read', 'Glob', 'Grep', 'Bash', 'Write'], NULL, NULL, '.claude/agents/uda-crawler.md'),
    ('uda-extractor', NULL, ARRAY['Read', 'Glob', 'Grep', 'Bash'], NULL, NULL, '.claude/agents/uda-extractor.md'),
    ('uda-thinker', 'opus', ARRAY['Read', 'Glob', 'Grep', 'Bash'], NULL, NULL, '.claude/agents/uda-thinker.md'),
    ('frontend-generator', NULL, ARRAY['Read', 'Glob', 'Grep', 'Bash', 'Write'], NULL, NULL, '.claude/agents/frontend-generator.md'),
    ('frontend-evaluator', NULL, ARRAY['Read', 'Glob', 'Grep', 'Bash'], ARRAY['Edit', 'Write', 'Agent'], NULL, '.claude/agents/frontend-evaluator.md');

-- ── Seed: DSPy Signatures ───────────────────────────────

INSERT INTO dspy_signatures (name, doc, input_fields, output_fields) VALUES
    ('ExtractEntities', 'Extract structured entities from crawled documentation page content.',
     '[{"name":"url","type":"str"},{"name":"content","type":"str"},{"name":"domain","type":"str"}]'::jsonb,
     '[{"name":"entities","type":"list"},{"name":"relationships","type":"list"},{"name":"summary","type":"str"}]'::jsonb),
    ('ClassifyContent', 'Classify crawled content into skill-relevant categories.',
     '[{"name":"content","type":"str"},{"name":"title","type":"str"}]'::jsonb,
     '[{"name":"primary_category","type":"str"},{"name":"skills","type":"list"},{"name":"languages","type":"list"},{"name":"confidence","type":"float"}]'::jsonb),
    ('ExtractAPIPatterns', 'Extract API usage patterns, code samples, and SDK constructor calls.',
     '[{"name":"content","type":"str"},{"name":"language","type":"str"}]'::jsonb,
     '[{"name":"patterns","type":"list"},{"name":"sdk_constructor","type":"str"},{"name":"auth_method","type":"str"},{"name":"models_referenced","type":"list"}]'::jsonb),
    ('AlignToOntology', 'Map extracted entities to AgentStreams ontology classes and properties.',
     '[{"name":"entities","type":"list"},{"name":"relationships","type":"list"},{"name":"ontology_classes","type":"list"}]'::jsonb,
     '[{"name":"mappings","type":"list"},{"name":"new_classes","type":"list"},{"name":"property_mappings","type":"list"}]'::jsonb);

-- ── Seed: Subagents ─────────────────────────────────────

INSERT INTO subagents (name, description, pipeline_modules, manifest_path) VALUES
    ('uda-crawler', 'Web crawling with bloom filter dedup and Neon persistence',
     ARRAY['UDACrawler', 'BloomFilter', 'NeonBloomStore'],
     '.claude/subagents/uda-crawler.md'),
    ('uda-extractor', 'DSPy structured extraction with ontology alignment',
     ARRAY['ExtractEntities', 'ClassifyContent', 'AlignToOntology'],
     '.claude/subagents/uda-extractor.md'),
    ('uda-projector', 'Ontology projection generator: Avro, GraphQL, DataContainer, Mapping',
     ARRAY['AvroProjection', 'GraphQLProjection', 'DataContainerProjection', 'MappingProjection'],
     '.claude/subagents/uda-projector.md'),
    ('uda-thinker', 'Deep reasoning with extended/adaptive thinking and Neon extensions',
     ARRAY['ExtendedThinking', 'AdaptiveThinking', 'record_thinking_trace'],
     '.claude/subagents/uda-thinker.md');
