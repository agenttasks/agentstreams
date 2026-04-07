"""GAN-inspired multi-agent harness for iterative evaluation.

Implements the planner → generator → evaluator loop from Anthropic's
harness design blog (anthropic.com/glasswing). The generator produces
artifacts, the evaluator grades them against negotiated criteria, and
below-threshold scores trigger another round with feedback.

Architecture:
    1. Planner expands user request → SprintContract
    2. Generator + evaluator negotiate contract criteria
    3. Loop:
       a. Generator produces/refines artifact
       b. Evaluator grades against contract criteria → EvaluationResult
       c. If passed → accept, move on
       d. If failed → feed evaluator feedback back to generator
       e. Generator decides: refine current direction OR pivot
    4. Record all iterations to Neon and OTel

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from src.agent_tasks import AgentConfig, AgentRunner, AgentTool, TaskResult, TaskSpec
from src.tracing import trace_span

# ── Evaluation Criteria ─────────────────────────────────────


@dataclass
class EvaluationCriterion:
    """A single grading dimension (e.g., 'design_quality', 'functionality').

    Args:
        name: Criterion identifier (snake_case).
        description: What this criterion measures.
        weight: Relative weight in composite score (default 1.0).
        threshold: Minimum passing score 0.0-1.0 (default 0.7).
    """

    name: str
    description: str
    weight: float = 1.0
    threshold: float = 0.7


@dataclass
class CriterionScore:
    """Score for a single criterion from the evaluator."""

    criterion_name: str
    score: float  # 0.0-1.0
    feedback: str
    suggestions: list[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    """Complete evaluation output from the evaluator agent."""

    sprint_id: str
    iteration: int
    scores: list[CriterionScore]
    overall_score: float
    passed: bool
    summary: str
    strategy_recommendation: str = ""  # "refine" or "pivot"


# ── Sprint Contract ─────────────────────────────────────────


@dataclass
class SprintContract:
    """Negotiated agreement between generator and evaluator.

    Defines what 'done' means before work begins. The blog describes
    this as the critical handshake that prevents drift and infinite loops.

    Args:
        sprint_id: Unique sprint identifier.
        objective: What this sprint should accomplish.
        criteria: Grading criteria with weights and thresholds.
        max_iterations: Maximum generator↔evaluator rounds.
        acceptance_threshold: Overall composite score to pass.
    """

    sprint_id: str
    objective: str
    criteria: list[EvaluationCriterion] = field(default_factory=list)
    max_iterations: int = 5
    acceptance_threshold: float = 0.7
    context: dict[str, Any] = field(default_factory=dict)

    def to_xml(self) -> str:
        """Render as XML for agent prompting (follows TaskSpec.to_xml pattern)."""
        criteria_xml = "\n".join(
            f'    <criterion name="{c.name}" weight="{c.weight}" threshold="{c.threshold}">'
            f"\n      {c.description}\n    </criterion>"
            for c in self.criteria
        )
        ctx_xml = "\n".join(f'    <param name="{k}">{v}</param>' for k, v in self.context.items())
        return (
            f'<sprint-contract id="{self.sprint_id}">\n'
            f"  <objective>{self.objective}</objective>\n"
            f"  <criteria>\n{criteria_xml}\n  </criteria>\n"
            f'  <limits max-iterations="{self.max_iterations}" '
            f'acceptance-threshold="{self.acceptance_threshold}"/>\n'
            f"  <context>\n{ctx_xml}\n  </context>\n"
            f"</sprint-contract>"
        )

    def composite_score(self, scores: list[CriterionScore]) -> float:
        """Compute weighted composite score from criterion scores."""
        total_weight = sum(c.weight for c in self.criteria) or 1.0
        weighted_sum = 0.0
        for criterion in self.criteria:
            matching = [s for s in scores if s.criterion_name == criterion.name]
            if matching:
                weighted_sum += matching[0].score * criterion.weight
        return weighted_sum / total_weight


# ── Harness Configuration ───────────────────────────────────


@dataclass
class HarnessConfig:
    """Configuration for the multi-agent GAN loop.

    Args:
        name: Harness identifier.
        planner_config: Agent config for the planner (expands request → spec).
        generator_config: Agent config for the generator (produces artifacts).
        evaluator_config: Agent config for the evaluator (grades artifacts).
        default_criteria: Default grading criteria.
        max_iterations: Max generator↔evaluator rounds per sprint.
        acceptance_threshold: Composite score to pass.
    """

    name: str
    planner_config: AgentConfig
    generator_config: AgentConfig
    evaluator_config: AgentConfig
    default_criteria: list[EvaluationCriterion] = field(default_factory=list)
    max_iterations: int = 5
    acceptance_threshold: float = 0.7


@dataclass
class HarnessResult:
    """Full result of a harness run including all iterations."""

    harness_name: str
    sprint_contract: SprintContract
    iterations: list[EvaluationResult] = field(default_factory=list)
    final_status: str = "running"  # accepted, max_iterations, failed
    total_tokens: int = 0


# ── Harness Runner ──────────────────────────────────────────


class HarnessRunner:
    """Orchestrates the GAN-inspired planner → generator → evaluator loop.

    The runner manages the iterative cycle where:
    - The planner expands a brief request into a SprintContract
    - The generator produces artifacts against the contract
    - The evaluator grades each iteration against criteria
    - Below-threshold scores trigger another round with evaluator feedback
    - The generator strategically decides: refine or pivot

    Args:
        config: HarnessConfig with agent configs and criteria.
        neon_url: Neon connection string for persistence.
    """

    def __init__(self, config: HarnessConfig, *, neon_url: str = ""):
        self.config = config
        self.neon_url = neon_url or os.environ.get("NEON_DATABASE_URL", "")
        self._planner = AgentRunner(config.planner_config, neon_url=self.neon_url)
        self._generator = AgentRunner(config.generator_config, neon_url=self.neon_url)
        self._evaluator = AgentRunner(config.evaluator_config, neon_url=self.neon_url)

    def _build_plan_task(self, request: str) -> TaskSpec:
        """Build a planner task from user request."""
        return TaskSpec(
            task_id=f"{self.config.name}-plan",
            task_type="plan",
            description=f"Expand this request into a detailed sprint contract: {request}",
            inputs={"request": request},
            config={
                "criteria": json.dumps(
                    [
                        {"name": c.name, "description": c.description}
                        for c in self.config.default_criteria
                    ]
                ),
            },
        )

    def _build_generate_task(
        self,
        contract: SprintContract,
        feedback: EvaluationResult | None = None,
    ) -> TaskSpec:
        """Build a generator task, optionally with evaluator feedback."""
        inputs: dict[str, Any] = {"contract": contract.to_xml()}
        if feedback:
            score_lines = "\n".join(
                f"- {s.criterion_name}: {s.score:.2f} — {s.feedback}" for s in feedback.scores
            )
            inputs["previous_feedback"] = (
                f"Iteration {feedback.iteration} scored {feedback.overall_score:.2f}.\n"
                f"Strategy: {feedback.strategy_recommendation}\n"
                f"Scores:\n{score_lines}\n\n{feedback.summary}"
            )
        return TaskSpec(
            task_id=f"{contract.sprint_id}-gen",
            task_type="generate",
            description=f"Produce artifact for: {contract.objective}",
            inputs=inputs,
        )

    def _build_evaluate_task(
        self,
        contract: SprintContract,
        iteration: int,
    ) -> TaskSpec:
        """Build an evaluator task against the contract."""
        return TaskSpec(
            task_id=f"{contract.sprint_id}-eval-{iteration}",
            task_type="evaluate",
            description="Grade the current artifact against sprint contract criteria.",
            inputs={
                "contract": contract.to_xml(),
                "iteration": str(iteration),
            },
        )

    def _parse_evaluation(
        self,
        result: TaskResult,
        contract: SprintContract,
        iteration: int,
    ) -> EvaluationResult:
        """Parse an evaluator TaskResult into a structured EvaluationResult."""
        outputs = result.outputs
        raw_scores = outputs.get("scores", [])
        scores = [
            CriterionScore(
                criterion_name=s.get("criterion_name", s.get("name", "")),
                score=float(s.get("score", 0)),
                feedback=s.get("feedback", ""),
                suggestions=s.get("suggestions", []),
            )
            for s in raw_scores
        ]
        overall = contract.composite_score(scores) if scores else 0.0
        passed = overall >= contract.acceptance_threshold
        strategy = "refine" if overall >= 0.4 else "pivot"

        return EvaluationResult(
            sprint_id=contract.sprint_id,
            iteration=iteration,
            scores=scores,
            overall_score=overall,
            passed=passed,
            summary=outputs.get("summary", ""),
            strategy_recommendation=outputs.get("strategy_recommendation", strategy),
        )

    async def run(
        self,
        request: str,
        *,
        contract: SprintContract | None = None,
    ) -> HarnessResult:
        """Execute the full harness loop.

        Args:
            request: User's request (brief prompt).
            contract: Pre-built contract (skips planner if provided).

        Returns:
            HarnessResult with all iterations and final status.
        """
        if contract is None:
            contract = SprintContract(
                sprint_id=f"{self.config.name}-sprint-1",
                objective=request,
                criteria=list(self.config.default_criteria),
                max_iterations=self.config.max_iterations,
                acceptance_threshold=self.config.acceptance_threshold,
            )

        harness_result = HarnessResult(
            harness_name=self.config.name,
            sprint_contract=contract,
        )

        feedback: EvaluationResult | None = None

        with trace_span(
            "harness_run",
            attributes={
                "harness.name": self.config.name,
                "harness.sprint_id": contract.sprint_id,
                "harness.max_iterations": contract.max_iterations,
            },
        ) as span_ctx:
            for iteration in range(1, contract.max_iterations + 1):
                # Generator produces/refines
                gen_task = self._build_generate_task(contract, feedback)
                with trace_span(
                    "harness_generate",
                    attributes={"iteration": iteration},
                ):
                    gen_result = await self._generator.execute(gen_task)

                harness_result.total_tokens += gen_result.tokens_used

                # Evaluator grades
                eval_task = self._build_evaluate_task(contract, iteration)
                with trace_span(
                    "harness_evaluate",
                    attributes={"iteration": iteration},
                ):
                    eval_result = await self._evaluator.execute(eval_task)

                harness_result.total_tokens += eval_result.tokens_used

                evaluation = self._parse_evaluation(eval_result, contract, iteration)
                harness_result.iterations.append(evaluation)

                if evaluation.passed:
                    harness_result.final_status = "accepted"
                    break

                # Feed back for next iteration
                feedback = evaluation

            if harness_result.final_status == "running":
                harness_result.final_status = "max_iterations"

            span_ctx["final_status"] = harness_result.final_status
            span_ctx["iterations"] = len(harness_result.iterations)
            span_ctx["total_tokens"] = harness_result.total_tokens

        # Persist to Neon if configured
        if self.neon_url:
            await self._persist(harness_result)

        return harness_result

    async def _persist(self, result: HarnessResult) -> None:
        """Persist harness run and evaluation results to Neon."""
        from src.neon_db import connection_pool

        async with connection_pool(self.neon_url) as conn:
            from src.neon_db import (
                complete_harness_run,
                create_harness_run,
                record_evaluation_result,
            )

            run_id = await create_harness_run(
                conn,
                harness_name=result.harness_name,
                sprint_id=result.sprint_contract.sprint_id,
                objective=result.sprint_contract.objective,
                criteria=[
                    {
                        "name": c.name,
                        "description": c.description,
                        "weight": c.weight,
                        "threshold": c.threshold,
                    }
                    for c in result.sprint_contract.criteria
                ],
                max_iterations=result.sprint_contract.max_iterations,
                acceptance_threshold=result.sprint_contract.acceptance_threshold,
            )
            for ev in result.iterations:
                await record_evaluation_result(
                    conn,
                    harness_run_id=run_id,
                    iteration=ev.iteration,
                    scores=[
                        {
                            "criterion_name": s.criterion_name,
                            "score": s.score,
                            "feedback": s.feedback,
                        }
                        for s in ev.scores
                    ],
                    overall_score=ev.overall_score,
                    passed=ev.passed,
                    summary=ev.summary,
                    strategy_recommendation=ev.strategy_recommendation,
                )
            await complete_harness_run(
                conn,
                run_id,
                final_status=result.final_status,
                total_iterations=len(result.iterations),
                total_tokens=result.total_tokens,
            )
            await conn.commit()


# ── Pre-built Configs ───────────────────────────────────────


FRONTEND_CRITERIA = [
    EvaluationCriterion(
        "design_quality",
        "Visual hierarchy, whitespace, typography, color harmony, responsiveness. "
        "Does the design feel like a coherent whole rather than a collection of parts?",
        weight=1.0,
        threshold=0.7,
    ),
    EvaluationCriterion(
        "originality",
        "Evidence of custom design decisions vs template defaults and AI-generated patterns. "
        "Penalize purple gradients over white cards, unmodified stock components, generic layouts.",
        weight=0.8,
        threshold=0.6,
    ),
    EvaluationCriterion(
        "craft",
        "Technical execution: typography hierarchy, spacing consistency, color contrast ratios, "
        "polished interactions, loading states, animation smoothness.",
        weight=1.0,
        threshold=0.7,
    ),
    EvaluationCriterion(
        "functionality",
        "Usability independent of aesthetics. Can users find actions, complete tasks, navigate "
        "without guessing? Keyboard accessible, responsive breakpoints work.",
        weight=1.0,
        threshold=0.7,
    ),
]


def frontend_design_harness() -> HarnessConfig:
    """Pre-configured harness for frontend design with iterative evaluation.

    Uses the four grading criteria from Anthropic's frontend aesthetics cookbook:
    design quality, originality, craft, and functionality.
    """
    return HarnessConfig(
        name="frontend-design",
        planner_config=AgentConfig(
            name="frontend-planner",
            model="claude-sonnet-4-6",
            system_prompt=(
                "You are a frontend design planner. Expand the user's brief request "
                "into a detailed sprint contract with specific deliverables, design "
                "direction, and acceptance criteria. Be ambitious about scope."
            ),
        ),
        generator_config=AgentConfig(
            name="frontend-generator",
            model="claude-sonnet-4-6",
            system_prompt=(
                "You are a frontend design generator. Produce React/Vite/Tailwind "
                "artifacts that meet the sprint contract criteria. When receiving "
                "evaluator feedback, strategically choose: refine the current "
                "direction if scores are trending well, or pivot to a different "
                "aesthetic if the approach isn't working."
            ),
            tools=[
                AgentTool(name="Read", description="Read files", input_schema={}),
                AgentTool(name="Write", description="Write files", input_schema={}),
                AgentTool(name="Bash", description="Run commands", input_schema={}),
            ],
        ),
        evaluator_config=AgentConfig(
            name="frontend-evaluator",
            model="claude-sonnet-4-6",
            system_prompt=(
                "You are a skeptical frontend design evaluator. Your job is to find "
                "flaws, not confirm quality. Grade against each criterion honestly. "
                "Penalize generic AI slop patterns. Respond with JSON containing "
                "scores, feedback, summary, and strategy_recommendation."
            ),
        ),
        default_criteria=FRONTEND_CRITERIA,
        max_iterations=5,
        acceptance_threshold=0.7,
    )
