# Local-First to Cloud Data Warehouse Switchover

## Phase 1: Local Storage (Default)

Start with SQLite + filesystem. This is sufficient for:
- Crawls under 10M pages
- Single-user access
- Development and prototyping

### Local Schema (SQLite)

```sql
-- Crawl metadata
CREATE TABLE crawl_urls (
    url_id INTEGER PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    domain TEXT NOT NULL,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_crawled TIMESTAMP,
    status_code INTEGER,
    content_hash TEXT,
    bloom_positive BOOLEAN DEFAULT FALSE
);

-- Extracted content
CREATE TABLE extracted_content (
    extract_id INTEGER PRIMARY KEY,
    url_id INTEGER REFERENCES crawl_urls(url_id),
    content_type TEXT,  -- 'product', 'article', 'listing', etc.
    extracted_json JSON NOT NULL,
    extraction_model TEXT,  -- 'claude-opus-4-6', 'dspy-optimized', etc.
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crawl session log
CREATE TABLE crawl_sessions (
    session_id INTEGER PRIMARY KEY,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    urls_crawled INTEGER,
    urls_new INTEGER,
    urls_deduplicated INTEGER,
    bloom_filter_path TEXT
);

CREATE INDEX idx_urls_domain ON crawl_urls(domain);
CREATE INDEX idx_urls_status ON crawl_urls(status_code);
CREATE INDEX idx_extract_type ON extracted_content(content_type);
```

## Phase 2: Cloud Switchover Triggers

Switch to a cloud data warehouse when ANY of these apply:

| Trigger | Threshold |
|---------|-----------|
| Total pages crawled | > 10M |
| SQLite file size | > 10 GB |
| Concurrent users/processes | > 1 |
| Need for analytics/BI | Yes |
| Data retention requirements | > 90 days |
| Cross-team data sharing | Yes |

## Phase 3: Kimball Dimensional Model (Cloud DW)

Apply the Kimball methodology from `taxonomy/kimball-dw-toolkit.md`:

### Bus Matrix

```
                        dim_date  dim_domain  dim_content_type  dim_extraction  dim_session
fact_crawl_events          X         X              X                              X
fact_extractions           X         X              X               X              X
fact_dedup_stats           X         X                                             X
```

### Fact Tables

```sql
-- Grain: one row per URL crawl attempt
CREATE TABLE fact_crawl_events (
    crawl_event_key BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    domain_key INT REFERENCES dim_domain(domain_key),
    content_type_key INT REFERENCES dim_content_type(content_type_key),
    session_key INT REFERENCES dim_session(session_key),
    url TEXT NOT NULL,
    status_code SMALLINT,
    response_time_ms INT,
    content_bytes BIGINT,
    content_hash TEXT,
    is_new_url BOOLEAN,
    is_duplicate_content BOOLEAN
);

-- Grain: one row per extraction result
CREATE TABLE fact_extractions (
    extraction_key BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    domain_key INT REFERENCES dim_domain(domain_key),
    content_type_key INT REFERENCES dim_content_type(content_type_key),
    extraction_key_type INT REFERENCES dim_extraction(extraction_key),
    session_key INT REFERENCES dim_session(session_key),
    url TEXT NOT NULL,
    extracted_fields_count INT,
    extraction_confidence DECIMAL(5,4),
    tokens_used INT,
    model_used TEXT,
    cost_usd DECIMAL(10,6)
);
```

### Dimension Tables

```sql
-- SCD Type 1 (overwrite)
CREATE TABLE dim_domain (
    domain_key INT PRIMARY KEY,
    domain_name TEXT,
    tld TEXT,
    robots_txt_last_checked TIMESTAMP,
    crawl_delay_seconds INT,
    total_pages_discovered BIGINT
);

-- SCD Type 0 (fixed)
CREATE TABLE dim_content_type (
    content_type_key INT PRIMARY KEY,
    content_type_code TEXT,  -- 'product', 'article', 'listing'
    content_type_description TEXT
);

-- SCD Type 2 (history tracking) for extraction model changes
CREATE TABLE dim_extraction (
    extraction_key INT PRIMARY KEY,
    model_name TEXT,
    dspy_signature_version TEXT,
    prompt_hash TEXT,
    effective_date DATE,
    expiration_date DATE,
    is_current BOOLEAN
);

-- Role-playing dimension
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_week TEXT,
    month_name TEXT,
    quarter INT,
    year INT,
    is_weekend BOOLEAN
);
```

## Cloud Platform Options

| Platform | Best For | Neon Integration |
|----------|----------|-----------------|
| **Neon Postgres** | Serverless, branching, scale-to-zero | Native (use neon MCP) |
| **Snowflake** | Heavy analytics, semi-structured data | Via connector |
| **BigQuery** | Google ecosystem, ML integration | Via connector |
| **DuckDB** | Local analytics → cloud transition | Embedded, no server |

### Neon Postgres (Recommended for this workspace)

Use the Neon MCP tools already available in this environment:
- `mcp__plugin_neon_neon__create_project` — create a new Neon project
- `mcp__plugin_neon_neon__run_sql` — execute schema DDL
- `mcp__plugin_neon_neon__create_branch` — create dev/staging branches

Migration path: Export SQLite → Neon Postgres via `pg_dump`-compatible SQL.

## ETL Subsystems (from Kimball's 34)

Most relevant for crawl-ingest:

1. **Extract** (Subsystem 1): Crawlers pull data from web sources
2. **Change Data Capture** (Subsystem 3): Bloom filter detects new/changed URLs
3. **Data Cleansing** (Subsystem 4): Claude SDK validates and normalizes extracted data
4. **Surrogate Key Pipeline** (Subsystem 9): Generate warehouse keys from natural keys (URLs)
5. **Slowly Changing Dimension Manager** (Subsystem 10): Track extraction model changes (SCD Type 2)
6. **Fact Table Loader** (Subsystem 14): Bulk insert crawl events and extractions
