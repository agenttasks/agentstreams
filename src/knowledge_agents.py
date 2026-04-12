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


def _register(name: str, category: PluginCategory) -> None:
    """Register a skill. First registration wins (for cross-plugin skills)."""
    if name not in SKILL_CATALOG:
        SKILL_CATALOG[name] = SkillMeta(name=name, category=category)


# ── Skill Registration ───────────────────────────────────────
# Only skills with a SKILL.md in vendors/knowledge-work-plugins/ are listed.
# First registration wins: first-party plugins take priority over partner-built
# for skills that appear in multiple plugin directories.

# bio-research (6 skills)
for _n in [
    "instrument-data-to-allotrope",
    "nextflow-development",
    "scientific-problem-selection",
    "scvi-tools",
    "single-cell-rna-qc",
    "start",
]:
    _register(_n, PluginCategory.BIO_RESEARCH)

# cowork-plugin-management (2 skills)
for _n in [
    "cowork-plugin-customizer",
    "create-cowork-plugin",
]:
    _register(_n, PluginCategory.COWORK_PLUGIN_MANAGEMENT)

# customer-support (5 skills)
for _n in [
    "customer-escalation",
    "customer-research",
    "draft-response",
    "kb-article",
    "ticket-triage",
]:
    _register(_n, PluginCategory.CUSTOMER_SUPPORT)

# data (10 skills from knowledge-work-plugins)
for _n in [
    "analyze",
    "build-dashboard",
    "create-viz",
    "data-context-extractor",
    "data-visualization",
    "explore-data",
    "sql-queries",
    "statistical-analysis",
    "validate-data",
    "write-query",
]:
    _register(_n, PluginCategory.DATA)

# neon-specific data skills (3 local skills in skills/)
for _n in [
    "neon-api",
    "neon-dashboard",
    "neon-team-setup",
]:
    _register(_n, PluginCategory.DATA)

# design (7 skills)
for _n in [
    "accessibility-review",
    "design-critique",
    "design-handoff",
    "design-system",
    "research-synthesis",
    "user-research",
    "ux-copy",
]:
    _register(_n, PluginCategory.DESIGN)

# engineering (10 skills)
for _n in [
    "architecture",
    "code-review",
    "debug",
    "deploy-checklist",
    "documentation",
    "incident-response",
    "standup",
    "system-design",
    "tech-debt",
    "testing-strategy",
]:
    _register(_n, PluginCategory.ENGINEERING)

# enterprise-search (5 skills)
for _n in [
    "digest",
    "knowledge-synthesis",
    "search",
    "search-strategy",
    "source-management",
]:
    _register(_n, PluginCategory.ENTERPRISE_SEARCH)

# finance (8 skills)
for _n in [
    "audit-support",
    "close-management",
    "financial-statements",
    "journal-entry",
    "journal-entry-prep",
    "reconciliation",
    "sox-testing",
    "variance-analysis",
]:
    _register(_n, PluginCategory.FINANCE)

# human-resources (9 skills)
for _n in [
    "comp-analysis",
    "draft-offer",
    "interview-prep",
    "onboarding",
    "org-planning",
    "people-report",
    "performance-review",
    "policy-lookup",
    "recruiting-pipeline",
]:
    _register(_n, PluginCategory.HUMAN_RESOURCES)

# legal (9 skills)
for _n in [
    "brief",
    "compliance-check",
    "legal-response",
    "legal-risk-assessment",
    "meeting-briefing",
    "review-contract",
    "signature-request",
    "triage-nda",
    "vendor-check",
]:
    _register(_n, PluginCategory.LEGAL)

# marketing (8 skills)
# competitive-brief is also in product-management; marketing registers first.
for _n in [
    "brand-review",
    "campaign-plan",
    "competitive-brief",
    "content-creation",
    "draft-content",
    "email-sequence",
    "performance-report",
    "seo-audit",
]:
    _register(_n, PluginCategory.MARKETING)

# operations (9 skills)
for _n in [
    "capacity-plan",
    "change-request",
    "compliance-tracking",
    "process-doc",
    "process-optimization",
    "risk-assessment",
    "runbook",
    "status-report",
    "vendor-review",
]:
    _register(_n, PluginCategory.OPERATIONS)

# partner-built — apollo, brand-voice, common-room, slack (13 unique slugs, 11 after dedup).
# account-research, call-prep already registered under first-party sales
# (common-room variants silently skipped by _register).
# prospect appears in both apollo and common-room; apollo registers first.
for _n in [
    # apollo
    "enrich-lead",
    "prospect",
    "sequence-load",
    # brand-voice
    "brand-voice-enforcement",
    "discover-brand",
    "guideline-generation",
    # common-room (account-research and call-prep already registered)
    "compose-outreach",
    "contact-research",
    "weekly-prep-brief",
    # slack
    "slack-messaging",
    "slack-search",
]:
    _register(_n, PluginCategory.PARTNER_BUILT)

# pdf-viewer (1 skill)
_register("view-pdf", PluginCategory.PDF_VIEWER)

# product-management (8 raw, 7 after dedup; competitive-brief yields to marketing)
# competitive-brief already registered under marketing; skipped here.
for _n in [
    "metrics-review",
    "product-brainstorming",
    "roadmap-update",
    "sprint-planning",
    "stakeholder-update",
    "synthesize-research",
    "write-spec",
    "competitive-brief",  # already taken by marketing; no-op
]:
    _register(_n, PluginCategory.PRODUCT_MANAGEMENT)

# productivity (4 raw, 3 after dedup; start yields to bio-research)
# start already registered under bio-research; skipped here.
for _n in [
    "memory-management",
    "task-management",
    "update",
    "start",  # already taken by bio-research; no-op
]:
    _register(_n, PluginCategory.PRODUCTIVITY)

# sales (9 skills)
# account-research and call-prep register here; partner-built/common-room
# versions will be silently skipped when partner-built registers later.
for _n in [
    "account-research",
    "call-prep",
    "call-summary",
    "competitive-intelligence",
    "create-an-asset",
    "daily-briefing",
    "draft-outreach",
    "forecast",
    "pipeline-review",
]:
    _register(_n, PluginCategory.SALES)


# ── financial-services-plugins ───────────────────────────────
# Source: vendors/financial-services-plugins/
# 5 plugins, 45 skills, 11 MCP integrations

# financial-analysis (11 skills) — core plugin, all MCP connectors
for _n in [
    "3-statement-model",
    "audit-xls",
    "clean-data-xls",
    "competitive-analysis",
    "comps-analysis",
    "dcf-model",
    "deck-refresh",
    "ib-check-deck",
    "lbo-model",
    "ppt-template-creator",
    "skill-creator",
]:
    _register(_n, PluginCategory.FSI_FINANCIAL_ANALYSIS)

# investment-banking (9 skills)
for _n in [
    "buyer-list",
    "cim-builder",
    "datapack-builder",
    "deal-tracker",
    "merger-model",
    "pitch-deck",
    "process-letter",
    "strip-profile",
    "teaser",
]:
    _register(_n, PluginCategory.FSI_INVESTMENT_BANKING)

# equity-research (9 skills)
for _n in [
    "catalyst-calendar",
    "earnings-analysis",
    "earnings-preview",
    "idea-generation",
    "initiating-coverage",
    "model-update",
    "morning-note",
    "sector-overview",
    "thesis-tracker",
]:
    _register(_n, PluginCategory.FSI_EQUITY_RESEARCH)

# private-equity (10 skills)
for _n in [
    "ai-readiness",
    "dd-checklist",
    "dd-meeting-prep",
    "deal-screening",
    "deal-sourcing",
    "ic-memo",
    "portfolio-monitoring",
    "returns-analysis",
    "unit-economics",
    "value-creation-plan",
]:
    _register(_n, PluginCategory.FSI_PRIVATE_EQUITY)

# wealth-management (6 skills)
for _n in [
    "client-report",
    "client-review",
    "financial-plan",
    "investment-proposal",
    "portfolio-rebalance",
    "tax-loss-harvesting",
]:
    _register(_n, PluginCategory.FSI_WEALTH_MANAGEMENT)


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
