"""Tests for LexGLUE eval metrics, prompt construction, and response parsing.

No API calls, no database connections — pure unit tests.

Auth: N/A (no API calls).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# Ensure scripts/ is importable
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lexglue_metrics import (  # noqa: E402
    accuracy,
    classification_report,
    macro_f1,
    micro_f1,
    multilabel_macro_f1,
    multilabel_micro_f1,
)

# Load run-lexglue-eval.py (hyphenated filename can't be imported normally)
_spec = importlib.util.spec_from_file_location(
    "run_lexglue_eval", PROJECT_ROOT / "scripts" / "run-lexglue-eval.py"
)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["run_lexglue_eval"] = _mod
_spec.loader.exec_module(_mod)

# ═══════════════════════════════════════════════════════════════
# Metric Tests
# ═══════════════════════════════════════════════════════════════


class TestAccuracy:
    def test_perfect(self):
        y_true = ["a", "b", "c", "a", "b"]
        y_pred = ["a", "b", "c", "a", "b"]
        assert accuracy(y_true, y_pred) == 1.0

    def test_zero(self):
        y_true = ["a", "b", "c"]
        y_pred = ["b", "c", "a"]
        assert accuracy(y_true, y_pred) == 0.0

    def test_partial(self):
        y_true = ["a", "b", "c", "a"]
        y_pred = ["a", "b", "a", "a"]
        assert accuracy(y_true, y_pred) == 0.75

    def test_empty(self):
        assert accuracy([], []) == 0.0


class TestMicroF1:
    def test_perfect(self):
        y_true = ["a", "b", "c", "a"]
        y_pred = ["a", "b", "c", "a"]
        assert micro_f1(y_true, y_pred) == 1.0

    def test_partial(self):
        # 2 correct (a, c), 2 errors
        y_true = ["a", "b", "c", "a"]
        y_pred = ["a", "c", "c", "b"]
        score = micro_f1(y_true, y_pred)
        assert 0.0 < score < 1.0

    def test_all_wrong(self):
        y_true = ["a", "a", "a"]
        y_pred = ["b", "b", "b"]
        assert micro_f1(y_true, y_pred) == 0.0

    def test_micro_equals_accuracy_for_single_label(self):
        """For single-label, micro-F1 equals accuracy."""
        y_true = ["a", "b", "c", "a", "b"]
        y_pred = ["a", "b", "a", "a", "b"]
        assert abs(micro_f1(y_true, y_pred) - accuracy(y_true, y_pred)) < 1e-10


class TestMacroF1:
    def test_perfect(self):
        y_true = ["a", "b", "c"]
        y_pred = ["a", "b", "c"]
        assert macro_f1(y_true, y_pred) == 1.0

    def test_imbalanced(self):
        """Macro-F1 weights all classes equally regardless of support."""
        # Class 'a' has 5 samples, class 'b' has 1
        y_true = ["a", "a", "a", "a", "a", "b"]
        y_pred = ["a", "a", "a", "a", "a", "a"]
        # 'a' F1 = ~0.909, 'b' F1 = 0.0 → macro = ~0.455
        score = macro_f1(y_true, y_pred)
        assert score < 0.5  # Penalized for missing class 'b'

    def test_symmetric_errors(self):
        """Symmetric confusion → same per-class F1."""
        y_true = ["a", "b", "a", "b"]
        y_pred = ["b", "a", "a", "b"]
        score = macro_f1(y_true, y_pred)
        assert 0.4 < score < 0.6


class TestMultilabelF1:
    def test_perfect(self):
        y_true = [{"a", "b"}, {"c"}, {"a", "c"}]
        y_pred = [{"a", "b"}, {"c"}, {"a", "c"}]
        assert multilabel_micro_f1(y_true, y_pred) == 1.0

    def test_partial_overlap(self):
        y_true = [{"a", "b"}, {"b", "c"}]
        y_pred = [{"a"}, {"b", "c", "d"}]
        # TP=3 (a, b, c), FP=1 (d), FN=1 (b from first)
        score = multilabel_micro_f1(y_true, y_pred)
        assert 0.5 < score < 1.0

    def test_no_overlap(self):
        y_true = [{"a"}, {"b"}]
        y_pred = [{"c"}, {"d"}]
        assert multilabel_micro_f1(y_true, y_pred) == 0.0

    def test_empty_sets(self):
        y_true = [set(), set()]
        y_pred = [set(), set()]
        # All empty → TP=0, FP=0, FN=0 → F1=0
        assert multilabel_micro_f1(y_true, y_pred) == 0.0

    def test_macro_vs_micro(self):
        """Macro-F1 <= micro-F1 when frequent labels are more accurate."""
        y_true = [{"a"}, {"a"}, {"a"}, {"b"}]
        y_pred = [{"a"}, {"a"}, {"a"}, {"a"}]
        micro = multilabel_micro_f1(y_true, y_pred)
        macro = multilabel_macro_f1(y_true, y_pred)
        # 'a' perfect, 'b' missed → macro penalized more
        assert macro <= micro


class TestClassificationReport:
    def test_report_structure(self):
        y_true = ["a", "b", "a"]
        y_pred = ["a", "a", "a"]
        report = classification_report(y_true, y_pred)
        assert len(report) == 2
        for entry in report:
            assert "label" in entry
            assert "precision" in entry
            assert "recall" in entry
            assert "f1" in entry
            assert "support" in entry

    def test_perfect_report(self):
        y_true = ["x", "y", "x"]
        y_pred = ["x", "y", "x"]
        report = classification_report(y_true, y_pred)
        for entry in report:
            assert entry["f1"] == 1.0


# ═══════════════════════════════════════════════════════════════
# Response Parsing Tests
# ═══════════════════════════════════════════════════════════════


class TestResponseParsing:
    """Test JSON extraction and task-specific parsing."""

    def _import_parser(self):
        return _mod.LexGLUETask, _mod.parse_response, _mod._extract_json

    def test_extract_json_plain(self):
        _, _, extract = self._import_parser()
        result = extract('{"provision_type": "Termination", "confidence": 0.95}')
        assert result is not None
        assert result["provision_type"] == "Termination"

    def test_extract_json_markdown_fence(self):
        _, _, extract = self._import_parser()
        text = '```json\n{"label": "entailment", "reasoning": "test"}\n```'
        result = extract(text)
        assert result is not None
        assert result["label"] == "entailment"

    def test_extract_json_with_surrounding_text(self):
        _, _, extract = self._import_parser()
        text = 'Here is my analysis:\n{"answer": "B", "reasoning": "test"}\nDone.'
        result = extract(text)
        assert result is not None
        assert result["answer"] == "B"

    def test_extract_json_invalid(self):
        _, _, extract = self._import_parser()
        assert extract("This is not JSON at all") is None

    def test_parse_ledgar(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="ledgar_0",
            task_type="ledgar",
            text="test",
            label="Termination",
            label_set=["Termination", "Governing Law"],
        )
        result = parse(
            task, '{"provision_type": "Termination", "confidence": 0.9, "reasoning": "x"}'
        )
        assert result.predicted_label == "Termination"
        assert result.is_correct is True

    def test_parse_ledgar_wrong(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="ledgar_0",
            task_type="ledgar",
            text="test",
            label="Termination",
            label_set=["Termination", "Governing Law"],
        )
        result = parse(
            task, '{"provision_type": "Governing Law", "confidence": 0.5, "reasoning": "x"}'
        )
        assert result.predicted_label == "Governing Law"
        assert result.is_correct is False

    def test_parse_casehold(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="casehold_0",
            task_type="casehold",
            text="context with <HOLDING>",
            label="2",
            holdings=["h0", "h1", "h2", "h3", "h4"],
        )
        result = parse(task, '{"answer": "C", "reasoning": "third holding is correct"}')
        assert result.predicted_label == "2"
        assert result.is_correct is True

    def test_parse_scotus(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="scotus_0",
            task_type="scotus",
            text="The defendant was convicted of robbery...",
            label="Criminal Procedure",
            label_set=["Criminal Procedure", "Civil Rights", "First Amendment"],
        )
        result = parse(
            task, '{"issue_area": "Criminal Procedure", "confidence": 0.9, "reasoning": "x"}'
        )
        assert result.predicted_label == "Criminal Procedure"
        assert result.is_correct is True

    def test_parse_unfair_tos(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="tos_0",
            task_type="unfair_tos",
            text="We can terminate at any time",
            labels=["unilateral_termination"],
        )
        result = parse(
            task,
            '{"is_unfair": true, "unfairness_types": ["unilateral_termination"], "reasoning": "x"}',
        )
        assert result.predicted_labels == ["unilateral_termination"]
        assert result.is_correct is True

    def test_parse_ecthr_a(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="ecthr_0",
            task_type="ecthr_a",
            text="detention without trial",
            labels=["5", "6"],
        )
        result = parse(task, '{"violated_articles": ["5", "6"], "reasoning": "x"}')
        assert result.predicted_labels == ["5", "6"]
        assert result.is_correct is True

    def test_parse_contract_nli(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="nli_0",
            task_type="contract_nli",
            text="Premise: X\nHypothesis: Y",
            label="entailment",
            label_set=["contradiction", "entailment", "neutral"],
        )
        result = parse(task, '{"label": "entailment", "confidence": 0.9, "reasoning": "x"}')
        assert result.predicted_label == "entailment"
        assert result.is_correct is True

    def test_parse_ecthr_b(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="ecthr_b_0",
            task_type="ecthr_b",
            text="detention case",
            labels=["3", "5"],
            label_set=["2", "3", "5", "6", "8", "9", "10", "11", "14", "P1-1"],
        )
        result = parse(task, '{"violated_articles": ["3", "5"], "reasoning": "x"}')
        assert result.predicted_labels == ["3", "5"]
        assert result.is_correct is True

    def test_parse_eurlex(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="eurlex_0",
            task_type="eurlex",
            text="EU regulation text",
            labels=["100163", "100199"],
            label_set=["100163", "100168", "100199"],
        )
        result = parse(task, '{"concepts": ["100163", "100199"], "reasoning": "x"}')
        assert result.predicted_labels == ["100163", "100199"]
        assert result.is_correct is True

    def test_parse_error(self):
        Task, parse, _ = self._import_parser()
        task = Task(task_id="err_0", task_type="ledgar", text="test", label="X")
        result = parse(task, "Not valid JSON output")
        assert result.error is not None

    def test_label_validation_rejects_hallucinated_label(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="val_0",
            task_type="ledgar",
            text="test provision",
            label="Termination",
            label_set=["Termination", "Governing Law"],
        )
        result = parse(
            task, '{"provision_type": "Imaginary Category", "confidence": 0.5, "reasoning": "x"}'
        )
        assert result.error is not None
        assert "Hallucinated" in result.error

    def test_label_validation_rejects_hallucinated_multi_label(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="val_1",
            task_type="ecthr_a",
            text="case text",
            labels=["5"],
            label_set=["2", "3", "5", "6", "8"],
        )
        result = parse(task, '{"violated_articles": ["5", "99"], "reasoning": "x"}')
        assert result.error is not None
        assert "Hallucinated" in result.error


# ═══════════════════════════════════════════════════════════════
# Prompt Building Tests
# ═══════════════════════════════════════════════════════════════


class TestPromptBuilding:
    """Test that prompts contain required elements."""

    def _import_builders(self):
        return _mod.LexGLUETask, {
            "ledgar": _mod.build_ledgar_prompt,
            "unfair_tos": _mod.build_unfair_tos_prompt,
            "scotus": _mod.build_scotus_prompt,
            "ecthr_a": _mod.build_ecthr_a_prompt,
            "ecthr_b": _mod.build_ecthr_b_prompt,
            "eurlex": _mod.build_eurlex_prompt,
            "contract_nli": _mod.build_contract_nli_prompt,
            "casehold": _mod.build_casehold_prompt,
        }

    def test_ledgar_prompt_has_label_set(self):
        Task, builders = self._import_builders()
        task = Task(
            task_id="test",
            task_type="ledgar",
            text="Some provision text",
            label_set=["Termination", "Governing Law", "Indemnification"],
        )
        prompt = builders["ledgar"](task, 0)
        assert "Termination" in prompt
        assert "Governing Law" in prompt
        assert "Indemnification" in prompt
        assert "<document>" in prompt

    def test_casehold_prompt_has_options(self):
        Task, builders = self._import_builders()
        task = Task(
            task_id="test",
            task_type="casehold",
            text="Context with <HOLDING>",
            holdings=["holding A", "holding B", "holding C", "holding D", "holding E"],
        )
        prompt = builders["casehold"](task, 0)
        assert "(A)" in prompt
        assert "(E)" in prompt
        assert "holding A" in prompt
        assert "holding E" in prompt

    def test_scotus_prompt_has_labels(self):
        Task, builders = self._import_builders()
        task = Task(
            task_id="test",
            task_type="scotus",
            text="The defendant was convicted of robbery...",
            label_set=["Criminal Procedure", "Civil Rights", "First Amendment"],
        )
        prompt = builders["scotus"](task, 0)
        assert "Criminal Procedure" in prompt
        assert "Civil Rights" in prompt
        assert "First Amendment" in prompt

    def test_unfair_tos_prompt_has_document_tags(self):
        Task, builders = self._import_builders()
        task = Task(
            task_id="test",
            task_type="unfair_tos",
            text="Terms of service text here",
            label_set=["limitation_of_liability", "unilateral_termination"],
        )
        prompt = builders["unfair_tos"](task, 0)
        assert "<document>" in prompt
        assert "Terms of service text here" in prompt
        assert "limitation_of_liability" in prompt

    def test_ecthr_prompt_has_articles(self):
        Task, builders = self._import_builders()
        task = Task(
            task_id="test",
            task_type="ecthr_a",
            text="Case description",
            label_set=["2", "3", "5", "6", "8"],
        )
        prompt = builders["ecthr_a"](task, 0)
        assert "Article 2" in prompt
        assert "Article 8" in prompt

    def test_contract_nli_prompt_has_labels(self):
        Task, builders = self._import_builders()
        task = Task(
            task_id="test",
            task_type="contract_nli",
            text="Premise: X\nHypothesis: Y",
        )
        prompt = builders["contract_nli"](task, 0)
        assert "entailment" in prompt
        assert "contradiction" in prompt
        assert "neutral" in prompt

    def test_ecthr_b_prompt_has_articles(self):
        Task, builders = self._import_builders()
        task = Task(
            task_id="test",
            task_type="ecthr_b",
            text="Case description about detention",
            label_set=["2", "3", "5", "6", "8", "P1-1"],
        )
        prompt = builders["ecthr_b"](task, 0)
        assert "Article 2" in prompt
        assert "Article P1-1" in prompt

    def test_eurlex_prompt_has_concepts(self):
        Task, builders = self._import_builders()
        task = Task(
            task_id="test",
            task_type="eurlex",
            text="EU directive on environmental protection",
            label_set=["100163", "100168", "100199"],
        )
        prompt = builders["eurlex"](task, 0)
        assert "100163" in prompt
        assert "EuroVoc" in prompt

    def test_prompts_use_document_tags(self):
        """All prompts should wrap document text in <document> tags for safety."""
        Task, builders = self._import_builders()
        for task_type, builder in builders.items():
            task = Task(
                task_id="test",
                task_type=task_type,
                text="sensitive document content",
                label_set=["a", "b"],
                holdings=["h1", "h2", "h3", "h4", "h5"] if task_type == "casehold" else None,
            )
            prompt = builder(task, 0)
            assert "<document>" in prompt, f"{task_type} prompt missing <document> tags"


# ═══════════════════════════════════════════════════════════════
# Metric Computation Tests (task-level)
# ═══════════════════════════════════════════════════════════════


class TestTaskMetrics:
    def _import_compute(self):
        return _mod.LexGLUEResult, _mod.compute_task_metrics

    def test_ledgar_metrics(self):
        Result, compute = self._import_compute()
        results = [
            Result(
                task_id="0",
                task_type="ledgar",
                gold_label="A",
                predicted_label="A",
                is_correct=True,
            ),
            Result(
                task_id="1",
                task_type="ledgar",
                gold_label="B",
                predicted_label="B",
                is_correct=True,
            ),
            Result(
                task_id="2",
                task_type="ledgar",
                gold_label="C",
                predicted_label="A",
                is_correct=False,
            ),
        ]
        metrics = compute("ledgar", results)
        assert metrics["metric"] == "micro_f1"
        assert metrics["total"] == 3
        assert metrics["score"] > 0

    def test_scotus_metrics(self):
        Result, compute = self._import_compute()
        results = [
            Result(
                task_id="0",
                task_type="scotus",
                gold_label="Criminal Procedure",
                predicted_label="Criminal Procedure",
                is_correct=True,
            ),
            Result(
                task_id="1",
                task_type="scotus",
                gold_label="Civil Rights",
                predicted_label="First Amendment",
                is_correct=False,
            ),
        ]
        metrics = compute("scotus", results)
        assert metrics["metric"] == "micro_f1"
        assert metrics["score"] == 50.0

    def test_contract_nli_metrics(self):
        Result, compute = self._import_compute()
        results = [
            Result(
                task_id="0",
                task_type="contract_nli",
                gold_label="entailment",
                predicted_label="entailment",
                is_correct=True,
            ),
            Result(
                task_id="1",
                task_type="contract_nli",
                gold_label="contradiction",
                predicted_label="neutral",
                is_correct=False,
            ),
        ]
        metrics = compute("contract_nli", results)
        assert metrics["metric"] == "accuracy"
        assert metrics["score"] == 50.0

    def test_eurlex_metrics(self):
        Result, compute = self._import_compute()
        results = [
            Result(
                task_id="0",
                task_type="eurlex",
                gold_labels=["100163", "100199"],
                predicted_labels=["100163", "100199"],
                is_correct=True,
            ),
            Result(
                task_id="1",
                task_type="eurlex",
                gold_labels=["100168"],
                predicted_labels=["100168", "100199"],
                is_correct=False,
            ),
        ]
        metrics = compute("eurlex", results)
        assert metrics["metric"] == "micro_f1"
        assert metrics["total"] == 2
        assert metrics["score"] > 0

    def test_ecthr_b_metrics(self):
        Result, compute = self._import_compute()
        results = [
            Result(
                task_id="0",
                task_type="ecthr_b",
                gold_labels=["3", "5"],
                predicted_labels=["3", "5"],
                is_correct=True,
            ),
            Result(
                task_id="1",
                task_type="ecthr_b",
                gold_labels=["8"],
                predicted_labels=["8", "10"],
                is_correct=False,
            ),
        ]
        metrics = compute("ecthr_b", results)
        assert metrics["metric"] == "micro_f1"
        assert metrics["total"] == 2

    def test_all_errors_returns_zero_metrics(self):
        Result, compute = self._import_compute()
        results = [
            Result(task_id="0", task_type="ledgar", error="API error"),
            Result(task_id="1", task_type="ledgar", error="timeout"),
        ]
        metrics = compute("ledgar", results)
        assert metrics["total"] == 0
        assert metrics["errors"] == 2
        assert metrics["score"] == 0.0
        assert metrics["exact_match_rate"] == 0.0

    def test_errors_excluded(self):
        Result, compute = self._import_compute()
        results = [
            Result(
                task_id="0",
                task_type="ledgar",
                gold_label="A",
                predicted_label="A",
                is_correct=True,
            ),
            Result(task_id="1", task_type="ledgar", error="API error"),
        ]
        metrics = compute("ledgar", results)
        assert metrics["total"] == 1
        assert metrics["errors"] == 1


# ═══════════════════════════════════════════════════════════════
# Few-Shot Builder Tests
# ═══════════════════════════════════════════════════════════════


class TestFewShotBuilder:
    """Test that _build_few_shot produces correct output for each task type."""

    def test_few_shot_disabled_returns_empty(self):
        result = _mod._build_few_shot("ledgar", 0)
        assert result == ""

    def test_few_shot_unknown_task_returns_empty(self):
        result = _mod._build_few_shot("nonexistent_task", 3)
        assert result == ""

    def test_few_shot_ledgar(self):
        result = _mod._build_few_shot("ledgar", 1)
        if result:  # Only if few_shot_examples.json exists
            assert "Example 1:" in result

    def test_few_shot_scotus(self):
        result = _mod._build_few_shot("scotus", 1)
        if result:
            assert "Example 1:" in result

    def test_few_shot_contract_nli(self):
        result = _mod._build_few_shot("contract_nli", 1)
        if result:
            assert "Premise:" in result

    def test_few_shot_ecthr_b(self):
        result = _mod._build_few_shot("ecthr_b", 1)
        if result:
            assert "articles:" in result

    def test_few_shot_eurlex(self):
        result = _mod._build_few_shot("eurlex", 1)
        if result:
            assert "concepts:" in result


# ═══════════════════════════════════════════════════════════════
# Label Validation Edge Cases
# ═══════════════════════════════════════════════════════════════


class TestLabelValidation:
    """Test label validation accepts valid labels and rejects invalid ones."""

    def _import_parser(self):
        return _mod.LexGLUETask, _mod.parse_response, _mod._extract_json

    def test_valid_single_label_passes(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="val_0",
            task_type="scotus",
            text="test case",
            label="Civil Rights",
            label_set=["Criminal Procedure", "Civil Rights", "First Amendment"],
        )
        result = parse(task, '{"issue_area": "Civil Rights", "confidence": 0.9, "reasoning": "x"}')
        assert result.error is None
        assert result.predicted_label == "Civil Rights"

    def test_valid_multi_label_passes(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="val_1",
            task_type="ecthr_b",
            text="case text",
            labels=["3", "5"],
            label_set=["2", "3", "5", "6", "8"],
        )
        result = parse(task, '{"violated_articles": ["3", "5"], "reasoning": "x"}')
        assert result.error is None

    def test_empty_label_set_skips_validation(self):
        Task, parse, _ = self._import_parser()
        task = Task(
            task_id="val_2",
            task_type="ledgar",
            text="test",
            label="X",
            label_set=[],
        )
        result = parse(task, '{"provision_type": "Anything", "confidence": 0.5, "reasoning": "x"}')
        assert result.error is None
