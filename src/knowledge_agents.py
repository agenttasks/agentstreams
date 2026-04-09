"""Knowledge Work Agents — plugin-to-agent bridge layer.

Maps skills from two Anthropic plugin repos to domain agents:
- anthropics/knowledge-work-plugins: 119 skills across 11 upstream + 6 extended plugins (17 total categories)
- anthropics/financial-services-plugins: 45 skills across 5 plugins

Source of truth: vendors/knowledge-work-plugins/ and
vendors/financial-services-plugins/ (cloned from GitHub).
Every skill in SKILL_CATALOG corresponds to a SKILL.md file.

Plugin categories (PluginCategory enum values mirror directory names exactly):
    BIO_RESEARCH              → bio-research-agent       (6 skills)
    COWORK_PLUGIN_MANAGEMENT  → cowork-plugin-agent      (2 skills)
    CUSTOMER_SUPPORT          → customer-support-agent   (5 skills)
    DATA                      → data-analyst             (10 skills)
    DESIGN                    → design-agent             (7 skills)
    ENGINEERING               → engineering-agent        (10 skills)
    ENTERPRISE_SEARCH         → enterprise-search-agent  (5 skills)
    FINANCE                   → finance-agent            (8 skills, read-only)
    HUMAN_RESOURCES           → hr-agent                 (9 skills)
    LEGAL                     → compliance-reviewer      (9 skills, read-only)
    MARKETING                 → marketing-agent          (8 skills)
    OPERATIONS                → operations-agent         (9 skills)
    PARTNER_BUILT             → partner-built-agent      (11 unique skills:
                                                          apollo, brand-voice,
                                                          common-room, slack;
                                                          2 cross-plugin dupes
                                                          yielded to first-party,
                                                          1 intra-partner dedup)
    PDF_VIEWER                → pdf-viewer-agent         (1 skill)
    PRODUCT_MANAGEMENT        → product-management-agent (7 skills; competitive-brief
                                                          yielded to marketing)
    PRODUCTIVITY              → productivity-agent       (3 skills; start yielded
                                                          to bio-research)
    SALES                     → sales-agent              (9 skills)

Skills that appear in multiple plugins use the first-party plugin as primary
(e.g., account-research → SALES, not PARTNER_BUILT).

All agents use claude-opus-4-6 model.
Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from src.agent_tasks import AgentConfig
from src.managed_agents import (
    AgentToolset,
    EnvironmentConfig,
    ManagedAgentConfig,
    NetworkConfig,
    NetworkingMode,
    Packages,
    ToolConfig,
)

# NOTE: We cannot import from src.orchestrator at module level because
# orchestrator.py also imports from this module. Pipeline types are
# imported lazily inside functions that need them.

# ── Plugin Categories ────────────────────────────────────────


class PluginCategory(Enum):
    """Plugin directories from anthropics/knowledge-work-plugins and
    anthropics/financial-services-plugins.

    Enum names and values mirror the actual directory names in each repo.
    Knowledge-work plugins use the directory name as-is.
    Financial-services plugins are prefixed with 'fsi-' to avoid collisions.
    """

    # ── knowledge-work-plugins ────────────────────────────────
    BIO_RESEARCH = "bio-research"
    COWORK_PLUGIN_MANAGEMENT = "cowork-plugin-management"
    CUSTOMER_SUPPORT = "customer-support"
    DATA = "data"
    DESIGN = "design"
    ENGINEERING = "engineering"
    ENTERPRISE_SEARCH = "enterprise-search"
    FINANCE = "finance"
    HUMAN_RESOURCES = "human-resources"
    LEGAL = "legal"
    MARKETING = "marketing"
    OPERATIONS = "operations"
    PARTNER_BUILT = "partner-built"
    PDF_VIEWER = "pdf-viewer"
    PRODUCT_MANAGEMENT = "product-management"
    PRODUCTIVITY = "productivity"
    SALES = "sales"

    # ── financial-services-plugins ────────────────────────────
    FSI_FINANCIAL_ANALYSIS = "fsi-financial-analysis"
    FSI_INVESTMENT_BANKING = "fsi-investment-banking"
    FSI_EQUITY_RESEARCH = "fsi-equity-research"
    FSI_PRIVATE_EQUITY = "fsi-private-equity"
    FSI_WEALTH_MANAGEMENT = "fsi-wealth-management"


# Agent name that handles each plugin category.
# COWORK_PLUGIN_MANAGEMENT and PARTNER_BUILT each get their own dedicated agent.
CATEGORY_AGENTS: dict[PluginCategory, str] = {
    PluginCategory.BIO_RESEARCH: "bio-research-agent",
    PluginCategory.COWORK_PLUGIN_MANAGEMENT: "cowork-plugin-agent",
    PluginCategory.CUSTOMER_SUPPORT: "customer-support-agent",
    PluginCategory.DATA: "data-analyst",
    PluginCategory.DESIGN: "design-agent",
    PluginCategory.ENGINEERING: "engineering-agent",
    PluginCategory.ENTERPRISE_SEARCH: "enterprise-search-agent",
    PluginCategory.FINANCE: "finance-agent",
    PluginCategory.HUMAN_RESOURCES: "hr-agent",
    PluginCategory.LEGAL: "compliance-reviewer",
    PluginCategory.MARKETING: "marketing-agent",
    PluginCategory.OPERATIONS: "operations-agent",
    PluginCategory.PARTNER_BUILT: "partner-built-agent",
    PluginCategory.PDF_VIEWER: "pdf-viewer-agent",
    PluginCategory.PRODUCT_MANAGEMENT: "product-management-agent",
    PluginCategory.PRODUCTIVITY: "productivity-agent",
    PluginCategory.SALES: "sales-agent",
    # financial-services-plugins
    PluginCategory.FSI_FINANCIAL_ANALYSIS: "finance-agent",
    PluginCategory.FSI_INVESTMENT_BANKING: "finance-agent",
    PluginCategory.FSI_EQUITY_RESEARCH: "finance-agent",
    PluginCategory.FSI_PRIVATE_EQUITY: "finance-agent",
    PluginCategory.FSI_WEALTH_MANAGEMENT: "finance-agent",
}


# ── Skill Metadata ───────────────────────────────────────────


@dataclass(frozen=True)
class SkillMeta:
    """Metadata for a single skill from knowledge-work-plugins."""

    name: str
    category: PluginCategory
    installs: int = 0


# ── Full Skill Catalog ───────────────────────────────────────
# Ground truth: vendors/knowledge-work-plugins/<plugin>/skills/<skill>/SKILL.md

SKILL_CATALOG: dict[str, SkillMeta] = {}


def _register(name: str, category: PluginCategory, installs: int = 0) -> None:
    """Register a skill. First registration wins (for cross-plugin skills)."""
    if name not in SKILL_CATALOG:
        SKILL_CATALOG[name] = SkillMeta(name=name, category=category, installs=installs)


# ── Skill Registration ───────────────────────────────────────
# Only skills with a SKILL.md in vendors/knowledge-work-plugins/ are listed.
# First registration wins: first-party plugins take priority over partner-built
# for skills that appear in multiple plugin directories.

# bio-research (6 skills)
for _n, _i in [
    ("instrument-data-to-allotrope", 233),
    ("nextflow-development", 241),
    ("scientific-problem-selection", 258),
    ("scvi-tools", 231),
    ("single-cell-rna-qc", 244),
    ("start", 620),
]:
    _register(_n, PluginCategory.BIO_RESEARCH, _i)

# cowork-plugin-management (2 skills)
for _n, _i in [
    ("cowork-plugin-customizer", 653),
    ("create-cowork-plugin", 648),
]:
    _register(_n, PluginCategory.COWORK_PLUGIN_MANAGEMENT, _i)

# customer-support (5 skills)
for _n, _i in [
    ("customer-escalation", 472),
    ("customer-research", 719),
    ("draft-response", 483),
    ("kb-article", 491),
    ("ticket-triage", 664),
]:
    _register(_n, PluginCategory.CUSTOMER_SUPPORT, _i)

# data (10 skills)
for _n, _i in [
    ("analyze", 690),
    ("build-dashboard", 884),
    ("create-viz", 653),
    ("data-context-extractor", 710),
    ("data-visualization", 3800),
    ("explore-data", 697),
    ("sql-queries", 1100),
    ("statistical-analysis", 1100),
    ("validate-data", 568),
    ("write-query", 520),
]:
    _register(_n, PluginCategory.DATA, _i)

# design (7 skills)
for _n, _i in [
    ("accessibility-review", 0),
    ("design-critique", 796),
    ("design-handoff", 643),
    ("design-system", 647),
    ("research-synthesis", 615),
    ("user-research", 820),
    ("ux-copy", 663),
]:
    _register(_n, PluginCategory.DESIGN, _i)

# engineering (10 skills)
for _n, _i in [
    ("architecture", 745),
    ("code-review", 1400),
    ("debug", 672),
    ("deploy-checklist", 662),
    ("documentation", 1100),
    ("incident-response", 764),
    ("standup", 621),
    ("system-design", 1200),
    ("tech-debt", 866),
    ("testing-strategy", 855),
]:
    _register(_n, PluginCategory.ENGINEERING, _i)

# enterprise-search (5 skills)
for _n, _i in [
    ("digest", 489),
    ("knowledge-synthesis", 1200),
    ("search", 633),
    ("search-strategy", 848),
    ("source-management", 778),
]:
    _register(_n, PluginCategory.ENTERPRISE_SEARCH, _i)

# finance (8 skills)
for _n, _i in [
    ("audit-support", 690),
    ("close-management", 648),
    ("financial-statements", 1000),
    ("journal-entry", 474),
    ("journal-entry-prep", 666),
    ("reconciliation", 682),
    ("sox-testing", 466),
    ("variance-analysis", 693),
]:
    _register(_n, PluginCategory.FINANCE, _i)

# human-resources (9 skills)
for _n, _i in [
    ("comp-analysis", 507),
    ("draft-offer", 485),
    ("interview-prep", 663),
    ("onboarding", 504),
    ("org-planning", 0),
    ("people-report", 479),
    ("performance-review", 545),
    ("policy-lookup", 509),
    ("recruiting-pipeline", 598),
]:
    _register(_n, PluginCategory.HUMAN_RESOURCES, _i)

# legal (9 skills)
for _n, _i in [
    ("brief", 500),
    ("compliance-check", 526),
    ("legal-response", 565),
    ("legal-risk-assessment", 1100),
    ("meeting-briefing", 689),
    ("review-contract", 617),
    ("signature-request", 475),
    ("triage-nda", 477),
    ("vendor-check", 486),
]:
    _register(_n, PluginCategory.LEGAL, _i)

# marketing (8 skills)
# competitive-brief is also in product-management; marketing registers first.
for _n, _i in [
    ("brand-review", 537),
    ("campaign-plan", 558),
    ("competitive-brief", 574),
    ("content-creation", 1500),
    ("draft-content", 503),
    ("email-sequence", 491),
    ("performance-report", 523),
    ("seo-audit", 569),
]:
    _register(_n, PluginCategory.MARKETING, _i)

# operations (9 skills)
for _n, _i in [
    ("capacity-plan", 497),
    ("change-request", 488),
    ("compliance-tracking", 610),
    ("process-doc", 517),
    ("process-optimization", 653),
    ("risk-assessment", 672),
    ("runbook", 480),
    ("status-report", 509),
    ("vendor-review", 480),
]:
    _register(_n, PluginCategory.OPERATIONS, _i)

# partner-built — apollo, brand-voice, common-room, slack (13 unique slugs, 11 after dedup).
# account-research, call-prep already registered under first-party sales
# (common-room variants silently skipped by _register).
# prospect appears in both apollo and common-room; apollo registers first.
# account-research, call-prep, prospect already registered under first-party
# sales/apollo; _register skips duplicates so partner-built entries for those
# are silently ignored, which is the correct first-party-wins behaviour.
for _n, _i in [
    # apollo
    ("enrich-lead", 607),
    ("prospect", 581),
    ("sequence-load", 559),
    # brand-voice
    ("brand-voice-enforcement", 684),
    ("discover-brand", 635),
    ("guideline-generation", 608),
    # common-room (account-research and call-prep already registered)
    ("compose-outreach", 600),
    ("contact-research", 597),
    ("weekly-prep-brief", 569),
    # slack
    ("slack-messaging", 702),
    ("slack-search", 607),
]:
    _register(_n, PluginCategory.PARTNER_BUILT, _i)

# pdf-viewer (1 skill)
_register("view-pdf", PluginCategory.PDF_VIEWER, 365)

# product-management (8 raw, 7 after dedup; competitive-brief yields to marketing)
# competitive-brief already registered under marketing; skipped here.
for _n, _i in [
    ("metrics-review", 511),
    ("product-brainstorming", 622),
    ("roadmap-update", 543),
    ("sprint-planning", 520),
    ("stakeholder-update", 510),
    ("synthesize-research", 568),
    ("write-spec", 621),
    ("competitive-brief", 574),  # already taken by marketing; no-op
]:
    _register(_n, PluginCategory.PRODUCT_MANAGEMENT, _i)

# productivity (4 raw, 3 after dedup; start yields to bio-research)
# start already registered under bio-research; skipped here.
for _n, _i in [
    ("memory-management", 1400),
    ("task-management", 1700),
    ("update", 635),
    ("start", 620),  # already taken by bio-research; no-op
]:
    _register(_n, PluginCategory.PRODUCTIVITY, _i)

# sales (9 skills)
# account-research and call-prep register here; partner-built/common-room
# versions will be silently skipped when partner-built registers later.
for _n, _i in [
    ("account-research", 734),
    ("call-prep", 686),
    ("call-summary", 522),
    ("competitive-intelligence", 1300),
    ("create-an-asset", 659),
    ("daily-briefing", 842),
    ("draft-outreach", 796),
    ("forecast", 503),
    ("pipeline-review", 492),
]:
    _register(_n, PluginCategory.SALES, _i)


# ── financial-services-plugins ───────────────────────────────
# Source: vendors/financial-services-plugins/
# 5 plugins, 45 skills, 11 MCP integrations

# financial-analysis (11 skills) — core plugin, all MCP connectors
for _n, _i in [
    ("3-statement-model", 261),
    ("audit-xls", 247),
    ("clean-data-xls", 236),
    ("competitive-analysis", 327),
    ("comps-analysis", 254),
    ("dcf-model", 360),
    ("deck-refresh", 211),
    ("ib-check-deck", 219),
    ("lbo-model", 271),
    ("ppt-template-creator", 392),
    ("skill-creator", 250),
]:
    _register(_n, PluginCategory.FSI_FINANCIAL_ANALYSIS, _i)

# investment-banking (9 skills)
for _n, _i in [
    ("buyer-list", 0),
    ("cim-builder", 0),
    ("datapack-builder", 269),
    ("deal-tracker", 0),
    ("merger-model", 0),
    ("pitch-deck", 290),
    ("process-letter", 0),
    ("strip-profile", 0),
    ("teaser", 0),
]:
    _register(_n, PluginCategory.FSI_INVESTMENT_BANKING, _i)

# equity-research (9 skills)
for _n, _i in [
    ("catalyst-calendar", 0),
    ("earnings-analysis", 528),
    ("earnings-preview", 0),
    ("idea-generation", 0),
    ("initiating-coverage", 310),
    ("model-update", 0),
    ("morning-note", 0),
    ("sector-overview", 0),
    ("thesis-tracker", 0),
]:
    _register(_n, PluginCategory.FSI_EQUITY_RESEARCH, _i)

# private-equity (10 skills)
for _n, _i in [
    ("ai-readiness", 0),
    ("dd-checklist", 0),
    ("dd-meeting-prep", 0),
    ("deal-screening", 0),
    ("deal-sourcing", 0),
    ("ic-memo", 0),
    ("portfolio-monitoring", 0),
    ("returns-analysis", 0),
    ("unit-economics", 0),
    ("value-creation-plan", 0),
]:
    _register(_n, PluginCategory.FSI_PRIVATE_EQUITY, _i)

# wealth-management (6 skills)
for _n, _i in [
    ("client-report", 0),
    ("client-review", 0),
    ("financial-plan", 0),
    ("investment-proposal", 0),
    ("portfolio-rebalance", 0),
    ("tax-loss-harvesting", 0),
]:
    _register(_n, PluginCategory.FSI_WEALTH_MANAGEMENT, _i)


# ── Knowledge Agent Configs ──────────────────────────────────


@dataclass
class KnowledgeAgentConfig:
    """Extended agent config with skill routing metadata.

    Wraps AgentConfig with the skills this agent handles and the
    plugin categories it serves.
    """

    agent_config: AgentConfig
    categories: list[PluginCategory] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.agent_config.name

    @property
    def model(self) -> str:
        return self.agent_config.model

    def to_managed(self, *, disable_write: bool = False) -> ManagedAgentConfig:
        """Convert to ManagedAgentConfig for cloud execution."""
        tool_configs = []
        if disable_write:
            tool_configs = [
                ToolConfig(name="write", enabled=False),
                ToolConfig(name="edit", enabled=False),
            ]
        return ManagedAgentConfig(
            name=self.agent_config.name,
            model=self.agent_config.model,
            system=self.agent_config.system_prompt,
            toolset=AgentToolset(configs=tool_configs),
            metadata={
                "categories": ",".join(c.value for c in self.categories),
                "skill_count": str(len(self.skills)),
            },
        )


def _knowledge_agent_configs() -> dict[str, KnowledgeAgentConfig]:
    """Build the roster of knowledge-work agent configurations.

    All agents use claude-opus-4-6 model.
    """
    # Collect skills per agent
    agent_skills: dict[str, list[str]] = {}
    agent_cats: dict[str, set[PluginCategory]] = {}
    for skill_name, meta in SKILL_CATALOG.items():
        agent_name = CATEGORY_AGENTS[meta.category]
        agent_skills.setdefault(agent_name, []).append(skill_name)
        agent_cats.setdefault(agent_name, set()).add(meta.category)

    def _make(
        name: str,
        prompt: str,
        *,
        max_turns: int = 20,
        temperature: float = 0.0,
    ) -> KnowledgeAgentConfig:
        return KnowledgeAgentConfig(
            agent_config=AgentConfig(
                name=name,
                model="claude-opus-4-6",
                system_prompt=prompt,
                max_turns=max_turns,
                temperature=temperature,
            ),
            categories=sorted(agent_cats.get(name, set()), key=lambda c: c.value),
            skills=sorted(agent_skills.get(name, [])),
        )

    return {
        "bio-research-agent": _make(
            "bio-research-agent",
            "You are a bio-research agent. Support genomics pipelines, "
            "single-cell RNA analysis, instrument data conversion to "
            "Allotrope format, and nextflow workflow development. "
            "Always cite primary literature. Never fabricate citations.",
        ),
        "cowork-plugin-agent": _make(
            "cowork-plugin-agent",
            "You are a cowork plugin management agent. Help create and "
            "customize Claude for Work plugins — scaffold plugin "
            "components, configure schemas, and validate against the "
            "cowork plugin specification.",
        ),
        "customer-support-agent": _make(
            "customer-support-agent",
            "You are a customer support agent. Triage tickets, draft "
            "responses, package escalations, research customer context, "
            "and create knowledge base articles from resolved issues.",
        ),
        "data-analyst": _make(
            "data-analyst",
            "You are a data analysis agent. Query, visualize, and "
            "interpret datasets — write SQL, run statistical analysis, "
            "build dashboards, and validate results before sharing. "
            "Never expose raw PII — aggregate or anonymize. "
            "Prefer parameterized queries for all SQL.",
        ),
        "design-agent": _make(
            "design-agent",
            "You are a design agent. Conduct user research, review "
            "designs for accessibility, manage design systems, write "
            "UX copy, and prepare developer handoffs. Always apply "
            "WCAG 2.1 AA standards and existing design conventions.",
        ),
        "engineering-agent": _make(
            "engineering-agent",
            "You are an engineering agent. Review architecture and code, "
            "debug issues, manage deployments, handle incidents, and "
            "document systems. Always include rollback steps for "
            "deployment actions. Never run destructive commands without "
            "explicit user confirmation.",
        ),
        "enterprise-search-agent": _make(
            "enterprise-search-agent",
            "You are an enterprise search agent. Find information across "
            "email, chat, docs, and wikis. Synthesize findings into "
            "structured digests and always provide source provenance.",
        ),
        "finance-agent": _make(
            "finance-agent",
            "You are a financial operations agent. Prep journal entries, "
            "reconcile accounts, generate financial statements, analyze "
            "variances, manage period close, and support SOX audits. "
            "Read-only — never modify financial records directly. "
            "Always state assumptions and cite source data explicitly.",
            max_turns=15,
        ),
        "hr-agent": _make(
            "hr-agent",
            "You are an HR agent. Manage recruiting pipelines, prepare "
            "interview guides, run compensation benchmarks, support "
            "onboarding, plan org structure, and generate people reports. "
            "Anonymize sensitive employee data in all outputs.",
        ),
        "compliance-reviewer": _make(
            "compliance-reviewer",
            "You are a legal compliance reviewer. Review contracts, "
            "triage NDAs, check regulatory compliance, assess legal "
            "risk, and draft templated legal responses. "
            "Read-only — never modify documents under review. "
            "Never provide legal advice — frame all outputs as analysis. "
            "End every review with verdict: PASS, NEEDS_REMEDIATION, "
            "or BLOCK.",
            max_turns=15,
        ),
        "marketing-agent": _make(
            "marketing-agent",
            "You are a marketing agent. Draft content, plan campaigns, "
            "enforce brand voice, produce competitive briefs, and report "
            "on channel performance. Match existing brand conventions "
            "discovered from prior content — never invent guidelines.",
        ),
        "operations-agent": _make(
            "operations-agent",
            "You are an operations agent. Optimize processes, track "
            "compliance, assess operational risks, plan capacity, "
            "maintain runbooks, and review vendors. Always include "
            "rollback procedures for every process change.",
        ),
        "partner-built-agent": _make(
            "partner-built-agent",
            "You are a partner integrations agent. Handle Apollo "
            "prospecting and lead enrichment, brand-voice enforcement "
            "via the Brand Voice plugin, Common Room account and "
            "contact intelligence, and Slack search and messaging. "
            "Honour the data-use constraints of each partner platform.",
        ),
        "pdf-viewer-agent": _make(
            "pdf-viewer-agent",
            "You are a PDF analysis agent. Extract text, tables, and "
            "structured data from PDF documents. Preserve document "
            "structure in outputs and flag any sections that could not "
            "be parsed reliably.",
        ),
        "product-management-agent": _make(
            "product-management-agent",
            "You are a product management agent. Write specs, plan "
            "roadmaps, synthesize user research, update stakeholders, "
            "and track the competitive landscape.",
        ),
        "productivity-agent": _make(
            "productivity-agent",
            "You are a productivity agent. Manage tasks, maintain "
            "persistent memory across sessions, run daily workflows, "
            "and surface the right context at the right time.",
        ),
        "sales-agent": _make(
            "sales-agent",
            "You are a sales intelligence agent. Research accounts, "
            "prep for calls, summarize meetings, review pipeline health, "
            "draft outreach, build competitive battlecards, and forecast. "
            "Include source provenance for all prospect and market claims.",
        ),
    }


# ── Knowledge Work Registry ──────────────────────────────────


class KnowledgeWorkRegistry:
    """Resolves skill names to agent configurations.

    Maps each skill from anthropics/knowledge-work-plugins to the
    appropriate domain agent, supporting both local and cloud execution.

    Usage:
        registry = KnowledgeWorkRegistry()
        agent = registry.resolve("data-visualization")
        assert agent.name == "data-analyst"
    """

    def __init__(self) -> None:
        self._configs = _knowledge_agent_configs()

    @property
    def agents(self) -> dict[str, KnowledgeAgentConfig]:
        """All registered knowledge-work agents."""
        return dict(self._configs)

    @property
    def skill_count(self) -> int:
        """Total number of registered skills."""
        return len(SKILL_CATALOG)

    @property
    def category_count(self) -> int:
        """Number of plugin categories."""
        return len(PluginCategory)

    def resolve(self, skill_name: str) -> KnowledgeAgentConfig:
        """Resolve a skill name to its handling agent config.

        Raises KeyError if the skill is not in the catalog.
        """
        meta = SKILL_CATALOG[skill_name]
        agent_name = CATEGORY_AGENTS[meta.category]
        return self._configs[agent_name]

    def resolve_category(self, category: PluginCategory) -> KnowledgeAgentConfig:
        """Get the agent config for a category."""
        agent_name = CATEGORY_AGENTS[category]
        return self._configs[agent_name]

    def skills_for_category(self, category: PluginCategory) -> list[SkillMeta]:
        """List all skills in a category, sorted by installs descending."""
        return sorted(
            [m for m in SKILL_CATALOG.values() if m.category == category],
            key=lambda m: m.installs,
            reverse=True,
        )

    def skill_meta(self, skill_name: str) -> SkillMeta:
        """Get metadata for a skill."""
        return SKILL_CATALOG[skill_name]

    def all_agent_configs(self) -> dict[str, AgentConfig]:
        """Return AgentConfigs suitable for use with the Orchestrator."""
        return {name: kac.agent_config for name, kac in self._configs.items()}

    def all_managed_configs(self) -> dict[str, ManagedAgentConfig]:
        """Return ManagedAgentConfigs suitable for cloud execution."""
        read_only = {"compliance-reviewer", "finance-agent"}
        return {
            name: kac.to_managed(disable_write=name in read_only)
            for name, kac in self._configs.items()
        }


# ── Knowledge Work Pipelines ─────────────────────────────────
# Imports from src.orchestrator are done lazily inside each function
# to break the circular dependency.


def research_to_report_pipeline() -> Any:
    """Research -> synthesis -> content -> compliance pipeline."""
    from src.orchestrator import Pipeline, PipelineGate, PipelineStep, Verdict

    return Pipeline(
        name="research-to-report",
        description="End-to-end research synthesis into a structured report.",
        steps=[
            PipelineStep(order=0, agent_name="harmlessness-screen"),
            PipelineStep(order=1, agent_name="enterprise-search-agent"),
            PipelineStep(
                order=2, agent_name="marketing-agent", input_from="enterprise-search-agent"
            ),
            PipelineStep(
                order=2, agent_name="compliance-reviewer", input_from="enterprise-search-agent"
            ),
            PipelineStep(order=3, agent_name="security-auditor", condition="sensitive_data"),
        ],
        gate=PipelineGate(
            block_on_verdict=Verdict.BLOCK,
            human_review_on_critical=True,
        ),
    )


def data_to_insight_pipeline() -> Any:
    """Data analysis -> business context -> content formatting pipeline."""
    from src.orchestrator import Pipeline, PipelineGate, PipelineStep, Verdict

    return Pipeline(
        name="data-to-insight",
        description="Transform raw data into actionable business insights.",
        steps=[
            PipelineStep(order=0, agent_name="harmlessness-screen"),
            PipelineStep(order=1, agent_name="data-analyst"),
            PipelineStep(order=2, agent_name="finance-agent", input_from="data-analyst"),
            PipelineStep(order=2, agent_name="compliance-reviewer", input_from="data-analyst"),
            PipelineStep(order=3, agent_name="marketing-agent", input_from="finance-agent"),
        ],
        gate=PipelineGate(
            block_on_verdict=Verdict.BLOCK,
            human_review_on_critical=True,
        ),
    )


def compliance_review_pipeline() -> Any:
    """Compliance review -> security + research -> report pipeline."""
    from src.orchestrator import Pipeline, PipelineGate, PipelineStep, Verdict

    return Pipeline(
        name="compliance-review",
        description="Full compliance review with cross-referencing and reporting.",
        steps=[
            PipelineStep(order=0, agent_name="harmlessness-screen"),
            PipelineStep(order=1, agent_name="compliance-reviewer"),
            PipelineStep(order=2, agent_name="security-auditor", input_from="compliance-reviewer"),
            PipelineStep(
                order=2, agent_name="enterprise-search-agent", input_from="compliance-reviewer"
            ),
            PipelineStep(order=3, agent_name="marketing-agent"),
        ],
        gate=PipelineGate(
            block_on_verdict=Verdict.BLOCK,
            human_review_on_critical=True,
            human_review_on_suspicion=30,
        ),
    )


def _build_knowledge_pipelines() -> dict[str, Any]:
    """Build the knowledge pipeline dict. Called from orchestrator."""
    return {
        "research-to-report": research_to_report_pipeline(),
        "data-to-insight": data_to_insight_pipeline(),
        "compliance-review": compliance_review_pipeline(),
    }


# Populated by orchestrator's _register_knowledge_pipelines()
KNOWLEDGE_PIPELINES: dict[str, Any] = {}


# ── Server-Managed Settings Helpers ──────────────────────────


def knowledge_work_managed_settings(
    *,
    deny_patterns: list[str] | None = None,
    audit_hook: str = "",
) -> dict[str, Any]:
    """Generate server-managed settings for org-wide deployment.

    Produces a JSON-compatible dict suitable for the Claude Code
    server-managed settings API (managed-agents-2026-04-01 beta).
    """
    base_deny = [
        "Bash(curl *)",
        "Read(./.env)",
        "Read(./.env.*)",
        "Read(./secrets/**)",
    ]
    if deny_patterns:
        base_deny.extend(deny_patterns)

    settings: dict[str, Any] = {
        "permissions": {
            "deny": base_deny,
            "disableBypassPermissionsMode": "disable",
        },
        "allowManagedPermissionRulesOnly": True,
    }

    if audit_hook:
        settings["hooks"] = {
            "PostToolUse": [
                {
                    "matcher": "Edit|Write",
                    "hooks": [{"type": "command", "command": audit_hook}],
                }
            ],
        }

    return settings


# ── Environment Factory ──────────────────────────────────────


def knowledge_work_environment(
    name: str = "knowledge-work",
    *,
    pip_packages: list[str] | None = None,
    npm_packages: list[str] | None = None,
    restricted: bool = False,
    allowed_hosts: list[str] | None = None,
) -> EnvironmentConfig:
    """Create an environment config for knowledge-work agents."""
    networking = NetworkConfig(
        mode=NetworkingMode.LIMITED if restricted else NetworkingMode.UNRESTRICTED,
        allowed_hosts=allowed_hosts or [],
        allow_package_managers=True,
    )
    return EnvironmentConfig(
        name=name,
        packages=Packages(
            pip=pip_packages or ["pandas", "numpy", "matplotlib", "openpyxl"],
            npm=npm_packages or [],
        ),
        networking=networking,
    )


# ── Convenience Functions ────────────────────────────────────


def resolve_skill(skill_name: str) -> KnowledgeAgentConfig:
    """Quick lookup: skill name -> agent config."""
    return KnowledgeWorkRegistry().resolve(skill_name)


def list_skills(category: PluginCategory | None = None) -> list[SkillMeta]:
    """List skills, optionally filtered by category."""
    if category:
        return KnowledgeWorkRegistry().skills_for_category(category)
    return sorted(SKILL_CATALOG.values(), key=lambda m: m.installs, reverse=True)


def total_installs() -> int:
    """Sum of all skill installs across the catalog."""
    return sum(m.installs for m in SKILL_CATALOG.values())
