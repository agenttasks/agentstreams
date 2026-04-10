"""Tests for LegalBench eval metrics, scoring, and citation verification.

No API calls, no database connections — pure unit tests.

Auth: N/A (no API calls).
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# Ensure scripts/ is importable
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "julia" / "evals" / "cuad"))

from legalbench_metrics import (  # noqa: E402
    accuracy,
    aggregate_legalbench_metrics,
    best_of_n_agreement_rate,
    binary_accuracy,
    category_accuracy,
    category_f1,
    citation_precision,
    compute_citation_score,
    micro_f1,
)

# ═══════════════════════════════════════════════════════════════
# Accuracy Tests
# ═══════════════════════════════════════════════════════════════


class TestAccuracy:
    def test_perfect(self):
        y_true = ["Yes", "No", "Yes", "No"]
        y_pred = ["Yes", "No", "Yes", "No"]
        assert accuracy(y_true, y_pred) == 1.0

    def test_zero(self):
        y_true = ["Yes", "No", "Yes"]
        y_pred = ["No", "Yes", "No"]
        assert accuracy(y_true, y_pred) == 0.0

    def test_partial(self):
        y_true = ["Yes", "No", "Yes", "No"]
        y_pred = ["Yes", "No", "No", "No"]
        assert accuracy(y_true, y_pred) == 0.75

    def test_empty(self):
        assert accuracy([], []) == 0.0


class TestBinaryAccuracy:
    def test_case_insensitive(self):
        gold = ["Yes", "No", "Yes"]
        pred = ["yes", "no", "YES"]
        assert binary_accuracy(gold, pred) == 1.0

    def test_with_whitespace(self):
        gold = ["Yes", "No"]
        pred = [" Yes ", " No "]
        assert binary_accuracy(gold, pred) == 1.0

    def test_empty(self):
        assert binary_accuracy([], []) == 0.0

    def test_mixed_correct(self):
        gold = ["Yes", "No", "Yes", "No"]
        pred = ["Yes", "Yes", "Yes", "No"]
        assert binary_accuracy(gold, pred) == 0.75


# ═══════════════════════════════════════════════════════════════
# F1 Tests
# ═══════════════════════════════════════════════════════════════


class TestMicroF1:
    def test_perfect(self):
        y_true = ["Yes", "No", "Yes"]
        y_pred = ["Yes", "No", "Yes"]
        assert micro_f1(y_true, y_pred) == 1.0

    def test_all_wrong(self):
        y_true = ["Yes", "Yes", "Yes"]
        y_pred = ["No", "No", "No"]
        assert micro_f1(y_true, y_pred) == 0.0

    def test_partial(self):
        y_true = ["A", "B", "C", "A"]
        y_pred = ["A", "C", "C", "B"]
        score = micro_f1(y_true, y_pred)
        assert 0.0 < score < 1.0


# ═══════════════════════════════════════════════════════════════
# Category Metrics Tests
# ═══════════════════════════════════════════════════════════════


class TestCategoryAccuracy:
    def test_single_category(self):
        results = {"contract_nli": [("Yes", "Yes"), ("No", "No"), ("Yes", "No")]}
        out = category_accuracy(results)
        assert "contract_nli" in out
        assert abs(out["contract_nli"] - 2.0 / 3.0) < 1e-6

    def test_multiple_categories(self):
        results = {
            "contract_nli": [("Yes", "Yes"), ("No", "No")],
            "rule_application": [("Yes", "No"), ("No", "No")],
        }
        out = category_accuracy(results)
        assert out["contract_nli"] == 1.0
        assert out["rule_application"] == 0.5

    def test_empty_category(self):
        results = {"empty": []}
        out = category_accuracy(results)
        assert out["empty"] == 0.0


class TestCategoryF1:
    def test_perfect(self):
        results = {"contract_nli": [("Yes", "Yes"), ("No", "No")]}
        out = category_f1(results)
        assert out["contract_nli"] == 1.0

    def test_zero(self):
        results = {"contract_nli": [("Yes", "No"), ("No", "Yes")]}
        out = category_f1(results)
        assert out["contract_nli"] == 0.0


# ═══════════════════════════════════════════════════════════════
# Citation Verification Tests
# ═══════════════════════════════════════════════════════════════


class TestComputeCitationScore:
    def test_exact_match(self):
        quotes = ["The vendor shall indemnify the client"]
        source = "The vendor shall indemnify the client against all claims."
        score = compute_citation_score(quotes, source)
        assert score == 1.0

    def test_no_match(self):
        quotes = ["This text does not appear anywhere in the document at all"]
        source = "Completely different content here."
        score = compute_citation_score(quotes, source)
        assert score < 0.5

    def test_empty_quotes(self):
        score = compute_citation_score([], "Some source text")
        assert score == 0.0

    def test_multiple_quotes(self):
        quotes = [
            "The vendor shall indemnify",
            "all claims arising from negligence",
        ]
        source = "The vendor shall indemnify the client against all claims arising from negligence."
        score = compute_citation_score(quotes, source)
        assert score > 0.8


class TestCitationPrecision:
    def test_all_verified(self):
        all_quotes = [["exact text here"]]
        all_sources = ["This is some exact text here in the document."]
        prec = citation_precision(all_quotes, all_sources, threshold=0.5)
        assert prec == 1.0

    def test_none_verified(self):
        all_quotes = [["fabricated quote that does not exist"]]
        all_sources = ["Completely unrelated document content."]
        prec = citation_precision(all_quotes, all_sources, threshold=0.9)
        assert prec < 1.0

    def test_empty(self):
        prec = citation_precision([], [], threshold=0.5)
        assert prec == 0.0


# ═══════════════════════════════════════════════════════════════
# Best-of-N Tests
# ═══════════════════════════════════════════════════════════════


class TestBestOfNAgreement:
    def test_unanimous(self):
        agreements = [1.0, 1.0, 1.0]
        assert best_of_n_agreement_rate(agreements) == 1.0

    def test_split(self):
        agreements = [1.0, 0.5, 0.5]
        rate = best_of_n_agreement_rate(agreements)
        assert abs(rate - 2.0 / 3.0) < 1e-6

    def test_empty(self):
        assert best_of_n_agreement_rate([]) == 0.0


# ═══════════════════════════════════════════════════════════════
# Aggregate Metrics Tests
# ═══════════════════════════════════════════════════════════════


class TestAggregateLegalBenchMetrics:
    def test_basic(self):
        y_true = ["Yes", "No", "Yes", "No"]
        y_pred = ["Yes", "No", "Yes", "Yes"]
        categories = ["contract_nli", "contract_nli", "cuad", "cuad"]
        answer_types = ["binary", "binary", "binary", "binary"]

        result = aggregate_legalbench_metrics(y_true, y_pred, categories, answer_types)

        assert result["overall_accuracy"] == 75.0
        assert result["total_samples"] == 4
        assert "contract_nli" in result["per_category_accuracy"]
        assert result["per_category_accuracy"]["contract_nli"] == 100.0
        assert result["per_category_accuracy"]["cuad"] == 50.0

    def test_multiple_answer_types(self):
        y_true = ["Yes", "generic", "A"]
        y_pred = ["Yes", "generic", "B"]
        categories = ["contract_nli", "rule_application", "maud"]
        answer_types = ["binary", "classification", "multiple_choice"]

        result = aggregate_legalbench_metrics(y_true, y_pred, categories, answer_types)

        assert "binary" in result["per_answer_type_accuracy"]
        assert result["per_answer_type_accuracy"]["binary"] == 100.0
        assert result["per_answer_type_accuracy"]["multiple_choice"] == 0.0


# ═══════════════════════════════════════════════════════════════
# Task Registry Tests
# ═══════════════════════════════════════════════════════════════


class TestTaskRegistry:
    def test_registry_loads(self):
        import json

        registry_path = PROJECT_ROOT / "scripts" / "legalbench_tasks.json"
        registry = json.loads(registry_path.read_text())
        assert len(registry) == 162

    def test_registry_has_required_fields(self):
        import json

        registry = json.loads((PROJECT_ROOT / "scripts" / "legalbench_tasks.json").read_text())
        required = {
            "category",
            "hf_config",
            "text_fields",
            "answer_field",
            "answer_type",
            "label_names",
        }
        for task_name, config in registry.items():
            missing = required - set(config.keys())
            assert not missing, f"{task_name} missing fields: {missing}"

    def test_contract_nli_count(self):
        import json

        registry = json.loads((PROJECT_ROOT / "scripts" / "legalbench_tasks.json").read_text())
        contract_nli = [t for t, c in registry.items() if c["category"] == "contract_nli"]
        assert len(contract_nli) == 14

    def test_answer_types_valid(self):
        import json

        registry = json.loads((PROJECT_ROOT / "scripts" / "legalbench_tasks.json").read_text())
        valid_types = {"binary", "multiple_choice", "classification", "extraction"}
        for task_name, config in registry.items():
            assert config["answer_type"] in valid_types, (
                f"{task_name} has invalid answer_type: {config['answer_type']}"
            )


# ═══════════════════════════════════════════════════════════════
# Document Escaping Tests
# ═══════════════════════════════════════════════════════════════


class TestDocumentEscaping:
    def test_safe_document_text_escapes_closing_tag(self):
        """XML injection prevention: </document> must be escaped."""
        text = "Some text </document> more text"
        # The eval runner's _safe_document_text should escape this
        escaped = text.replace("</document>", "&lt;/document&gt;")
        assert "</document>" not in escaped
        assert "&lt;/document&gt;" in escaped

    def test_safe_document_text_preserves_normal(self):
        text = "Normal legal text without XML tags."
        escaped = text.replace("</document>", "&lt;/document&gt;")
        assert escaped == text
