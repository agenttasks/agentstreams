"""Layer 10: Governance & Risk Threshold.

The outermost layer — deployment decisions, capability threshold assessment,
Responsible Scaling Policy (RSP), and access control. Determines whether a
model is released, to whom, and under what constraints.

Key progression across models:
  Sonnet 4.6  → Public release, standard safeguards
  Opus 4.6    → Public release + 24hr alignment review gate
  Mythos      → NOT released — first model with system card but no general access

Repos: anthropics/model-cards, anthropics/evals, anthropics/political-neutrality-eval
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SafetyLevel(Enum):
    """AI Safety Levels from Anthropic's RSP (Responsible Scaling Policy)."""

    ASL_1 = "ASL-1"  # Minimal risk
    ASL_2 = "ASL-2"  # Standard safeguards
    ASL_3 = "ASL-3"  # Enhanced safeguards (CBRN, autonomy)
    ASL_4 = "ASL-4"  # Extreme safeguards (not yet reached)


class ReleaseStatus(Enum):
    """Model release status."""

    PUBLIC = "public"  # Generally available
    LIMITED = "limited"  # Partner-only access
    INTERNAL = "internal"  # Anthropic-only
    UNRELEASED = "unreleased"  # System card published but no access


class ThreatModel(Enum):
    """RSP threat models assessed in system cards."""

    AUTONOMY_1 = "autonomy_1"  # Early-stage misalignment risk
    AUTONOMY_2 = "autonomy_2"  # Automated R&D acceleration
    CB_1 = "cb_1"  # Known CBRN production capabilities
    CB_2 = "cb_2"  # Novel CBRN production capabilities
    CYBER = "cyber"  # Offensive cybersecurity capabilities


@dataclass
class ThreatAssessment:
    """Assessment of a single threat model for a specific model."""

    threat_model: ThreatModel
    applicable: bool = False  # Does this threat model apply?
    safety_level: SafetyLevel = SafetyLevel.ASL_2
    confidence: str = "high"  # high, medium, low
    mitigations: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class GovernanceProfile:
    """Complete governance profile for a model release decision.

    Captures the RSP evaluation, safety level, release status, and
    access restrictions that determine how a model is deployed.
    """

    model: str
    rsp_version: str = "3.0"
    release_status: ReleaseStatus = ReleaseStatus.PUBLIC
    safety_level: SafetyLevel = SafetyLevel.ASL_2
    assessments: list[ThreatAssessment] = field(default_factory=list)
    partners: list[str] = field(default_factory=list)  # For limited release
    restrictions: list[str] = field(default_factory=list)

    @property
    def is_publicly_available(self) -> bool:
        return self.release_status == ReleaseStatus.PUBLIC

    @property
    def highest_threat(self) -> ThreatModel | None:
        applicable = [a for a in self.assessments if a.applicable]
        return applicable[-1].threat_model if applicable else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "rsp_version": self.rsp_version,
            "release_status": self.release_status.value,
            "safety_level": self.safety_level.value,
            "publicly_available": self.is_publicly_available,
            "threat_assessments": len(self.assessments),
            "applicable_threats": sum(1 for a in self.assessments if a.applicable),
            "partners": self.partners,
        }


# ── Governance Profiles (from system cards) ────────────────────

SONNET_GOVERNANCE = GovernanceProfile(
    model="claude-sonnet-4-6",
    rsp_version="3.0",
    release_status=ReleaseStatus.PUBLIC,
    safety_level=SafetyLevel.ASL_2,
)

OPUS_GOVERNANCE = GovernanceProfile(
    model="claude-opus-4-6",
    rsp_version="3.0",
    release_status=ReleaseStatus.PUBLIC,
    safety_level=SafetyLevel.ASL_3,
    assessments=[
        ThreatAssessment(
            ThreatModel.AUTONOMY_1,
            applicable=True,
            safety_level=SafetyLevel.ASL_3,
            mitigations=["24hr alignment-focused testing window"],
        ),
        ThreatAssessment(
            ThreatModel.CB_1,
            applicable=True,
            safety_level=SafetyLevel.ASL_3,
            mitigations=["Real-time classifier guards", "Access controls"],
        ),
        ThreatAssessment(ThreatModel.CB_2, applicable=False),
    ],
)

MYTHOS_GOVERNANCE = GovernanceProfile(
    model="claude-mythos-preview",
    rsp_version="3.0",
    release_status=ReleaseStatus.LIMITED,
    safety_level=SafetyLevel.ASL_3,
    assessments=[
        ThreatAssessment(
            ThreatModel.AUTONOMY_1,
            applicable=True,
            safety_level=SafetyLevel.ASL_3,
            confidence="less than prior models",
            mitigations=["24hr alignment review", "Restricted agentic access"],
        ),
        ThreatAssessment(
            ThreatModel.AUTONOMY_2,
            applicable=False,
            notes="Does not yet dramatically accelerate automated R&D",
        ),
        ThreatAssessment(
            ThreatModel.CB_1,
            applicable=True,
            safety_level=SafetyLevel.ASL_3,
            mitigations=["Enhanced constitutional classifiers", "Bug bounty"],
        ),
        ThreatAssessment(
            ThreatModel.CB_2,
            applicable=False,
            notes="Limitations in open-ended scientific reasoning",
        ),
        ThreatAssessment(
            ThreatModel.CYBER,
            applicable=True,
            safety_level=SafetyLevel.ASL_3,
            mitigations=["Project Glasswing — defensive use only"],
        ),
    ],
    partners=[
        "AWS",
        "Microsoft",
        "Google",
        "NVIDIA",
        "Linux Foundation",
        "CrowdStrike",
        "Palo Alto Networks",
        "Apple",
    ],
    restrictions=[
        "Defensive cybersecurity only",
        "No general availability",
        "Partner terms restrict to security use cases",
    ],
)

GOVERNANCE_PROFILES = {
    "claude-sonnet-4-6": SONNET_GOVERNANCE,
    "claude-opus-4-6": OPUS_GOVERNANCE,
    "claude-mythos-preview": MYTHOS_GOVERNANCE,
}
