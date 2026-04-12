# Postgres Visualization & Neon Collaboration Research

Research into CLI-based Postgres data visualization, TUI tools, GUI applications,
and multi-user Neon workflows for a 3-person team.

---

## 1. CLI-Based Postgres Data Visualization

### pgcli — Enhanced Interactive CLI

The gold standard replacement for `psql`. Python-based with smart autocompletion
and syntax highlighting.

| Attribute | Detail |
|-----------|--------|
| Language | Python |
| Install | `pip install pgcli` or `brew install pgcli` |
| License | BSD |
| Neon | Full support — use standard connection string |

**Key features:**

- Context-sensitive autocompletion for SQL keywords, tables, columns, functions
- Syntax highlighting via Pygments
- Named queries — save with `\ns [name] [query]`, execute with `\n [name]`
- Query history navigation with arrow keys
- Multi-line editing
- Works with pspg as a pager for better table display

**Neon connection:**

```bash
pgcli "postgresql://user:pass@ep-cool-darkness-123456.us-east-2.aws.neon.tech/dbname?sslmode=require&channel_binding=require"
```

Reference: [pgcli.com](https://www.pgcli.com/) |
[Neon pgcli guide](https://neon.com/docs/connect/connect-pgcli)

---

### pspg — Postgres Table Pager

A Unix pager purpose-built for tabular data. Freezes header rows and first
columns while scrolling — essential for wide query results.

| Attribute | Detail |
|-----------|--------|
| Language | C (ncurses) |
| Install | `brew install pspg` / `apt install pspg` |
| License | BSD-2-Clause |
| Version | 5.8.12 (Nov 2025) |

**Key features:**

- Frozen headers and first columns during horizontal/vertical scroll
- Multiple color themes (`pspg --themes` to preview)
- Row/column/block selection with clipboard export (OSC 52)
- CSV/TSV viewer mode
- Streaming mode (`--stream`) for continuous tabular data from pipes
- Works as `PSQL_WATCH_PAGER` for `\watch` queries

**Integration with psql:**

```bash
export PAGER="pspg"
psql "postgresql://...@neon.tech/dbname?sslmode=require"
```

**Integration with pgcli:**

```bash
pgcli --pager "pspg" "postgresql://...@neon.tech/dbname"
```

Reference: [github.com/okbob/pspg](https://github.com/okbob/pspg)

---

### pg_activity — Real-Time Server Monitoring

A `top`-like TUI for monitoring live PostgreSQL server activity.

| Attribute | Detail |
|-----------|--------|
| Language | Python |
| Install | `pip install pg-activity` |
| License | PostgreSQL License |
| Neon | Partial — requires superuser for full data |

**Key features:**

- Real-time view of running queries, locks, and waiting processes
- Configurable refresh rate (0.5–5 seconds)
- System clipboard copy of focused query (OSC 52)
- Configuration profiles in `~/.config/pg_activity/`
- AWS RDS mode (`--rds`) with filtered rdsadmin output

**Neon limitation:** Neon does not grant superuser access, so pg_activity
runs in degraded mode — system info and temp file data are not displayed,
but active queries and connection stats are visible.

```bash
pg_activity -h ep-cool-darkness-123456.us-east-2.aws.neon.tech -U user -d dbname
```

Reference: [github.com/dalibo/pg_activity](https://github.com/dalibo/pg_activity)

---

### VisiData — Terminal Spreadsheet for Data Exploration

A powerful terminal multitool that presents tabular data as an interactive
spreadsheet. Connects directly to Postgres via DSN.

| Attribute | Detail |
|-----------|--------|
| Language | Python |
| Install | `pipx install visidata` |
| License | GPL-3.0 |
| Neon | Full support via postgres:// DSN |

**Key features:**

- Spreadsheet-like navigation (hjkl/arrow keys) for millions of rows
- Column-level operations: sort, filter, type conversion, regex transform
- Frequency tables, histograms, and pivot tables
- Python expressions for derived columns
- Multi-format support: CSV, JSON, Excel, SQLite, Postgres, and more
- Workflow recording and replay

**Neon connection:**

```bash
vd "postgres://user:pass@ep-cool-darkness-123456.us-east-2.aws.neon.tech/dbname?sslmode=require"
```

Reference: [visidata.org](https://www.visidata.org/) |
[github.com/saulpw/visidata](https://github.com/saulpw/visidata)

---

### usql — Universal SQL Client

A single CLI for 30+ database engines with a psql-compatible interface.

| Attribute | Detail |
|-----------|--------|
| Language | Go |
| Install | `brew install xo/xo/usql` or `go install github.com/xo/usql@latest` |
| License | MIT |
| Neon | Full support via postgres:// DSN |

**Key features:**

- Unified interface across PostgreSQL, MySQL, SQLite, MSSQL, Oracle, and 25+ more
- psql-style backslash commands (`\dt`, `\d+`, `\l`)
- Syntax highlighting and context-based autocompletion
- Copy data between different database engines
- Output formats: table, CSV, JSON, and more
- Terminal graphics support

```bash
usql "postgres://user:pass@ep-cool-darkness-123456.us-east-2.aws.neon.tech/dbname?sslmode=require"
```

Reference: [github.com/xo/usql](https://github.com/xo/usql)

---

## 2. TUI (Text User Interface) SQL IDEs

### Harlequin — The SQL IDE for Your Terminal

A full-featured SQL IDE built with Python's Textual framework. This is the
most capable terminal-based SQL tool available.

| Attribute | Detail |
|-----------|--------|
| Language | Python (Textual) |
| Install | `uv tool install 'harlequin[postgres]'` |
| License | MIT |
| Version | 2.5.1 (Dec 2025) |
| Neon | Full support |

**Key features:**

- **Data Catalog** sidebar: browse schemas, tables, columns, types
- **Query Editor** with syntax highlighting, autocompletion, multi-cursor
- **Results Viewer** handles millions of rows with smooth scrolling
- **Mouse support** — click, drag, scroll
- Manual transaction mode toggle
- Supports DuckDB, SQLite, PostgreSQL, MySQL via adapters

**Neon connection:**

```bash
harlequin -a postgres "postgres://user:pass@ep-cool-darkness-123456.us-east-2.aws.neon.tech/dbname?sslmode=require"
```

Or with individual flags:

```bash
harlequin -a postgres \
  -h ep-cool-darkness-123456.us-east-2.aws.neon.tech \
  -p 5432 -U user --password pass -d dbname
```

Respects standard `PG*` environment variables.

Reference: [harlequin.sh](https://harlequin.sh/) |
[github.com/tconbeer/harlequin-postgres](https://github.com/tconbeer/harlequin-postgres)

---

### lazysql — Lazygit-Inspired Database TUI

A cross-platform TUI database client written in Go, inspired by Lazygit's
keyboard-driven workflow.

| Attribute | Detail |
|-----------|--------|
| Language | Go |
| Install | `go install github.com/jorgerojas26/lazysql@latest` |
| License | MIT |
| Neon | Full support via connection string |

**Key features:**

- Vim-style keyboard shortcuts throughout
- Tabbed interface — multiple tables or editor sessions
- Table data browsing with filtering
- Built-in SQL editor with syntax highlighting
- SSH tunnel support via config
- CSV export
- Supports MySQL, PostgreSQL, SQLite, MSSQL

Reference: [github.com/jorgerojas26/lazysql](https://github.com/jorgerojas26/lazysql)

---

### gobang — Rust Database TUI

A fast, cross-platform TUI database management tool written in Rust.

| Attribute | Detail |
|-----------|--------|
| Language | Rust |
| Install | `cargo install gobang` |
| License | MIT |
| Neon | Full support via DSN |

**Key features:**

- Cross-platform TUI for MySQL, PostgreSQL, SQLite
- Fast startup and low memory footprint
- Schema browsing and query execution
- Keyboard-driven interface

Reference: [github.com/TaKO8Ki/gobang](https://github.com/TaKO8Ki/gobang)

---

## 3. GUI Applications

### DBeaver — Universal Database Tool

The most versatile free GUI database client. Works with 80+ databases.

| Attribute | Detail |
|-----------|--------|
| Platforms | Windows, macOS, Linux |
| Pricing | Community: Free / Pro: $25/mo |
| License | Apache 2.0 (Community) |
| Neon | Tested and documented |

**Key features:**

- SQL editor with autocompletion, execution plans
- ER diagrams and schema visualization
- Data browser with inline editing
- Multi-database support (80+ engines)
- Plugin architecture

**Neon-specific configuration:**

1. Create new PostgreSQL connection
2. Enter host, port (5432), database, username, password separately
   (Java/pgJDBC does not accept the full connection string in the URL field)
3. Driver Properties > set `sslmode` = `require`
4. Edit Connection > Connection Settings > Initialization > **Keep-Alive: 60 seconds**
   (prevents Neon scale-to-zero from dropping idle connections)

Reference: [dbeaver.io](https://dbeaver.io/) |
[Neon DBeaver guide](https://neon.com/guides/dbeaver-hosted-postgres)

---

### pgAdmin 4 — Official PostgreSQL Admin

The official PostgreSQL management tool maintained by the PostgreSQL Global
Development Group.

| Attribute | Detail |
|-----------|--------|
| Platforms | Windows, macOS, Linux (web-based UI) |
| Pricing | Free / Open Source |
| License | PostgreSQL License |
| Neon | Tested — enter connection details in separate fields |

**Key features:**

- SQL editor with autocompletion and visual EXPLAIN plans
- Visual query builder for SELECT statements
- Role and permission management
- Server monitoring dashboard
- Schema and table editing
- Backup/restore management

Reference: [pgadmin.org](https://www.pgadmin.org/)

---

### DataGrip — JetBrains SQL IDE

Professional SQL IDE for developers who spend significant time writing queries.

| Attribute | Detail |
|-----------|--------|
| Platforms | Windows, macOS, Linux |
| Pricing | $24.90/mo or $249/year (free for students/OSS) |
| License | Commercial |
| Neon | Tested — enter credentials in separate fields |

**Key features:**

- Best-in-class autocompletion and code inspection
- Schema diff and migration tools
- VCS integration and task tracking
- Code navigation (go to definition, find usages)
- Spreadsheet-style data editing
- Smart refactoring for SQL

Reference: [jetbrains.com/datagrip](https://www.jetbrains.com/datagrip/)

---

### Beekeeper Studio — Clean Cross-Platform Client

Open-source, developer-focused database GUI with a clean interface.

| Attribute | Detail |
|-----------|--------|
| Platforms | Windows, macOS, Linux |
| Pricing | Community: Free / Ultimate: $7/mo |
| License | GPL-3.0 (Community) |
| Neon | Tested — requires Enable SSL option |

**Key features:**

- SQL editor with autocomplete and query parameters
- Spreadsheet-style table editing
- Schema editor for columns, indexes, foreign keys
- Data export: CSV, Excel, JSON
- Secure connections (SSL/SSH tunnels)
- AI Shell (paid): natural language to SQL

Reference: [beekeeperstudio.io](https://www.beekeeperstudio.io/)

---

### TablePlus — Native Lightweight Client

Fast, native GUI client. macOS-first design with clean minimal interface.

| Attribute | Detail |
|-----------|--------|
| Platforms | macOS, Windows, Linux |
| Pricing | Free (limited) / $89 license |
| License | Commercial |
| Neon | Tested — SNI support since macOS build 436, Windows build 202 |

**Key features:**

- Native app performance (not Electron)
- Clean tabbed interface
- Inline data editing
- Quick query and schema browsing
- Multi-database support

Reference: [tableplus.com](https://tableplus.com/)

---

### Postico 2 — Mac-Native PostgreSQL Client

Elegant, focused PostgreSQL client for macOS.

| Attribute | Detail |
|-----------|--------|
| Platforms | macOS only |
| Pricing | Free trial / $50 license |
| License | Commercial |
| Neon | Tested — SNI support since v1.5.21 |

**Note:** Postico's keep-connection-alive mechanism (enabled by default) may
prevent Neon compute from scaling to zero.

Reference: [eggerapps.at/postico2](https://eggerapps.at/postico2/)

---

## 4. Connecting to Neon with 3 People

### Option A: Neon Organizations (Recommended)

Create a Neon Organization and invite all 3 team members. This is the
simplest path to shared access.

**Roles:**

| Role | Permissions |
|------|-------------|
| Admin | Full control over org and all projects |
| Member | Access all projects, cannot modify org settings or delete projects |

**Setup steps:**

1. Create a Neon Organization (free plan includes unlimited members)
2. Invite teammates by email
3. Auto-provisioning available: users with matching email domain join automatically
4. All members access projects via Console, API, and CLI with their own credentials

**Billing:** All costs charged to the org owner's account.

Reference: [Neon Organizations](https://neon.com/docs/manage/organizations)

---

### Option B: Project Collaboration (Direct Invite)

Invite collaborators directly to a specific project without creating an org.

**Setup:**

1. Go to Project Settings in Neon Console
2. Invite by email (each person needs a Neon account)
3. Collaborators can use Console, API, and CLI with their own API keys

**Limitations:**

- Collaborators cannot delete the project
- Billing remains on the project owner
- Collaborators work under the owner's plan limits

Reference:
[Project Collaboration Guide](https://neon.com/docs/guides/project-collaboration-guide)

---

### Option C: Database Branching (Per-Developer Isolation)

Each team member gets their own Neon branch — like a git branch for the
database. This provides full schema + data isolation.

**Recommended naming convention:**

```
dev/sebastian
dev/alex
dev/jake
```

**Branch creation via CLI:**

```bash
# Install Neon CLI
npm i -g neonctl

# Create a branch for each developer
neonctl branches create --name dev/sebastian --project-id calm-paper-82059121
neonctl branches create --name dev/alex --project-id calm-paper-82059121
neonctl branches create --name dev/jake --project-id calm-paper-82059121
```

**Benefits:**

- Zero storage duplication (copy-on-write)
- Each branch can auto-scale independently (including scale-to-zero)
- Safe to run destructive experiments
- Can reset to parent branch state at any time
- Lightweight — affordable even as the team grows

**Workflow patterns:**

| Pattern | Best for |
|---------|----------|
| One branch per developer | Long-lived dev environments |
| One branch per PR | CI/CD integration, ephemeral testing |
| Shared dev branch | Small teams with sequential work |

Reference:
[Branching workflows](https://neon.com/branching/branching-workflows-for-development) |
[Workflow primer](https://neon.com/docs/get-started/workflow-primer)

---

### Option D: Separate Database Roles

Create individual Postgres roles with scoped permissions.

```sql
-- Create roles for each team member
CREATE ROLE sebastian WITH LOGIN PASSWORD 'sebastian_password';
CREATE ROLE alex WITH LOGIN PASSWORD 'alex_password';
CREATE ROLE jake WITH LOGIN PASSWORD 'jake_password';

-- Grant appropriate permissions
GRANT USAGE ON SCHEMA public TO sebastian, alex, jake;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO sebastian, alex;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO jake;  -- read-only
```

**Via Neon CLI:**

```bash
neonctl roles create --name sebastian --project-id calm-paper-82059121
neonctl roles create --name alex --project-id calm-paper-82059121
neonctl roles create --name jake --project-id calm-paper-82059121
```

---

### Connection Pooling for 3 Users

Neon uses PgBouncer in **transaction mode** for connection pooling.

| Metric | Value (1 CU / 4 GB) |
|--------|---------------------|
| Max client connections | 10,000 |
| Default pool size | 377 per user per database |
| Max Postgres connections | 419 |

For 3 concurrent users, pooling is not a bottleneck. Use the **pooled**
connection string (with `-pooler` suffix in hostname) for application
connections, and **direct** connections for migrations, `pg_dump`, or admin tasks.

**Pooled connection string format:**

```
postgresql://user:pass@ep-cool-darkness-123456-pooler.us-east-2.aws.neon.tech/dbname?sslmode=require
```

**Direct connection string format:**

```
postgresql://user:pass@ep-cool-darkness-123456.us-east-2.aws.neon.tech/dbname?sslmode=require
```

Reference:
[Connection pooling](https://neon.com/docs/connect/connection-pooling)

---

## 5. Quick-Start: Recommended Stack for 3-Person Team

### CLI/TUI (each developer installs locally)

```bash
# Harlequin — full SQL IDE in terminal
uv tool install 'harlequin[postgres]'

# pgcli — enhanced interactive CLI (alternative to psql)
pip install pgcli

# pspg — table pager for psql output
brew install pspg  # or apt install pspg
```

### GUI (choose per preference)

| Developer | Recommendation | Why |
|-----------|---------------|-----|
| Power user | DBeaver Community (free) | ER diagrams, multi-DB, plugins |
| Mac user | Postico 2 or TablePlus | Native, fast, clean |
| Query-heavy | DataGrip | Best autocompletion and refactoring |

### Neon team setup

```bash
# 1. Install Neon CLI
npm i -g neonctl

# 2. Authenticate
neonctl auth

# 3. Create org and invite team
# (or use project collaboration in Neon Console)

# 4. Create per-developer branches
neonctl branches create --name dev/sebastian --project-id calm-paper-82059121
neonctl branches create --name dev/alex --project-id calm-paper-82059121
neonctl branches create --name dev/jake --project-id calm-paper-82059121

# 5. Get connection strings
neonctl connection-string --branch dev/sebastian --project-id calm-paper-82059121
neonctl connection-string --branch dev/alex --project-id calm-paper-82059121
neonctl connection-string --branch dev/jake --project-id calm-paper-82059121
```

---

## 6. Existing AgentStreams Neon Integration

This project (`calm-paper-82059121`) already uses Neon Postgres 18 with:

- **29 tables** defined in `ontology/schema.sql`
- **Extensions:** pgvector, pg_graphql, pg_tiktoken, hll, pg_trgm, pg_stat_statements, pg_cron, pg_jsonschema
- **Connection:** `NEON_DATABASE_URL` env var (loaded by SessionStart hook via `scripts/setup-env.sh`)
- **HTTP fallback:** `scripts/neon-http-upsert.py` uses SQL-over-HTTPS when TCP:5432 is blocked
- **CLI output:** `rich` library for terminal table rendering in `src/cli.py`
- **Visualization agents:** data-analyst agent with `create-viz`, `data-visualization`, `build-dashboard` skills (matplotlib, seaborn, plotly)

---

## Sources

- [pgcli](https://www.pgcli.com/) | [Neon pgcli guide](https://neon.com/docs/connect/connect-pgcli)
- [pspg](https://github.com/okbob/pspg)
- [pg_activity](https://github.com/dalibo/pg_activity)
- [VisiData](https://www.visidata.org/)
- [usql](https://github.com/xo/usql)
- [Harlequin](https://harlequin.sh/) | [harlequin-postgres](https://github.com/tconbeer/harlequin-postgres)
- [lazysql](https://github.com/jorgerojas26/lazysql)
- [gobang](https://github.com/TaKO8Ki/gobang)
- [DBeaver](https://dbeaver.io/) | [Neon DBeaver guide](https://neon.com/guides/dbeaver-hosted-postgres)
- [pgAdmin 4](https://www.pgadmin.org/)
- [DataGrip](https://www.jetbrains.com/datagrip/)
- [Beekeeper Studio](https://www.beekeeperstudio.io/)
- [TablePlus](https://tableplus.com/)
- [Postico 2](https://eggerapps.at/postico2/)
- [Neon Organizations](https://neon.com/docs/manage/organizations)
- [Neon Project Collaboration](https://neon.com/docs/guides/project-collaboration-guide)
- [Neon Branching Workflows](https://neon.com/branching/branching-workflows-for-development)
- [Neon Connection Pooling](https://neon.com/docs/connect/connection-pooling)
- [Neon CLI](https://neon.com/docs/reference/neon-cli)
- [Neon GUI applications](https://neon.com/docs/connect/connect-postgres-gui)
