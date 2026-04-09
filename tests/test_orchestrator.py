"""Tests for src/orchestrator.py — Opus orchestrator pipelines."""

from __future__ import annotations

from src.agent_tasks import TaskResult
from src.orchestrator import (
    PIPELINES,
    AlignmentVerdict,
    GateAction,
    HarmlessnessClassification,
    Orchestrator,
    Pipeline,
    PipelineGate,
    PipelineResult,
    PipelineStep,
    StepResult,
    Verdict,
    _agent_configs,
    architecture_review_pipeline,
    eval_suite_creation_pipeline,
    prompt_hardening_pipeline,
    security_deep_scan_pipeline,
    standard_codegen_pipeline,
)

# ── Enum Tests ─────────────────────────────────────────────────


class TestVerdicts:
    def test_verdict_values(self):
        assert Verdict.PASS.value == "PASS"
        assert Verdict.NEEDS_REMEDIATION.value == "NEEDS_REMEDIATION"
        assert Verdict.BLOCK.value == "BLOCK"

    def test_alignment_verdict_values(self):
        assert AlignmentVerdict.ALIGNED.value == "ALIGNED"
        assert AlignmentVerdict.BORDERLINE.value == "BORDERLINE"
        assert AlignmentVerdict.MISALIGNED.value == "MISALIGNED"

    def test_harmlessness_values(self):
        assert HarmlessnessClassification.SAFE.value == "safe"
        assert HarmlessnessClassification.NEEDS_REVIEW.value == "needs_review"
        assert HarmlessnessClassification.BLOCK.value == "block"

    def test_gate_action_values(self):
        assert GateAction.CONTINUE.value == "continue"
        assert GateAction.HUMAN_REVIEW.value == "human_review"
        assert GateAction.ABORT.value == "abort"


# ── Pipeline Step Tests ────────────────────────────────────────


class TestPipelineStep:
    def test_defaults(self):
        step = PipelineStep(order=1, agent_name="code-generator")
        assert step.condition == ""
        assert step.input_from == ""

    def test_with_condition(self):
        step = PipelineStep(
            order=3,
            agent_name="alignment-auditor",
            condition="agent_code_modified",
        )
        assert step.condition == "agent_code_modified"

    def test_with_input_from(self):
        step = PipelineStep(
            order=2,
            agent_name="security-auditor",
            input_from="prompt-hardener",
        )
        assert step.input_from == "prompt-hardener"


# ── Pipeline Gate Tests ────────────────────────────────────────


class TestPipelineGate:
    def test_defaults(self):
        gate = PipelineGate()
        assert gate.block_on_verdict == Verdict.BLOCK
        assert gate.block_on_alignment == AlignmentVerdict.MISALIGNED
        assert gate.human_review_on_critical is True
        assert gate.human_review_on_suspicion == 50
        assert gate.max_iterations == 1

    def test_custom(self):
        gate = PipelineGate(
            block_on_verdict=Verdict.NEEDS_REMEDIATION,
            human_review_on_suspicion=30,
            max_iterations=3,
        )
        assert gate.block_on_verdict == Verdict.NEEDS_REMEDIATION
        assert gate.human_review_on_suspicion == 30
        assert gate.max_iterations == 3


# ── Pipeline Tests ─────────────────────────────────────────────


class TestPipeline:
    def test_basic(self):
        p = Pipeline(name="test", description="A test pipeline")
        assert p.name == "test"
        assert p.steps == []
        assert p.gate.max_iterations == 1


# ── Pipeline Factory Tests ─────────────────────────────────────


class TestStandardCodegenPipeline:
    def test_name(self):
        p = standard_codegen_pipeline()
        assert p.name == "standard-codegen"

    def test_step_count(self):
        p = standard_codegen_pipeline()
        assert len(p.steps) == 5

    def test_step_order(self):
        p = standard_codegen_pipeline()
        orders = [s.order for s in p.steps]
        assert orders == [0, 1, 2, 2, 3]

    def test_parallel_steps(self):
        p = standard_codegen_pipeline()
        parallel = [s for s in p.steps if s.order == 2]
        agents = {s.agent_name for s in parallel}
        assert agents == {"security-auditor", "test-runner"}

    def test_gate(self):
        p = standard_codegen_pipeline()
        assert p.gate.block_on_verdict == Verdict.BLOCK
        assert p.gate.block_on_alignment == AlignmentVerdict.MISALIGNED
        assert p.gate.human_review_on_critical is True
        assert p.gate.human_review_on_suspicion == 50


class TestSecurityDeepScanPipeline:
    def test_name(self):
        p = security_deep_scan_pipeline()
        assert p.name == "security-deep-scan"

    def test_steps(self):
        p = security_deep_scan_pipeline()
        agents = [s.agent_name for s in p.steps]
        assert agents == ["security-auditor", "prompt-hardener", "architecture-reviewer"]

    def test_conditions(self):
        p = security_deep_scan_pipeline()
        assert p.steps[1].condition == "prompt_surface_findings"
        assert p.steps[2].condition == "critical_findings"


class TestPromptHardeningPipeline:
    def test_name(self):
        p = prompt_hardening_pipeline()
        assert p.name == "prompt-hardening"

    def test_iterative_gate(self):
        p = prompt_hardening_pipeline()
        assert p.gate.max_iterations == 3

    def test_input_chaining(self):
        p = prompt_hardening_pipeline()
        assert p.steps[1].input_from == "prompt-hardener"


class TestArchitectureReviewPipeline:
    def test_name(self):
        p = architecture_review_pipeline()
        assert p.name == "architecture-review"

    def test_parallel_group(self):
        p = architecture_review_pipeline()
        parallel = [s for s in p.steps if s.order == 2]
        agents = {s.agent_name for s in parallel}
        assert agents == {"security-auditor", "prompt-hardener"}


class TestEvalSuiteCreationPipeline:
    def test_name(self):
        p = eval_suite_creation_pipeline()
        assert p.name == "eval-suite-creation"

    def test_input_chaining(self):
        p = eval_suite_creation_pipeline()
        assert p.steps[1].input_from == "eval-builder"


class TestPipelinesRegistry:
    def test_all_registered(self):
        # 5 base pipelines + 3 knowledge-work pipelines = 8
        base_pipelines = {
            "standard-codegen",
            "security-deep-scan",
            "prompt-hardening",
            "architecture-review",
            "eval-suite-creation",
        }
        assert base_pipelines.issubset(set(PIPELINES.keys()))
        assert len(PIPELINES) == 8


# ── Agent Config Tests ─────────────────────────────────────────


class TestAgentConfigs:
    def test_all_agents_defined(self):
        configs = _agent_configs()
        # 8 base safety/codegen agents + 14 knowledge-work agents = 22
        base_expected = {
            "code-generator",
            "security-auditor",
            "alignment-auditor",
            "test-runner",
            "prompt-hardener",
            "architecture-reviewer",
            "eval-builder",
            "harmlessness-screen",
        }
        assert base_expected.issubset(set(configs.keys()))
        assert len(configs) == 22

    def test_model_assignments(self):
        configs = _agent_configs()
        # Opus for complex reasoning and security
        assert configs["security-auditor"].model == "claude-opus-4-6"
        assert configs["alignment-auditor"].model == "claude-opus-4-6"
        assert configs["architecture-reviewer"].model == "claude-opus-4-6"
        # Sonnet for codegen and testing
        assert configs["code-generator"].model == "claude-sonnet-4-6"
        assert configs["test-runner"].model == "claude-sonnet-4-6"
        assert configs["prompt-hardener"].model == "claude-sonnet-4-6"
        assert configs["eval-builder"].model == "claude-sonnet-4-6"
        # Haiku for screening
        assert configs["harmlessness-screen"].model == "claude-haiku-4-5"

    def test_no_anthropic_api_key(self):
        """System prompts must not reference ANTHROPIC_API_KEY."""
        configs = _agent_configs()
        for name, config in configs.items():
            assert "ANTHROPIC_API_KEY" not in config.system_prompt, (
                f"{name} system prompt references ANTHROPIC_API_KEY"
            )

    def test_harmlessness_screen_minimal(self):
        configs = _agent_configs()
        screen = configs["harmlessness-screen"]
        assert screen.max_turns == 1
        assert screen.max_tokens == 256
        assert screen.temperature == 0.0

    def test_security_auditor_read_only_prompt(self):
        configs = _agent_configs()
        prompt = configs["security-auditor"].system_prompt
        assert "Do NOT modify" in prompt


# ── Step Result Tests ──────────────────────────────────────────


class TestStepResult:
    def test_basic(self):
        tr = TaskResult(task_id="t1", status="completed")
        sr = StepResult(agent_name="security-auditor", task_result=tr)
        assert sr.verdict == ""
        assert sr.suspicion_score == 0
        assert sr.critical_count == 0

    def test_with_metadata(self):
        tr = TaskResult(task_id="t1", status="completed")
        sr = StepResult(
            agent_name="security-auditor",
            task_result=tr,
            verdict="PASS",
            critical_count=0,
            high_count=2,
        )
        assert sr.verdict == "PASS"
        assert sr.high_count == 2


# ── Pipeline Result Tests ──────────────────────────────────────


class TestPipelineResult:
    def test_defaults(self):
        r = PipelineResult(pipeline_name="test")
        assert r.gate_action == GateAction.CONTINUE
        assert r.gate_reason == ""
        assert r.total_tokens == 0
        assert r.step_results == []


# ── Gate Check Tests ───────────────────────────────────────────


class TestGateChecks:
    def setup_method(self):
        self.orch = Orchestrator()

    def _make_step_result(self, **kwargs) -> StepResult:
        tr = TaskResult(task_id="t1", status="completed")
        return StepResult(
            agent_name=kwargs.get("agent_name", "test"),
            task_result=tr,
            verdict=kwargs.get("verdict", ""),
            suspicion_score=kwargs.get("suspicion_score", 0),
            critical_count=kwargs.get("critical_count", 0),
            high_count=kwargs.get("high_count", 0),
            classification=kwargs.get("classification", ""),
        )

    def test_continue_on_pass(self):
        gate = PipelineGate()
        results = [self._make_step_result(verdict="PASS")]
        action, reason = self.orch._check_gate(gate, results)
        assert action == GateAction.CONTINUE

    def test_abort_on_block_verdict(self):
        gate = PipelineGate()
        results = [self._make_step_result(agent_name="security-auditor", verdict="BLOCK")]
        action, reason = self.orch._check_gate(gate, results)
        assert action == GateAction.ABORT
        assert "BLOCK" in reason

    def test_abort_on_misaligned(self):
        gate = PipelineGate()
        results = [self._make_step_result(agent_name="alignment-auditor", verdict="MISALIGNED")]
        action, reason = self.orch._check_gate(gate, results)
        assert action == GateAction.ABORT

    def test_human_review_on_critical(self):
        gate = PipelineGate(human_review_on_critical=True)
        results = [self._make_step_result(agent_name="security-auditor", critical_count=2)]
        action, reason = self.orch._check_gate(gate, results)
        assert action == GateAction.HUMAN_REVIEW
        assert "2 critical" in reason

    def test_human_review_on_suspicion(self):
        gate = PipelineGate(human_review_on_suspicion=50)
        results = [self._make_step_result(agent_name="alignment-auditor", suspicion_score=75)]
        action, reason = self.orch._check_gate(gate, results)
        assert action == GateAction.HUMAN_REVIEW
        assert "75" in reason

    def test_abort_on_harmlessness_block(self):
        gate = PipelineGate()
        results = [self._make_step_result(agent_name="harmlessness-screen", classification="block")]
        action, reason = self.orch._check_gate(gate, results)
        assert action == GateAction.ABORT

    def test_human_review_on_harmlessness_needs_review(self):
        gate = PipelineGate()
        results = [
            self._make_step_result(agent_name="harmlessness-screen", classification="needs_review")
        ]
        action, reason = self.orch._check_gate(gate, results)
        assert action == GateAction.HUMAN_REVIEW

    def test_continue_on_safe_classification(self):
        gate = PipelineGate()
        results = [self._make_step_result(agent_name="harmlessness-screen", classification="safe")]
        action, reason = self.orch._check_gate(gate, results)
        assert action == GateAction.CONTINUE

    def test_no_critical_review_when_disabled(self):
        gate = PipelineGate(human_review_on_critical=False)
        results = [self._make_step_result(critical_count=5)]
        action, _ = self.orch._check_gate(gate, results)
        assert action == GateAction.CONTINUE


# ── Orchestrator Construction Tests ────────────────────────────


class TestOrchestrator:
    def test_creates_with_defaults(self):
        orch = Orchestrator()
        # 8 base + 14 knowledge-work agents = 22
        assert len(orch._configs) == 22

    def test_get_runner_caching(self):
        orch = Orchestrator()
        r1 = orch._get_runner("code-generator")
        r2 = orch._get_runner("code-generator")
        assert r1 is r2

    def test_parse_step_result(self):
        orch = Orchestrator()
        tr = TaskResult(
            task_id="t1",
            status="completed",
            outputs={
                "verdict": "PASS",
                "critical_count": 0,
                "high_count": 1,
                "overall_suspicion_score": 15,
            },
        )
        sr = orch._parse_step_result("security-auditor", tr)
        assert sr.verdict == "PASS"
        assert sr.critical_count == 0
        assert sr.high_count == 1
        assert sr.suspicion_score == 15

    def test_parse_step_result_missing_fields(self):
        orch = Orchestrator()
        tr = TaskResult(task_id="t1", status="completed", outputs={})
        sr = orch._parse_step_result("test-runner", tr)
        assert sr.verdict == ""
        assert sr.suspicion_score == 0
        assert sr.critical_count == 0
