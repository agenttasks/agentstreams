# agentstreams

Safety-grounded multi-agent orchestration for Claude Code. Composable pipelines across codegen, security audit, alignment audit, and evaluation — powered by 18 open-source [safety-research](https://github.com/safety-research) tools and Mythos System Card methodology.

## Architecture

```
Opus 4.6 (orchestrator)
├── security-auditor    [opus]   Glasswing-depth vulnerability scanning
├── alignment-auditor   [opus]   Petri 2.0 methodology, suspicion scoring
├── architecture-reviewer [opus] Agent topology + observability review
├── code-generator      [sonnet] Python/TypeScript codegen
├── test-runner         [sonnet] Test execution + result analysis
├── prompt-hardener     [sonnet] Inoculation-prompting defense
├── eval-builder        [sonnet] Behavioral eval suites (bloom, lie-detector)
└── harmlessness-screen [haiku]  Ultra-fast input classification
```

## Quick start

```bash
# Prerequisites: Python 3.12+, Node.js 22+, uv
make install-all        # Install Python + webapp deps
make ci                 # Run full CI locally (lint, test, build, validate)
make dev-webapp         # Start Next.js dev server
```

## Project structure

```
src/                    Python source (orchestrator, bloom filter, crawlers, Neon DB)
scripts/                Developer tools (crawlers, validators, security audit)
webapp/                 Next.js 16 + Tailwind + Motion landing page
.claude/agents/         8 agent configurations with YAML frontmatter
.claude/subagents/      Orchestration rules (opus-orchestrator.md)
.claude/commands/       Slash commands (/security-review)
.claude/skills/         Skills (frontend-design, agent-development)
ontology/               Schema (12 tables, Neon Postgres)
skills/                 Multi-language skill definitions (8 languages)
evals/                  Promptfoo evaluation suites
tests/                  Python test suite
```

## Make targets

```
make help               Show all targets
make install            Install Python deps (uv sync)
make install-all        Install Python + webapp deps
make lint               Lint everything (ruff + ESLint + tsc)
make test               Run Python tests (pytest)
make build              Build webapp static export
make validate           Validate skills + ontology
make validate-agents    Check agent boundaries (tool grants, API key ban)
make security-audit     Run security-audit.py
make ci                 Run full CI locally
make format             Auto-format Python code
make clean              Clean build artifacts
```

## CI/CD

9 GitHub Actions workflows with 4 blocking layers before merge:

| Layer | Check | Workflow |
|-------|-------|----------|
| 1 | Python lint + test | `required-checks.yml` |
| 2 | Webapp TypeScript + build | `required-checks.yml` |
| 3 | Agent boundary enforcement | `required-checks.yml` |
| 4 | AI security review | `required-checks.yml` |

Additional workflows: `claude-review.yml` (security + consistency), `deploy-webapp.yml` (Cloudflare Pages), `neon-preview.yml` (DB branches), `evals.yml` (promptfoo), `validate-skills.yml`, `agent-boundary-check.yml`, `webapp-ci.yml`, `claude-interactive.yml`.

See [`.github/BRANCH_PROTECTION.md`](.github/BRANCH_PROTECTION.md) for branch protection configuration.

## Safety-research integration

18 repos from [github.com/safety-research](https://github.com/safety-research) provide Mythos-grade methodology:

| Agent | Key repos |
|-------|-----------|
| alignment-auditor | petri, trusted-monitor, SHADE-Arena, lie-detector, ciphered-reasoning-llms, A3, alignment-faking |
| security-auditor | auditing-agents, finetuning-auditor, PurpleLlama, SCONE-bench, lie-detector |
| eval-builder | bloom, impossiblebench, lie-detector, A3, alignment-faking |
| prompt-hardener | inoculation-prompting, persona_vectors |
| harmlessness-screen | assistant-axis, ciphered-reasoning-llms, persona_vectors |

Install the pip-installable packages: `make install-safety`

## Auth

All auth flows through `CLAUDE_CODE_OAUTH_TOKEN`. Never use `ANTHROPIC_API_KEY`.

## Stack

- **Python** managed with `uv` exclusively
- **Node.js** for webapp (`webapp/`) and MCP server (`mcp-server/`)
- **Neon Postgres** for persistence (project `calm-paper-82059121`)
- **Cloudflare Pages** for webapp hosting (`agentcrawls.com`)
- **Claude Agent SDK** (`@anthropic-ai/claude-agent-sdk`) for agent runtime

## License

See individual component licenses.
