# Contributing to agentstreams

## Prerequisites

- Python 3.12+ with [uv](https://docs.astral.sh/uv/)
- Node.js 22+ with npm
- Git

## Setup

```bash
git clone https://github.com/agenttasks/agentstreams.git
cd agentstreams
make install-all
```

## Development workflow

### 1. Create a branch

```bash
git checkout -b feat/your-feature main
```

### 2. Make changes

- Python source lives in `src/`, scripts in `scripts/`, tests in `tests/`
- Webapp lives in `webapp/` (Next.js + Tailwind + Motion)
- Agent configs live in `.claude/agents/` with YAML frontmatter
- Orchestrator pipelines are defined in `.claude/subagents/opus-orchestrator.md`

### 3. Run CI locally

```bash
make ci       # Full CI: lint, test, build, validate, security audit
```

Or run individual checks:

```bash
make lint             # Ruff + ESLint + TypeScript
make test             # pytest
make build            # webapp static export
make validate         # Skills + ontology validation
make validate-agents  # Agent boundary checks
make security-audit   # Security audit script
```

### 4. Submit a PR

- Fill in the PR template (auto-populated)
- All required checks must pass before merge
- PRs are squash-merged with linear history

## Code style

### Python
- Managed with `uv` exclusively (no pip, no virtualenv)
- Formatted and linted with `ruff` (line length 100)
- `set -euo pipefail` in all shell scripts
- No trailing whitespace

### TypeScript/React (webapp)
- Next.js 16 App Router with TypeScript strict mode
- Tailwind CSS for styling
- Motion (`motion/react`) for animations
- `npm ci` for deterministic installs

### Agent configs (.claude/agents/*.md)
- YAML frontmatter with `name`, `description`, `tools`, `model`, `color`
- Read-only agents (`security-auditor`, `alignment-auditor`, `architecture-reviewer`) must have `disallowedTools: Edit, Write`
- No agent may have `Agent` in its tools array except `coordinator`
- All security-critical agents must include the inoculation block

### Markdown
- ATX headings (`#`, `##`, not underlines)
- Fenced code blocks with language tags

## Conventional Commits

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

### Commit types

| Type | Semver bump | Description |
|------|-------------|-------------|
| `feat` | minor | A new feature |
| `fix` | patch | A bug fix |
| `perf` | patch | Performance improvement |
| `docs` | none | Documentation only |
| `style` | none | Formatting, whitespace |
| `refactor` | none | Code restructuring (no behavior change) |
| `test` | none | Adding or fixing tests |
| `build` | none | Build system or dependency changes |
| `ci` | none | CI/CD pipeline changes |
| `chore` | none | Maintenance tasks |
| `revert` | patch | Revert a previous commit |

### Breaking changes

Append `!` after the type/scope or add a `BREAKING CHANGE:` footer:

```bash
feat(sdk)!: redesign hook event types    # major bump
feat(api): add search endpoint           # minor bump
fix(tui): handle empty metric rows       # patch bump
```

### Scopes

Common scopes: `sdk`, `api`, `tui`, `mcp`, `hooks`, `skills`, `agents`, `ci`

## Version Management (release-please)

This project uses [release-please](https://github.com/googleapis/release-please) for automated versioning:

- Conventional commits are analyzed to determine the next semver version
- `CHANGELOG.md` is auto-generated from commit messages
- Version bumps are applied to `pyproject.toml` and `src/sdk_models.py`
- Upstream SDK dependencies (claude-code-sdk, mcp, anthropic) are tracked in `src/sdk_models.py`

When an upstream dependency releases a new version:
1. Update the version in `default_manifest()` in `src/sdk_models.py`
2. Use `feat(sdk): bump <package> to <version>` for new features
3. Use `fix(sdk): bump <package> to <version>` for bug fixes
4. Use `feat(sdk)!: bump <package> to <version>` for breaking changes

## Session Logs

Session transcripts are logged in `.claude/sessions/`. Each file documents:
- Session IDs and context continuations
- All user prompts (verbatim)
- Deliverables produced
- Commit history

## Auth rules

- **Never use `ANTHROPIC_API_KEY`** — all auth flows through `CLAUDE_CODE_OAUTH_TOKEN`
- Never hardcode credentials in code, examples, or configs
- Database credentials come from environment variables (`.env` is gitignored)

## Model naming

Always use hyphen format: `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`. Never dots or date suffixes.

## Required checks

All PRs must pass these before merge (see [`.github/BRANCH_PROTECTION.md`](.github/BRANCH_PROTECTION.md)):

| Check | What it validates |
|-------|-------------------|
| Python Lint & Test | `ruff check` + `ruff format --check` + `pytest` |
| Webapp Build | `tsc --noEmit` + `next build` (static export) |
| Agent Boundaries | No recursive spawning, read-only enforcement, API key ban |
| Security Review | `claude-code-security-review` with custom rules |
| Consistency Review | Model names, version strings, cross-references (advisory) |

## Adding a new agent

1. Create `.claude/agents/your-agent.md` with YAML frontmatter
2. Add the agent config to `src/orchestrator.py` in `_agent_configs()`
3. Reference relevant safety-research repos in a `## Safety Research Tooling` section
4. Add inoculation block if the agent handles untrusted input
5. Run `make validate-agents` to verify boundaries
6. Update `.claude/subagents/opus-orchestrator.md` subagent roster

## Adding a safety-research reference

1. Add the repo reference to the relevant agent's `.md` file
2. If pip-installable, add to `pyproject.toml` under `[project.optional-dependencies] safety`
3. Add to `opus-orchestrator.md` `<safety-research-tooling>` block
4. Update the agent's system prompt in `orchestrator.py`
5. Run tests: `make test`
