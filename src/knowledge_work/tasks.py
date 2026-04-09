"""Layer 4: knowledge-work-tasks — Task definition and routing.

A Task is a discrete unit of knowledge work mapped to a plugin skill.
The TaskRouter matches natural-language requests to the appropriate
plugin category, skill, and agent — bridging user intent to the
knowledge-work-plugins skill catalog.

Bridges:
    vendors/knowledge-work-plugins → Plugin skills as task targets
    src/knowledge_agents.py        → CATEGORY_AGENTS, PluginCategory
    Layer 3 (prompts)              → PromptRegistry for prompt selection
    Layer 5 (subtasks)             → Tasks decompose into SubtaskGraphs
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskDomain(Enum):
    """High-level domain categories for knowledge-work tasks."""

    SALES = "sales"
    MARKETING = "marketing"
    FINANCE = "finance"
    LEGAL = "legal"
    ENGINEERING = "engineering"
    DATA = "data"
    DESIGN = "design"
    HR = "human-resources"
    OPERATIONS = "operations"
    RESEARCH = "bio-research"
    SUPPORT = "customer-support"
    SEARCH = "enterprise-search"
    PRODUCT = "product-management"
    PRODUCTIVITY = "productivity"


class TaskComplexity(Enum):
    """Complexity tier determining decomposition strategy."""

    ATOMIC = "atomic"  # Single skill, single agent, no decomposition
    COMPOSITE = "composite"  # Multiple skills, single agent
    ORCHESTRATED = "orchestrated"  # Multiple agents, requires coordination


@dataclass
class Task:
    """A discrete unit of knowledge work.

    Maps to one or more SKILL.md files in knowledge-work-plugins.
    """

    name: str
    description: str
    domain: TaskDomain
    complexity: TaskComplexity = TaskComplexity.ATOMIC
    plugin_category: str = ""
    skill_name: str = ""
    agent_name: str = ""
    model: str = "claude-opus-4-6"
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 300

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "domain": self.domain.value,
            "complexity": self.complexity.value,
            "plugin_category": self.plugin_category,
            "skill_name": self.skill_name,
            "agent_name": self.agent_name,
            "model": self.model,
        }


# ── Task Catalog ────────────────────────────────────────────────
# Maps (plugin_category, skill_name) → Task metadata
# Built from vendors/knowledge-work-plugins skill directories

TASK_CATALOG: dict[tuple[str, str], Task] = {}


def _register_task(category: str, skill: str, description: str, **kwargs: Any) -> None:
    """Register a task in the catalog."""
    domain = kwargs.pop("domain", None)
    if domain is None:
        domain_map = {
            "sales": TaskDomain.SALES,
            "marketing": TaskDomain.MARKETING,
            "finance": TaskDomain.FINANCE,
            "legal": TaskDomain.LEGAL,
            "engineering": TaskDomain.ENGINEERING,
            "data": TaskDomain.DATA,
            "design": TaskDomain.DESIGN,
            "human-resources": TaskDomain.HR,
            "operations": TaskDomain.OPERATIONS,
            "bio-research": TaskDomain.RESEARCH,
            "customer-support": TaskDomain.SUPPORT,
            "enterprise-search": TaskDomain.SEARCH,
            "product-management": TaskDomain.PRODUCT,
            "productivity": TaskDomain.PRODUCTIVITY,
        }
        domain = domain_map.get(category, TaskDomain.PRODUCTIVITY)

    task = Task(
        name=f"{category}/{skill}",
        description=description,
        domain=domain,
        plugin_category=category,
        skill_name=skill,
        **kwargs,
    )
    TASK_CATALOG[(category, skill)] = task


# Representative tasks from each plugin category
_register_task("sales", "account-research", "Research a prospect account")
_register_task("sales", "call-prep", "Prepare for a sales call")
_register_task("sales", "draft-outreach", "Draft outreach email or message")
_register_task("sales", "pipeline-review", "Review sales pipeline")
_register_task("marketing", "create-an-asset", "Create marketing content asset")
_register_task("marketing", "competitive-intelligence", "Competitive landscape brief")
_register_task("finance", "journal-entry", "Create accounting journal entry")
_register_task("finance", "variance-analysis", "Analyze financial variances")
_register_task("legal", "contract-review", "Review contract for risks")
_register_task("legal", "nda-triage", "Triage NDA for risk assessment")
_register_task("engineering", "architecture-design", "Design system architecture")
_register_task("engineering", "code-improvement", "Improve code quality")
_register_task("data", "sql-query", "Write and execute SQL queries")
_register_task("data", "dashboard", "Build data visualization dashboard")
_register_task("design", "design-critique", "Critique a design artifact")
_register_task("design", "accessibility-review", "Review accessibility compliance")
_register_task("human-resources", "comp-analysis", "Compensation analysis")
_register_task("human-resources", "recruiting-pipeline", "Manage recruiting pipeline")
_register_task("customer-support", "ticket-triage", "Triage support ticket")
_register_task("enterprise-search", "search", "Cross-tool knowledge search")
_register_task("product-management", "spec", "Write product specification")
_register_task("bio-research", "single-cell-rna-qc", "scRNA-seq QC pipeline")


class TaskRouter:
    """Routes natural-language requests to knowledge-work tasks.

    Uses keyword matching against the task catalog and plugin skills.
    In production, this would use Claude for intent classification.
    """

    def __init__(self, catalog: dict[tuple[str, str], Task] | None = None) -> None:
        self._catalog = catalog or TASK_CATALOG

    def route(self, request: str) -> Task | None:
        """Find the best matching task for a natural-language request."""
        request_lower = request.lower()

        # Score each task by keyword overlap
        best_task: Task | None = None
        best_score = 0

        for _key, task in self._catalog.items():
            score = 0
            # Check domain keywords
            if task.domain.value in request_lower:
                score += 3
            # Check skill name words
            for word in task.skill_name.replace("-", " ").split():
                if word in request_lower:
                    score += 2
            # Check description words
            for word in task.description.lower().split():
                if len(word) > 3 and word in request_lower:
                    score += 1

            if score > best_score:
                best_score = score
                best_task = task

        return best_task if best_score > 0 else None

    def list_tasks(self, domain: TaskDomain | None = None) -> list[Task]:
        """List tasks, optionally filtered by domain."""
        tasks = list(self._catalog.values())
        if domain:
            tasks = [t for t in tasks if t.domain == domain]
        return tasks
