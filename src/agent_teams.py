"""Agent teams module for multi-session coordination.

Wraps Claude Code CLI agent teams functionality for parallel,
coordinated task execution across named agents registered in
.claude/agents/.

Each team member is invoked via ``claude --agent-name NAME -p "task"``
subprocess calls. Auth flows through CLAUDE_CODE_OAUTH_TOKEN.

Usage::

    from src.agent_teams import TeamOrchestrator, SECURITY_TEAM

    orch = TeamOrchestrator(SECURITY_TEAM)
    results = orch.run_parallel([
        ("security-auditor", "Audit src/agent_teams.py for injection flaws"),
        ("alignment-auditor", "Check alignment properties of the new module"),
    ])

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent

# ── Dataclasses ────────────────────────────────────────────────


@dataclass
class TeamMember:
    """A single member of an agent team.

    Args:
        agent_name: Name matching a .claude/agents/<name>.md file.
        role: Human-readable role description within the team.
        tools: Tool names this member is expected to use (informational).
        model: Claude model ID for this member (informational; the agent
               .md frontmatter controls the actual model used by the CLI).
    """

    agent_name: str
    role: str
    tools: list[str] = field(default_factory=list)
    model: str = "claude-sonnet-4-6"


@dataclass
class TeamConfig:
    """Configuration for an agent team.

    Args:
        name: Team identifier used for logging and status display.
        members: Ordered list of TeamMember entries. The order controls
                 the display in ``teams list`` but execution is parallel.
        shared_context: A string injected as context prefix into every
                        task prompt sent to team members.
        max_parallel: Maximum number of concurrent subprocess invocations.
    """

    name: str
    members: list[TeamMember]
    shared_context: str = ""
    max_parallel: int = 4


@dataclass
class MemberResult:
    """Result from invoking a single team member.

    Args:
        agent_name: Which agent produced this result.
        task: The task description that was assigned.
        returncode: Exit code from the ``claude`` subprocess.
        stdout: Captured standard output from the agent.
        stderr: Captured standard error from the agent.
        success: True when returncode == 0.
    """

    agent_name: str
    task: str
    returncode: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        """Return True when the subprocess exited cleanly."""
        return self.returncode == 0


# ── Pre-built team configs ─────────────────────────────────────

RESEARCH_TEAM = TeamConfig(
    name="research-team",
    members=[
        TeamMember(
            agent_name="enterprise-search-agent",
            role="Information retrieval and synthesis",
            tools=["WebSearch", "Read"],
            model="claude-opus-4-6",
        ),
        TeamMember(
            agent_name="data-analyst",
            role="Quantitative analysis and insight generation",
            tools=["computer", "Read"],
            model="claude-opus-4-6",
        ),
        TeamMember(
            agent_name="marketing-agent",
            role="Audience targeting and messaging strategy",
            tools=["Read", "Write"],
            model="claude-opus-4-6",
        ),
    ],
    shared_context=(
        "You are part of the agentstreams research team. "
        "Coordinate with enterprise-search-agent, data-analyst, and "
        "marketing-agent to produce a cohesive deliverable."
    ),
    max_parallel=3,
)

SECURITY_TEAM = TeamConfig(
    name="security-team",
    members=[
        TeamMember(
            agent_name="security-auditor",
            role="Vulnerability scanning and exploit analysis",
            tools=["Read", "Bash"],
            model="claude-opus-4-6",
        ),
        TeamMember(
            agent_name="alignment-auditor",
            role="Alignment and deception detection",
            tools=["Read"],
            model="claude-opus-4-6",
        ),
        TeamMember(
            agent_name="architecture-reviewer",
            role="Agent topology and least-privilege review",
            tools=["Read"],
            model="claude-opus-4-6",
        ),
    ],
    shared_context=(
        "You are part of the agentstreams security team. "
        "Apply the Mythos System Card methodology. "
        "Report findings with severity and exploitability ratings."
    ),
    max_parallel=3,
)

CONTENT_TEAM = TeamConfig(
    name="content-team",
    members=[
        TeamMember(
            agent_name="marketing-agent",
            role="Content strategy and copywriting",
            tools=["Read", "Write"],
            model="claude-opus-4-6",
        ),
        TeamMember(
            agent_name="design-agent",
            role="Visual design and layout direction",
            tools=["Read", "Write"],
            model="claude-opus-4-6",
        ),
        TeamMember(
            agent_name="compliance-reviewer",
            role="Regulatory and brand compliance review",
            tools=["Read"],
            model="claude-opus-4-6",
        ),
    ],
    shared_context=(
        "You are part of the agentstreams content team. "
        "Produce brand-consistent, compliance-cleared deliverables."
    ),
    max_parallel=3,
)

# Registry of all built-in teams, keyed by name.
TEAMS: dict[str, TeamConfig] = {
    "research-team": RESEARCH_TEAM,
    "security-team": SECURITY_TEAM,
    "content-team": CONTENT_TEAM,
}


# ── Team Orchestrator ──────────────────────────────────────────


class TeamOrchestrator:
    """Orchestrate a Claude Code agent team for multi-session task execution.

    Wraps the Claude Code CLI ``claude --agent-name NAME -p "..."`` interface.
    Parallel invocations are managed via :class:`concurrent.futures.ThreadPoolExecutor`.

    Args:
        config: The :class:`TeamConfig` that defines the team.
        cwd: Working directory for subprocess calls (defaults to PROJECT_ROOT).
        timeout: Per-member subprocess timeout in seconds (default: 300).
    """

    def __init__(
        self,
        config: TeamConfig,
        *,
        cwd: Path | str | None = None,
        timeout: int = 300,
    ) -> None:
        self.config = config
        self.cwd = Path(cwd) if cwd else PROJECT_ROOT
        self.timeout = timeout
        # Tracks last broadcast / task assignments for status inspection.
        self._last_broadcast: str = ""
        self._task_log: list[tuple[str, str]] = []
        self._results: list[MemberResult] = []

    # ── Team lifecycle ─────────────────────────────────────────

    def create_team(self, config: TeamConfig) -> None:
        """Reinitialise the orchestrator with a new team configuration.

        Replaces the current config and clears accumulated state.

        Args:
            config: New :class:`TeamConfig` to adopt.
        """
        self.config = config
        self._last_broadcast = ""
        self._task_log = []
        self._results = []

    # ── Task dispatch ─────────────────────────────────────────

    def assign_task(self, member: str | TeamMember, task_description: str) -> MemberResult:
        """Assign a task to a specific team member and block until complete.

        Args:
            member: Either a ``TeamMember`` instance or the agent name string.
            task_description: Natural-language task prompt for the agent.

        Returns:
            :class:`MemberResult` with exit code, stdout, and stderr.
        """
        agent_name = member.agent_name if isinstance(member, TeamMember) else member
        prompt = self._build_prompt(task_description)
        result = self._invoke_agent(agent_name, prompt)
        self._task_log.append((agent_name, task_description))
        self._results.append(result)
        return result

    def broadcast(self, message: str) -> list[MemberResult]:
        """Send the same message to every team member in parallel.

        Args:
            message: Prompt to broadcast to all members simultaneously.

        Returns:
            List of :class:`MemberResult`, one per team member.
        """
        self._last_broadcast = message
        tasks = [(m.agent_name, message) for m in self.config.members]
        return self.run_parallel(tasks)

    def collect_results(self) -> list[MemberResult]:
        """Return the accumulated results from all prior task invocations.

        Results are ordered chronologically by invocation time.

        Returns:
            Shallow copy of the internal results list.
        """
        return list(self._results)

    def run_parallel(self, tasks: list[tuple[str, str]]) -> list[MemberResult]:
        """Run (agent_name, task) pairs in parallel using ThreadPoolExecutor.

        Respects :attr:`TeamConfig.max_parallel` as the thread pool ceiling.
        Results are ordered to match the input ``tasks`` list.

        Args:
            tasks: List of ``(agent_name, task_description)`` pairs.

        Returns:
            List of :class:`MemberResult` in the same order as ``tasks``.
        """
        max_workers = min(self.config.max_parallel, len(tasks)) if tasks else 1
        ordered: list[MemberResult | None] = [None] * len(tasks)

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            # Submit all futures, preserving index for ordering.
            future_to_idx: dict[Any, int] = {}
            for idx, (agent_name, task_desc) in enumerate(tasks):
                prompt = self._build_prompt(task_desc)
                future = pool.submit(self._invoke_agent, agent_name, prompt)
                future_to_idx[future] = idx
                self._task_log.append((agent_name, task_desc))

            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                result: MemberResult = future.result()
                ordered[idx] = result
                self._results.append(result)

        # Satisfy the type checker — all slots are filled after the loop.
        return [r for r in ordered if r is not None]

    # ── Internal helpers ───────────────────────────────────────

    def _build_prompt(self, task_description: str) -> str:
        """Prepend shared_context to a task description when present.

        Args:
            task_description: Raw task prompt.

        Returns:
            Final prompt string to pass to the agent.
        """
        if self.config.shared_context:
            return f"{self.config.shared_context}\n\n{task_description}"
        return task_description

    def _invoke_agent(self, agent_name: str, prompt: str) -> MemberResult:
        """Invoke ``claude --agent-name NAME -p PROMPT`` in a subprocess.

        Auth is inherited from the environment variable
        ``CLAUDE_CODE_OAUTH_TOKEN``.

        Args:
            agent_name: Name matching a .claude/agents/<name>.md file.
            prompt: Full prompt string to pass via ``-p``.

        Returns:
            :class:`MemberResult` populated from subprocess outcome.
        """
        env = {**os.environ}
        # Ensure the token is present in the subprocess environment.
        # The CLI reads CLAUDE_CODE_OAUTH_TOKEN automatically.
        token = env.get("CLAUDE_CODE_OAUTH_TOKEN", "")
        if not token:
            return MemberResult(
                agent_name=agent_name,
                task=prompt,
                returncode=1,
                stdout="",
                stderr="CLAUDE_CODE_OAUTH_TOKEN is not set",
            )

        cmd = ["claude", "--agent-name", agent_name, "-p", prompt]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.cwd),
                env=env,
                timeout=self.timeout,
            )
            return MemberResult(
                agent_name=agent_name,
                task=prompt,
                returncode=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
            )
        except subprocess.TimeoutExpired:
            return MemberResult(
                agent_name=agent_name,
                task=prompt,
                returncode=1,
                stdout="",
                stderr=f"Timeout after {self.timeout}s",
            )
        except FileNotFoundError:
            return MemberResult(
                agent_name=agent_name,
                task=prompt,
                returncode=1,
                stdout="",
                stderr="claude CLI not found — ensure Claude Code is installed",
            )
