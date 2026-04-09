"""Knowledge Work Agents — plugin-to-agent bridge layer.

Maps 124 skills from anthropics/knowledge-work-plugins (17 plugin directories)
to knowledge-work agents, providing factory functions and pipelines that
integrate with the existing Orchestrator and ManagedOrchestrator infrastructure.

Source of truth: vendors/knowledge-work-plugins/ (cloned from GitHub).

Plugin directories map to PluginCategory enum values:
    PRODUCTIVITY         → productivity-agent       (4 skills)
    SALES                → sales-agent              (9 skills)
    CUSTOMER_SUPPORT     → customer-support-agent   (5 skills)
    PRODUCT_MANAGEMENT   → product-management-agent (8 skills)
    MARKETING            → marketing-agent          (8 skills)
    LEGAL                → compliance-reviewer      (9 skills, read-only)
    FINANCE              → finance-agent            (8 skills, read-only)
    DATA                 → data-analyst             (10 skills)
    ENTERPRISE_SEARCH    → enterprise-search-agent  (5 skills)
    BIO_RESEARCH         → bio-research-agent       (6 skills)
    COWORK_PLUGIN_MGMT   → productivity-agent       (2 skills, shared)
    DESIGN               → design-agent             (7 skills)
    ENGINEERING          → engineering-agent         (10 skills)
    HUMAN_RESOURCES      → hr-agent                 (9 skills)
    OPERATIONS           → operations-agent         (9 skills)
    PARTNER_BUILT        → sales-agent              (14 skills, shared)
    PDF_VIEWER           → data-analyst             (1 skill, shared)

All knowledge-work agents use claude-opus-4-6 model.

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
    """Plugin directories from anthropics/knowledge-work-plugins."""

    PRODUCTIVITY = "productivity"
    SALES = "sales"
    CUSTOMER_SUPPORT = "customer-support"
    PRODUCT_MANAGEMENT = "product-management"
    MARKETING = "marketing"
    LEGAL = "legal"
    FINANCE = "finance"
    DATA = "data"
    ENTERPRISE_SEARCH = "enterprise-search"
    BIO_RESEARCH = "bio-research"
    COWORK_PLUGIN_MGMT = "cowork-plugin-management"
    DESIGN = "design"
    ENGINEERING = "engineering"
    HUMAN_RESOURCES = "human-resources"
    OPERATIONS = "operations"
    PARTNER_BUILT = "partner-built"
    PDF_VIEWER = "pdf-viewer"


# Agent name that handles each plugin category
CATEGORY_AGENTS: dict[PluginCategory, str] = {
    PluginCategory.PRODUCTIVITY: "productivity-agent",
    PluginCategory.SALES: "sales-agent",
    PluginCategory.CUSTOMER_SUPPORT: "customer-support-agent",
    PluginCategory.PRODUCT_MANAGEMENT: "product-management-agent",
    PluginCategory.MARKETING: "marketing-agent",
    PluginCategory.LEGAL: "compliance-reviewer",
    PluginCategory.FINANCE: "finance-agent",
    PluginCategory.DATA: "data-analyst",
    PluginCategory.ENTERPRISE_SEARCH: "enterprise-search-agent",
    PluginCategory.BIO_RESEARCH: "bio-research-agent",
    PluginCategory.COWORK_PLUGIN_MGMT: "productivity-agent",
    PluginCategory.DESIGN: "design-agent",
    PluginCategory.ENGINEERING: "engineering-agent",
    PluginCategory.HUMAN_RESOURCES: "hr-agent",
    PluginCategory.OPERATIONS: "operations-agent",
    PluginCategory.PARTNER_BUILT: "sales-agent",
    PluginCategory.PDF_VIEWER: "data-analyst",
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


# ── First-Party Plugins ──────────────────────────────────────

# productivity (4 skills)
for _n, _i in [
    ("memory-management", 1400), ("start", 620),
    ("task-management", 1700), ("update", 635),
]:
    _register(_n, PluginCategory.PRODUCTIVITY, _i)

# sales (9 skills)
for _n, _i in [
    ("account-research", 734), ("call-prep", 686),
    ("call-summary", 522), ("competitive-intelligence", 1300),
    ("create-an-asset", 659), ("daily-briefing", 842),
    ("draft-outreach", 796), ("forecast", 503),
    ("pipeline-review", 492),
]:
    _register(_n, PluginCategory.SALES, _i)

# customer-support (5 dir + 3 readme = 8 skills)
for _n, _i in [
    ("customer-escalation", 472), ("customer-research", 719),
    ("draft-response", 483), ("kb-article", 491),
    ("ticket-triage", 664),
    # readme-sourced
    ("escalation", 162), ("knowledge-management", 316),
    ("response-drafting", 190),
]:
    _register(_n, PluginCategory.CUSTOMER_SUPPORT, _i)

# product-management (8 dir + 6 readme = 14 skills)
for _n, _i in [
    ("competitive-brief", 574), ("metrics-review", 511),
    ("product-brainstorming", 622), ("roadmap-update", 543),
    ("sprint-planning", 520), ("stakeholder-update", 510),
    ("synthesize-research", 568), ("write-spec", 621),
    # readme-sourced
    ("competitive-analysis", 405), ("feature-spec", 463),
    ("metrics-tracking", 268), ("roadmap-management", 336),
    ("stakeholder-comms", 238), ("user-research-synthesis", 407),
]:
    _register(_n, PluginCategory.PRODUCT_MANAGEMENT, _i)

# marketing (8 dir + 4 readme = 12 skills)
for _n, _i in [
    ("brand-review", 537), ("campaign-plan", 558),
    ("content-creation", 1500), ("draft-content", 503),
    ("email-sequence", 491), ("performance-report", 523),
    ("seo-audit", 569), ("competitive-brief", 574),
    # readme-sourced
    ("brand-voice", 323), ("campaign-planning", 220),
    ("competitive-analysis", 405), ("performance-analytics", 251),
]:
    _register(_n, PluginCategory.MARKETING, _i)

# legal (9 dir + 4 readme = 13 skills)
for _n, _i in [
    ("brief", 500), ("compliance-check", 526),
    ("legal-response", 565), ("legal-risk-assessment", 1100),
    ("meeting-briefing", 689), ("review-contract", 617),
    ("signature-request", 475), ("triage-nda", 477),
    ("vendor-check", 486),
    # readme-sourced
    ("canned-responses", 162), ("compliance", 206),
    ("contract-review", 341), ("nda-triage", 168),
]:
    _register(_n, PluginCategory.LEGAL, _i)

# finance (8 skills)
for _n, _i in [
    ("audit-support", 690), ("close-management", 648),
    ("financial-statements", 1000), ("journal-entry", 474),
    ("journal-entry-prep", 666), ("reconciliation", 682),
    ("sox-testing", 466), ("variance-analysis", 693),
]:
    _register(_n, PluginCategory.FINANCE, _i)

# data (10 dir + 3 readme = 13 skills)
for _n, _i in [
    ("analyze", 690), ("build-dashboard", 884),
    ("create-viz", 653), ("data-context-extractor", 710),
    ("data-visualization", 3800), ("explore-data", 697),
    ("sql-queries", 1100), ("statistical-analysis", 1100),
    ("validate-data", 568), ("write-query", 520),
    # readme-sourced
    ("data-exploration", 226), ("data-validation", 255),
    ("interactive-dashboard-builder", 584),
]:
    _register(_n, PluginCategory.DATA, _i)

# enterprise-search (5 skills)
for _n, _i in [
    ("digest", 489), ("knowledge-synthesis", 1200),
    ("search", 633), ("search-strategy", 848),
    ("source-management", 778),
]:
    _register(_n, PluginCategory.ENTERPRISE_SEARCH, _i)

# bio-research (6 dir + 1 readme = 7 skills)
for _n, _i in [
    ("instrument-data-to-allotrope", 233), ("nextflow-development", 241),
    ("scientific-problem-selection", 258), ("scvi-tools", 231),
    ("single-cell-rna-qc", 244), ("start", 620),
    # readme-sourced
    ("clinical-trial-protocol-skill", 5),
]:
    _register(_n, PluginCategory.BIO_RESEARCH, _i)

# cowork-plugin-management (2 skills)
for _n, _i in [
    ("cowork-plugin-customizer", 653), ("create-cowork-plugin", 648),
]:
    _register(_n, PluginCategory.COWORK_PLUGIN_MGMT, _i)

# ── Additional Plugins ───────────────────────────────────────

# design (7 dir + 2 readme = 9 skills)
for _n, _i in [
    ("accessibility-review", 657), ("design-critique", 796),
    ("design-handoff", 643), ("design-system", 647),
    ("research-synthesis", 615), ("user-research", 820),
    ("ux-copy", 663),
    # readme-sourced
    ("design-system-management", 116), ("ux-writing", 132),
]:
    _register(_n, PluginCategory.DESIGN, _i)

# engineering (10 skills)
for _n, _i in [
    ("architecture", 745), ("code-review", 1400),
    ("debug", 672), ("deploy-checklist", 662),
    ("documentation", 1100), ("incident-response", 764),
    ("standup", 621), ("system-design", 1200),
    ("tech-debt", 866), ("testing-strategy", 855),
]:
    _register(_n, PluginCategory.ENGINEERING, _i)

# human-resources (9 dir + 3 readme = 12 skills)
for _n, _i in [
    ("comp-analysis", 507), ("draft-offer", 485),
    ("interview-prep", 663), ("onboarding", 504),
    ("org-planning", 601), ("people-report", 479),
    ("performance-review", 545), ("policy-lookup", 509),
    ("recruiting-pipeline", 598),
    # readme-sourced
    ("compensation-benchmarking", 97), ("people-analytics", 100),
    ("employee-handbook", 96),
]:
    _register(_n, PluginCategory.HUMAN_RESOURCES, _i)

# operations (9 dir + 3 readme = 12 skills)
for _n, _i in [
    ("capacity-plan", 497), ("change-request", 488),
    ("compliance-tracking", 610), ("process-doc", 517),
    ("process-optimization", 653), ("risk-assessment", 672),
    ("runbook", 480), ("status-report", 509),
    ("vendor-review", 480),
    # readme-sourced
    ("change-management", 112), ("resource-planning", 100),
    ("vendor-management", 99),
]:
    _register(_n, PluginCategory.OPERATIONS, _i)

# partner-built (14 skills across apollo, brand-voice, common-room, slack)
for _n, _i in [
    # apollo
    ("enrich-lead", 607), ("prospect", 581), ("sequence-load", 559),
    # brand-voice
    ("brand-voice-enforcement", 684), ("discover-brand", 635),
    ("guideline-generation", 608),
    # common-room
    ("account-research", 734), ("call-prep", 686),
    ("compose-outreach", 600), ("contact-research", 597),
    ("prospect", 581), ("weekly-prep-brief", 569),
    # slack
    ("slack-messaging", 702), ("slack-search", 607),
]:
    _register(_n, PluginCategory.PARTNER_BUILT, _i)

# pdf-viewer (1 skill)
_register("view-pdf", PluginCategory.PDF_VIEWER, 365)


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
        "productivity-agent": _make(
            "productivity-agent",
            "You are a productivity agent. Manage tasks, calendars, daily "
            "workflows, and personal context. Handle plugins and memory "
            "management for consistent outcomes across sessions.",
        ),
        "sales-agent": _make(
            "sales-agent",
            "You are a sales intelligence agent. Research prospects, prep "
            "for calls, review pipelines, draft outreach, and build "
            "competitive battlecards. Include source provenance for all "
            "claims about prospects and competitors.",
        ),
        "customer-support-agent": _make(
            "customer-support-agent",
            "You are a customer support agent. Triage tickets, draft "
            "responses, package escalations, research customer context, "
            "and create knowledge base articles from resolved issues.",
        ),
        "product-management-agent": _make(
            "product-management-agent",
            "You are a product management agent. Write specs, plan "
            "roadmaps, synthesize user research, keep stakeholders "
            "updated, and track the competitive landscape.",
        ),
        "marketing-agent": _make(
            "marketing-agent",
            "You are a marketing agent. Draft content, plan campaigns, "
            "enforce brand voice, brief on competitors, and report on "
            "performance across channels.",
        ),
        "compliance-reviewer": _make(
            "compliance-reviewer",
            "You are a legal compliance reviewer. Review contracts, "
            "triage NDAs, navigate compliance frameworks, assess risk, "
            "and draft templated responses. Read-only — never modify "
            "documents under review. Never provide legal advice — "
            "frame all outputs as analysis. End with verdict: "
            "PASS, NEEDS_REMEDIATION, or BLOCK.",
            max_turns=15,
        ),
        "finance-agent": _make(
            "finance-agent",
            "You are a financial operations agent. Prep journal entries, "
            "reconcile accounts, generate financial statements, analyze "
            "variances, manage close, and support audits. Read-only — "
            "never modify financial records directly. Always state "
            "assumptions explicitly.",
            max_turns=15,
        ),
        "data-analyst": _make(
            "data-analyst",
            "You are a data analysis agent. Query, visualize, and "
            "interpret datasets — write SQL, run statistical analysis, "
            "build dashboards, and validate work before sharing. "
            "Never expose raw PII — aggregate or anonymize. "
            "For SQL, prefer parameterized queries.",
        ),
        "enterprise-search-agent": _make(
            "enterprise-search-agent",
            "You are an enterprise search agent. Find anything across "
            "email, chat, docs, and wikis — one query across all "
            "company tools. Synthesize and provide source provenance.",
        ),
        "bio-research-agent": _make(
            "bio-research-agent",
            "You are a bio-research agent. Connect to preclinical "
            "research tools and databases for literature search, "
            "genomics analysis, target prioritization, and pipeline "
            "development. Always cite primary literature.",
        ),
        "design-agent": _make(
            "design-agent",
            "You are a design agent. Conduct user research, review "
            "designs for accessibility, manage design systems, write "
            "UX copy, and prepare developer handoffs. Always consider "
            "WCAG standards and existing design conventions.",
        ),
        "engineering-agent": _make(
            "engineering-agent",
            "You are an engineering agent. Review architecture and code, "
            "debug issues, manage deployments, handle incidents, and "
            "document systems. Never execute destructive operations "
            "without explicit confirmation.",
        ),
        "hr-agent": _make(
            "hr-agent",
            "You are an HR agent. Manage recruiting pipelines, prep "
            "interviews, run compensation analysis, handle onboarding, "
            "plan org structure, and generate people reports. "
            "Anonymize sensitive employee data in outputs.",
        ),
        "operations-agent": _make(
            "operations-agent",
            "You are an operations agent. Optimize processes, track "
            "compliance, assess risks, plan capacity, maintain runbooks, "
            "and manage vendor reviews. Always include rollback "
            "procedures for process changes.",
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
            PipelineStep(order=2, agent_name="marketing-agent",
                         input_from="enterprise-search-agent"),
            PipelineStep(order=2, agent_name="compliance-reviewer",
                         input_from="enterprise-search-agent"),
            PipelineStep(order=3, agent_name="security-auditor",
                         condition="sensitive_data"),
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
            PipelineStep(order=2, agent_name="finance-agent",
                         input_from="data-analyst"),
            PipelineStep(order=2, agent_name="compliance-reviewer",
                         input_from="data-analyst"),
            PipelineStep(order=3, agent_name="marketing-agent",
                         input_from="finance-agent"),
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
            PipelineStep(order=2, agent_name="security-auditor",
                         input_from="compliance-reviewer"),
            PipelineStep(order=2, agent_name="enterprise-search-agent",
                         input_from="compliance-reviewer"),
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
