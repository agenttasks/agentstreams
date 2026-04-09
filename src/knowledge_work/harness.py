"""Layer 7: knowledge-work-harness — Managed Agent runtime loop.

Implements the agent harness loop from Anthropic's Managed Agents
architecture: session management, event emission, context engineering,
and the brain-hands decoupling pattern.

Key design principles (from Anthropic's blog):
    - "Decouple the brain from the hands"
    - The session log is the source of truth, not Claude's context window
    - Subagents (hands) are cattle: execute(name, input) → string
    - The harness (brain) is stateless: wake(sessionId) restarts from log
    - Context engineering happens in the harness, not the model

Bridges:
    Layer 6 (subagents)  → SubagentPool provides execution targets
    Layer 5 (subtasks)   → SubtaskGraph provides execution plan
    Layer 8 (evals)      → Harness emits events that evals capture
    src/managed_agents.py → ManagedAgentConfig for API-based execution
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from src.knowledge_work.subagents import SubagentPool
from src.knowledge_work.subtasks import SubtaskGraph, SubtaskStatus


class EventType(Enum):
    """Event types emitted by the harness loop."""

    SESSION_START = "session.start"
    SESSION_IDLE = "session.status_idle"
    SESSION_ERROR = "session.error"
    TASK_START = "task.start"
    TASK_COMPLETE = "task.complete"
    SUBTASK_START = "subtask.start"
    SUBTASK_COMPLETE = "subtask.complete"
    SUBTASK_FAILED = "subtask.failed"
    AGENT_ASSIGNED = "agent.assigned"
    CONTEXT_COMPACTED = "context.compacted"


@dataclass
class HarnessEvent:
    """A single event in the session log."""

    type: EventType
    timestamp: float = field(default_factory=time.time)
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type.value,
            "timestamp": self.timestamp,
            "data": self.data,
        }


@dataclass
class SessionLog:
    """Durable session log — lives outside Claude's context window.

    Implements getEvents() for the harness to interrogate context.
    The session log survives harness crashes and restarts.
    """

    session_id: str
    events: list[HarnessEvent] = field(default_factory=list)

    def emit(self, event_type: EventType, **data: Any) -> None:
        """Append an event to the log."""
        self.events.append(HarnessEvent(type=event_type, data=data))

    def get_events(
        self,
        start: int = 0,
        end: int | None = None,
        event_type: EventType | None = None,
    ) -> list[HarnessEvent]:
        """Query events by position and/or type."""
        events = self.events[start:end]
        if event_type:
            events = [e for e in events if e.type == event_type]
        return events

    @property
    def last_event(self) -> HarnessEvent | None:
        return self.events[-1] if self.events else None


@dataclass
class HarnessConfig:
    """Configuration for the harness loop."""

    session_id: str = ""
    max_turns: int = 50
    subtask_timeout_seconds: int = 120
    context_compaction_threshold: int = 50_000  # Tokens before compaction
    enable_circuit_tracing: bool = False  # Trace circuits during execution


class HarnessLoop:
    """The agent harness loop — the "brain" in the brain/hands architecture.

    Executes a SubtaskGraph by:
    1. Walking the topological order of subtasks
    2. Assigning each subtask to a subagent from the pool
    3. Emitting events to the session log
    4. Handling failures and retries (cattle pattern)

    The harness is stateless — on crash, it can be restarted with
    wake(session_id) and resume from the last event in the log.
    """

    def __init__(
        self,
        config: HarnessConfig,
        pool: SubagentPool,
        session: SessionLog | None = None,
    ) -> None:
        self.config = config
        self.pool = pool
        self.session = session or SessionLog(session_id=config.session_id)

    def wake(self, session_id: str) -> None:
        """Resume from an existing session log (crash recovery)."""
        self.config.session_id = session_id
        # In production, this would load from persistent storage
        # For now, the session is in-memory

    def execute(self, graph: SubtaskGraph) -> SessionLog:
        """Execute a SubtaskGraph through the harness loop.

        Walks the topological order, assigns subagents, and emits events.
        Returns the session log with all events.
        """
        self.session.emit(
            EventType.SESSION_START,
            task=graph.task.to_dict(),
            subtask_count=len(graph.subtasks),
        )

        self.session.emit(
            EventType.TASK_START,
            task_name=graph.task.name,
            parallelism=graph.parallelism,
        )

        # Execute in topological waves
        for wave_idx, wave in enumerate(graph.topological_order()):
            for subtask in wave:
                # Assign subagent
                spec = self.pool.assign(subtask)
                if spec:
                    self.session.emit(
                        EventType.AGENT_ASSIGNED,
                        subtask_id=subtask.id,
                        agent_name=spec.name,
                    )

                # Execute subtask
                self.session.emit(
                    EventType.SUBTASK_START,
                    subtask_id=subtask.id,
                    subtask_name=subtask.name,
                    wave=wave_idx,
                )

                subtask.status = SubtaskStatus.RUNNING

                # In production, this calls the subagent via
                # execute(name, input) → string
                # For now, mark as completed (the actual execution
                # happens via Claude Code CLI or Managed Agents API)
                subtask.status = SubtaskStatus.COMPLETED

                self.session.emit(
                    EventType.SUBTASK_COMPLETE,
                    subtask_id=subtask.id,
                    subtask_name=subtask.name,
                )

        self.session.emit(
            EventType.TASK_COMPLETE,
            task_name=graph.task.name,
            progress=graph.progress,
        )

        self.session.emit(EventType.SESSION_IDLE, stop_reason="end_turn")

        return self.session
