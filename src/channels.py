"""Channel integration for Claude Code sessions.

Wraps Claude Code's channel integration for pushing events into active
sessions via MCP.  A channel is a named event stream — CI failures,
GitHub webhooks, Slack messages, or any custom source — that can be
registered with ChannelBridge and forwarded into the running agent loop.

Pre-built configs (CI_CHANNEL, GITHUB_CHANNEL, SLACK_CHANNEL) cover the
most common integration surfaces.

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

# ── Enums ──────────────────────────────────────────────────────


class SourceType(Enum):
    """Channel source classification."""

    WEBHOOK = "webhook"
    CI = "ci"
    CHAT = "chat"
    CUSTOM = "custom"


# ── Dataclasses ─────────────────────────────────────────────────


@dataclass
class ChannelConfig:
    """Configuration for a registered channel.

    Args:
        channel_name: Unique name for this channel (e.g., "ci-failures").
        source_type: Where events originate (webhook, ci, chat, custom).
        filter_pattern: Optional glob/regex pattern to filter incoming
            payloads.  Empty string means accept all.
    """

    channel_name: str
    source_type: SourceType
    filter_pattern: str = ""


@dataclass
class ChannelMessage:
    """A single event pushed through a channel.

    Args:
        source: Channel name or originating service (e.g., "github").
        type: Event type string (e.g., "ci.failure", "pr.comment").
        payload: Arbitrary event data.
        timestamp: ISO-8601 UTC timestamp; defaults to now.
    """

    source: str
    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_json(self) -> str:
        """Serialise the message to a compact JSON string."""
        return json.dumps(
            {
                "source": self.source,
                "type": self.type,
                "payload": self.payload,
                "timestamp": self.timestamp,
            },
            separators=(",", ":"),
        )


# ── ChannelBridge ───────────────────────────────────────────────


class ChannelBridge:
    """Bridge that manages channel registrations and event delivery.

    Channels are registered once; events are pushed into the active
    Claude Code session by invoking ``claude mcp`` over subprocess so
    the same CLAUDE_CODE_OAUTH_TOKEN flow is respected.

    Example::

        bridge = ChannelBridge()
        bridge.register(CI_CHANNEL)
        msg = bridge.on_ci_failure(webhook_payload)
        bridge.push(msg)
    """

    def __init__(self) -> None:
        self._channels: dict[str, ChannelConfig] = {}

    # ── Registration ────────────────────────────────────────────

    def register(self, config: ChannelConfig) -> None:
        """Register a channel configuration.

        Args:
            config: Channel config to register.  Overwrites any existing
                registration with the same channel_name.
        """
        self._channels[config.channel_name] = config

    def registered_channels(self) -> list[ChannelConfig]:
        """Return all currently registered channel configs."""
        return list(self._channels.values())

    # ── Push ────────────────────────────────────────────────────

    def push(self, message: ChannelMessage) -> subprocess.CompletedProcess[str]:
        """Push an event into the active Claude Code session.

        Invokes ``claude mcp send-event`` so the session receives the
        message as a structured MCP event.  The channel must be registered
        before pushing; if the source does not match a registered channel
        the message is still forwarded (channel acts as pass-through).

        Args:
            message: The event to push.

        Returns:
            CompletedProcess from the ``claude`` subprocess call.

        Raises:
            FileNotFoundError: If ``claude`` CLI is not on PATH.
        """
        token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
        env = {**os.environ, "CLAUDE_CODE_OAUTH_TOKEN": token}

        cmd = [
            "claude",
            "mcp",
            "send-event",
            "--channel",
            message.source,
            "--type",
            message.type,
            "--data",
            message.to_json(),
        ]

        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
        )

    # ── Webhook parsers ─────────────────────────────────────────

    def on_ci_failure(self, webhook_payload: dict[str, Any]) -> ChannelMessage:
        """Parse a CI failure webhook into a ChannelMessage.

        Extracts the branch, commit SHA, failed job names, and a log URL
        from a generic CI webhook payload (compatible with GitHub Actions
        and CircleCI schema shapes).

        Args:
            webhook_payload: Raw webhook body as a dict.

        Returns:
            ChannelMessage with type ``ci.failure``.
        """
        # Normalise across GitHub Actions / CircleCI / generic shapes
        branch = (
            webhook_payload.get("branch")
            or webhook_payload.get("head_branch")
            or webhook_payload.get("ref", "").removeprefix("refs/heads/")
        )
        commit = (
            webhook_payload.get("sha")
            or webhook_payload.get("head_sha")
            or webhook_payload.get("after", "")
        )
        failed_jobs: list[str] = []
        for job in webhook_payload.get("workflow_run", {}).get("jobs", []):
            if job.get("conclusion") == "failure":
                failed_jobs.append(job.get("name", "unknown"))
        if not failed_jobs:
            # Fallback: top-level job name field
            name = webhook_payload.get("job", {}).get("name") or webhook_payload.get("name", "")
            if name:
                failed_jobs = [name]

        log_url = (
            webhook_payload.get("workflow_run", {}).get("html_url")
            or webhook_payload.get("build_url")
            or webhook_payload.get("url", "")
        )

        return ChannelMessage(
            source="ci",
            type="ci.failure",
            payload={
                "branch": branch,
                "commit": commit[:12] if commit else "",
                "failed_jobs": failed_jobs,
                "log_url": log_url,
                "raw": webhook_payload,
            },
        )

    def on_pr_comment(self, webhook_payload: dict[str, Any]) -> ChannelMessage:
        """Parse a GitHub PR comment webhook into a ChannelMessage.

        Args:
            webhook_payload: Raw GitHub ``pull_request_review_comment``
                or ``issue_comment`` webhook body.

        Returns:
            ChannelMessage with type ``pr.comment``.
        """
        comment = webhook_payload.get("comment", {})
        pull_request = webhook_payload.get("pull_request", {})
        repo = webhook_payload.get("repository", {})

        return ChannelMessage(
            source="github",
            type="pr.comment",
            payload={
                "pr_number": pull_request.get("number")
                or webhook_payload.get("issue", {}).get("number"),
                "pr_title": pull_request.get("title", ""),
                "repo": repo.get("full_name", ""),
                "author": comment.get("user", {}).get("login", ""),
                "body": comment.get("body", ""),
                "comment_url": comment.get("html_url", ""),
                "raw": webhook_payload,
            },
        )

    def on_chat_message(self, message: str) -> ChannelMessage:
        """Wrap a plain chat message string into a ChannelMessage.

        Args:
            message: Human-authored chat text (e.g., from Slack or Teams).

        Returns:
            ChannelMessage with type ``chat.message``.
        """
        return ChannelMessage(
            source="chat",
            type="chat.message",
            payload={"text": message},
        )


# ── Pre-built channel configs ────────────────────────────────────

CI_CHANNEL = ChannelConfig(
    channel_name="ci-failures",
    source_type=SourceType.CI,
    filter_pattern="ci.*",
)

GITHUB_CHANNEL = ChannelConfig(
    channel_name="github-events",
    source_type=SourceType.WEBHOOK,
    filter_pattern="pr.*",
)

SLACK_CHANNEL = ChannelConfig(
    channel_name="slack-messages",
    source_type=SourceType.CHAT,
    filter_pattern="chat.*",
)
