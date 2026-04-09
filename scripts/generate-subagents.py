#!/usr/bin/env python3
"""Generate Claude Code subagent .md files from vendored Cowork plugins.

Thin CLI wrapper around src/knowledge_subagents.py.

Usage:
    uv run scripts/generate-subagents.py              # Generate all
    uv run scripts/generate-subagents.py --dry-run    # Preview without writing
    uv run scripts/generate-subagents.py --list       # List agents and skill counts

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.knowledge_subagents import (
    _is_stub_skill,
    collect_subagents,
    generate_all_subagents,
    generate_subagent_md,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Claude Code subagent .md files from vendored plugins."
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing.")
    parser.add_argument("--list", action="store_true", help="List agents, then exit.")
    parser.add_argument("--agent", help="Generate only this agent (e.g., sales-agent).")
    args = parser.parse_args()

    agents = collect_subagents()

    if args.agent:
        if args.agent not in agents:
            print(f"Agent '{args.agent}' not found. Available: {', '.join(sorted(agents))}")
            sys.exit(1)
        agents = {args.agent: agents[args.agent]}

    if args.list:
        total_skills = 0
        for name in sorted(agents):
            a = agents[name]
            real = sum(1 for s in a.skills if not _is_stub_skill(s))
            stubs = sum(1 for s in a.skills if _is_stub_skill(s))
            mcp = len(a.mcp_servers)
            plugins = ", ".join(p.name for p in a.plugins)
            skill_info = f"{real} skills"
            if stubs:
                skill_info += f" + {stubs} stubs"
            print(f"  {name:30s} {skill_info:20s} {mcp:2d} MCP  [{plugins}]")
            total_skills += real + stubs
        print(f"\n  {len(agents)} agents, {total_skills} total skills")
        return

    if args.dry_run:
        for name in sorted(agents):
            content = generate_subagent_md(agents[name])
            print(f"\n{'=' * 60}")
            print(
                f"  {name}.md ({len(agents[name].skills)} skills, {len(agents[name].mcp_servers)} MCP)"
            )
            print(f"{'=' * 60}")
            print(content[:800])
            if len(content) > 800:
                print(f"  ... ({len(content)} chars total)")
        print(f"\n  Would generate {len(agents)} subagent files")
    else:
        results = generate_all_subagents()
        for name in sorted(results):
            print(f"  wrote .claude/agents/{name}.md")
        print(f"\n  Generated {len(results)} subagent files")


if __name__ == "__main__":
    main()
