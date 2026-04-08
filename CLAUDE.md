# agentstreams

## Project

Multi-language skill system for Claude Code. Skills provide web crawling, Anthropic SDK integration, bloom filter deduplication, programmatic prompts (DSPy), LSP code intelligence, and evals — across 8 languages (TypeScript, Python, Java, Go, Ruby, C#, PHP, cURL).

## Auth

**Never use `ANTHROPIC_API_KEY`**. All auth flows through `CLAUDE_CODE_OAUTH_TOKEN`.

For SDK constructors:
- TypeScript: `new Anthropic()` (reads env automatically)
- Python: `anthropic.Anthropic()` (reads env automatically)
- Java: `AnthropicClient.builder().build()` (reads env automatically)
- Go: `anthropic.NewClient()` (reads env automatically)
- Ruby: `Anthropic::Client.new` (reads env automatically)
- C#: `new AnthropicClient()` (reads env automatically)
- PHP: `Anthropic::client()` (reads env automatically)
- cURL: `-H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN"`

## Review Criteria

When reviewing PRs, check:
- Model names use hyphen format: `claude-opus-4-6`, `claude-sonnet-4-6` (never dots or date suffixes)
- Versions are consistent across `SKILL.md`, language READMEs, `package-matrix.md`, and setup scripts
- Cross-references in "Further Reading" sections point to files that actually exist
- Every language README mentions its MCP SDK availability
- Star counts are consistent across files for the same repositories
- SDK constructor patterns match the actual SDK API for each language
- No `ANTHROPIC_API_KEY` anywhere except "never use" warnings

## Code Style

- Markdown: ATX headings, fenced code blocks with language tags
- Shell scripts: `set -euo pipefail`
- No trailing whitespace
- Python managed with `uv` exclusively
- Frontend webapp in `webapp/` managed with `npm`

## Neon Postgres

Project: `calm-paper-82059121` — database `neondb`
Console: https://console.neon.tech/app/projects/calm-paper-82059121?database=neondb

Credentials live in `.env` (gitignored), loaded automatically by the `SessionStart` hook in `.claude/settings.json` → `scripts/setup-env.sh`.

Environment variables available after session start:
- `NEON_DATABASE_URL` — full psycopg connection string (use when TCP:5432 is reachable)
- `NEON_HTTP_HOST` — pooler hostname for SQL-over-HTTP (`/sql` endpoint)
- `NEON_HTTP_CONN` — connection string passed in `Neon-Connection-String` header

**Always use `NEON_DATABASE_URL` from env** — never hardcode credentials in scripts.

Access patterns:
- **psycopg (TCP)**: `src/neon_db.py` reads `NEON_DATABASE_URL` automatically
- **SQL-over-HTTP (HTTPS)**: `scripts/neon-http-upsert.py` for proxy-only environments where TCP:5432 is blocked — uses `httpx` + Neon's `/sql` endpoint
- **Crawl pipeline**: `scripts/crawl-sitemap.py` writes to Neon via `--neon-url` or `NEON_DATABASE_URL`

Schema: `ontology/schema.sql` (12 tables, `resources.url` has UNIQUE constraint)

## Stack

- Python only for executable code (managed with `uv`)
- Claude Code CLI with `CLAUDE_CODE_OAUTH_TOKEN` (Pro Max)
- Agent SDK: `claude-agent-sdk` run locally via scripts
