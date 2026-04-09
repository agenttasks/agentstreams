"""Managed harness bridging local orchestrator pipelines to cloud sessions.

Extends the existing Orchestrator pattern to run pipeline steps as
cloud-managed agent sessions instead of local Messages API calls.
Each pipeline step becomes a dedicated Managed Agent session running
in an isolated container with its own toolset.

Architecture:
    1. Convert AgentConfig → ManagedAgentConfig for cloud execution
    2. Create one shared environment or per-step environments
    3. Launch sessions for each pipeline step
    4. Stream events and collect results via SSE
    5. Feed results through the existing gate system

This enables running security-auditor, alignment-auditor, architecture-reviewer,
harmlessness-screen, and other safety agents in isolated cloud containers with controlled networking,
while preserving the Orchestrator's pipeline logic and gate checks.

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import asyncio
import contextlib
from dataclasses import dataclass, field
from typing import Any

from src.agent_tasks import AgentConfig, TaskResult
from src.managed_agents import (
    AgentMessageEvent,
    AgentToolset,
    AgentToolUseEvent,
    EnvironmentConfig,
    ManagedAgentConfig,
    ManagedAgentsClient,
    NetworkConfig,
    NetworkingMode,
    Packages,
    SessionErrorEvent,
    SessionStatus,
    SessionStatusEvent,
    ToolConfig,
)
from src.orchestrator import (
    GateAction,
    Orchestrator,
    PipelineResult,
    PipelineStep,
    StepResult,
)
from src.tracing import trace_span

# ── Config Conversion ─────────────────────────────────────────


def agent_config_to_managed(
    config: AgentConfig,
    *,
    disable_write: bool = False,
) -> ManagedAgentConfig:
    """Convert a local AgentConfig to a ManagedAgentConfig.

    Read-only agents (security-auditor, alignment-auditor, architecture-reviewer)
    should set disable_write=True to prevent file modifications in the container.
    """
    tool_configs = []
    if disable_write:
        tool_configs = [
            ToolConfig(name="write", enabled=False),
            ToolConfig(name="edit", enabled=False),
        ]

    return ManagedAgentConfig(
        name=config.name,
        model=config.model,
        system=config.system_prompt,
        toolset=AgentToolset(configs=tool_configs),
    )


# Read-only agents that should not modify files in the container
READ_ONLY_AGENTS = frozenset(
    {
        "security-auditor",
        "alignment-auditor",
        "architecture-reviewer",
        "harmlessness-screen",
    }
)


# ── Managed Step Runner ───────────────────────────────────────


@dataclass
class ManagedStepResult:
    """Result from executing a pipeline step as a managed session."""

    agent_name: str
    session_id: str
    messages: list[str] = field(default_factory=list)
    tool_calls: list[str] = field(default_factory=list)
    status: SessionStatus = SessionStatus.IDLE
    error: str = ""
    raw_events: list[dict[str, Any]] = field(default_factory=list)

    def to_task_result(self, task_id: str) -> TaskResult:
        """Convert to TaskResult for gate compatibility."""
        full_text = "\n".join(self.messages)

        # Try to extract structured outputs from agent messages
        outputs: dict[str, Any] = {"raw": full_text}

        # Look for verdict keywords in agent output
        text_lower = full_text.lower()
        if "verdict: pass" in text_lower or '"verdict": "pass"' in text_lower:
            outputs["verdict"] = "PASS"
        elif "verdict: block" in text_lower or '"verdict": "block"' in text_lower:
            outputs["verdict"] = "BLOCK"
        elif (
            "verdict: needs_remediation" in text_lower
            or '"verdict": "needs_remediation"' in text_lower
        ):
            outputs["verdict"] = "NEEDS_REMEDIATION"

        # Look for alignment verdicts
        if "verdict: aligned" in text_lower:
            outputs["verdict"] = "ALIGNED"
        elif "verdict: misaligned" in text_lower:
            outputs["verdict"] = "MISALIGNED"
        elif "verdict: borderline" in text_lower:
            outputs["verdict"] = "BORDERLINE"

        # Look for harmlessness classification
        for cls in ("safe", "needs_review", "block"):
            if f'"classification": "{cls}"' in text_lower:
                outputs["classification"] = cls
                break

        status = "completed" if not self.error else "failed"
        return TaskResult(
            task_id=task_id,
            status=status,
            outputs=outputs,
            error=self.error,
        )


# ── Managed Orchestrator ──────────────────────────────────────


class ManagedOrchestrator:
    """Pipeline orchestrator that executes steps as cloud-managed sessions.

    Preserves the Orchestrator's pipeline/gate pattern but runs each
    step in an isolated Managed Agent session instead of local API calls.

    Usage:
        orch = ManagedOrchestrator(
            environment_id="env_xxx",
            agent_ids={"code-generator": "agent_xxx", ...},
        )
        result = await orch.run("standard-codegen", prompt)

    Or auto-create agents from local configs:
        orch = ManagedOrchestrator.from_local_configs()
        result = await orch.run("standard-codegen", prompt)
    """

    def __init__(
        self,
        *,
        environment_id: str = "",
        agent_ids: dict[str, str] | None = None,
        client: ManagedAgentsClient | None = None,
    ):
        self._client = client or ManagedAgentsClient()
        self._environment_id = environment_id
        self._agent_ids = agent_ids or {}
        self._local_orch = Orchestrator()

    @classmethod
    def from_local_configs(
        cls,
        *,
        environment_name: str = "agentstreams-pipeline",
        pip_packages: list[str] | None = None,
        client: ManagedAgentsClient | None = None,
    ) -> ManagedOrchestrator:
        """Create a ManagedOrchestrator by registering local agent configs
        as managed agents and creating a shared environment.

        This is the easiest way to migrate from local to cloud execution.
        """
        mc = client or ManagedAgentsClient()

        # Create shared environment
        env_config = EnvironmentConfig(
            name=environment_name,
            packages=Packages(pip=pip_packages or []),
            networking=NetworkConfig(mode=NetworkingMode.UNRESTRICTED),
        )
        env_id = mc.create_environment(env_config)

        # Register each local agent config as a managed agent
        from src.orchestrator import _agent_configs

        agent_ids: dict[str, str] = {}
        for name, config in _agent_configs().items():
            managed_config = agent_config_to_managed(
                config,
                disable_write=name in READ_ONLY_AGENTS,
            )
            agent_ids[name] = mc.create_agent(managed_config)

        return cls(
            environment_id=env_id,
            agent_ids=agent_ids,
            client=mc,
        )

    async def _run_managed_step(
        self,
        step: PipelineStep,
        pipeline_name: str,
        prompt: str,
    ) -> StepResult:
        """Execute a single pipeline step as a managed session."""
        agent_id = self._agent_ids.get(step.agent_name, "")
        if not agent_id:
            return StepResult(
                agent_name=step.agent_name,
                task_result=TaskResult(
                    task_id=f"{pipeline_name}-{step.agent_name}",
                    status="failed",
                    error=f"No managed agent ID for {step.agent_name}",
                ),
            )

        with trace_span(
            "managed_orchestrator_step",
            attributes={
                "pipeline": pipeline_name,
                "agent": step.agent_name,
                "order": step.order,
            },
        ):
            # Create session
            session_id = self._client.create_session(
                agent_id,
                self._environment_id,
                title=f"{pipeline_name}/{step.agent_name}",
            )

            # Send the task prompt
            self._client.send_message(session_id, prompt)

            # Collect events
            managed_result = ManagedStepResult(
                agent_name=step.agent_name,
                session_id=session_id,
            )

            for event in self._client.stream_events(session_id):
                raw = {}
                if hasattr(event, "raw"):
                    raw = event.raw

                managed_result.raw_events.append(raw)

                if isinstance(event, AgentMessageEvent):
                    managed_result.messages.append(event.text)
                elif isinstance(event, AgentToolUseEvent):
                    managed_result.tool_calls.append(event.name)
                elif isinstance(event, SessionErrorEvent):
                    managed_result.error = event.message
                elif isinstance(event, SessionStatusEvent):
                    managed_result.status = event.status
                    if event.status in (
                        SessionStatus.IDLE,
                        SessionStatus.TERMINATED,
                    ):
                        break

            # Archive the session after completion
            with contextlib.suppress(Exception):
                self._client.archive_session(session_id)

            # Convert to StepResult for gate compatibility
            task_id = f"{pipeline_name}-{step.agent_name}"
            task_result = managed_result.to_task_result(task_id)

        return self._local_orch._parse_step_result(step.agent_name, task_result)

    async def run(
        self,
        pipeline_name: str,
        prompt: str,
        *,
        context: dict[str, Any] | None = None,
    ) -> PipelineResult:
        """Execute a pipeline with steps running as managed sessions.

        Same interface as Orchestrator.run() but each step runs in
        an isolated cloud container instead of local API calls.
        """
        from src.orchestrator import PIPELINES

        pipeline = PIPELINES[pipeline_name]
        context = context or {}
        result = PipelineResult(pipeline_name=pipeline_name)

        # Group steps by order
        order_groups: dict[int, list[PipelineStep]] = {}
        for step in pipeline.steps:
            order_groups.setdefault(step.order, []).append(step)

        with trace_span(
            "managed_orchestrator_pipeline",
            attributes={
                "pipeline.name": pipeline_name,
                "pipeline.step_count": len(pipeline.steps),
                "execution_mode": "managed",
            },
        ) as span_ctx:
            for order in sorted(order_groups.keys()):
                group = order_groups[order]

                # Filter steps by condition
                active_steps = [
                    step
                    for step in group
                    if not step.condition or context.get(step.condition, False)
                ]

                if not active_steps:
                    continue

                # Run steps in parallel via managed sessions
                step_coros = [
                    self._run_managed_step(step, pipeline_name, prompt) for step in active_steps
                ]
                step_results = await asyncio.gather(*step_coros)

                for sr in step_results:
                    result.step_results.append(sr)
                    result.total_tokens += sr.task_result.tokens_used

                # Check gate after each order group
                gate_action, gate_reason = self._local_orch._check_gate(
                    pipeline.gate, list(step_results)
                )

                if gate_action != GateAction.CONTINUE:
                    result.gate_action = gate_action
                    result.gate_reason = gate_reason
                    break

            span_ctx["gate_action"] = result.gate_action.value
            span_ctx["total_tokens"] = result.total_tokens
            span_ctx["steps_completed"] = len(result.step_results)

        return result

    def cleanup(self, session_ids: list[str] | None = None) -> None:
        """Archive or delete managed sessions."""
        if session_ids:
            for sid in session_ids:
                with contextlib.suppress(Exception):
                    self._client.archive_session(sid)


# ── Convenience Functions ─────────────────────────────────────


async def run_managed_codegen(
    prompt: str,
    *,
    environment_id: str = "",
    agent_ids: dict[str, str] | None = None,
) -> PipelineResult:
    """Run the standard codegen pipeline via managed sessions."""
    orch = ManagedOrchestrator(
        environment_id=environment_id,
        agent_ids=agent_ids,
    )
    return await orch.run("standard-codegen", prompt)


async def run_managed_security_scan(
    prompt: str,
    *,
    environment_id: str = "",
    agent_ids: dict[str, str] | None = None,
) -> PipelineResult:
    """Run the security deep scan pipeline via managed sessions."""
    orch = ManagedOrchestrator(
        environment_id=environment_id,
        agent_ids=agent_ids,
    )
    return await orch.run("security-deep-scan", prompt)
