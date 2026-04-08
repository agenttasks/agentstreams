# Branch Protection Configuration

Configure these settings at:
**Settings → Branches → Add branch protection rule**

## Rule: `main`

### Required status checks before merging

Enable **"Require status checks to pass before merging"** and add:

| Check Name | Workflow | Blocking |
|---|---|---|
| `All Checks Pass` | `required-checks.yml` | **Yes** |
| `Security Review` | `claude-review.yml` | **Yes** |
| `Merge Gate` | `claude-review.yml` | **Yes** |

The `All Checks Pass` job aggregates 4 sub-checks:
1. **Python Lint & Test** — ruff check, ruff format, pytest
2. **Webapp Build** — TypeScript check, Next.js static export
3. **Agent Boundaries** — tool grant validation, ANTHROPIC_API_KEY ban
4. **Security Review** — claude-code-security-review with custom rules

### Additional settings

- [x] **Require a pull request before merging**
  - Require 1 approval
  - Dismiss stale reviews when new commits are pushed
- [x] **Require conversation resolution before merging**
- [x] **Require linear history** (squash and merge only)
- [x] **Do not allow bypassing the above settings**

## Required Secrets

Add these in **Settings → Secrets and variables → Actions**:

| Secret | Purpose | Source |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code OAuth (security review + interactive + consistency) | Claude Code CLI |
| `CLOUDFLARE_API_TOKEN` | Cloudflare Pages deploy | dash.cloudflare.com/profile/api-tokens |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account | `e6294e3ea89f8207af387d459824aaae` |
| `NEON_API_KEY` | Neon preview branches | console.neon.tech |
| `NEON_PROJECT_ID` | Neon project | `calm-paper-82059121` |

## Workflow Architecture

```
PR opened/synced
├── required-checks.yml (BLOCKING — must pass for merge)
│   ├── python-lint (ruff + pytest)
│   ├── webapp-build (tsc + next build)
│   ├── agent-boundaries (tool grants, API key ban)
│   ├── security-review (claude-code-security-review@main)
│   └── all-checks-pass (gate)
│
├── claude-review.yml (BLOCKING — security + advisory consistency)
│   ├── claude-security (claude-code-security-review@main)
│   ├── claude-consistency (claude-code-action@v1, advisory)
│   └── merge-gate (blocks on security findings)
│
├── agent-boundary-check.yml (on agent/orchestrator changes)
│   ├── recursive spawning check
│   ├── read-only enforcement
│   ├── model hierarchy compliance
│   ├── inoculation block presence
│   └── ANTHROPIC_API_KEY ban
│
├── validate-skills.yml (on skills/ontology/scripts changes)
│   ├── skill validation
│   ├── ontology validation
│   ├── python quality (ruff + pytest + security-audit.py)
│   └── MCP server tests (vitest)
│
├── webapp-ci.yml (on webapp/ changes)
│   └── TypeScript + ESLint + build verification
│
├── deploy-webapp.yml (on push to main, webapp/ changes)
│   └── Cloudflare Pages deploy via wrangler-action@v3
│
├── neon-preview.yml (on schema changes)
│   ├── create preview branch + apply schema
│   └── delete on PR close
│
├── evals.yml (on skills/evals changes)
│   ├── config validation (always)
│   └── live evals (workflow_dispatch only)
│
└── claude-interactive.yml (on @claude mentions)
    └── interactive Claude response
```
