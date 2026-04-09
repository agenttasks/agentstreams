.PHONY: help install install-safety install-webapp dev dev-webapp \
       lint lint-py lint-webapp format test test-py test-webapp \
       build build-webapp typecheck security-audit validate \
       eval-codegen eval-codegen-quick eval-codegen-dry eval-promptfoo \
       eval-cuad eval-casehold eval-cuad-quick eval-cuad-recall eval-legal \
       eval-lexglue eval-lexglue-quick eval-lexglue-dry ingest-lexglue \
       install-managed-agents build-managed-agents check-managed-agents \
       clean ci ci-py ci-webapp

# ── Help ─────────────────────────────────────────────────────
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Install ──────────────────────────────────────────────────
install: ## Install Python deps (uv sync)
	uv sync

install-safety: ## Install safety-research extras (petri, bloom)
	uv sync --extra safety

install-webapp: ## Install webapp Node deps
	cd webapp && npm ci

install-all: install install-webapp ## Install everything

# ── Development ──────────────────────────────────────────────
dev: ## Start Python dev environment
	uv run python -c "print('agentstreams ready')"

cli: ## Run the agentstreams CLI (pass ARGS, e.g., make cli ARGS="agents list")
	uv run agentstreams $(ARGS)

cli-help: ## Show agentstreams CLI help tree
	@uv run agentstreams --help
	@echo ""
	@echo "Subcommands:"
	@for cmd in agents eval pdf pipeline validate layers; do \
	  echo ""; echo "  agentstreams $$cmd:"; \
	  uv run agentstreams $$cmd --help 2>/dev/null | grep -E "^  [a-z]" || true; \
	done

dev-webapp: ## Start Next.js dev server
	cd webapp && npm run dev

# ── Lint ─────────────────────────────────────────────────────
lint: lint-py lint-webapp ## Lint everything

lint-py: ## Lint Python (ruff check)
	uv run ruff check src/ scripts/ tests/

lint-webapp: ## Lint webapp (ESLint + TypeScript)
	cd webapp && npx next lint
	cd webapp && npx tsc --noEmit

# ── Format ───────────────────────────────────────────────────
format: ## Auto-format Python code
	uv run ruff check --fix src/ scripts/ tests/
	uv run ruff format src/ scripts/ tests/

# ── Test ─────────────────────────────────────────────────────
test: test-py ## Run all tests

test-py: ## Run Python tests
	uv run pytest tests/ -v --tb=short

test-cov: ## Run Python tests with coverage
	uv run pytest tests/ -v --tb=short --cov=src --cov-report=term-missing

test-webapp: ## Verify webapp builds
	cd webapp && npx next build

# ── Build ────────────────────────────────────────────────────
build: build-webapp ## Build all artifacts

build-webapp: ## Build webapp static export
	cd webapp && npm run build

# ── Type check ───────────────────────────────────────────────
typecheck: ## TypeScript type check (webapp)
	cd webapp && npx tsc --noEmit

# ── Security ─────────────────────────────────────────────────
security-audit: ## Run security audit (scripts + agents)
	uv run scripts/security-audit.py --check-only --paths scripts/ .claude/

security-review: ## Run /security-review via Claude Code
	claude /security-review

# ── Validate ─────────────────────────────────────────────────
validate: ## Validate skills + ontology
	uv run python scripts/validate-skills.py --check-only
	uv run python scripts/validate-ontology.py

validate-agents: ## Validate agent boundaries (no recursive spawning, API key ban)
	@echo "Checking agent tool grants..."
	@for f in .claude/agents/*.md; do \
	  AGENT=$$(basename "$$f" .md); \
	  [ "$$AGENT" = "coordinator" ] && continue; \
	  TOOLS=$$(sed -n '/^---$$/,/^---$$/p' "$$f" | grep -E '^tools:' | head -1); \
	  if echo "$$TOOLS" | grep -qw "Agent"; then \
	    echo "FAIL: $$AGENT has recursive Agent tool"; exit 1; \
	  fi; \
	done
	@echo "Checking ANTHROPIC_API_KEY in source files..."
	@VIOLATIONS=$$(grep -rn "ANTHROPIC_API_KEY" \
	  --include="*.py" --include="*.ts" --include="*.sh" \
	  src/ .claude/ webapp/src/ 2>/dev/null | \
	  grep -vi "never use" | grep -vi "NEVER" | \
	  grep -v "security-audit.py" | grep -v "validate-skills.py" | \
	  grep -v "node_modules" | grep -vi "BLOCKED\|block-secrets\|violations\.push\|output\.includes" || true); \
	if [ -n "$$VIOLATIONS" ]; then \
	  echo "FAIL: ANTHROPIC_API_KEY found in source files"; \
	  echo "$$VIOLATIONS"; exit 1; \
	fi
	@echo "All agent boundary checks passed."

# ── Evals ────────────────────────────────────────────────────
eval-codegen: ## Run A/B code generation eval (all models, all languages)
	uv run scripts/run-codegen-eval.py

eval-codegen-quick: ## Quick codegen eval (sonnet only, 1 sample)
	uv run scripts/run-codegen-eval.py --models sonnet --samples 1

eval-codegen-dry: ## Dry-run codegen eval (show task matrix)
	uv run scripts/run-codegen-eval.py --dry-run

eval-cuad: ## Run CUAD contract understanding benchmark
	uv run julia/evals/cuad/runner.py --benchmark cuad

eval-casehold: ## Run CaseHOLD precedent ranking benchmark
	uv run julia/evals/cuad/runner.py --benchmark casehold

eval-cuad-quick: ## Quick CUAD eval (20 contracts, 5 high-priority clause types)
	uv run julia/evals/cuad/runner.py --benchmark cuad --contracts 20

eval-cuad-recall: ## CUAD vault recall@K (pgvector vs lancedb vs pg_trgm)
	uv run julia/evals/cuad/runner.py --vault-recall --contracts 50

eval-legal: ## Run all legal benchmarks (CUAD + CaseHOLD)
	uv run julia/evals/cuad/runner.py

eval-lexglue: ## Run LexGLUE legal benchmark (all 5 tasks)
	uv run scripts/run-lexglue-eval.py

eval-lexglue-quick: ## Quick LexGLUE eval (CaseHOLD, 10 samples)
	uv run scripts/run-lexglue-eval.py --task casehold --samples 10

eval-lexglue-dry: ## Dry-run LexGLUE eval (show task matrix)
	uv run scripts/run-lexglue-eval.py --dry-run

ingest-lexglue: ## Download LexGLUE from HuggingFace → Neon + local JSON
	uv run --extra lexglue scripts/ingest-lexglue.py --task all --lance

## ── Managed Agents ──────────────────────────────────────────
install-managed-agents: ## Install managed agents TS package deps
	cd src/knowledge-work-managed-agents && npm install

build-managed-agents: ## Build managed agents TypeScript
	cd src/knowledge-work-managed-agents && npx tsc

check-managed-agents: ## Type-check managed agents
	cd src/knowledge-work-managed-agents && npx tsc --noEmit

eval-promptfoo: ## Run all promptfoo eval suites
	@for dir in evals/*/; do \
	  if [ -f "$$dir/promptfooconfig.yaml" ]; then \
	    echo "Running: $$dir"; \
	    cd "$$dir" && npx promptfoo eval && cd ../..; \
	  fi; \
	done

# ── CI (mirrors GitHub Actions) ──────────────────────────────
ci: ci-py ci-webapp validate validate-agents security-audit ## Run full CI locally

ci-py: ## Python CI (lint + test)
	uv run ruff check src/ scripts/ tests/
	uv run pytest tests/ -v --tb=short

ci-webapp: ## Webapp CI (typecheck + build)
	cd webapp && npm ci
	cd webapp && npx tsc --noEmit
	cd webapp && npx next build

# ── Clean ────────────────────────────────────────────────────
clean: ## Clean build artifacts
	rm -rf webapp/out webapp/.next
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
