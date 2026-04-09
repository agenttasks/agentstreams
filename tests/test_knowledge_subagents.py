"""Tests for src/knowledge_subagents.py — Claude Code CLI subagent layer."""

from __future__ import annotations

from src.knowledge_subagents import (
    AGENT_COLORS,
    AGENT_DESCRIPTIONS,
    AGENT_TOOLS,
    KNOWLEDGE_AGENT_NAMES,
    MergedSubagent,
    _is_stub_skill,
    _resolve_agent_name,
    collect_subagents,
    generate_all_subagents,
    generate_subagent_md,
)
from src.plugin_bridge import ParsedSkill, PluginLoader, VENDORS_DIR


class TestConstants:
    def test_knowledge_agent_names_populated(self):
        assert len(KNOWLEDGE_AGENT_NAMES) == 17

    def test_all_agents_have_colors(self):
        for name in KNOWLEDGE_AGENT_NAMES:
            assert name in AGENT_COLORS, f"{name} missing color"

    def test_all_agents_have_descriptions(self):
        for name in KNOWLEDGE_AGENT_NAMES:
            assert name in AGENT_DESCRIPTIONS, f"{name} missing description"

    def test_no_api_key_in_descriptions(self):
        for name, desc in AGENT_DESCRIPTIONS.items():
            if "ANTHROPIC_API_KEY" in desc:
                assert "never" in desc.lower()


class TestResolveAgentName:
    def test_direct_match(self):
        loader = PluginLoader()
        sales_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales"
        if not sales_dir.exists():
            return
        manifest = loader.load(sales_dir)
        assert _resolve_agent_name(manifest) == "sales-agent"

    def test_partner_built_subplugin(self):
        loader = PluginLoader()
        apollo_dir = VENDORS_DIR / "knowledge-work-plugins" / "partner-built" / "apollo"
        if not apollo_dir.exists():
            return
        manifest = loader.load(apollo_dir)
        assert _resolve_agent_name(manifest) == "partner-built-agent"

    def test_fsi_prefix_match(self):
        loader = PluginLoader()
        fa_dir = VENDORS_DIR / "financial-services-plugins" / "financial-analysis"
        if not fa_dir.exists():
            return
        manifest = loader.load(fa_dir)
        assert _resolve_agent_name(manifest) == "finance-agent"


class TestCollectSubagents:
    def test_collects_17_agents(self):
        agents = collect_subagents()
        assert len(agents) == 17

    def test_sales_agent_has_skills(self):
        agents = collect_subagents()
        assert "sales-agent" in agents
        assert len(agents["sales-agent"].skills) >= 9

    def test_finance_agent_merges_plugins(self):
        agents = collect_subagents()
        fa = agents["finance-agent"]
        plugin_names = [p.name for p in fa.plugins]
        assert "finance" in plugin_names

    def test_partner_built_merges_subplugins(self):
        agents = collect_subagents()
        pb = agents["partner-built-agent"]
        assert len(pb.plugins) >= 4


class TestGenerateSubagentMd:
    def test_has_frontmatter(self):
        agents = collect_subagents()
        md = generate_subagent_md(agents["sales-agent"])
        assert md.startswith("---\n")
        assert "\n---\n" in md

    def test_has_skills_frontmatter(self):
        agents = collect_subagents()
        md = generate_subagent_md(agents["sales-agent"])
        assert "skills:" in md
        assert "vendors/knowledge-work-plugins/sales/skills/" in md

    def test_has_mcp_servers(self):
        agents = collect_subagents()
        md = generate_subagent_md(agents["sales-agent"])
        assert "mcpServers:" in md
        assert "hubspot" in md

    def test_has_inoculation(self):
        agents = collect_subagents()
        md = generate_subagent_md(agents["sales-agent"])
        assert "## Inoculation" in md

    def test_read_only_agent_tools(self):
        agents = collect_subagents()
        md = generate_subagent_md(agents["compliance-reviewer"])
        assert "tools: Read, Glob, Grep" in md
        assert "Write" not in md.split("---")[1].split("tools:")[1].split("\n")[0]

    def test_claude_code_cli_framing(self):
        agents = collect_subagents()
        md = generate_subagent_md(agents["sales-agent"])
        assert "Claude Code CLI" in md

    def test_productivity_uses_user_memory(self):
        agents = collect_subagents()
        md = generate_subagent_md(agents["productivity-agent"])
        assert "memory: user" in md

    def test_no_api_key_outside_warning(self):
        results = generate_all_subagents(dry_run=True)
        for name, content in results.items():
            for line in content.split("\n"):
                if "ANTHROPIC_API_KEY" in line:
                    assert "never" in line.lower(), (
                        f"{name}: ANTHROPIC_API_KEY outside warning: {line}"
                    )


class TestGenerateAll:
    def test_generates_17_agents(self):
        results = generate_all_subagents(dry_run=True)
        assert len(results) == 17

    def test_all_have_valid_frontmatter(self):
        results = generate_all_subagents(dry_run=True)
        for name, content in results.items():
            assert content.startswith("---\n"), f"{name} missing frontmatter"
            assert f"name: {name}" in content, f"{name} missing name field"
            assert "model: opus" in content, f"{name} missing model"
