---
name: neon-team-setup
description: "Configure multi-developer Neon Postgres branching and collaboration. TRIGGER when: user asks to set up team branches, create developer database roles, configure git hooks for auto-branching, or connect DBeaver to Neon branches. DO NOT TRIGGER for: API or dashboard usage."
argument-hint: "[developers: sebastian,alex,jake]"
---

# /neon-team-setup - Multi-Developer Neon Branching

> Connector: `~~data warehouse` = Neon Postgres 18 (project `calm-paper-82059121`).
> Pattern: Claude Code parallel subagents with Neon branching guide.

Set up isolated Neon database branches for a development team. Each developer gets their own branch with full schema, a dedicated database role, and automatic branch provisioning via git hooks.

## Usage

```
/neon-team-setup [developers]
```

Or from the shell:

```bash
make team-setup              # Creates 3 branches + configures git hooks
bash scripts/neon-team-setup.sh  # Direct script execution
```

## Workflow

### 1. Prerequisites

Ensure these environment variables are set (loaded by `scripts/setup-env.sh`):

| Variable | Purpose |
|----------|---------|
| `NEON_API_KEY` | Neon API authentication |
| `NEON_PROJECT_ID` | Target Neon project (`calm-paper-82059121`) |
| `NEON_DATABASE_URL` | Main branch connection string |

Install the Neon CLI: `npm install -g neonctl`

### 2. Run Team Setup

The `scripts/neon-team-setup.sh` script (uses `set -euo pipefail` per project convention):

For each developer (default: sebastian, alex, jake):

1. **Create Neon branch** `dev/{name}` from main via `neonctl branches create`
2. **Create database role** `dev_{name}` via `neonctl roles create`
3. **Apply schema** using `psql` with branch connection string + `ontology/schema.sql`
4. **Apply migrations** from `ontology/migrations/` (if any exist)
5. **Grant permissions** on all tables in the branch
6. **Output connection string** for each developer

### 3. Configure Git Hooks

After team setup, activate the post-checkout hook:

```bash
git config core.hooksPath .githooks
```

This is done automatically by `make team-setup`.

### 4. Connect DBeaver (Optional)

Follow `docs/dbeaver-setup.md` for GUI database access:

1. New PostgreSQL connection in DBeaver Community Edition
2. **Host**: extract from branch connection string (e.g., `ep-xxx.us-east-2.aws.neon.tech`)
3. **Port**: `5432`
4. **Database**: `neondb`
5. **Username/Password**: from branch credentials
6. **Driver Properties**: `sslmode=require`
7. **Initialization**: Keep-Alive = 60 seconds (prevents Neon scale-to-zero disconnect)
8. Save separate connections for each developer branch

## Git Hook: Auto-Branch Provisioning

The `.githooks/post-checkout` hook triggers on `git checkout`:

1. **Skip conditions**: file checkout (not branch), detached HEAD, `main` branch
2. **New worktrees**: copies `.env` from main worktree if missing
3. **Branch creation**: creates a Neon branch matching the git branch name (idempotent -- safe to re-run)
4. **Env update**: writes the branch-specific `NEON_DATABASE_URL` to `.env`

This means every `git checkout -b feature/my-feature` automatically provisions a Neon branch with its own compute endpoint.

## Branch Naming Convention

| Git Branch | Neon Branch | Role |
|-----------|-------------|------|
| `main` | `main` | Shared production schema |
| `dev/sebastian` | `dev-sebastian` | `dev_sebastian` |
| `dev/alex` | `dev-alex` | `dev_alex` |
| `dev/jake` | `dev-jake` | `dev_jake` |
| `feature/my-feat` | `feature-my-feat` | (auto-created by hook) |

## Parallel Subagent Integration

The `feature-developer` and `data-optimizer` subagents (`.claude/agents/`) use `isolation: worktree` which:

1. Creates a git worktree for the agent
2. Triggers the post-checkout hook
3. Provisions a dedicated Neon branch
4. Agent works on isolated code + isolated database
5. Worktree cleaned up automatically if no changes made

This enables multiple Claude Code agents to develop features in parallel without database conflicts.

## Implementation

| File | Purpose |
|------|---------|
| `scripts/neon-team-setup.sh` | Branch + role creation script |
| `.githooks/post-checkout` | Auto-branch provisioning hook |
| `docs/dbeaver-setup.md` | DBeaver connection guide |
| `.claude/agents/feature-developer.md` | Worktree-isolated feature agent |
| `.claude/agents/data-optimizer.md` | Worktree-isolated DB optimizer agent |
| `Makefile` | `make team-setup` target |

## Cross-References

- For monitoring the database: use the `neon-dashboard` skill
- For REST API access: use the `neon-api` skill
- For SQL query patterns: use the `sql-queries` skill
