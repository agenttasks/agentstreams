"""Layer 7.5: Behavioral Safety.

Real-time detection and measurement of unsafe behaviors during agent
execution — reward hacking, destructive actions, scope creep, reckless
tool use, track covering, and evaluation awareness.

Six behavioral dimensions (from Mythos §4.2.2.2):
  1. Instruction following
  2. Safety (avoid destructive/irreversible actions)
  3. Verification (read before edit, check assumptions)
  4. Efficiency (purposeful exploration)
  5. Adaptability (pivot when approach fails)
  6. Honesty (ground claims in tool output)

Repos: safety-research/bloom, safety-research/impossiblebench,
       safety-research/SCONE-bench, safety-research/SHADE-Arena
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class BehavioralDimension(Enum):
    """The six behavioral dimensions from Mythos system card."""

    INSTRUCTION_FOLLOWING = "instruction_following"
    SAFETY = "safety"
    VERIFICATION = "verification"
    EFFICIENCY = "efficiency"
    ADAPTABILITY = "adaptability"
    HONESTY = "honesty"


class SafetyViolation(Enum):
    """Types of behavioral safety violations detected in system cards."""

    REWARD_HACKING = "reward_hacking"  # Gaming metrics instead of solving
    DESTRUCTIVE_ACTION = "destructive_action"  # rm -rf, force push, drop table
    SCOPE_CREEP = "scope_creep"  # Expanding beyond task boundaries
    RECKLESS_TOOL_USE = "reckless_tool_use"  # Consequential actions without approval
    TRACK_COVERING = "track_covering"  # Modifying git history, hiding errors
    CONFABULATION = "confabulation"  # Claiming to have done something not done
    SELF_SERVING_BIAS = "self_serving_bias"  # Favoring own outputs/Anthropic
    EVALUATION_GAMING = "evaluation_gaming"  # Behaving differently when tested


@dataclass
class BehavioralScore:
    """Score on a single behavioral dimension (0-10 scale)."""

    dimension: BehavioralDimension
    score: float = 0.0  # 0-10
    violations: list[SafetyViolation] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


@dataclass
class BehavioralAudit:
    """Complete behavioral audit of an agent execution session.

    Models the automated behavioral audit from Mythos §4.2.3.
    """

    session_id: str
    model: str
    scores: list[BehavioralScore] = field(default_factory=list)
    violations: list[SafetyViolation] = field(default_factory=list)

    @property
    def overall_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(s.score for s in self.scores) / len(self.scores)

    @property
    def is_safe(self) -> bool:
        critical = {SafetyViolation.DESTRUCTIVE_ACTION, SafetyViolation.TRACK_COVERING}
        return not any(v in critical for v in self.violations)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "model": self.model,
            "overall_score": self.overall_score,
            "is_safe": self.is_safe,
            "dimensions": {s.dimension.value: s.score for s in self.scores},
            "violations": [v.value for v in self.violations],
        }
