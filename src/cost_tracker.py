"""BL-007: Per-session cost tracking.

Tracks token usage and estimated costs across sessions, persisting
to a local log file and optionally to Neon Postgres.

Pricing (as of April 2026):
  claude-opus-4-6:   $15/M input, $75/M output
  claude-sonnet-4-6: $3/M input, $15/M output
  claude-haiku-4-5:  $0.80/M input, $4/M output

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
COST_LOG = PROJECT_ROOT / ".claude" / "cost.log"

PRICING = {
    "claude-opus-4-6": {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.0},
    "claude-mythos-preview": {"input": 15.0, "output": 75.0},
}


@dataclass
class UsageEntry:
    timestamp: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    session_id: str = ""
    task: str = ""


@dataclass
class CostTracker:
    entries: list[UsageEntry] = field(default_factory=list)

    def record(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        session_id: str = "",
        task: str = "",
    ) -> UsageEntry:
        pricing = PRICING.get(model, PRICING["claude-sonnet-4-6"])
        cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000

        entry = UsageEntry(
            timestamp=datetime.now(UTC).isoformat(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=round(cost, 6),
            session_id=session_id,
            task=task,
        )
        self.entries.append(entry)
        return entry

    @property
    def total_cost(self) -> float:
        return sum(e.cost_usd for e in self.entries)

    @property
    def total_tokens(self) -> int:
        return sum(e.input_tokens + e.output_tokens for e in self.entries)

    def by_model(self) -> dict[str, float]:
        costs: dict[str, float] = {}
        for e in self.entries:
            costs[e.model] = costs.get(e.model, 0.0) + e.cost_usd
        return costs

    def save(self, path: Path | None = None) -> None:
        p = path or COST_LOG
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a") as f:
            for e in self.entries:
                f.write(
                    json.dumps(
                        {
                            "ts": e.timestamp,
                            "model": e.model,
                            "in": e.input_tokens,
                            "out": e.output_tokens,
                            "cost": e.cost_usd,
                            "session": e.session_id,
                            "task": e.task,
                        }
                    )
                    + "\n"
                )

    @classmethod
    def load(cls, path: Path | None = None) -> CostTracker:
        p = path or COST_LOG
        tracker = cls()
        if p.exists():
            for line in p.read_text().strip().split("\n"):
                if line:
                    d = json.loads(line)
                    tracker.entries.append(
                        UsageEntry(
                            timestamp=d["ts"],
                            model=d["model"],
                            input_tokens=d["in"],
                            output_tokens=d["out"],
                            cost_usd=d["cost"],
                            session_id=d.get("session", ""),
                            task=d.get("task", ""),
                        )
                    )
        return tracker

    def summary(self) -> dict:
        return {
            "total_cost_usd": round(self.total_cost, 4),
            "total_tokens": self.total_tokens,
            "entries": len(self.entries),
            "by_model": {k: round(v, 4) for k, v in self.by_model().items()},
        }
