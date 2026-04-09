-- ═══════════════════════════════════════════════════════════
-- Kimball Dimensional Model — Data Warehouse Toolkit Vol. 3
-- Fact/dimension star schema for crawl-to-markdown pipeline
-- Neon Postgres 18 extensions: pgvector, pg_tiktoken, hll,
--   pg_trgm, pg_cron, JSONB, GENERATED columns
-- ═══════════════════════════════════════════════════════════

-- ── Dimension: Date (role-playing, SCD Type 0 — fixed) ─────

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,           -- YYYYMMDD integer
    full_date DATE NOT NULL UNIQUE,
    day_of_week TEXT NOT NULL,              -- 'Monday', 'Tuesday', ...
    day_of_week_num SMALLINT NOT NULL,     -- 1=Mon, 7=Sun (ISO)
    day_of_month SMALLINT NOT NULL,
    month_num SMALLINT NOT NULL,
    month_name TEXT NOT NULL,
    quarter SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    iso_week SMALLINT NOT NULL
);

-- Seed dim_date: 2024-01-01 → 2027-12-31 via generate_series
INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_week_num,
    day_of_month, month_num, month_name, quarter, year, is_weekend, iso_week)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER AS date_key,
    d AS full_date,
    TO_CHAR(d, 'Day') AS day_of_week,
    EXTRACT(ISODOW FROM d)::SMALLINT AS day_of_week_num,
    EXTRACT(DAY FROM d)::SMALLINT AS day_of_month,
    EXTRACT(MONTH FROM d)::SMALLINT AS month_num,
    TO_CHAR(d, 'Month') AS month_name,
    EXTRACT(QUARTER FROM d)::SMALLINT AS quarter,
    EXTRACT(YEAR FROM d)::SMALLINT AS year,
    EXTRACT(ISODOW FROM d) IN (6, 7) AS is_weekend,
    EXTRACT(WEEK FROM d)::SMALLINT AS iso_week
FROM generate_series('2024-01-01'::DATE, '2027-12-31'::DATE, '1 day'::INTERVAL) AS d
ON CONFLICT (date_key) DO NOTHING;

-- ── Dimension: Domain (SCD Type 1 — overwrite) ────────────

CREATE TABLE IF NOT EXISTS dim_domain (
    domain_key SERIAL PRIMARY KEY,
    domain_name TEXT NOT NULL UNIQUE,       -- 'neon.com', 'claude.com'
    tld TEXT NOT NULL,                      -- '.com', '.dev'
    sitemap_url TEXT,                       -- source sitemap URL
    robots_txt_checked_at TIMESTAMPTZ,
    crawl_delay_seconds INTEGER DEFAULT 0,
    total_pages_discovered BIGINT DEFAULT 0,
    first_crawled_at TIMESTAMPTZ DEFAULT now(),
    last_crawled_at TIMESTAMPTZ DEFAULT now()
);

-- ── Dimension: Content Type (SCD Type 0 — fixed) ──────────

CREATE TABLE IF NOT EXISTS dim_content_type (
    content_type_key SERIAL PRIMARY KEY,
    content_type_code TEXT NOT NULL UNIQUE,  -- 'docs', 'blog', 'api-ref', 'changelog', 'tutorial'
    content_type_label TEXT NOT NULL,
    description TEXT
);

INSERT INTO dim_content_type (content_type_code, content_type_label, description) VALUES
    ('docs',       'Documentation',  'Product documentation and guides'),
    ('blog',       'Blog Post',      'Blog articles and announcements'),
    ('api-ref',    'API Reference',  'API endpoint and SDK documentation'),
    ('changelog',  'Changelog',      'Release notes and version history'),
    ('tutorial',   'Tutorial',       'Step-by-step tutorials and walkthroughs'),
    ('landing',    'Landing Page',   'Marketing and product landing pages'),
    ('guide',      'Guide',          'In-depth conceptual guides'),
    ('reference',  'Reference',      'Technical reference material'),
    ('pricing',    'Pricing',        'Pricing and plan information'),
    ('unknown',    'Unknown',        'Unclassified content type')
ON CONFLICT (content_type_code) DO NOTHING;

-- ── Dimension: Extraction Model (SCD Type 2 — history) ────

CREATE TABLE IF NOT EXISTS dim_extraction (
    extraction_key SERIAL PRIMARY KEY,
    model_name TEXT NOT NULL,              -- 'html-to-markdown', 'dspy-extract'
    pipeline_version TEXT NOT NULL,        -- 'crawl-to-markdown/1.0'
    config_hash TEXT,                      -- SHA-256 of extraction config
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    expiration_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT true
);

-- ── Dimension: Crawl Session (degenerate/junk) ────────────

CREATE TABLE IF NOT EXISTS dim_crawl_session (
    session_key SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,       -- UUID or timestamp-based
    pipeline_name TEXT NOT NULL,           -- 'crawl-to-markdown'
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    ended_at TIMESTAMPTZ,
    config JSONB NOT NULL DEFAULT '{}',    -- full pipeline config snapshot
    total_urls_discovered INTEGER DEFAULT 0,
    total_pages_crawled INTEGER DEFAULT 0,
    total_pages_new INTEGER DEFAULT 0,
    total_errors INTEGER DEFAULT 0,
    bloom_fp_rate DOUBLE PRECISION DEFAULT 0.0
);

-- ═══════════════════════════════════════════════════════════
-- Fact Tables (grain documented per Kimball Vol. 3 Ch. 3)
-- ═══════════════════════════════════════════════════════════

-- ── Fact: Crawl Events ────────────────────────────────────
-- Grain: one row per URL crawl attempt in a session

CREATE TABLE IF NOT EXISTS fact_crawl_events (
    crawl_event_id BIGSERIAL PRIMARY KEY,
    -- Foreign keys to dimensions
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    domain_key INTEGER NOT NULL REFERENCES dim_domain(domain_key),
    content_type_key INTEGER REFERENCES dim_content_type(content_type_key),
    extraction_key INTEGER REFERENCES dim_extraction(extraction_key),
    session_key INTEGER NOT NULL REFERENCES dim_crawl_session(session_key),
    -- Degenerate dimensions
    url TEXT NOT NULL,
    content_hash TEXT,
    title TEXT DEFAULT '',
    -- Measures (additive)
    status_code SMALLINT NOT NULL DEFAULT 200,
    response_time_ms INTEGER,
    content_bytes BIGINT DEFAULT 0,
    markdown_bytes BIGINT DEFAULT 0,
    token_count INTEGER DEFAULT 0,          -- via pg_tiktoken
    chunk_count INTEGER DEFAULT 0,          -- embedding chunks produced
    -- Flags (semi-additive)
    is_new_url BOOLEAN NOT NULL DEFAULT true,
    is_duplicate_content BOOLEAN NOT NULL DEFAULT false,
    is_error BOOLEAN NOT NULL DEFAULT false,
    -- orjson cache path (filesystem reference)
    orjson_cache_path TEXT,
    -- Timestamp
    crawled_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fact_crawl_date ON fact_crawl_events(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_crawl_domain ON fact_crawl_events(domain_key);
CREATE INDEX IF NOT EXISTS idx_fact_crawl_session ON fact_crawl_events(session_key);
CREATE INDEX IF NOT EXISTS idx_fact_crawl_url ON fact_crawl_events(url);
CREATE INDEX IF NOT EXISTS idx_fact_crawl_hash ON fact_crawl_events(content_hash);

-- ── Fact: Page Content (factless fact / snapshot) ─────────
-- Grain: one row per unique page content version
-- Links crawl_pages to dimensional model for analytics

CREATE TABLE IF NOT EXISTS fact_page_content (
    page_content_id BIGSERIAL PRIMARY KEY,
    -- Foreign keys
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    domain_key INTEGER NOT NULL REFERENCES dim_domain(domain_key),
    content_type_key INTEGER REFERENCES dim_content_type(content_type_key),
    -- Degenerate dimensions
    url TEXT NOT NULL UNIQUE,
    content_hash TEXT NOT NULL,
    title TEXT DEFAULT '',
    -- Measures
    markdown_bytes BIGINT DEFAULT 0,
    raw_html_bytes BIGINT DEFAULT 0,
    token_count INTEGER DEFAULT 0,
    heading_count INTEGER DEFAULT 0,        -- # of markdown headings
    link_count INTEGER DEFAULT 0,           -- # of extracted links
    code_block_count INTEGER DEFAULT 0,     -- # of fenced code blocks
    image_count INTEGER DEFAULT 0,
    -- Content quality indicators
    has_structured_data BOOLEAN DEFAULT false,
    has_code_samples BOOLEAN DEFAULT false,
    has_api_references BOOLEAN DEFAULT false,
    -- Embedding reference
    embedding_wing TEXT DEFAULT 'docs',
    embedding_room TEXT DEFAULT '',
    lance_record_count INTEGER DEFAULT 0,
    -- Timestamps
    first_seen_at TIMESTAMPTZ DEFAULT now(),
    last_updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fact_page_domain ON fact_page_content(domain_key);
CREATE INDEX IF NOT EXISTS idx_fact_page_type ON fact_page_content(content_type_key);
CREATE INDEX IF NOT EXISTS idx_fact_page_hash ON fact_page_content(content_hash);

-- ── Aggregate: Domain Daily Summary (pg_cron materialized) ─
-- Grain: one row per domain per day

CREATE TABLE IF NOT EXISTS agg_domain_daily (
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    domain_key INTEGER NOT NULL REFERENCES dim_domain(domain_key),
    pages_crawled INTEGER DEFAULT 0,
    pages_new INTEGER DEFAULT 0,
    pages_error INTEGER DEFAULT 0,
    total_bytes BIGINT DEFAULT 0,
    total_tokens BIGINT DEFAULT 0,
    total_chunks BIGINT DEFAULT 0,
    avg_response_ms DOUBLE PRECISION DEFAULT 0,
    bloom_fp_rate DOUBLE PRECISION DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (date_key, domain_key)
);

-- ── pg_cron: nightly aggregation job ───────────────────────
-- Uncomment after schema is applied:
-- SELECT cron.schedule('nightly-crawl-agg', '0 3 * * *', $$
--   INSERT INTO agg_domain_daily (date_key, domain_key, pages_crawled, pages_new,
--     pages_error, total_bytes, total_tokens, avg_response_ms)
--   SELECT
--     date_key, domain_key,
--     COUNT(*),
--     COUNT(*) FILTER (WHERE is_new_url),
--     COUNT(*) FILTER (WHERE is_error),
--     SUM(content_bytes),
--     SUM(token_count),
--     AVG(response_time_ms)
--   FROM fact_crawl_events
--   WHERE date_key = TO_CHAR(CURRENT_DATE - INTERVAL '1 day', 'YYYYMMDD')::INTEGER
--   GROUP BY date_key, domain_key
--   ON CONFLICT (date_key, domain_key) DO UPDATE SET
--     pages_crawled = EXCLUDED.pages_crawled,
--     pages_new = EXCLUDED.pages_new,
--     pages_error = EXCLUDED.pages_error,
--     total_bytes = EXCLUDED.total_bytes,
--     total_tokens = EXCLUDED.total_tokens,
--     avg_response_ms = EXCLUDED.avg_response_ms,
--     updated_at = now()
-- $$);
