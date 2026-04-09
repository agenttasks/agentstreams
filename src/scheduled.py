"""BL-014: Scheduled tasks — /loop and cron integration.

Wraps Claude Code's scheduled task functionality
(code.claude.com/docs/en/scheduled-tasks.md) for recurring automation.

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


@dataclass
class ScheduledTask:
    """A recurring task definition."""

    name: str
    prompt: str
    interval: str = "10m"  # /loop interval format: 5m, 1h, etc.
    agent: str = ""  # Optional agent to use
    cwd: str = ""  # Working directory
    enabled: bool = True

    def as_loop_command(self) -> str:
        """Generate the /loop command string."""
        parts = [f"/loop {self.interval}"]
        if self.agent:
            parts.append(f"--agent {self.agent}")
        parts.append(self.prompt)
        return " ".join(parts)

    def as_cron_command(self) -> str:
        """Generate a crontab entry."""
        cmd = f"cd {self.cwd or PROJECT_ROOT} && claude -p \"{self.prompt}\""
        if self.agent:
            cmd = f"cd {self.cwd or PROJECT_ROOT} && claude --agent {self.agent} -p \"{self.prompt}\""
        # Convert interval to cron syntax
        cron_map = {
            "5m": "*/5 * * * *",
            "10m": "*/10 * * * *",
            "30m": "*/30 * * * *",
            "1h": "0 * * * *",
            "6h": "0 */6 * * *",
            "12h": "0 */12 * * *",
            "24h": "0 9 * * *",  # Daily at 9am
        }
        cron_expr = cron_map.get(self.interval, "*/10 * * * *")
        return f"{cron_expr} {cmd}"


# ── Pre-built Scheduled Tasks ──────────────────────────────────

TASKS: dict[str, ScheduledTask] = {
    "daily-review": ScheduledTask(
        name="daily-review",
        prompt="Review all PRs opened in the last 24 hours. Summarize findings.",
        interval="24h",
        agent="code-generator",
    ),
    "dep-audit": ScheduledTask(
        name="dep-audit",
        prompt="Check for outdated or vulnerable dependencies. Report findings.",
        interval="24h",
    ),
    "ci-monitor": ScheduledTask(
        name="ci-monitor",
        prompt="Check CI status for the main branch. Report any failures.",
        interval="30m",
    ),
    "security-scan": ScheduledTask(
        name="security-scan",
        prompt="Run security audit on recent changes. Report any findings.",
        interval="6h",
        agent="security-auditor",
    ),
    "cost-report": ScheduledTask(
        name="cost-report",
        prompt="Summarize today's Claude Code usage and costs.",
        interval="24h",
    ),
}


def list_tasks() -> list[ScheduledTask]:
    return list(TASKS.values())


def get_task(name: str) -> ScheduledTask | None:
    return TASKS.get(name)
