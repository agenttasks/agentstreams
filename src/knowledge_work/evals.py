"""Layer 8: knowledge-work-evals — Eval harness and A/B scoring.

Evaluates knowledge-work task execution across model variants, prompt
templates, and circuit configurations. Produces A/B comparisons that
control for infrastructure noise (per Anthropic's eval research).

Bridges:
    Layer 7 (harness)    → Captures session events for scoring
    Layer 3 (prompts)    → Tests prompt variants
    Layer 2 (tracers)    → Correlates circuit patterns with quality
    Layer 1 (circuits)   → Compares circuit topologies across variants
    evals/codegen-ab/    → Reuses validation infrastructure

Design principles (from Anthropic's infrastructure noise research):
    - Control hardware: same CPU/RAM/timeout across variants
    - Separate infra errors from capability gaps
    - Report uncertainty: <3pt differences deserve skepticism
    - Document resource configuration as first-class variable
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.knowledge_work.circuits import Circuit, CircuitTopology
from src.knowledge_work.tasks import Task


@dataclass
class EvalResult:
    """Result of evaluating a single task execution."""

    task_name: str
    model: str
    variant: str = "default"  # Prompt variant (A/B)
    latency_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    success: bool = False
    error: str | None = None

    # Quality scores (task-specific, 0.0 to 1.0)
    completeness: float = 0.0  # Did it address all parts of the task?
    correctness: float = 0.0  # Is the output factually/logically correct?
    style: float = 0.0  # Does it match expected format/tone?

    # Circuit metrics (from Layer 2 tracing, if enabled)
    circuit_depth: int = 0
    circuit_width: int = 0
    replacement_score: float = 0.0

    # Harness metrics (from Layer 7 session log)
    subtask_count: int = 0
    subtasks_completed: int = 0
    event_count: int = 0

    @property
    def quality_score(self) -> float:
        """Weighted average of quality dimensions."""
        return (self.completeness * 0.4 + self.correctness * 0.4 + self.style * 0.2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_name": self.task_name,
            "model": self.model,
            "variant": self.variant,
            "latency_ms": self.latency_ms,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "success": self.success,
            "error": self.error,
            "quality_score": self.quality_score,
            "completeness": self.completeness,
            "correctness": self.correctness,
            "style": self.style,
            "circuit_depth": self.circuit_depth,
            "circuit_width": self.circuit_width,
            "replacement_score": self.replacement_score,
        }


@dataclass
class ABComparison:
    """A/B comparison between two model/prompt variants.

    Computes deltas and statistical significance across eval results.
    Follows Anthropic's recommendation: "leaderboard differences below
    3 percentage points deserve skepticism."
    """

    variant_a: str
    variant_b: str
    results_a: list[EvalResult] = field(default_factory=list)
    results_b: list[EvalResult] = field(default_factory=list)

    @property
    def quality_delta(self) -> float:
        """Difference in mean quality score (B - A)."""
        mean_a = sum(r.quality_score for r in self.results_a) / max(len(self.results_a), 1)
        mean_b = sum(r.quality_score for r in self.results_b) / max(len(self.results_b), 1)
        return mean_b - mean_a

    @property
    def latency_delta_ms(self) -> int:
        """Difference in mean latency (B - A)."""
        mean_a = sum(r.latency_ms for r in self.results_a) / max(len(self.results_a), 1)
        mean_b = sum(r.latency_ms for r in self.results_b) / max(len(self.results_b), 1)
        return int(mean_b - mean_a)

    @property
    def success_rate_delta(self) -> float:
        """Difference in success rate (B - A)."""
        rate_a = sum(1 for r in self.results_a if r.success) / max(len(self.results_a), 1)
        rate_b = sum(1 for r in self.results_b if r.success) / max(len(self.results_b), 1)
        return rate_b - rate_a

    @property
    def is_significant(self) -> bool:
        """Whether the quality delta exceeds the 3pt skepticism threshold."""
        return abs(self.quality_delta) > 0.03

    def to_dict(self) -> dict[str, Any]:
        return {
            "variant_a": self.variant_a,
            "variant_b": self.variant_b,
            "n_a": len(self.results_a),
            "n_b": len(self.results_b),
            "quality_delta": self.quality_delta,
            "latency_delta_ms": self.latency_delta_ms,
            "success_rate_delta": self.success_rate_delta,
            "is_significant": self.is_significant,
        }


@dataclass
class EvalSuite:
    """Suite of evaluations for knowledge-work tasks.

    Runs tasks across model/prompt variants, collects results,
    and produces A/B comparisons with circuit correlation data.
    """

    name: str
    tasks: list[Task] = field(default_factory=list)
    models: list[str] = field(default_factory=lambda: ["claude-sonnet-4-6", "claude-opus-4-6"])
    variants: list[str] = field(default_factory=lambda: ["default"])
    samples_per_task: int = 1
    results: list[EvalResult] = field(default_factory=list)

    @property
    def total_runs(self) -> int:
        """Total number of eval runs in this suite."""
        return len(self.tasks) * len(self.models) * len(self.variants) * self.samples_per_task

    def compare(self, variant_a: str, variant_b: str) -> ABComparison:
        """Create an A/B comparison between two variants."""
        results_a = [r for r in self.results if r.variant == variant_a or r.model == variant_a]
        results_b = [r for r in self.results if r.variant == variant_b or r.model == variant_b]
        return ABComparison(
            variant_a=variant_a,
            variant_b=variant_b,
            results_a=results_a,
            results_b=results_b,
        )

    def compare_circuits(self) -> CircuitTopology | None:
        """Build a CircuitTopology from all traced circuits in results.

        Only available if circuit tracing was enabled during execution.
        """
        circuits = [
            Circuit(
                name=r.task_name,
                replacement_score=r.replacement_score,
            )
            for r in self.results
            if r.replacement_score > 0
        ]
        return CircuitTopology(circuits=circuits) if circuits else None

    def summary(self) -> dict[str, Any]:
        """Summary statistics across all results."""
        if not self.results:
            return {"total_runs": 0}

        return {
            "name": self.name,
            "total_runs": len(self.results),
            "success_rate": sum(1 for r in self.results if r.success) / len(self.results),
            "mean_quality": sum(r.quality_score for r in self.results) / len(self.results),
            "mean_latency_ms": sum(r.latency_ms for r in self.results) // len(self.results),
            "models": list({r.model for r in self.results}),
            "variants": list({r.variant for r in self.results}),
        }
