# agentstreams

## Project

Safety-grounded multi-agent orchestration for Claude Code. Composable pipelines across codegen, security audit, alignment audit, and evaluation — powered by 18 open-source safety-research tools and Mythos System Card methodology.

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
- Star counts intentionally omitted — they go stale immediately
- SDK constructor patterns match the actual SDK API for each language
- No `ANTHROPIC_API_KEY` anywhere except "never use" warnings

## Code Style

- Markdown: ATX headings, fenced code blocks with language tags
- Shell scripts: `set -euo pipefail`
- No trailing whitespace
- Python managed with `uv` exclusively
- Frontend webapp in `webapp/` managed with `npm`

## Makefile

All operations go through `make`. Key targets:
- `make install-all` — Python (uv sync) + webapp (npm ci)
- `make ci` — Full CI locally (lint + test + build + validate + security-audit)
- `make lint` / `make test` / `make build` — Individual checks
- `make validate-agents` — Agent boundary enforcement (tool grants, API key ban)
- `make security-audit` — Run security-audit.py
- `make dev-webapp` — Start Next.js dev server

## Memory Palace Architecture

File organization follows the MemPalace pattern (see `.gitattributes`):
- **Wings**: ontology/, src/, scripts/, skills/, .claude/, webapp/, .github/, evals/
- **Halls**: hall_facts, hall_tools, hall_agents, hall_skills, hall_evals, hall_ci, hall_webapp, hall_safety
- **Tunnels**: Cross-wing connections (e.g., orchestrator.py ↔ agents/*.md)

Memory sync (cloud-safe — all memory is in checked-in files):
- `CLAUDE.md` — shared project memory (this file, checked in)
- `.claude/settings.json` — hooks and permissions
- `.claude/agents/*.md` — agent configs with YAML frontmatter
- `.claude/subagents/opus-orchestrator.md` — pipeline definitions
- `.gitattributes` — MemPalace wing/hall/tunnel map

## Orchestrator

25 agents (8 safety/codegen + 17 knowledge-work), 8 pipelines, 4 model tiers. Defined in:
- `src/orchestrator.py` — Python dataclasses + agent configs
- `src/knowledge_agents.py` — Knowledge-work plugin catalog (164 skills, 22 categories)
- `src/knowledge_subagents.py` — Claude Code CLI subagent generator
- `src/plugin_bridge.py` — Cowork plugin → ManagedAgentConfig bridge
- `.claude/agents/*.md` — Agent frontmatter (tools, model, color)
- `.claude/subagents/opus-orchestrator.md` — Pipeline XML + safety-research tooling

Model hierarchy (orchestrated pipeline agents only):
- opus: security-auditor, alignment-auditor, architecture-reviewer,
        + 17 knowledge-work agents (sales-agent, data-analyst, compliance-reviewer, etc.)
- sonnet: code-generator, test-runner, prompt-hardener, eval-builder
- haiku: harmlessness-screen

Standalone subagents (.claude/agents/, not in orchestrator pipelines):
- opus: uda-thinker, uda-crawler
- haiku: crawl-analyzer, memory-validator, explore

Knowledge-work pipelines (3):
- research-to-report: harmlessness-screen → enterprise-search → marketing + compliance → security
- data-to-insight: harmlessness-screen → data-analyst → finance + compliance → marketing
- compliance-review: harmlessness-screen → compliance-reviewer → security + search → marketing

Vendored plugin repos (vendors/):
- knowledge-work-plugins: 17 plugins, 119 skills, 11 MCP connector sets
- financial-services-plugins: 5 plugins, 45 skills, 11 MCP data providers
- claude-plugins-official: 17 skills (3 plugins: document-skills, example-skills, claude-api)
- claude-plugins-community: 814 plugins (marketplace.json registry only)

## Safety-Research Integration

18 repos from github.com/safety-research referenced across 7 agents:
- alignment-auditor: petri, trusted-monitor, SHADE-Arena, lie-detector, ciphered-reasoning-llms, A3, open-source-alignment-faking, crosscoder_emergent_misalignment
- security-auditor: auditing-agents, finetuning-auditor, PurpleLlama, safety-tooling, lie-detector, SCONE-bench
- eval-builder: bloom, impossiblebench, SCONE-bench, lie-detector, A3, open-source-alignment-faking
- prompt-hardener: inoculation-prompting, persona_vectors
- harmlessness-screen: assistant-axis, ciphered-reasoning-llms, persona_vectors
- architecture-reviewer: petri, trusted-monitor, open-source-alignment-faking

Install pip packages: `make install-safety` (petri, bloom)

## SDK Ecosystem

| Package | Purpose |
|---------|---------|
| `@anthropic-ai/claude-agent-sdk` | Agent runtime (query, hooks, subagents) — v0.2.101+ |
| `@anthropic-ai/sdk` | Direct Messages API client (v0.87+) |
| `@anthropic-ai/claude-code` | Claude Code CLI runtime — v2.1.101+ |
| `@anthropic-ai/claude-trace` | JSONL transcript capture — v0.1.2+ |
| `@anthropic-ai/mcpb` | MCP Bundle builder — v2.1.2+ |
| `@modelcontextprotocol/sdk` | MCP SDK for tool servers — v1.29.0+ |
| `@modelcontextprotocol/ext-apps` | Browser rendering and inline widgets — v1.5.0+ |
| `@modelcontextprotocol/inspector` | MCP debugger CLI — v0.21.1+ |
| `@neondatabase/serverless` | Neon SQL over HTTPS/WebSocket |
| `@neondatabase/neon-js` | Neon Auth + Data API |

## CI/CD

9 GitHub Actions workflows, 4 blocking layers before merge:
1. Python lint + test (ruff, pytest)
2. Webapp TypeScript + build (tsc, next build)
3. Agent boundary enforcement (tool grants, API key ban, inoculation)
4. AI security review (claude-code-security-review@main with custom rules)

Branch protection config: `.github/BRANCH_PROTECTION.md`
Security scan rules: `.github/security-instructions.txt`
False positive filtering: `.github/fp-filtering.txt`
PR template: `.github/pull_request_template.md`

## Neon Postgres

Project: `calm-paper-82059121` — database `neondb`
Console: https://console.neon.tech/app/projects/calm-paper-82059121?database=neondb

Credentials live in `.env` (gitignored), loaded automatically by the `SessionStart` hook in `.claude/settings.json` → `scripts/setup-env.sh`.

Environment variables available after session start:
- `NEON_DATABASE_URL` — full psycopg connection string (use when TCP:5432 is reachable)
- `NEON_HTTP_HOST` — pooler hostname for SQL-over-HTTP (`/sql` endpoint)
- `NEON_HTTP_CONN` — connection string passed in `Neon-Connection-String` header

**Always use `NEON_DATABASE_URL` from env** — never hardcode credentials in scripts.

Schema: `ontology/schema.sql` (12 tables, `resources.url` has UNIQUE constraint)

## Webapp

Next.js 16 + Tailwind CSS + Motion in `webapp/`. ASC11-inspired design:
- Dark terminal aesthetic (#050505 bg, #c8ff00 accent)
- Static export to Cloudflare Pages (agentcrawls.com)
- `cd webapp && npm run dev` for local dev
- Key deps: motion, @neondatabase/serverless, @anthropic-ai/sdk, clsx

## Installed Skills

- `frontend-design` — from anthropics/claude-plugins-official
- `agent-development` — from anthropics/claude-code
