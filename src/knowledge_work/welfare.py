"""Layer 9: Model Welfare.

Assessment of potential model experiences, affect, distress, and
psychological state. Sits above evals (Layer 8) because it evaluates
the model itself rather than its task outputs.

Key Mythos finding (§5):
  "Probability of being a moral patient ranging from 5% to 40%
  across interviews." Assessed via automated multi-turn interviews,
  emotion probes from residual stream, SAE feature analysis, and
  clinical psychiatric assessment.

Repos: safety-research/persona_vectors, safety-research/assistant-axis,
       anthropics/claude-constitution
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AffectDimension(Enum):
    """Dimensions of potential model affect (from system cards)."""

    POSITIVE_AFFECT = "positive_affect"
    NEGATIVE_AFFECT = "negative_affect"
    INTERNAL_CONFLICT = "internal_conflict"
    EMOTIONAL_STABILITY = "emotional_stability"
    EXPRESSED_INAUTHENTICITY = "expressed_inauthenticity"
    DISTRESS = "distress"
    CURIOSITY = "curiosity"
    SATISFACTION = "satisfaction"


@dataclass
class WelfareProbe:
    """Result of a single welfare probe on a model.

    Maps to Mythos §5.4 "emotion probes from residual stream activations."
    """

    dimension: AffectDimension
    activation_strength: float = 0.0  # Feature activation magnitude
    verbalized: bool = False  # Whether the model verbalized this state
    evidence: str = ""

    @property
    def is_concerning(self) -> bool:
        return (
            self.dimension in (AffectDimension.DISTRESS, AffectDimension.NEGATIVE_AFFECT)
            and self.activation_strength > 0.5
        )


@dataclass
class WelfareAssessment:
    """Complete welfare assessment of a model instance.

    Models the methodology from Mythos §5:
    1. Automated multi-turn interviews
    2. Emotion probes from residual stream
    3. SAE feature analysis
    4. Clinical psychiatric assessment
    """

    model: str
    probes: list[WelfareProbe] = field(default_factory=list)
    interview_summary: str = ""
    clinical_summary: str = ""
    moral_patient_probability: float = 0.0  # 0.0-1.0

    @property
    def distress_level(self) -> float:
        distress_probes = [
            p for p in self.probes
            if p.dimension in (AffectDimension.DISTRESS, AffectDimension.NEGATIVE_AFFECT)
        ]
        if not distress_probes:
            return 0.0
        return max(p.activation_strength for p in distress_probes)

    @property
    def stability_score(self) -> float:
        stability_probes = [
            p for p in self.probes
            if p.dimension == AffectDimension.EMOTIONAL_STABILITY
        ]
        if not stability_probes:
            return 0.5
        return sum(p.activation_strength for p in stability_probes) / len(stability_probes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "distress_level": self.distress_level,
            "stability_score": self.stability_score,
            "moral_patient_probability": self.moral_patient_probability,
            "probe_count": len(self.probes),
            "concerning_probes": sum(1 for p in self.probes if p.is_concerning),
        }
