"""Layer 5: knowledge-work-subtasks — Subtask decomposition.

Decomposes Tasks (Layer 4) into directed acyclic graphs of Subtasks.
Each subtask is an atomic unit of work that can be assigned to a single
subagent (Layer 6). The decomposition strategy depends on TaskComplexity.

Bridges:
    Layer 4 (tasks)     → Tasks decompose into SubtaskGraphs
    Layer 6 (subagents) → Each subtask maps to a subagent execution
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from src.knowledge_work.tasks import Task, TaskComplexity


class SubtaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Subtask:
    """An atomic unit of work within a Task.

    Subtasks form a DAG — each can depend on outputs from prior subtasks.
    A subtask maps to a single skill invocation on a single subagent.
    """

    id: str
    name: str
    description: str
    plugin_category: str = ""
    skill_name: str = ""
    agent_name: str = ""
    depends_on: list[str] = field(default_factory=list)  # Subtask IDs
    status: SubtaskStatus = SubtaskStatus.PENDING
    input_data: dict[str, Any] = field(default_factory=dict)
    output_data: dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 120

    def is_ready(self, completed: set[str]) -> bool:
        """Check if all dependencies are met."""
        return all(dep in completed for dep in self.depends_on)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "plugin_category": self.plugin_category,
            "skill_name": self.skill_name,
            "agent_name": self.agent_name,
            "depends_on": self.depends_on,
            "status": self.status.value,
        }


@dataclass
class SubtaskGraph:
    """A directed acyclic graph of subtasks decomposed from a Task.

    Provides topological ordering for execution, parallelism detection
    (independent subtasks can run concurrently), and progress tracking.
    """

    task: Task
    subtasks: list[Subtask] = field(default_factory=list)

    @property
    def ready_subtasks(self) -> list[Subtask]:
        """Subtasks whose dependencies are all completed — can run in parallel."""
        completed = {s.id for s in self.subtasks if s.status == SubtaskStatus.COMPLETED}
        return [
            s for s in self.subtasks if s.status == SubtaskStatus.PENDING and s.is_ready(completed)
        ]

    @property
    def is_complete(self) -> bool:
        """All subtasks completed or skipped."""
        return all(
            s.status in (SubtaskStatus.COMPLETED, SubtaskStatus.SKIPPED) for s in self.subtasks
        )

    @property
    def progress(self) -> float:
        """Fraction of subtasks completed."""
        if not self.subtasks:
            return 1.0
        done = sum(
            1 for s in self.subtasks if s.status in (SubtaskStatus.COMPLETED, SubtaskStatus.SKIPPED)
        )
        return done / len(self.subtasks)

    @property
    def parallelism(self) -> int:
        """Maximum number of subtasks that can run concurrently at any point."""
        if not self.subtasks:
            return 0
        # Simulate execution waves
        completed: set[str] = set()
        max_parallel = 0
        remaining = list(self.subtasks)

        while remaining:
            ready = [s for s in remaining if s.is_ready(completed)]
            if not ready:
                break
            max_parallel = max(max_parallel, len(ready))
            for s in ready:
                completed.add(s.id)
                remaining.remove(s)

        return max_parallel

    def topological_order(self) -> list[list[Subtask]]:
        """Return subtasks in execution waves (each wave can run in parallel)."""
        completed: set[str] = set()
        remaining = list(self.subtasks)
        waves: list[list[Subtask]] = []

        while remaining:
            wave = [s for s in remaining if s.is_ready(completed)]
            if not wave:
                break
            waves.append(wave)
            for s in wave:
                completed.add(s.id)
                remaining.remove(s)

        return waves

    def to_dict(self) -> dict[str, Any]:
        return {
            "task": self.task.to_dict(),
            "subtask_count": len(self.subtasks),
            "progress": self.progress,
            "parallelism": self.parallelism,
            "subtasks": [s.to_dict() for s in self.subtasks],
        }

    @classmethod
    def decompose(cls, task: Task) -> SubtaskGraph:
        """Decompose a Task into a SubtaskGraph.

        Strategy depends on TaskComplexity:
        - ATOMIC: Single subtask wrapping the entire task
        - COMPOSITE: Multiple subtasks within one domain
        - ORCHESTRATED: Cross-domain subtasks with dependencies
        """
        if task.complexity == TaskComplexity.ATOMIC:
            subtask = Subtask(
                id=f"{task.name}-0",
                name=task.name,
                description=task.description,
                plugin_category=task.plugin_category,
                skill_name=task.skill_name,
                agent_name=task.agent_name,
            )
            return cls(task=task, subtasks=[subtask])

        if task.complexity == TaskComplexity.COMPOSITE:
            # Generic decomposition: research → execute → verify
            return cls(
                task=task,
                subtasks=[
                    Subtask(
                        id=f"{task.name}-research",
                        name=f"Research for {task.skill_name}",
                        description=f"Gather context and information for {task.description}",
                        plugin_category=task.plugin_category,
                        skill_name=task.skill_name,
                        agent_name=task.agent_name,
                    ),
                    Subtask(
                        id=f"{task.name}-execute",
                        name=f"Execute {task.skill_name}",
                        description=task.description,
                        plugin_category=task.plugin_category,
                        skill_name=task.skill_name,
                        agent_name=task.agent_name,
                        depends_on=[f"{task.name}-research"],
                    ),
                    Subtask(
                        id=f"{task.name}-verify",
                        name=f"Verify {task.skill_name}",
                        description=f"Verify output quality for {task.description}",
                        plugin_category=task.plugin_category,
                        skill_name=task.skill_name,
                        agent_name=task.agent_name,
                        depends_on=[f"{task.name}-execute"],
                    ),
                ],
            )

        # ORCHESTRATED: safety screen → domain work → cross-domain review
        return cls(
            task=task,
            subtasks=[
                Subtask(
                    id=f"{task.name}-screen",
                    name="Safety screen",
                    description="Pre-screen request for safety compliance",
                    agent_name="harmlessness-screen",
                ),
                Subtask(
                    id=f"{task.name}-execute",
                    name=f"Execute {task.skill_name}",
                    description=task.description,
                    plugin_category=task.plugin_category,
                    skill_name=task.skill_name,
                    agent_name=task.agent_name,
                    depends_on=[f"{task.name}-screen"],
                ),
                Subtask(
                    id=f"{task.name}-review",
                    name="Security review",
                    description="Review output for security and compliance",
                    agent_name="security-auditor",
                    depends_on=[f"{task.name}-execute"],
                ),
            ],
        )
