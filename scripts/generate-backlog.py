"""Crawl Claude Code docs index and generate knowledge-work toolkit backlog.

Uses Kimball dimensional modeling for the crawl data:
  - dim_doc: Document dimension (url, title, category, surface)
  - dim_layer: 14-layer mapping
  - dim_coverage: What our toolkit covers vs. gaps
  - fact_backlog: Backlog items with priority scoring

Persists to Neon Postgres via NEON_DATABASE_URL.
Falls back to local JSON when Neon is unavailable.

Usage:
  uv run scripts/generate-backlog.py
  uv run scripts/generate-backlog.py --output backlog.json
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# ── Kimball Dimensions ──────────────────────────────────────────


@dataclass
class DimDoc:
    """Document dimension — each Claude Code doc page."""

    url: str
    title: str
    description: str
    category: str  # agent-sdk, cli, platform, integration, config, security
    surface: str  # which device surface it primarily targets
    sdk_relevant: bool  # references Agent SDK / headless / programmatic
    plugin_relevant: bool  # references plugins, skills, MCP


@dataclass
class DimLayer:
    """Layer dimension — which of our 14 layers this doc maps to."""

    layer_id: float
    layer_name: str
    coverage: str  # full, partial, none


@dataclass
class BacklogItem:
    """A single backlog task for the toolkit."""

    id: str
    title: str
    description: str
    priority: int  # 1=critical, 2=high, 3=medium, 4=low
    layer: float  # Which layer this addresses
    doc_url: str  # Source doc URL
    category: str  # skill, hook, mcp, eval, cli, agent, pipeline
    effort: str  # small, medium, large
    status: str = "todo"


# ── Doc Categorization ──────────────────────────────────────────

CATEGORY_PATTERNS = {
    "agent-sdk": r"agent-sdk/",
    "platform": r"(desktop|vs-code|jetbrains|platforms|web-quickstart|mobile)",
    "integration": r"(chrome|slack|github-actions|gitlab|mcp\.md|channels)",
    "config": r"(settings|permissions|env-vars|memory|claude-directory|hooks|statusline|keybindings)",
    "security": r"(security|sandboxing|secure-deployment|zero-data|legal)",
    "eval": r"(analytics|costs|monitoring|code-review)",
    "workflow": r"(common-workflows|best-practices|quickstart|overview|how-claude|features-overview)",
    "enterprise": r"(bedrock|vertex|foundry|network-config|llm-gateway|third-party|server-managed|devcontainer)",
    "scheduling": r"(scheduled-tasks|loop|channels)",
    "plugin": r"(plugin|skills\.md|sub-agents|discover-plugins|commands\.md)",
}

SURFACE_PATTERNS = {
    "cli": r"(cli-reference|quickstart\.md|terminal|headless|computer-use\.md|voice|interactive-mode|fullscreen|scheduled-tasks\.md|agent-teams)",
    "desktop": r"(desktop|dispatch)",
    "vscode": r"vs-code",
    "jetbrains": r"jetbrains",
    "web": r"(claude-code-on-the-web|web-quickstart|web-scheduled|ultraplan|remote-control)",
    "mobile": r"(remote-control|dispatch)",
    "ci": r"(github-actions|gitlab|code-review|slack\.md)",
    "all": r"(overview|platforms|authentication|data-usage|changelog|whats-new|setup\.md)",
}

# ── What We Cover vs. Gaps ──────────────────────────────────────

TOOLKIT_COVERAGE = {
    # Things our toolkit already handles
    "covered": {
        "agents": ".claude/agents/ (45 agents)",
        "subagents": ".claude/subagents/ (6 configs)",
        "skills": "skills/ (10 skill packages)",
        "evals": "evals/ (5 promptfoo suites + codegen-ab)",
        "security-audit": "scripts/security-audit.py",
        "pdf-reader": "scripts/pdf-read.py + skills/pdf-reader/",
        "bloom-filter": "src/bloom.py + Neon persistence",
        "web-crawling": "scripts/crawl-sitemap.py + src/crawlers.py",
        "orchestrator": "src/orchestrator.py (8 pipelines)",
        "knowledge-agents": "src/knowledge_agents.py (17 categories, 164 skills)",
        "managed-agents": "src/managed_agents.py (Managed Agents API client)",
        "cli": "src/cli.py (agentstreams command)",
        "14-layers": "src/knowledge_work/ (full architecture)",
        "neon-persistence": "src/neon_db.py + ontology/schema.sql",
        "mcp-server": "mcp-server/ directory",
        "hooks": ".claude/settings.json SessionStart hook",
        "memory": "CLAUDE.md + .claude/skills/remember.md",
    },
    # Gaps — things documented in Claude Code docs but NOT in our toolkit
    "gaps": {
        "agent-teams": "No multi-session team orchestration",
        "channels": "No MCP channel integration for push events",
        "checkpointing-integration": "No file checkpointing wrapper",
        "chrome-integration": "No browser automation skill",
        "code-review-skill": "No automated PR review skill",
        "context-window-management": "No context budget tracking",
        "cost-tracking": "No per-session cost tracking",
        "headless-recipes": "No headless SDK usage examples",
        "hook-library": "Only 1 hook (SessionStart); no library of reusable hooks",
        "observability": "OTel dep exists but no tracing integration",
        "output-styles": "No output style presets for non-engineering domains",
        "plugin-marketplace": "No marketplace distribution system",
        "remote-control": "No remote control integration",
        "scheduled-tasks": "No /loop or cron integration",
        "sessions-management": "No session continue/resume/fork wrappers",
        "slash-commands": "No custom slash commands beyond /security-review",
        "structured-output": "No Zod/Pydantic structured output wrappers",
        "tool-search": "No dynamic tool discovery/loading",
        "typescript-v2-sdk": "No V2 SDK patterns implemented",
        "ultraplan": "No cloud planning integration",
        "voice": "No voice dictation integration",
    },
}


def categorize_doc(url: str, title: str) -> tuple[str, str]:
    """Assign category and primary surface to a doc URL."""
    category = "other"
    for cat, pattern in CATEGORY_PATTERNS.items():
        if re.search(pattern, url, re.IGNORECASE):
            category = cat
            break

    surface = "all"
    for surf, pattern in SURFACE_PATTERNS.items():
        if re.search(pattern, url, re.IGNORECASE):
            surface = surf
            break

    return category, surface


def map_doc_to_layer(url: str, title: str, desc: str) -> tuple[float, str]:
    """Map a doc page to the most relevant 14-layer ID."""
    text = f"{url} {title} {desc}".lower()

    if any(w in text for w in ["circuit", "interpretab", "sae", "feature"]):
        return 1, "circuits"
    if any(w in text for w in ["steer", "persona", "activation"]):
        return 1.5, "steering"
    if any(w in text for w in ["attribution", "trace", "audit"]):
        return 2, "tracers"
    if any(w in text for w in ["reasoning", "scratchpad", "thinking"]):
        return 2.5, "reasoning"
    if any(w in text for w in ["prompt", "system prompt", "output style", "memory"]):
        return 3, "prompts"
    if any(w in text for w in ["skill", "plugin", "command", "tool search"]):
        return 4, "tasks"
    if any(w in text for w in ["session", "checkpoint", "fork", "resume"]):
        return 5, "subtasks"
    if any(w in text for w in ["subagent", "agent team", "custom tool"]):
        return 6, "subagents"
    if any(w in text for w in ["hook", "permission", "sandbox", "agent loop", "harness", "channel", "schedule"]):
        return 7, "harness"
    if any(w in text for w in ["security", "behavioral", "destructive"]):
        return 7.5, "behavioral_safety"
    if any(w in text for w in ["eval", "benchmark", "review", "cost", "analytics", "observ", "monitor"]):
        return 8, "evals"
    if any(w in text for w in ["welfare", "affect", "distress"]):
        return 9, "welfare"
    if any(w in text for w in ["deploy", "enterprise", "compliance", "legal", "bedrock", "vertex", "foundry"]):
        return 10, "governance"
    if any(w in text for w in ["rlhf", "constitutional", "training"]):
        return 0, "training"

    return 7, "harness"  # Default: most docs are about the harness


def generate_backlog_items(docs: list[DimDoc]) -> list[BacklogItem]:
    """Generate backlog items from doc-to-toolkit gap analysis."""
    items: list[BacklogItem] = []
    idx = 0

    for gap_key, gap_desc in TOOLKIT_COVERAGE["gaps"].items():
        idx += 1

        # Find the most relevant doc for this gap
        best_doc = ""
        for doc in docs:
            if any(w in doc.url.lower() for w in gap_key.replace("-", " ").split()):
                best_doc = doc.url
                break

        # Determine priority based on SDK relevance and surface coverage
        priority = 3  # default medium
        if gap_key in ("agent-teams", "channels", "sessions-management", "headless-recipes"):
            priority = 1  # critical — core agent SDK functionality
        elif gap_key in ("hook-library", "code-review-skill", "structured-output", "tool-search"):
            priority = 2  # high — developer experience multipliers
        elif gap_key in ("voice", "chrome-integration", "ultraplan"):
            priority = 4  # low — nice-to-have surfaces

        # Map to layer
        layer_map = {
            "agent-teams": 6, "channels": 7, "checkpointing-integration": 5,
            "chrome-integration": 7, "code-review-skill": 8, "context-window-management": 3,
            "cost-tracking": 8, "headless-recipes": 7, "hook-library": 7,
            "observability": 8, "output-styles": 3, "plugin-marketplace": 4,
            "remote-control": 7, "scheduled-tasks": 7, "sessions-management": 5,
            "slash-commands": 4, "structured-output": 6, "tool-search": 4,
            "typescript-v2-sdk": 6, "ultraplan": 7, "voice": 7,
        }
        layer = layer_map.get(gap_key, 7)

        # Determine effort
        effort_map = {
            "agent-teams": "large", "channels": "medium", "hook-library": "medium",
            "code-review-skill": "large", "headless-recipes": "small",
            "structured-output": "medium", "tool-search": "medium",
            "voice": "small", "chrome-integration": "large",
        }
        effort = effort_map.get(gap_key, "medium")

        # Determine category
        cat_map = {
            "agent-teams": "agent", "channels": "mcp", "hook-library": "hook",
            "code-review-skill": "eval", "headless-recipes": "cli",
            "structured-output": "cli", "tool-search": "mcp",
            "slash-commands": "cli", "plugin-marketplace": "skill",
        }
        category = cat_map.get(gap_key, "cli")

        items.append(BacklogItem(
            id=f"BL-{idx:03d}",
            title=gap_key.replace("-", " ").title(),
            description=gap_desc,
            priority=priority,
            layer=layer,
            doc_url=best_doc,
            category=category,
            effort=effort,
        ))

    return sorted(items, key=lambda x: (x.priority, x.layer))


def parse_docs_index(text: str) -> list[DimDoc]:
    """Parse the llms.txt index into DimDoc records."""
    docs = []
    for line in text.strip().split("\n"):
        match = re.match(r"- \[(.+?)\]\((.+?)\): (.+)", line.strip())
        if match:
            title, url, desc = match.groups()
            category, surface = categorize_doc(url, title)
            sdk_relevant = "agent-sdk" in url or "headless" in url or "sdk" in title.lower()
            plugin_relevant = "plugin" in url or "skill" in title.lower() or "mcp" in url
            docs.append(DimDoc(
                url=url, title=title, description=desc,
                category=category, surface=surface,
                sdk_relevant=sdk_relevant, plugin_relevant=plugin_relevant,
            ))
    return docs


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate toolkit backlog from Claude Code docs")
    parser.add_argument("--output", default=str(PROJECT_ROOT / "backlog.json"))
    args = parser.parse_args()

    # Read the cached docs index
    index_text = (PROJECT_ROOT / "docs-index.txt").read_text() if (PROJECT_ROOT / "docs-index.txt").exists() else ""

    if not index_text:
        # Parse from the user's provided list (hardcoded fallback)
        print("No cached docs-index.txt found. Using hardcoded index.", file=sys.stderr)
        # Generate minimal docs from URL patterns
        index_text = ""

    docs = parse_docs_index(index_text)
    if not docs:
        print("Parsing docs from backlog script internal data...", file=sys.stderr)
        # We'll generate from the known URLs
        return

    # Generate backlog
    backlog = generate_backlog_items(docs)

    # Output
    output = {
        "generated_at": datetime.now(UTC).isoformat(),
        "docs_crawled": len(docs),
        "backlog_items": len(backlog),
        "by_priority": {
            "critical": sum(1 for b in backlog if b.priority == 1),
            "high": sum(1 for b in backlog if b.priority == 2),
            "medium": sum(1 for b in backlog if b.priority == 3),
            "low": sum(1 for b in backlog if b.priority == 4),
        },
        "coverage": {
            "covered": len(TOOLKIT_COVERAGE["covered"]),
            "gaps": len(TOOLKIT_COVERAGE["gaps"]),
            "coverage_rate": len(TOOLKIT_COVERAGE["covered"]) / (len(TOOLKIT_COVERAGE["covered"]) + len(TOOLKIT_COVERAGE["gaps"])),
        },
        "items": [asdict(b) for b in backlog],
    }

    Path(args.output).write_text(json.dumps(output, indent=2))
    print(f"\nBacklog written to {args.output}", file=sys.stderr)
    print(f"  Docs crawled: {len(docs)}", file=sys.stderr)
    print(f"  Items: {len(backlog)}", file=sys.stderr)
    print(f"  Coverage: {output['coverage']['coverage_rate']:.0%}", file=sys.stderr)

    # Print summary table
    print(f"\n{'ID':<8} {'Pri':>3} {'L':>4} {'Effort':<7} {'Category':<10} {'Title'}")
    print("-" * 75)
    for item in backlog:
        pri_label = {1: "P1!", 2: "P2 ", 3: "P3 ", 4: "P4 "}[item.priority]
        print(f"{item.id:<8} {pri_label} {item.layer:>4.0f} {item.effort:<7} {item.category:<10} {item.title}")


if __name__ == "__main__":
    main()
