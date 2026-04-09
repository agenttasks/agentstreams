"""Tests for src/plugin_bridge.py — Plugin-to-ManagedAgent bridge."""

from __future__ import annotations

from pathlib import Path

from src.plugin_bridge import (
    VENDORS_DIR,
    ParsedSkill,
    PluginBridge,
    PluginLoader,
    PluginManifest,
    all_managed_agents,
    load_all_plugins,
    plugin_to_managed,
)


# ── ParsedSkill Tests ────────────────────────────────────────


class TestParsedSkill:
    def test_from_path_with_frontmatter(self):
        # Use a real skill from vendors/
        skill_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales" / "skills" / "account-research"
        if not skill_dir.exists():
            return  # skip if vendors not populated
        skill = ParsedSkill.from_path(skill_dir)
        assert skill is not None
        assert skill.slug == "account-research"
        assert skill.name == "account-research"
        assert len(skill.description) > 0
        assert len(skill.body) > 0

    def test_from_path_nonexistent(self):
        result = ParsedSkill.from_path(Path("/nonexistent/path"))
        assert result is None

    def test_from_path_stub(self):
        # FSI stubs have minimal content
        skill_dir = VENDORS_DIR / "financial-services-plugins" / "financial-analysis" / "skills" / "dcf-model"
        if not skill_dir.exists():
            return
        skill = ParsedSkill.from_path(skill_dir)
        assert skill is not None
        assert skill.slug == "dcf-model"


# ── PluginLoader Tests ───────────────────────────────────────


class TestPluginLoader:
    def test_load_single_plugin(self):
        loader = PluginLoader()
        sales_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales"
        if not sales_dir.exists():
            return
        manifest = loader.load(sales_dir)
        assert manifest.name == "sales"
        assert len(manifest.skills) >= 9
        assert len(manifest.mcp_servers) > 0
        assert "slack" in manifest.mcp_servers

    def test_load_plugin_metadata(self):
        loader = PluginLoader()
        sales_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales"
        if not sales_dir.exists():
            return
        manifest = loader.load(sales_dir)
        assert manifest.version == "1.2.0"
        assert len(manifest.description) > 0

    def test_load_repo_knowledge_work(self):
        loader = PluginLoader()
        manifests = loader.load_repo("knowledge-work-plugins")
        if not manifests:
            return
        names = [m.name for m in manifests]
        assert "sales" in names
        assert "data" in names
        assert "legal" in names
        assert len(manifests) >= 17

    def test_load_repo_financial_services(self):
        loader = PluginLoader()
        manifests = loader.load_repo("financial-services-plugins")
        if not manifests:
            return
        names = [m.name for m in manifests]
        assert "financial-analysis" in names
        assert len(manifests) >= 5

    def test_load_all(self):
        loader = PluginLoader()
        repos = loader.load_all()
        assert "knowledge-work-plugins" in repos
        assert "financial-services-plugins" in repos

    def test_skill_slugs_property(self):
        loader = PluginLoader()
        sales_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales"
        if not sales_dir.exists():
            return
        manifest = loader.load(sales_dir)
        slugs = manifest.skill_slugs
        assert "account-research" in slugs
        assert "pipeline-review" in slugs

    def test_mcp_servers_parsed(self):
        loader = PluginLoader()
        sales_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales"
        if not sales_dir.exists():
            return
        manifest = loader.load(sales_dir)
        assert "hubspot" in manifest.mcp_servers
        assert manifest.mcp_servers["hubspot"].startswith("https://")


# ── PluginBridge Tests ───────────────────────────────────────


class TestPluginBridge:
    def test_to_managed_agent_basic(self):
        loader = PluginLoader()
        bridge = PluginBridge()
        sales_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales"
        if not sales_dir.exists():
            return
        manifest = loader.load(sales_dir)
        config = bridge.to_managed_agent(manifest)
        assert config.name == "sales-agent"
        assert config.model == "claude-opus-4-6"
        assert "inoculation" in config.system.lower()
        # ANTHROPIC_API_KEY only appears in "never" warning context
        for line in config.system.split("\n"):
            if "ANTHROPIC_API_KEY" in line:
                assert "never" in line.lower(), (
                    f"ANTHROPIC_API_KEY in non-warning context: {line}"
                )

    def test_to_managed_agent_has_mcp_servers(self):
        loader = PluginLoader()
        bridge = PluginBridge()
        sales_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales"
        if not sales_dir.exists():
            return
        manifest = loader.load(sales_dir)
        config = bridge.to_managed_agent(manifest)
        server_names = [s.name for s in config.mcp_servers]
        assert "hubspot" in server_names or "slack" in server_names

    def test_to_managed_agent_read_only(self):
        loader = PluginLoader()
        bridge = PluginBridge()
        legal_dir = VENDORS_DIR / "knowledge-work-plugins" / "legal"
        if not legal_dir.exists():
            return
        manifest = loader.load(legal_dir)
        config = bridge.to_managed_agent(manifest)
        assert config.name == "compliance-reviewer"
        write_disabled = [c for c in config.toolset.configs if c.name == "write"]
        assert len(write_disabled) == 1
        assert write_disabled[0].enabled is False

    def test_to_managed_agent_metadata(self):
        loader = PluginLoader()
        bridge = PluginBridge()
        data_dir = VENDORS_DIR / "knowledge-work-plugins" / "data"
        if not data_dir.exists():
            return
        manifest = loader.load(data_dir)
        config = bridge.to_managed_agent(manifest)
        assert config.metadata["plugin"] == "data"
        assert int(config.metadata["skill_count"]) >= 10
        assert "data-visualization" in config.metadata["skills"]

    def test_to_managed_agents_merges_fsi(self):
        bridge = PluginBridge()
        agents = bridge.to_managed_agents("financial-services-plugins")
        if not agents:
            return
        # All FSI plugins should merge into finance-agent
        assert "finance-agent" in agents
        skills = agents["finance-agent"].metadata.get("skills", "")
        assert "dcf-model" in skills

    def test_to_all_managed_agents(self):
        agents = all_managed_agents()
        if not agents:
            return
        assert len(agents) >= 17
        # Should have both KW and FSI agents
        assert "sales-agent" in agents
        assert "finance-agent" in agents

    def test_system_prompt_structure(self):
        loader = PluginLoader()
        bridge = PluginBridge()
        eng_dir = VENDORS_DIR / "knowledge-work-plugins" / "engineering"
        if not eng_dir.exists():
            return
        manifest = loader.load(eng_dir)
        config = bridge.to_managed_agent(manifest)
        # Should have purpose, skills list, and inoculation
        assert "## Purpose" in config.system
        assert "## Skills" in config.system
        assert "## Inoculation" in config.system
        assert "code-review" in config.system

    def test_no_anthropic_api_key_in_any_agent(self):
        agents = all_managed_agents()
        for name, config in agents.items():
            for line in config.system.split("\n"):
                if "ANTHROPIC_API_KEY" in line:
                    assert "never" in line.lower(), (
                        f"{name}: ANTHROPIC_API_KEY in non-warning context: {line}"
                    )


# ── Convenience Function Tests ───────────────────────────────


class TestConvenienceFunctions:
    def test_load_all_plugins(self):
        repos = load_all_plugins()
        assert len(repos) >= 2

    def test_plugin_to_managed(self):
        sales_dir = VENDORS_DIR / "knowledge-work-plugins" / "sales"
        if not sales_dir.exists():
            return
        config = plugin_to_managed(sales_dir)
        assert config.name == "sales-agent"
        assert config.model == "claude-opus-4-6"
