## Summary

<!-- 1-3 bullet points describing what this PR does and why -->

-

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Refactor (no functional change)
- [ ] Agent config change (`.claude/agents/` or `.claude/subagents/`)
- [ ] Schema / database change (`ontology/schema.sql` or `ontology/migrations/`)
- [ ] Webapp change (`webapp/`)
- [ ] CI/CD or workflow change (`.github/`)
- [ ] Documentation
- [ ] Dependency update

## Checklist

### Required (all PRs)

- [ ] `make ci` passes locally (lint, test, build, validate)
- [ ] No `ANTHROPIC_API_KEY` usage (auth flows through `CLAUDE_CODE_OAUTH_TOKEN`)
- [ ] No hardcoded credentials or secrets
- [ ] Model names use hyphen format (`claude-opus-4-6`, `claude-sonnet-4-6`)

### If modifying agents

- [ ] No agent has `Agent` in tools (only `coordinator` may spawn subagents)
- [ ] Read-only agents have `disallowedTools: Edit, Write`
- [ ] Model assignment follows hierarchy (opus/sonnet/haiku)
- [ ] Inoculation block present for security-critical agents
- [ ] `src/orchestrator.py` updated to match frontmatter changes
- [ ] `opus-orchestrator.md` subagent roster updated

### If modifying webapp

- [ ] `cd webapp && npx tsc --noEmit` passes
- [ ] `cd webapp && npx next build` produces static export
- [ ] No `dangerouslySetInnerHTML` or XSS vectors

### If modifying schema or database

- [ ] Changes are idempotent (`CREATE TABLE IF NOT EXISTS`, `ON CONFLICT DO NOTHING/UPDATE`)
- [ ] New tables added to both `ontology/schema.sql` (DDL) and `ontology/agentstreams.ttl` (ontology class)
- [ ] New seed data uses `ON CONFLICT` — safe to re-run on production
- [ ] Migrations in `ontology/migrations/` are numbered sequentially (`002-*.sql`, etc.)
- [ ] `neon-preview.yml` will create a preview branch — verify schema applies cleanly
- [ ] `pg_graphql` validation passes (auto-checked in preview workflow)
- [ ] No destructive DDL (`DROP TABLE`, `DROP COLUMN`) without migration plan
- [ ] JSONB columns have `DEFAULT '{}'::jsonb` or `DEFAULT '[]'::jsonb`

### If modifying safety-research references

- [ ] Star counts consistent across files
- [ ] Repo URLs valid (`github.com/safety-research/...`)
- [ ] Pip-installable packages added to `pyproject.toml [safety]` if applicable

## Test plan

<!-- How to verify these changes work -->

-

## Related

<!-- Link to issues, other PRs, or safety-research repos if relevant -->
