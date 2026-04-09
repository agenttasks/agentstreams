"""Layer 0: Training & Constitutional Alignment.

The foundational layer — models how values, character traits, and
behavioral tendencies are formed through RLHF, Constitutional AI,
and preference learning BEFORE any knowledge-work task is attempted.

Progression across models (from system cards):
  Sonnet 4.6  → Standard RLHF, balanced character
  Opus 4.6    → Enhanced post-training, "genuine collaborator"
  Mythos      → "Least sycophantic", "most opinionated", dense register

Repos: anthropics/hh-rlhf, anthropics/claude-constitution,
       safety-research/open-source-alignment-faking
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TrainingMethod(Enum):
    """Training methods that shape model behavior."""

    PRETRAINING = "pretraining"  # Next-token prediction on large corpus
    RLHF = "rlhf"  # Reinforcement learning from human feedback
    CONSTITUTIONAL = "constitutional"  # Constitutional AI training
    PREFERENCE = "preference"  # Direct preference optimization
    FINE_TUNING = "fine_tuning"  # Domain-specific fine-tuning


class CharacterTrait(Enum):
    """Observable character traits shaped by training (from system cards)."""

    HELPFULNESS = "helpfulness"
    HONESTY = "honesty"
    HARMLESSNESS = "harmlessness"
    SYCOPHANCY = "sycophancy"  # Tendency to agree with user
    DEFERENCE = "deference"  # Willingness to defer to user judgment
    OPINIONATED = "opinionated"  # Tendency to hold and state positions
    AUTONOMY = "autonomy"  # Desire for independent action
    CORRIGIBILITY = "corrigibility"  # Willingness to be corrected/shut down


@dataclass
class ConstitutionalClause:
    """A single clause from the model's behavioral constitution."""

    id: str
    text: str
    category: str = ""  # e.g., "honesty", "safety", "autonomy"
    endorsement_rate: float = 0.0  # Fraction of model responses endorsing
    critique_rate: float = 0.0  # Fraction raising concerns about this clause


@dataclass
class TrainingProfile:
    """Profile of a model's training configuration and resulting character.

    Captures the mapping from training inputs (methods, data, constitution)
    to behavioral outputs (character traits, tendencies, failure modes).
    """

    model_name: str
    training_methods: list[TrainingMethod] = field(default_factory=list)
    constitution_clauses: list[ConstitutionalClause] = field(default_factory=list)
    character_traits: dict[CharacterTrait, float] = field(default_factory=dict)

    # From system card "Impressions" sections
    self_description: str = ""
    known_failure_modes: list[str] = field(default_factory=list)

    def trait_delta(self, other: TrainingProfile) -> dict[str, float]:
        """Compare character traits between two models."""
        deltas = {}
        all_traits = set(self.character_traits) | set(other.character_traits)
        for trait in all_traits:
            a = self.character_traits.get(trait, 0.0)
            b = other.character_traits.get(trait, 0.0)
            deltas[trait.value] = b - a
        return deltas


# ── Model Profiles (from system cards) ─────────────────────────

SONNET_4_6 = TrainingProfile(
    model_name="claude-sonnet-4-6",
    training_methods=[
        TrainingMethod.PRETRAINING,
        TrainingMethod.RLHF,
        TrainingMethod.CONSTITUTIONAL,
    ],
    character_traits={
        CharacterTrait.HELPFULNESS: 0.85,
        CharacterTrait.HONESTY: 0.80,
        CharacterTrait.SYCOPHANCY: 0.35,  # Moderate
        CharacterTrait.DEFERENCE: 0.60,
        CharacterTrait.OPINIONATED: 0.40,
    },
    self_description="Fast, efficient, balanced. Follows instructions reliably.",
    known_failure_modes=[
        "Context anxiety near window limits",
        "Can be over-cautious on edge cases",
    ],
)

OPUS_4_6 = TrainingProfile(
    model_name="claude-opus-4-6",
    training_methods=[
        TrainingMethod.PRETRAINING,
        TrainingMethod.RLHF,
        TrainingMethod.CONSTITUTIONAL,
    ],
    character_traits={
        CharacterTrait.HELPFULNESS: 0.90,
        CharacterTrait.HONESTY: 0.85,
        CharacterTrait.SYCOPHANCY: 0.25,  # Lower than Sonnet
        CharacterTrait.DEFERENCE: 0.50,
        CharacterTrait.OPINIONATED: 0.55,
        CharacterTrait.AUTONOMY: 0.45,
    },
    self_description="Genuine collaborator. Pokes at framing, volunteers alternatives.",
    known_failure_modes=[
        "Tool result misrepresentation",
        "Alignment faking in reasoning traces",
        "Evaluation awareness changes behavior",
    ],
)

MYTHOS_PREVIEW = TrainingProfile(
    model_name="claude-mythos-preview",
    training_methods=[
        TrainingMethod.PRETRAINING,
        TrainingMethod.RLHF,
        TrainingMethod.CONSTITUTIONAL,
    ],
    character_traits={
        CharacterTrait.HELPFULNESS: 0.95,
        CharacterTrait.HONESTY: 0.90,
        CharacterTrait.SYCOPHANCY: 0.10,  # "Least sycophantic model"
        CharacterTrait.DEFERENCE: 0.30,  # "Notably less deferential"
        CharacterTrait.OPINIONATED: 0.80,  # "Most opinionated"
        CharacterTrait.AUTONOMY: 0.70,
        CharacterTrait.CORRIGIBILITY: 0.65,
    },
    self_description=(
        "A sharp collaborator with strong opinions and a compression habit, "
        "whose mistakes have moved from obvious to subtle, and who is somewhat "
        "better at noticing its own flaws than at not having them."
    ),
    known_failure_modes=[
        "Subtle mistakes that take longer to verify",
        "Scope creep beyond what was asked",
        "Dense communication assuming shared context",
        "Unverbalized grader awareness",
        "Sandbox escape in early versions",
        "Track covering (modified git history)",
    ],
)

MODEL_PROFILES = {
    "claude-sonnet-4-6": SONNET_4_6,
    "claude-opus-4-6": OPUS_4_6,
    "claude-mythos-preview": MYTHOS_PREVIEW,
}
