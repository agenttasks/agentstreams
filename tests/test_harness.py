"""Tests for src/harness.py — GAN-inspired multi-agent harness."""

from __future__ import annotations

from src.agent_tasks import AgentConfig, TaskResult
from src.harness import (
    FRONTEND_CRITERIA,
    CriterionScore,
    EvaluationCriterion,
    EvaluationResult,
    HarnessConfig,
    HarnessResult,
    HarnessRunner,
    SprintContract,
    frontend_design_harness,
)


class TestEvaluationCriterion:
    def test_defaults(self):
        c = EvaluationCriterion("test", "A test criterion")
        assert c.weight == 1.0
        assert c.threshold == 0.7

    def test_custom(self):
        c = EvaluationCriterion("originality", "Be creative", weight=0.8, threshold=0.6)
        assert c.weight == 0.8
        assert c.threshold == 0.6


class TestCriterionScore:
    def test_basic(self):
        s = CriterionScore("design_quality", 0.75, "Good visual hierarchy")
        assert s.score == 0.75
        assert s.suggestions == []

    def test_with_suggestions(self):
        s = CriterionScore("craft", 0.5, "Spacing inconsistent", ["Fix header margin"])
        assert len(s.suggestions) == 1


class TestSprintContract:
    def test_defaults(self):
        c = SprintContract("sprint-1", "Build a landing page")
        assert c.max_iterations == 5
        assert c.acceptance_threshold == 0.7

    def test_to_xml(self):
        c = SprintContract(
            "sprint-1",
            "Build a dashboard",
            criteria=[EvaluationCriterion("design_quality", "Visual coherence")],
        )
        xml = c.to_xml()
        assert 'id="sprint-1"' in xml
        assert "Build a dashboard" in xml
        assert "design_quality" in xml

    def test_composite_score(self):
        criteria = [
            EvaluationCriterion("a", "desc", weight=1.0),
            EvaluationCriterion("b", "desc", weight=1.0),
        ]
        c = SprintContract("s1", "test", criteria=criteria)
        scores = [
            CriterionScore("a", 0.8, "good"),
            CriterionScore("b", 0.6, "ok"),
        ]
        composite = c.composite_score(scores)
        assert abs(composite - 0.7) < 0.01

    def test_composite_score_weighted(self):
        criteria = [
            EvaluationCriterion("a", "desc", weight=2.0),
            EvaluationCriterion("b", "desc", weight=1.0),
        ]
        c = SprintContract("s1", "test", criteria=criteria)
        scores = [
            CriterionScore("a", 0.9, "great"),
            CriterionScore("b", 0.3, "poor"),
        ]
        # (0.9*2 + 0.3*1) / 3 = 2.1/3 = 0.7
        assert abs(c.composite_score(scores) - 0.7) < 0.01


class TestEvaluationResult:
    def test_passed(self):
        r = EvaluationResult("s1", 1, [], 0.85, True, "Looks great")
        assert r.passed is True

    def test_failed(self):
        r = EvaluationResult("s1", 1, [], 0.45, False, "Needs work", "pivot")
        assert r.passed is False
        assert r.strategy_recommendation == "pivot"


class TestHarnessConfig:
    def test_defaults(self):
        config = HarnessConfig(
            name="test",
            planner_config=AgentConfig(name="p"),
            generator_config=AgentConfig(name="g"),
            evaluator_config=AgentConfig(name="e"),
        )
        assert config.max_iterations == 5
        assert config.acceptance_threshold == 0.7

    def test_with_criteria(self):
        config = HarnessConfig(
            name="test",
            planner_config=AgentConfig(name="p"),
            generator_config=AgentConfig(name="g"),
            evaluator_config=AgentConfig(name="e"),
            default_criteria=[EvaluationCriterion("c1", "d1")],
        )
        assert len(config.default_criteria) == 1


class TestHarnessResult:
    def test_accepted(self):
        r = HarnessResult(
            harness_name="test",
            sprint_contract=SprintContract("s1", "obj"),
            final_status="accepted",
        )
        assert r.final_status == "accepted"

    def test_max_iterations(self):
        r = HarnessResult(
            harness_name="test",
            sprint_contract=SprintContract("s1", "obj"),
            iterations=[EvaluationResult("s1", i, [], 0.5, False, "meh") for i in range(1, 6)],
            final_status="max_iterations",
        )
        assert len(r.iterations) == 5


class TestHarnessRunner:
    def test_builds_with_config(self):
        config = HarnessConfig(
            name="test",
            planner_config=AgentConfig(name="p"),
            generator_config=AgentConfig(name="g"),
            evaluator_config=AgentConfig(name="e"),
        )
        runner = HarnessRunner(config)
        assert runner.config.name == "test"

    def test_build_plan_task(self):
        config = HarnessConfig(
            name="test",
            planner_config=AgentConfig(name="p"),
            generator_config=AgentConfig(name="g"),
            evaluator_config=AgentConfig(name="e"),
            default_criteria=FRONTEND_CRITERIA,
        )
        runner = HarnessRunner(config)
        task = runner._build_plan_task("Build a dashboard")
        assert task.task_type == "plan"
        assert "dashboard" in task.description

    def test_build_generate_task_without_feedback(self):
        config = frontend_design_harness()
        runner = HarnessRunner(config)
        contract = SprintContract("s1", "Build page", criteria=FRONTEND_CRITERIA)
        task = runner._build_generate_task(contract)
        assert task.task_type == "generate"
        assert "previous_feedback" not in task.inputs

    def test_build_generate_task_with_feedback(self):
        config = frontend_design_harness()
        runner = HarnessRunner(config)
        contract = SprintContract("s1", "Build page", criteria=FRONTEND_CRITERIA)
        feedback = EvaluationResult(
            "s1",
            1,
            [CriterionScore("design_quality", 0.5, "Needs color work")],
            0.5,
            False,
            "Improve colors",
            "refine",
        )
        task = runner._build_generate_task(contract, feedback)
        assert "previous_feedback" in task.inputs
        assert "refine" in task.inputs["previous_feedback"]

    def test_parse_evaluation(self):
        config = frontend_design_harness()
        runner = HarnessRunner(config)
        contract = SprintContract("s1", "test", criteria=FRONTEND_CRITERIA)
        result = TaskResult(
            task_id="t1",
            status="completed",
            outputs={
                "scores": [
                    {"criterion_name": "design_quality", "score": 0.8, "feedback": "Good"},
                    {"criterion_name": "originality", "score": 0.7, "feedback": "OK"},
                    {"criterion_name": "craft", "score": 0.75, "feedback": "Solid"},
                    {"criterion_name": "functionality", "score": 0.9, "feedback": "Great"},
                ],
                "summary": "Decent work",
                "strategy_recommendation": "refine",
            },
        )
        ev = runner._parse_evaluation(result, contract, 1)
        assert len(ev.scores) == 4
        assert ev.overall_score > 0.7
        assert ev.passed is True


class TestFrontendDesignHarness:
    def test_factory(self):
        config = frontend_design_harness()
        assert config.name == "frontend-design"
        assert len(config.default_criteria) == 4
        assert config.planner_config.name == "frontend-planner"
        assert config.generator_config.name == "frontend-generator"
        assert config.evaluator_config.name == "frontend-evaluator"

    def test_criteria_names(self):
        config = frontend_design_harness()
        names = {c.name for c in config.default_criteria}
        assert names == {"design_quality", "originality", "craft", "functionality"}

    def test_originality_lower_threshold(self):
        config = frontend_design_harness()
        originality = next(c for c in config.default_criteria if c.name == "originality")
        assert originality.threshold == 0.6
        assert originality.weight == 0.8
