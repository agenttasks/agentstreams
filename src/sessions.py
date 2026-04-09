"""Claude Code session lifecycle manager for the agentstreams toolkit.

Wraps Claude Code CLI (v2.1.97+) session continue/resume/fork capabilities
into a typed Python interface for use in knowledge-work pipelines.

The claude CLI owns the agent loop. This module wraps it via subprocess,
parsing JSONL transcripts at ~/.claude/projects/{project}/{sessionId}/ to
provide list_sessions and get_session_events without re-implementing any
agent logic.

Session ID lifecycle (via CLI flags):
    --continue              Resume the most-recent session (current dir)
    --resume <id|name>      Resume a specific session by ID or name
    --resume <id> --fork-session   Branch into a new session ID
    --output-format json    Emits {"session_id": "...", "result": "..."} on stdout

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# ── Data classes ───────────────────────────────────────────────


@dataclass
class SessionInfo:
    """Metadata for a single Claude Code session."""

    session_id: str
    project_path: str
    transcript_path: str
    message_count: int
    last_updated: datetime
    display_name: str = ""

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation."""
        return {
            "session_id": self.session_id,
            "project_path": self.project_path,
            "transcript_path": self.transcript_path,
            "message_count": self.message_count,
            "last_updated": self.last_updated.isoformat(),
            "display_name": self.display_name,
        }


@dataclass
class SessionEvent:
    """A single entry from a session JSONL transcript."""

    index: int
    event_type: str  # "user", "assistant", "tool_use", "tool_result", "system"
    content: str
    raw: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation."""
        return {
            "index": self.index,
            "event_type": self.event_type,
            "content": self.content,
        }


@dataclass
class SessionRunResult:
    """Result of a session lifecycle call (continue/resume/fork)."""

    session_id: str
    result: str
    cost_usd: float = 0.0
    duration_ms: int = 0
    raw: dict[str, Any] = field(default_factory=dict)


# ── Helpers ────────────────────────────────────────────────────


def _claude_projects_root() -> Path:
    """Return ~/.claude/projects, the root of all session transcripts."""
    return Path.home() / ".claude" / "projects"


def _transcript_path_for(session_id: str) -> Path | None:
    """Locate the main JSONL transcript for a given session_id.

    Claude Code stores transcripts at:
        ~/.claude/projects/{url-encoded-project-path}/{session_id}/
            {session_id}.jsonl   (or messages.jsonl in older versions)

    This walks the projects root and returns the first match.
    """
    root = _claude_projects_root()
    if not root.exists():
        return None
    # Search all project dirs for the session subdirectory
    for project_dir in root.iterdir():
        if not project_dir.is_dir():
            continue
        session_dir = project_dir / session_id
        if session_dir.is_dir():
            # Prefer explicit {session_id}.jsonl, fall back to messages.jsonl
            for name in (f"{session_id}.jsonl", "messages.jsonl"):
                candidate = session_dir / name
                if candidate.exists():
                    return candidate
            # Fall back to any .jsonl in the session dir
            candidates = list(session_dir.glob("*.jsonl"))
            if candidates:
                return sorted(candidates, key=lambda p: p.stat().st_mtime)[-1]
    return None


def _parse_transcript(path: Path) -> list[SessionEvent]:
    """Parse a JSONL transcript file into SessionEvent objects.

    Each line is a JSON object.  Claude Code uses a mix of formats across
    versions; we normalise the common fields that are useful for display.
    """
    events: list[SessionEvent] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return events

    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Determine event type
        role = obj.get("role", "")
        msg_type = obj.get("type", "")

        if role == "user":
            event_type = "user"
        elif role == "assistant":
            event_type = "assistant"
        elif msg_type in ("tool_use", "tool_result"):
            event_type = msg_type
        elif msg_type == "system":
            event_type = "system"
        else:
            event_type = role or msg_type or "unknown"

        # Extract readable content
        content_raw = obj.get("content", "")
        if isinstance(content_raw, str):
            content = content_raw
        elif isinstance(content_raw, list):
            # Array of content blocks — join text blocks
            parts: list[str] = []
            for block in content_raw:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        parts.append(block.get("text", ""))
                    elif block.get("type") == "tool_use":
                        parts.append(f"[tool: {block.get('name', '?')}]")
                    elif block.get("type") == "tool_result":
                        inner = block.get("content", "")
                        if isinstance(inner, list):
                            inner = " ".join(
                                b.get("text", "") for b in inner if isinstance(b, dict)
                            )
                        parts.append(f"[result: {str(inner)[:120]}]")
            content = " ".join(parts)
        else:
            content = str(content_raw)

        events.append(SessionEvent(index=idx, event_type=event_type, content=content, raw=obj))

    return events


def _run_claude(
    args: list[str],
    *,
    prompt: str = "Acknowledge session continuation.",
    cwd: Path | None = None,
) -> SessionRunResult:
    """Invoke the claude CLI in print mode and parse JSON output.

    Args:
        args:   Extra CLI flags (e.g. ["--resume", session_id]).
        prompt: The -p prompt text sent to Claude.
        cwd:    Working directory for the subprocess (defaults to cwd of the
                current process so Claude picks up the right project context).

    Returns:
        SessionRunResult with session_id, result text, and cost metadata.

    Raises:
        RuntimeError: If claude is not found on PATH or returns a non-zero exit.
    """
    env = os.environ.copy()

    # Ensure auth token is present — never fall back to ANTHROPIC_API_KEY
    if not env.get("CLAUDE_CODE_OAUTH_TOKEN"):
        raise RuntimeError(
            "CLAUDE_CODE_OAUTH_TOKEN is not set. "
            "Set it before calling SessionManager methods."
        )

    cmd = [
        "claude",
        "-p", prompt,
        "--output-format", "json",
    ] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(cwd or Path.cwd()),
            env=env,
            timeout=300,  # 5-minute safety timeout
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "claude CLI not found on PATH. "
            "Install it with: npm install -g @anthropic-ai/claude-agent-sdk"
        ) from exc

    if result.returncode != 0:
        raise RuntimeError(
            f"claude exited with code {result.returncode}.\n"
            f"stderr: {result.stderr[:1000]}"
        )

    # claude --output-format json writes one JSON object to stdout
    stdout = result.stdout.strip()
    if not stdout:
        raise RuntimeError("claude produced no output. Is the session valid?")

    # Handle stream-json: take the last complete line that has session_id
    parsed: dict[str, Any] = {}
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if "session_id" in obj or "result" in obj:
                parsed = obj
                break
        except json.JSONDecodeError:
            continue

    if not parsed:
        # Fallback: try the whole stdout as one JSON object
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Could not parse claude output as JSON: {stdout[:500]}"
            ) from exc

    return SessionRunResult(
        session_id=parsed.get("session_id", ""),
        result=parsed.get("result", ""),
        cost_usd=parsed.get("cost_usd", 0.0),
        duration_ms=int(parsed.get("duration_ms", 0)),
        raw=parsed,
    )


# ── SessionManager ─────────────────────────────────────────────


class SessionManager:
    """Wraps the Claude Code CLI session lifecycle for agentstreams pipelines.

    All methods delegate agent execution to the claude CLI binary;
    this class manages the invocation flags, output parsing, and
    transcript indexing only.

    Auth: reads CLAUDE_CODE_OAUTH_TOKEN from environment automatically.
    The sdk constructors (Anthropic()) also read it automatically, but
    session management here goes via subprocess, not the SDK client.

    Example:
        sm = SessionManager()
        result = sm.continue_session()
        events = sm.get_session_events(result.session_id)
    """

    def __init__(self, *, cwd: Path | None = None) -> None:
        """Create a SessionManager.

        Args:
            cwd: Project working directory used for all subprocess calls.
                 Defaults to the current process working directory, which
                 determines which session is "most recent" for --continue.
        """
        self.cwd = cwd or Path.cwd()

    # ── Core lifecycle methods ─────────────────────────────────

    def continue_session(
        self,
        *,
        prompt: str = "Acknowledge session continuation.",
    ) -> SessionRunResult:
        """Resume the most-recent session in the current directory.

        Equivalent to: claude -p <prompt> --continue --output-format json

        Args:
            prompt: The message sent to Claude on resumption.

        Returns:
            SessionRunResult containing the new session_id and response.
        """
        return _run_claude(["--continue"], prompt=prompt, cwd=self.cwd)

    def resume_session(
        self,
        session_id: str,
        *,
        prompt: str = "Acknowledge session resumption.",
    ) -> SessionRunResult:
        """Resume a specific session from its last message.

        Equivalent to: claude -p <prompt> --resume <session_id> --output-format json

        Args:
            session_id: UUID or display name of the session to resume.
            prompt:     The message sent to Claude on resumption.

        Returns:
            SessionRunResult — note the returned session_id will match
            session_id (the original is reused unless --fork-session is set).
        """
        return _run_claude(["--resume", session_id], prompt=prompt, cwd=self.cwd)

    def fork_session(
        self,
        session_id: str,
        *,
        prompt: str = "Acknowledge session fork.",
    ) -> SessionRunResult:
        """Branch from an existing session into a fresh session ID.

        Equivalent to:
            claude -p <prompt> --resume <session_id> --fork-session --output-format json

        The original session is left intact.  The returned SessionRunResult
        carries the newly-minted session_id for the fork.

        Args:
            session_id: UUID or display name of the session to fork from.
            prompt:     The initial message sent in the new forked session.

        Returns:
            SessionRunResult with a new session_id distinct from session_id.
        """
        return _run_claude(
            ["--resume", session_id, "--fork-session"],
            prompt=prompt,
            cwd=self.cwd,
        )

    # ── Introspection methods ──────────────────────────────────

    def list_sessions(self, *, limit: int = 50) -> list[SessionInfo]:
        """List recent Claude Code sessions by scanning JSONL transcripts.

        Walks ~/.claude/projects/{project}/ for session directories whose
        project path URL-decodes to the current cwd (or any project if cwd
        is not matched).  Sessions are sorted by last-modified time,
        newest first.

        Args:
            limit: Maximum number of sessions to return.

        Returns:
            List of SessionInfo objects ordered by recency.
        """
        root = _claude_projects_root()
        if not root.exists():
            return []

        sessions: list[SessionInfo] = []

        for project_dir in root.iterdir():
            if not project_dir.is_dir():
                continue

            # Decode the URL-encoded project path stored as the directory name
            from urllib.parse import unquote
            project_path = unquote(project_dir.name)

            for session_dir in project_dir.iterdir():
                if not session_dir.is_dir():
                    continue
                session_id = session_dir.name

                # Find the transcript file
                transcript: Path | None = None
                for name in (f"{session_id}.jsonl", "messages.jsonl"):
                    candidate = session_dir / name
                    if candidate.exists():
                        transcript = candidate
                        break
                if transcript is None:
                    candidates = list(session_dir.glob("*.jsonl"))
                    if candidates:
                        transcript = sorted(
                            candidates, key=lambda p: p.stat().st_mtime
                        )[-1]
                if transcript is None:
                    continue

                stat = transcript.stat()
                last_updated = datetime.fromtimestamp(stat.st_mtime)

                # Count non-empty lines as a proxy for message count
                try:
                    lines = [
                        line for line in transcript.read_text(encoding="utf-8").splitlines()
                        if line.strip()
                    ]
                    message_count = len(lines)
                except OSError:
                    message_count = 0

                # Try to find a display name from the first system event
                display_name = _extract_display_name(transcript)

                sessions.append(
                    SessionInfo(
                        session_id=session_id,
                        project_path=project_path,
                        transcript_path=str(transcript),
                        message_count=message_count,
                        last_updated=last_updated,
                        display_name=display_name,
                    )
                )

        sessions.sort(key=lambda s: s.last_updated, reverse=True)
        return sessions[:limit]

    def get_session_events(
        self,
        session_id: str,
        *,
        event_types: list[str] | None = None,
    ) -> list[SessionEvent]:
        """Return parsed events from a session's JSONL transcript.

        Args:
            session_id:  UUID of the session.
            event_types: Optional filter list (e.g. ["user", "assistant"]).
                         Pass None to return all event types.

        Returns:
            List of SessionEvent objects in transcript order.

        Raises:
            FileNotFoundError: If no transcript can be found for session_id.
        """
        path = _transcript_path_for(session_id)
        if path is None:
            raise FileNotFoundError(
                f"No transcript found for session {session_id!r}. "
                f"Sessions are stored at {_claude_projects_root()}."
            )

        events = _parse_transcript(path)
        if event_types is not None:
            events = [e for e in events if e.event_type in event_types]
        return events


# ── Private helpers ────────────────────────────────────────────


def _extract_display_name(transcript: Path) -> str:
    """Attempt to extract a human-readable display name from a transcript.

    Claude Code records the session name (set via --name or /rename) in a
    system event.  We read the first few lines to find it cheaply.
    """
    try:
        with transcript.open(encoding="utf-8") as fh:
            for _ in range(20):
                line = fh.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Check several possible locations for the name
                for key in ("session_name", "name", "display_name"):
                    val = obj.get(key, "")
                    if val and isinstance(val, str):
                        return val
    except OSError:
        pass
    return ""
