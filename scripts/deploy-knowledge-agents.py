#!/usr/bin/env python3
"""Deploy knowledge-work agents to the Managed Agents API.

Reads plugin manifests from vendors/ and registers each as a
managed agent via the Anthropic Managed Agents API.

Usage:
    # Deploy all plugins from all repos
    uv run scripts/deploy-knowledge-agents.py

    # Deploy only knowledge-work-plugins
    uv run scripts/deploy-knowledge-agents.py --repo knowledge-work-plugins

    # Deploy only financial-services-plugins
    uv run scripts/deploy-knowledge-agents.py --repo financial-services-plugins

    # Dry run (print configs without deploying)
    uv run scripts/deploy-knowledge-agents.py --dry-run

    # List all plugins and skills
    uv run scripts/deploy-knowledge-agents.py --list

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure src/ is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.plugin_bridge import PluginBridge, PluginLoader


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deploy knowledge-work agents to Managed Agents API."
    )
    parser.add_argument(
        "--repo",
        help="Only deploy plugins from this repo (e.g., knowledge-work-plugins).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print configs without deploying.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all plugins and skills, then exit.",
    )
    parser.add_argument(
        "--model",
        default="claude-opus-4-6",
        help="Model for all agents (default: claude-opus-4-6).",
    )
    args = parser.parse_args()

    loader = PluginLoader()

    # List mode
    if args.list:
        repos = loader.load_all()
        total_skills = 0
        for repo_name, manifests in repos.items():
            print(f"\n{'='*60}")
            print(f"  {repo_name}")
            print(f"{'='*60}")
            for m in manifests:
                print(f"\n  {m.name} (v{m.version}) — {m.skill_count} skills")
                if m.description:
                    print(f"    {m.description[:80]}...")
                for s in m.skills:
                    desc = s.description[:60] + "..." if len(s.description) > 60 else s.description
                    print(f"      - {s.slug}: {desc}")
                if m.mcp_servers:
                    print(f"    MCP: {', '.join(m.mcp_servers.keys())}")
                total_skills += m.skill_count
        print(f"\nTotal: {total_skills} skills across {sum(len(v) for v in repos.values())} plugins")
        return

    bridge = PluginBridge(model=args.model)

    # Build configs
    if args.repo:
        agents = bridge.to_managed_agents(args.repo)
    else:
        agents = bridge.to_all_managed_agents()

    print(f"Prepared {len(agents)} agent configs")

    if args.dry_run:
        for name, config in agents.items():
            params = config.to_create_params()
            print(f"\n--- {name} ---")
            print(json.dumps(params, indent=2, default=str)[:500])
            print(f"  Skills: {config.metadata.get('skills', '')[:80]}")
            print(f"  MCP: {[s.name for s in config.mcp_servers]}")
        print(f"\nDry run complete. {len(agents)} agents would be deployed.")
        return

    # Deploy
    print(f"\nDeploying {len(agents)} agents...")
    agent_ids = bridge.deploy_all(
        repos=[args.repo] if args.repo else None,
    )

    print(f"\nDeployed {len(agent_ids)} agents:")
    for name, agent_id in agent_ids.items():
        print(f"  {name}: {agent_id}")


if __name__ == "__main__":
    main()
