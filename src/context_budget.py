"""BL-006: Context window budget tracking.

Tracks token usage across a session and warns before hitting limits.
Wraps Claude Code's context window model (code.claude.com/docs/en/context-window.md).

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ContextBudget:
    """Track context window usage and warn before limits."""

    max_tokens: int = 1_000_000  # Opus 4.6 1M context
    used_tokens: int = 0
    entries: list[dict] = field(default_factory=list)

    @property
    def remaining(self) -> int:
        return max(0, self.max_tokens - self.used_tokens)

    @property
    def usage_pct(self) -> float:
        return self.used_tokens / self.max_tokens if self.max_tokens > 0 else 0.0

    @property
    def needs_compaction(self) -> bool:
        return self.usage_pct > 0.8

    def add(self, label: str, tokens: int) -> None:
        self.entries.append({"label": label, "tokens": tokens})
        self.used_tokens += tokens

    def estimate_file_tokens(self, path: str, char_count: int) -> int:
        return char_count // 4  # ~4 chars per token

    def summary(self) -> dict:
        return {
            "max_tokens": self.max_tokens,
            "used_tokens": self.used_tokens,
            "remaining": self.remaining,
            "usage_pct": f"{self.usage_pct:.1%}",
            "needs_compaction": self.needs_compaction,
            "top_entries": sorted(self.entries, key=lambda e: e["tokens"], reverse=True)[:5],
        }
