"""Tests for src/knowledge_agents.py — Knowledge Work Agents plugin layer."""

from __future__ import annotations

from src.knowledge_agents import (
    CATEGORY_AGENTS,
    SKILL_CATALOG,
    KnowledgeAgentConfig,
    KnowledgeWorkRegistry,
    PluginCategory,
    SkillMeta,
    _build_knowledge_pipelines,
    _knowledge_agent_configs,
    compliance_review_pipeline,
    data_to_insight_pipeline,
    knowledge_work_environment,
    knowledge_work_managed_settings,
    list_skills,
    research_to_report_pipeline,
    resolve_skill,
    total_installs,
)
from src.managed_agents import NetworkingMode


# ── Enum Tests ────────────────────────────────────────────────


class TestPluginCategory:
    def test_all_categories(self):
        # 17 knowledge-work + 5 FSI = 22
        assert len(PluginCategory) == 22

    def test_category_values_match_directory_names(self):
        assert PluginCategory.PRODUCTIVITY.value == "productivity"
        assert PluginCategory.SALES.value == "sales"
        assert PluginCategory.CUSTOMER_SUPPORT.value == "customer-support"
        assert PluginCategory.PRODUCT_MANAGEMENT.value == "product-management"
        assert PluginCategory.MARKETING.value == "marketing"
        assert PluginCategory.LEGAL.value == "legal"
        assert PluginCategory.FINANCE.value == "finance"
        assert PluginCategory.DATA.value == "data"
        assert PluginCategory.ENTERPRISE_SEARCH.value == "enterprise-search"
        assert PluginCategory.BIO_RESEARCH.value == "bio-research"
        assert PluginCategory.COWORK_PLUGIN_MANAGEMENT.value == "cowork-plugin-management"
        assert PluginCategory.DESIGN.value == "design"
        assert PluginCategory.ENGINEERING.value == "engineering"
        assert PluginCategory.HUMAN_RESOURCES.value == "human-resources"
        assert PluginCategory.OPERATIONS.value == "operations"
        assert PluginCategory.PARTNER_BUILT.value == "partner-built"
        assert PluginCategory.PDF_VIEWER.value == "pdf-viewer"


# ── Skill Catalog Tests ──────────────────────────────────────


class TestSkillCatalog:
    def test_catalog_populated(self):
        assert len(SKILL_CATALOG) >= 100

    def test_top_skill_by_installs(self):
        top = max(SKILL_CATALOG.values(), key=lambda m: m.installs)
        assert top.name == "data-visualization"
        assert top.installs == 3800

    def test_every_skill_has_category(self):
        for name, meta in SKILL_CATALOG.items():
            assert isinstance(meta.category, PluginCategory), f"{name} missing category"

    def test_no_duplicate_skills(self):
        names = list(SKILL_CATALOG.keys())
        assert len(names) == len(set(names))

    def test_all_plugins_have_skills(self):
        """Every plugin category should have at least one skill."""
        for cat in PluginCategory:
            skills = [m for m in SKILL_CATALOG.values() if m.category == cat]
            assert len(skills) > 0, f"Plugin {cat.value} has no skills"

    def test_data_plugin_skills(self):
        data_skills = [m.name for m in SKILL_CATALOG.values()
                       if m.category == PluginCategory.DATA]
        assert "data-visualization" in data_skills
        assert "sql-queries" in data_skills
        assert "statistical-analysis" in data_skills

    def test_legal_plugin_skills(self):
        legal_skills = [m.name for m in SKILL_CATALOG.values()
                        if m.category == PluginCategory.LEGAL]
        assert "legal-risk-assessment" in legal_skills
        assert "review-contract" in legal_skills
        assert "triage-nda" in legal_skills


# ── Category Agent Mapping Tests ─────────────────────────────


class TestCategoryAgents:
    def test_every_category_has_agent(self):
        for cat in PluginCategory:
            assert cat in CATEGORY_AGENTS, f"{cat} not mapped to an agent"

    def test_knowledge_work_one_to_one(self):
        """Each knowledge-work plugin category has its own dedicated agent."""
        kw_agents = [
            CATEGORY_AGENTS[cat] for cat in PluginCategory
            if not cat.value.startswith("fsi-")
        ]
        assert len(kw_agents) == len(set(kw_agents)), "KW categories share agents"

    def test_fsi_categories_share_finance_agent(self):
        """All FSI categories route to finance-agent."""
        fsi_agents = {
            CATEGORY_AGENTS[cat] for cat in PluginCategory
            if cat.value.startswith("fsi-")
        }
        assert fsi_agents == {"finance-agent"}

    def test_key_agent_names(self):
        assert CATEGORY_AGENTS[PluginCategory.SALES] == "sales-agent"
        assert CATEGORY_AGENTS[PluginCategory.LEGAL] == "compliance-reviewer"
        assert CATEGORY_AGENTS[PluginCategory.FINANCE] == "finance-agent"
        assert CATEGORY_AGENTS[PluginCategory.DATA] == "data-analyst"
        assert CATEGORY_AGENTS[PluginCategory.ENGINEERING] == "engineering-agent"
        assert CATEGORY_AGENTS[PluginCategory.PARTNER_BUILT] == "partner-built-agent"
        assert CATEGORY_AGENTS[PluginCategory.PDF_VIEWER] == "pdf-viewer-agent"
        assert CATEGORY_AGENTS[PluginCategory.COWORK_PLUGIN_MANAGEMENT] == "cowork-plugin-agent"


# ── SkillMeta Tests ──────────────────────────────────────────


class TestSkillMeta:
    def test_frozen(self):
        meta = SkillMeta(name="test", category=PluginCategory.DATA)
        try:
            meta.name = "changed"  # type: ignore[misc]
            raise AssertionError("Should be frozen")
        except AttributeError:
            pass

    def test_defaults(self):
        meta = SkillMeta(name="test", category=PluginCategory.DATA)
        assert meta.installs == 0


# ── Knowledge Agent Config Tests ─────────────────────────────


class TestKnowledgeAgentConfig:
    def test_seventeen_unique_agents(self):
        configs = _knowledge_agent_configs()
        assert len(configs) == 17

    def test_expected_agent_names(self):
        configs = _knowledge_agent_configs()
        expected = {
            "productivity-agent", "sales-agent", "customer-support-agent",
            "product-management-agent", "marketing-agent", "compliance-reviewer",
            "finance-agent", "data-analyst", "enterprise-search-agent",
            "bio-research-agent", "design-agent", "engineering-agent",
            "hr-agent", "operations-agent", "cowork-plugin-agent",
            "partner-built-agent", "pdf-viewer-agent",
        }
        assert set(configs.keys()) == expected

    def test_all_agents_use_opus(self):
        configs = _knowledge_agent_configs()
        for name, kac in configs.items():
            assert kac.model == "claude-opus-4-6", (
                f"{name} uses {kac.model} instead of opus"
            )

    def test_skills_populated(self):
        configs = _knowledge_agent_configs()
        for name, kac in configs.items():
            assert len(kac.skills) > 0, f"{name} has no skills"

    def test_to_managed_basic(self):
        configs = _knowledge_agent_configs()
        managed = configs["data-analyst"].to_managed()
        assert managed.name == "data-analyst"
        assert managed.model == "claude-opus-4-6"

    def test_to_managed_read_only(self):
        configs = _knowledge_agent_configs()
        managed = configs["compliance-reviewer"].to_managed(disable_write=True)
        tool_names = [c.name for c in managed.toolset.configs]
        assert "write" in tool_names
        assert "edit" in tool_names
        for tc in managed.toolset.configs:
            if tc.name in ("write", "edit"):
                assert tc.enabled is False

    def test_no_anthropic_api_key_in_prompts(self):
        configs = _knowledge_agent_configs()
        for name, kac in configs.items():
            assert "ANTHROPIC_API_KEY" not in kac.agent_config.system_prompt, (
                f"{name} contains ANTHROPIC_API_KEY"
            )

    def test_model_names_use_hyphens(self):
        configs = _knowledge_agent_configs()
        for name, kac in configs.items():
            model = kac.agent_config.model
            assert "." not in model, f"{name} model has dots: {model}"
            assert model.startswith("claude-"), f"{name} model invalid: {model}"


# ── Registry Tests ───────────────────────────────────────────


class TestKnowledgeWorkRegistry:
    def test_init(self):
        registry = KnowledgeWorkRegistry()
        assert registry.skill_count >= 160  # 119 KW + 45 FSI
        assert registry.category_count == 22  # 17 KW + 5 FSI

    def test_resolve_data_skill(self):
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve("data-visualization")
        assert agent.name == "data-analyst"

    def test_resolve_sales_skill(self):
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve("competitive-intelligence")
        assert agent.name == "sales-agent"

    def test_resolve_legal_skill(self):
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve("review-contract")
        assert agent.name == "compliance-reviewer"

    def test_resolve_engineering_skill(self):
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve("incident-response")
        assert agent.name == "engineering-agent"

    def test_resolve_finance_skill(self):
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve("financial-statements")
        assert agent.name == "finance-agent"

    def test_resolve_marketing_skill(self):
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve("content-creation")
        assert agent.name == "marketing-agent"

    def test_resolve_partner_built_skill(self):
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve("slack-messaging")
        assert agent.name == "partner-built-agent"

    def test_resolve_unknown_skill(self):
        registry = KnowledgeWorkRegistry()
        try:
            registry.resolve("nonexistent-skill")
            raise AssertionError("Should raise KeyError")
        except KeyError:
            pass

    def test_resolve_category(self):
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve_category(PluginCategory.DATA)
        assert agent.name == "data-analyst"

    def test_skills_for_category_sorted(self):
        registry = KnowledgeWorkRegistry()
        skills = registry.skills_for_category(PluginCategory.DATA)
        assert len(skills) >= 10
        installs = [s.installs for s in skills]
        assert installs == sorted(installs, reverse=True)

    def test_all_agent_configs(self):
        registry = KnowledgeWorkRegistry()
        configs = registry.all_agent_configs()
        assert len(configs) == 17
        for name, config in configs.items():
            assert config.name == name

    def test_all_managed_configs(self):
        registry = KnowledgeWorkRegistry()
        managed = registry.all_managed_configs()
        assert len(managed) == 17
        # compliance-reviewer and finance-agent should be read-only
        for ro_name in ("compliance-reviewer", "finance-agent"):
            ro = managed[ro_name]
            write_configs = [c for c in ro.toolset.configs if c.name == "write"]
            assert len(write_configs) == 1
            assert write_configs[0].enabled is False


# ── Pipeline Tests ───────────────────────────────────────────


class TestKnowledgePipelines:
    def test_three_pipelines_available(self):
        pipelines = _build_knowledge_pipelines()
        assert len(pipelines) == 3

    def test_pipeline_names(self):
        pipelines = _build_knowledge_pipelines()
        expected = {"research-to-report", "data-to-insight", "compliance-review"}
        assert set(pipelines.keys()) == expected

    def test_research_to_report_steps(self):
        pipeline = research_to_report_pipeline()
        assert pipeline.name == "research-to-report"
        agents = [s.agent_name for s in pipeline.steps]
        assert "harmlessness-screen" in agents
        assert "enterprise-search-agent" in agents
        assert "compliance-reviewer" in agents

    def test_data_to_insight_steps(self):
        pipeline = data_to_insight_pipeline()
        assert pipeline.name == "data-to-insight"
        agents = [s.agent_name for s in pipeline.steps]
        assert "harmlessness-screen" in agents
        assert "data-analyst" in agents
        assert "finance-agent" in agents

    def test_compliance_review_steps(self):
        pipeline = compliance_review_pipeline()
        assert pipeline.name == "compliance-review"
        agents = [s.agent_name for s in pipeline.steps]
        assert "harmlessness-screen" in agents
        assert "compliance-reviewer" in agents
        assert "security-auditor" in agents

    def test_all_pipelines_start_with_harmlessness_screen(self):
        pipelines = _build_knowledge_pipelines()
        for name, pipeline in pipelines.items():
            first_step = min(pipeline.steps, key=lambda s: s.order)
            assert first_step.agent_name == "harmlessness-screen", (
                f"{name} doesn't start with harmlessness-screen"
            )

    def test_pipeline_gates_block_on_block(self):
        pipelines = _build_knowledge_pipelines()
        for name, pipeline in pipelines.items():
            assert pipeline.gate.block_on_verdict.value == "BLOCK", (
                f"{name} gate doesn't block on BLOCK"
            )

    def test_pipeline_parallel_steps(self):
        pipeline = research_to_report_pipeline()
        order_counts: dict[int, int] = {}
        for step in pipeline.steps:
            order_counts[step.order] = order_counts.get(step.order, 0) + 1
        assert order_counts.get(2, 0) >= 2


# ── Server-Managed Settings Tests ────────────────────────────


class TestManagedSettings:
    def test_default_settings(self):
        settings = knowledge_work_managed_settings()
        assert "permissions" in settings
        deny = settings["permissions"]["deny"]
        assert "Read(./.env)" in deny
        assert settings["allowManagedPermissionRulesOnly"] is True

    def test_custom_deny_patterns(self):
        settings = knowledge_work_managed_settings(deny_patterns=["Bash(rm *)"])
        assert "Bash(rm *)" in settings["permissions"]["deny"]

    def test_audit_hook(self):
        settings = knowledge_work_managed_settings(
            audit_hook="/usr/local/bin/audit.sh"
        )
        hooks = settings["hooks"]["PostToolUse"]
        assert hooks[0]["matcher"] == "Edit|Write"
        assert hooks[0]["hooks"][0]["command"] == "/usr/local/bin/audit.sh"

    def test_no_hook_by_default(self):
        settings = knowledge_work_managed_settings()
        assert "hooks" not in settings


# ── Environment Factory Tests ────────────────────────────────


class TestEnvironmentFactory:
    def test_default_environment(self):
        env = knowledge_work_environment()
        assert env.name == "knowledge-work"
        assert env.networking.mode == NetworkingMode.UNRESTRICTED

    def test_restricted_environment(self):
        env = knowledge_work_environment(
            restricted=True, allowed_hosts=["api.example.com"]
        )
        assert env.networking.mode == NetworkingMode.LIMITED

    def test_serialization(self):
        env = knowledge_work_environment()
        params = env.to_create_params()
        assert params["name"] == "knowledge-work"
        assert params["config"]["type"] == "cloud"


# ── Convenience Function Tests ───────────────────────────────


class TestConvenienceFunctions:
    def test_resolve_skill(self):
        agent = resolve_skill("data-visualization")
        assert agent.name == "data-analyst"

    def test_list_all_skills(self):
        skills = list_skills()
        assert len(skills) >= 100
        installs = [s.installs for s in skills]
        assert installs == sorted(installs, reverse=True)

    def test_list_skills_by_category(self):
        skills = list_skills(PluginCategory.LEGAL)
        assert len(skills) >= 9
        for s in skills:
            assert s.category == PluginCategory.LEGAL

    def test_total_installs(self):
        total = total_installs()
        assert total > 50000


# ── Financial Services Plugin Tests ──────────────────────────


class TestFinancialServicesPlugins:
    def test_fsi_categories_exist(self):
        assert PluginCategory.FSI_FINANCIAL_ANALYSIS.value == "fsi-financial-analysis"
        assert PluginCategory.FSI_INVESTMENT_BANKING.value == "fsi-investment-banking"
        assert PluginCategory.FSI_EQUITY_RESEARCH.value == "fsi-equity-research"
        assert PluginCategory.FSI_PRIVATE_EQUITY.value == "fsi-private-equity"
        assert PluginCategory.FSI_WEALTH_MANAGEMENT.value == "fsi-wealth-management"

    def test_fsi_skills_count(self):
        fsi_skills = [m for m in SKILL_CATALOG.values()
                      if m.category.value.startswith("fsi-")]
        assert len(fsi_skills) == 45

    def test_fsi_core_skills(self):
        assert "dcf-model" in SKILL_CATALOG
        assert "comps-analysis" in SKILL_CATALOG
        assert "lbo-model" in SKILL_CATALOG
        assert "3-statement-model" in SKILL_CATALOG

    def test_fsi_equity_research_skills(self):
        assert "earnings-analysis" in SKILL_CATALOG
        assert "initiating-coverage" in SKILL_CATALOG

    def test_fsi_private_equity_skills(self):
        assert "ic-memo" in SKILL_CATALOG
        assert "deal-sourcing" in SKILL_CATALOG
        assert "returns-analysis" in SKILL_CATALOG

    def test_fsi_wealth_management_skills(self):
        assert "tax-loss-harvesting" in SKILL_CATALOG
        assert "portfolio-rebalance" in SKILL_CATALOG

    def test_fsi_skills_route_to_finance_agent(self):
        registry = KnowledgeWorkRegistry()
        for skill_name in ("dcf-model", "earnings-analysis", "ic-memo",
                           "tax-loss-harvesting", "pitch-deck"):
            agent = registry.resolve(skill_name)
            assert agent.name == "finance-agent", (
                f"{skill_name} routes to {agent.name} instead of finance-agent"
            )
