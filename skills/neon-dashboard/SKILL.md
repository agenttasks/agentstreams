---
name: neon-dashboard
description: "Launch and interact with the AgentStreams Neon Postgres TUI dashboard. TRIGGER when: user asks to view metrics, monitor tasks, browse agents, or run ad-hoc SQL queries via terminal UI. Also triggers for Textual dashboard launch. DO NOT TRIGGER for: API endpoints (use neon-api), team setup (use neon-team-setup), or one-off SQL queries outside the TUI (use `make sql` for Harlequin)."
argument-hint: "[screen: metrics|tasks|agents|sql]"
---

# /neon-dashboard - Neon Postgres TUI Dashboard

> Connector: `~~data warehouse` = Neon Postgres 18 (via `NEON_DATABASE_URL` env var).
> See [CONNECTORS.md](../../vendors/knowledge-work-plugins/data/CONNECTORS.md) for the placeholder model.

Launch an interactive terminal dashboard for monitoring AgentStreams data in Neon Postgres. Four screens cover metrics, tasks, agents, and ad-hoc SQL.

## Usage

```
/neon-dashboard [screen]
```

Or from the shell:

```bash
make tui                     # via Makefile
agentstreams tui             # via CLI
uv run agentstreams tui      # explicit uv
```

## Screens

### 1. Metrics (keybinding: `m`)

- **DataTable** of all metric definitions (name, type, unit, dimensions, description)
- Select a row to load recent values in a detail table below
- Values show recorded_at, value, and tags for the last 50 entries
- Auto-refresh available via `r` keybinding

**SQL source:**
```sql
SELECT name, type, unit, dimensions, description FROM metrics ORDER BY name;
SELECT recorded_at, value, tags FROM metric_values
  WHERE metric_name = %s ORDER BY recorded_at DESC LIMIT 50;
```

### 2. Tasks (keybinding: `t`)

- **Header bar** with 24h aggregate stats (status counts)
- **DataTable** of recent tasks (ID, queue, type, status, skill, model, created)
- Auto-refresh every 3 seconds
- Manual refresh via `r` keybinding

**SQL source:**
```sql
SELECT status, COUNT(*) FROM tasks
  WHERE created_at > now() - interval '24 hours'
  GROUP BY status ORDER BY COUNT(*) DESC;
SELECT id, queue_name, type, status, skill_name, model_id, created_at
  FROM tasks ORDER BY created_at DESC LIMIT 50;
```

### 3. Agents (keybinding: `a`)

- **Split pane**: DataTable of agent manifests (name, model, tools) on the left
- **RichLog detail** on the right: select a row to view the agent's full markdown config from `.claude/agents/{name}.md` or database fields
- Displays allowed/denied tools and description

### 4. SQL Query Editor (keybinding: `s`)

- **TextArea** for writing SQL (pre-populated with a sample query)
- **DataTable** for results (up to 500 rows, 80 char column truncation)
- Execute with `Ctrl+R`
- Status bar shows row count or error messages
- Supports both SELECT (returns rows) and DML (commits automatically)

## Keybindings

| Key | Action |
|-----|--------|
| `m` | Switch to Metrics screen |
| `t` | Switch to Tasks screen |
| `a` | Switch to Agents screen |
| `s` | Switch to SQL Query Editor |
| `r` | Refresh current screen data |
| `q` | Quit the dashboard |

## Architecture

- **Data layer**: Queries `src/neon_db.py` directly (not via the REST API)
- **Async**: Uses `@work(thread=False)` since psycopg 3.2+ is natively async
- **Framework**: Textual 3.0+ with DataTable, TextArea, RichLog widgets
- **Connection**: `connection_pool()` context manager, one connection per query

## Neon-Specific Tips

- **Scale-to-zero**: If Neon suspends the compute after idle timeout, the next query triggers a cold start (~1-3s). The dashboard handles this transparently via connection retry in `connection_pool()`.
- **Branch-aware queries**: The dashboard connects to whichever Neon branch is configured in `NEON_DATABASE_URL`. After `git checkout` with the post-checkout hook active, the env var updates to the branch-specific compute.
- **Read-only safety**: All dashboard queries are read-only except the SQL Editor screen. Use caution with DML in the editor.

## Implementation

| File | Purpose |
|------|---------|
| `src/tui.py` | Textual App with 4 Screen classes |
| `src/neon_db.py` | Shared async query functions |
| `src/cli.py` | `agentstreams tui` command entry point |
| `Makefile` | `make tui` target |

## Cross-References

- For REST API access to the same data: use the `neon-api` skill
- For raw SQL IDE with full Postgres semantics: `make sql` (launches Harlequin)
- For team branch setup: use the `neon-team-setup` skill
- For general SQL query patterns: use `make sql` (Harlequin)
