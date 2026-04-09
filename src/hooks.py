"""BL-009: Reusable hook library for Claude Code.

Pre-built hooks that extend .claude/settings.json with common automation
patterns. Each hook is a shell command that runs on a Claude Code event.

Hook events (from code.claude.com/docs/en/hooks.md):
  PreToolUse   — before a tool executes
  PostToolUse  — after a tool executes
  Notification — when Claude wants to notify the user
  Stop         — when Claude finishes a turn
  SubagentStop — when a subagent completes

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


@dataclass
class Hook:
    """A reusable Claude Code hook definition."""

    name: str
    event: str  # PreToolUse, PostToolUse, Notification, Stop, SubagentStop
    command: str  # Shell command to run
    description: str = ""
    matcher: str = ""  # Tool name pattern to match (for PreToolUse/PostToolUse)
    timeout: int = 10000  # ms


# ── Pre-built Hook Library ──────────────────────────────────────

HOOKS: dict[str, Hook] = {
    # ── Format on save ──────────────────────────────────────
    "format-python": Hook(
        name="format-python",
        event="PostToolUse",
        command="ruff format $CLAUDE_FILE_PATH 2>/dev/null; ruff check --fix $CLAUDE_FILE_PATH 2>/dev/null",
        description="Auto-format Python files after Claude edits them",
        matcher="write|edit",
    ),
    "format-typescript": Hook(
        name="format-typescript",
        event="PostToolUse",
        command="npx prettier --write $CLAUDE_FILE_PATH 2>/dev/null",
        description="Auto-format TypeScript files after Claude edits them",
        matcher="write|edit",
    ),
    # ── Git safety ──────────────────────────────────────────
    "git-check-untracked": Hook(
        name="git-check-untracked",
        event="Stop",
        command="~/.claude/stop-hook-git-check.sh",
        description="Warn about untracked files when Claude stops",
    ),
    "git-no-force-push": Hook(
        name="git-no-force-push",
        event="PreToolUse",
        command='echo "$CLAUDE_TOOL_INPUT" | grep -q "push.*--force" && echo "BLOCKED: force push" && exit 1 || exit 0',
        description="Block git push --force",
        matcher="bash",
    ),
    # ── Notifications ───────────────────────────────────────
    "notify-desktop": Hook(
        name="notify-desktop",
        event="Notification",
        command='osascript -e \'display notification "$CLAUDE_NOTIFICATION" with title "Claude Code"\'',
        description="macOS desktop notification on Claude events",
    ),
    "notify-slack": Hook(
        name="notify-slack",
        event="Stop",
        command='curl -s -X POST "$SLACK_WEBHOOK_URL" -d "{\"text\": \"Claude finished: $CLAUDE_STOP_REASON\"}" 2>/dev/null',
        description="Post to Slack when Claude finishes",
    ),
    # ── Security ────────────────────────────────────────────
    "block-secrets": Hook(
        name="block-secrets",
        event="PreToolUse",
        command='echo "$CLAUDE_TOOL_INPUT" | grep -qiE "(ANTHROPIC_API_KEY|password|secret|token)" && echo "BLOCKED: potential secret in command" && exit 1 || exit 0',
        description="Block commands that might expose secrets",
        matcher="bash",
    ),
    "audit-file-writes": Hook(
        name="audit-file-writes",
        event="PostToolUse",
        command='echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) WRITE $CLAUDE_FILE_PATH" >> .claude/audit.log',
        description="Log all file writes to an audit trail",
        matcher="write|edit",
    ),
    # ── Quality ─────────────────────────────────────────────
    "lint-on-edit": Hook(
        name="lint-on-edit",
        event="PostToolUse",
        command='case "$CLAUDE_FILE_PATH" in *.py) ruff check "$CLAUDE_FILE_PATH" 2>&1 | head -5;; *.ts|*.tsx) npx tsc --noEmit 2>&1 | head -5;; esac',
        description="Run linter after each file edit",
        matcher="write|edit",
    ),
    "test-on-stop": Hook(
        name="test-on-stop",
        event="Stop",
        command="make test-py 2>&1 | tail -3",
        description="Run tests when Claude finishes a turn",
        timeout=60000,
    ),
    # ── Cost tracking ───────────────────────────────────────
    "log-token-usage": Hook(
        name="log-token-usage",
        event="Stop",
        command='echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) tokens=$CLAUDE_TOKEN_USAGE cost=$CLAUDE_COST" >> .claude/cost.log',
        description="Log token usage and cost per turn",
    ),
    # ── Environment setup ───────────────────────────────────
    "session-start-env": Hook(
        name="session-start-env",
        event="PreToolUse",
        command="scripts/setup-env.sh",
        description="Load environment variables from .env on session start",
        matcher="bash",
    ),
}


def get_hook(name: str) -> Hook | None:
    """Get a hook by name."""
    return HOOKS.get(name)


def list_hooks(event: str = "") -> list[Hook]:
    """List hooks, optionally filtered by event type."""
    hooks = list(HOOKS.values())
    if event:
        hooks = [h for h in hooks if h.event == event]
    return hooks


def install_hook(name: str, settings_path: Path | None = None) -> bool:
    """Install a hook into .claude/settings.json."""
    hook = HOOKS.get(name)
    if not hook:
        return False

    path = settings_path or PROJECT_ROOT / ".claude" / "settings.json"
    if path.exists():
        settings = json.loads(path.read_text())
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})
    event_hooks = hooks.setdefault(hook.event, [])

    # Check if already installed
    for existing in event_hooks:
        if existing.get("command") == hook.command:
            return False  # Already installed

    entry: dict = {"command": hook.command}
    if hook.matcher:
        entry["matcher"] = hook.matcher
    if hook.timeout != 10000:
        entry["timeout"] = hook.timeout

    event_hooks.append(entry)
    path.write_text(json.dumps(settings, indent=2) + "\n")
    return True
