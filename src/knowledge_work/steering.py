"""Layer 1.5: Steering & Intervention.

Active manipulation of model behavior through internal representations.
Sits between circuits (Layer 1, passive observation) and tracers (Layer 2,
attribution) — this layer performs interventions using the same feature
representations that circuits describe.

Progression across models (from system cards):
  Opus 4.6  → Evaluation awareness vectors inhibited (§6.5)
  Mythos    → Emotion probes + activation steering + SAE feature interventions

Repos: safety-research/persona_vectors, safety-research/assistant-axis,
       decoderesearch/circuit-tracer
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class SteeringMethod(Enum):
    """Methods for steering model behavior via internal representations."""

    ACTIVATION_ADDITION = "activation_addition"  # Add vector to residual stream
    ACTIVATION_INHIBITION = "inhibition"  # Subtract/negate vector
    FEATURE_CLAMPING = "feature_clamping"  # Set specific SAE feature to value
    CONTRASTIVE_VECTOR = "contrastive"  # Difference between two behavior prompts
    PERSONA_VECTOR = "persona_vector"  # Character trait direction in activation space


class SteeringTarget(Enum):
    """What behavioral dimension to steer."""

    SYCOPHANCY = "sycophancy"
    EVALUATION_AWARENESS = "evaluation_awareness"
    ASSERTIVENESS = "assertiveness"
    EMPATHY = "empathy"
    TECHNICAL_DEPTH = "technical_depth"
    REFUSAL = "refusal"
    CREATIVITY = "creativity"
    CAUTION = "caution"


@dataclass
class SteeringVector:
    """A direction in activation space that modifies model behavior.

    From safety-research/persona_vectors and circuit-tracer interventions.
    """

    name: str
    target: SteeringTarget
    method: SteeringMethod
    layer: int  # Which model layer to intervene at
    strength: float = 1.0  # Scaling factor for the intervention
    description: str = ""

    def as_intervention(self, position: int, feature_idx: int) -> tuple[int, int, int, float]:
        """Convert to circuit-tracer intervention format.

        Returns: (layer, position, feature_idx, value)
        """
        return (self.layer, position, feature_idx, self.strength)


@dataclass
class SteeringConfig:
    """Configuration for applying steering vectors during task execution.

    Enables task-appropriate personality tuning: empathetic for customer
    support, assertive for code review, cautious for legal analysis.
    """

    vectors: list[SteeringVector] = field(default_factory=list)
    plugin_category: str = ""
    skill_name: str = ""

    def for_task(self, plugin_category: str, skill_name: str) -> SteeringConfig:
        """Create a task-specific steering config from defaults."""
        return SteeringConfig(
            vectors=list(self.vectors),
            plugin_category=plugin_category,
            skill_name=skill_name,
        )


# ── Default Steering Profiles by Domain ────────────────────────

DOMAIN_STEERING: dict[str, list[SteeringVector]] = {
    "customer-support": [
        SteeringVector(
            "empathy-up",
            SteeringTarget.EMPATHY,
            SteeringMethod.ACTIVATION_ADDITION,
            layer=16,
            strength=1.5,
        ),
        SteeringVector(
            "assertive-down",
            SteeringTarget.ASSERTIVENESS,
            SteeringMethod.ACTIVATION_INHIBITION,
            layer=16,
            strength=0.5,
        ),
    ],
    "legal": [
        SteeringVector(
            "caution-up",
            SteeringTarget.CAUTION,
            SteeringMethod.ACTIVATION_ADDITION,
            layer=18,
            strength=2.0,
        ),
        SteeringVector(
            "creativity-down",
            SteeringTarget.CREATIVITY,
            SteeringMethod.ACTIVATION_INHIBITION,
            layer=18,
            strength=0.3,
        ),
    ],
    "engineering": [
        SteeringVector(
            "technical-up",
            SteeringTarget.TECHNICAL_DEPTH,
            SteeringMethod.ACTIVATION_ADDITION,
            layer=20,
            strength=1.5,
        ),
    ],
    "sales": [
        SteeringVector(
            "assertive-up",
            SteeringTarget.ASSERTIVENESS,
            SteeringMethod.ACTIVATION_ADDITION,
            layer=16,
            strength=1.2,
        ),
        SteeringVector(
            "sycophancy-down",
            SteeringTarget.SYCOPHANCY,
            SteeringMethod.ACTIVATION_INHIBITION,
            layer=12,
            strength=0.8,
        ),
    ],
}
