# Claude Review Gate — Performance Report

## Summary

Built a multi-language skill system (`crawl-ingest`) with 28 files across 8 languages, then established a Claude-powered CI/CD review gate that runs on every PR. This document records the pipeline history, issues caught, and gate configuration evolution.

## Pipeline History

### PRs Merged

| PR | Branch | Scope | Gate | Duration |
|----|--------|-------|------|----------|
| #1 | `fix/comprehensive-code-review` | 28 skill files + 7 fixes | Pre-gate | — |
| #2 | `feat/ci-foundation` | CLAUDE.md, REVIEW.md, settings, 2 review skills | Pre-gate | — |
| #3 | `feat/ci-workflows` | 2 GitHub Actions workflows | Pre-gate | — |
| #7 | `feat/review-shared` | SQL injection fix in curl/README.md | **First gated PR** | Security 5m30s, Merge Gate 4s |

### PRs Closed

| PR | Reason |
|----|--------|
| #8 | Duplicate — `/install-github-app` generated overlapping workflows; closed after extracting CLAUDE_CODE_OAUTH_TOKEN secret setup |

## Issues Caught Across All PRs

### PR #1 — Comprehensive Code Review (7 fixes)

| Category | File | Issue | Fix |
|----------|------|-------|-----|
| Auth violation | `curl/README.md` (3 occurrences) | `ANTHROPIC_API_KEY` in curl examples | Replaced with `CLAUDE_CODE_OAUTH_TOKEN` |
| Auth violation | `shared/evals.md` | `ANTHROPIC_API_KEY` in GitHub Actions config | Replaced with `CLAUDE_CODE_OAUTH_TOKEN` |
| Model name format | `shared/programmatic-prompts.md` | `claude-sonnet-4-20250514` (date suffix) | Changed to `claude-sonnet-4-6` |
| Version pin | `java/gradle-setup.md` | MCP Java SDK using `latest` | Pinned to `0.9.0` |
| Missing install | `scripts/setup_ts.sh` | `@modelcontextprotocol/sdk` not installed | Added install line |
| Missing auth docs | `SKILL.md` | Only TS/Python/Java constructors documented | Added Go, Ruby, C#, PHP, cURL patterns |
| Wrong dependency | `php/README.md` | `rize/uri-template` (unused) in composer.json | Replaced with `guzzlehttp/psr7` (actually used) |

### PR #7 — SQL Injection Fix (1 fix)

| Category | File | Issue | Fix |
|----------|------|-------|-----|
| SQL injection | `curl/README.md` | Raw `$url` interpolated into sqlite3 SQL | Added single-quote escaping via `${url//\'/\'\'}` |

### Total: 8 issues found and fixed

| Category | Count |
|----------|-------|
| Auth violations (ANTHROPIC_API_KEY) | 4 |
| SQL injection | 1 |
| Model name format | 1 |
| Missing dependencies/installs | 2 |
| Version pins | 1 |
| Missing documentation | 1 |

## Gate Configuration Evolution

The gate required 4 iterations to reach a working state:

| Iteration | Run | Change | Problem Solved |
|-----------|-----|--------|----------------|
| v1 | `23802440028` | Initial config: `--max-turns 8`, `--json-schema`, sequential jobs | — |
| v2 | `23802531715` | Added `id-token: write` permission | `Unable to get ACTIONS_ID_TOKEN_REQUEST_URL` — OAuth token exchange needs OIDC |
| v3 | `23802608936` | Pushed workflow fix to `main` first | `Workflow file must have identical content to default branch` — GitHub validates workflow identity |
| v4 | `23802677083` | Increased `--max-turns` to 20, removed `--json-schema` | `error_max_turns` at 8 turns — structured JSON output consumed turn budget |
| v5 | `23802928138` | Scoped to PR diff, parallel jobs, advisory consistency | Consistency review reading all 28 files (12+ min, turn limit hit) |
| **v5 result** | `23802928138` | **Security ✅ 5m30s, Merge Gate ✅ 4s** | **First successful gate pass** |

## Gate Architecture (Final)

```
PR opened/updated
    │
    ├──→ Security Review (blocking, 15 turns, diff-scoped)
    │    └── Checks: auth, secrets, injection, SSRF, path traversal
    │
    ├──→ Consistency Review (advisory, 15 turns, diff-scoped)
    │    └── Checks: versions, model names, cross-refs, SDK patterns
    │
    └──→ Merge Gate (blocks on security only)
```

### Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project rules loaded into every Claude session |
| `REVIEW.md` | Code review focus areas and ignore list |
| `.claude/settings.json` | Read-only permissions, deny destructive ops |
| `.claude/skills/review-security.md` | Security review skill definition |
| `.claude/skills/review-consistency.md` | Consistency review skill definition |
| `.github/workflows/claude-review.yml` | 3-job gate workflow |
| `.github/workflows/claude-interactive.yml` | `@claude` mention handler |

## Lessons Learned

1. **Workflow files must match `main`** — GitHub validates that the PR's workflow YAML is identical to the default branch version. Push workflow changes to `main` first.

2. **`id-token: write` is required** — `CLAUDE_CODE_OAUTH_TOKEN` uses OIDC token exchange, which needs the `id-token` permission.

3. **`--json-schema` consumes turns** — Forcing structured JSON output eats into the turn budget. For CI reviews, let Claude post comments naturally instead.

4. **Scope reviews to the diff** — A consistency review reading all 28 files for a 1-file PR took 12+ min and hit turn limits. Scoping to `git diff` makes reviews fast and focused.

5. **Parallel > sequential** — Running security and consistency in parallel halves wall-clock time with no downside.

6. **Advisory consistency, blocking security** — Security issues (secrets, injection) must block. Consistency issues (version mismatches) are important but shouldn't prevent merging.
