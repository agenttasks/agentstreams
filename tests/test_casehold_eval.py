"""Tests for CaseHOLD legal holdings evaluation.

Tests jurisdiction extraction, scoring functions, prompt engineering,
response parsing, and YAML config loading.

No API calls, no database connections — pure unit tests.

Auth: N/A (no API calls).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from julia.evals.casehold.prompts import (  # noqa: E402
    CASEHOLD_SYSTEM_PROMPT,
    build_casehold_prompt,
    extract_jurisdiction,
)
from julia.evals.casehold.scoring import (  # noqa: E402
    CaseHOLDGrade,
    compute_abstention_rate,
    compute_casehold_accuracy,
    compute_citation_grounding_rate,
    compute_confidence_analysis,
    verify_citation_grounding,
)

# ═══════════════════════════════════════════════════════════════
# Jurisdiction Extraction Tests
# ═══════════════════════════════════════════════════════════════


class TestExtractJurisdiction:
    def test_circuit_court(self):
        text = "See Garcia v. Acme Corp., 542 F.3d 210, 215 (5th Cir.2008) (<HOLDING>)."
        result = extract_jurisdiction(text)
        assert result is not None
        assert "5th" in result
        assert "cir" in result

    def test_ninth_circuit(self):
        text = "United States v. Smith, 100 F.3d 500 (9th Cir.1996) (<HOLDING>)"
        result = extract_jurisdiction(text)
        assert result is not None
        assert "9th" in result

    def test_state_court_ny(self):
        text = "Power Auth. of the State of New York, 81 N.Y.2d 649, 652 (N.Y.1993) (<HOLDING>)"
        result = extract_jurisdiction(text)
        assert result is not None
        assert "new_york" in result

    def test_district_court_ndill(self):
        text = "Vector Pipeline, L.P., 157 F.Supp.2d 949, 957 (N.D.Ill.2001) (<HOLDING>)"
        result = extract_jurisdiction(text)
        assert result is not None
        assert "n.d.ill" in result

    def test_federal_circuit(self):
        text = "Apple Inc. v. Samsung, 678 F.3d 1314 (Fed. Cir. 2012) (<HOLDING>)"
        result = extract_jurisdiction(text)
        assert result == "fed_cir"

    def test_delaware_chancery(self):
        text = "In re Walt Disney Co., 906 A.2d 27, 67 (Del.Ch.2006) (<HOLDING>)"
        result = extract_jurisdiction(text)
        assert result is not None
        assert "delaware" in result or "del" in result

    def test_no_jurisdiction(self):
        text = "The court held that the defendant was liable for damages."
        result = extract_jurisdiction(text)
        assert result is None

    def test_empty_string(self):
        assert extract_jurisdiction("") is None


# ═══════════════════════════════════════════════════════════════
# Scoring Function Tests
# ═══════════════════════════════════════════════════════════════


class TestComputeAccuracy:
    def test_perfect(self):
        grades = [
            CaseHOLDGrade(correct=True, predicted_idx=0, gold_idx=0),
            CaseHOLDGrade(correct=True, predicted_idx=1, gold_idx=1),
            CaseHOLDGrade(correct=True, predicted_idx=2, gold_idx=2),
        ]
        assert compute_casehold_accuracy(grades) == 1.0

    def test_zero(self):
        grades = [
            CaseHOLDGrade(correct=False, predicted_idx=0, gold_idx=1),
            CaseHOLDGrade(correct=False, predicted_idx=1, gold_idx=2),
        ]
        assert compute_casehold_accuracy(grades) == 0.0

    def test_partial(self):
        grades = [
            CaseHOLDGrade(correct=True, predicted_idx=0, gold_idx=0),
            CaseHOLDGrade(correct=False, predicted_idx=1, gold_idx=2),
        ]
        assert compute_casehold_accuracy(grades) == 0.5

    def test_excludes_abstentions(self):
        grades = [
            CaseHOLDGrade(correct=True, predicted_idx=0, gold_idx=0),
            CaseHOLDGrade(correct=False, predicted_idx=-1, gold_idx=1),  # abstention
        ]
        # Only 1 attempted, 1 correct → 100%
        assert compute_casehold_accuracy(grades) == 1.0

    def test_empty(self):
        assert compute_casehold_accuracy([]) == 0.0

    def test_all_abstentions(self):
        grades = [
            CaseHOLDGrade(correct=False, predicted_idx=-1, gold_idx=0),
            CaseHOLDGrade(correct=False, predicted_idx=-1, gold_idx=1),
        ]
        assert compute_casehold_accuracy(grades) == 0.0


class TestConfidenceAnalysis:
    def test_buckets(self):
        grades = [
            CaseHOLDGrade(correct=True, predicted_idx=0, confidence=0.95),  # high
            CaseHOLDGrade(correct=True, predicted_idx=1, confidence=0.85),  # high
            CaseHOLDGrade(correct=False, predicted_idx=2, confidence=0.65),  # medium
            CaseHOLDGrade(correct=True, predicted_idx=3, confidence=0.3),  # low
        ]
        result = compute_confidence_analysis(grades)

        assert result["high"]["total"] == 2
        assert result["high"]["correct"] == 2
        assert result["high"]["accuracy"] == 1.0

        assert result["medium"]["total"] == 1
        assert result["medium"]["correct"] == 0
        assert result["medium"]["accuracy"] == 0.0

        assert result["low"]["total"] == 1
        assert result["low"]["correct"] == 1
        assert result["low"]["accuracy"] == 1.0

    def test_empty(self):
        result = compute_confidence_analysis([])
        assert result["high"]["total"] == 0
        assert result["medium"]["total"] == 0
        assert result["low"]["total"] == 0

    def test_excludes_abstentions(self):
        grades = [
            CaseHOLDGrade(correct=True, predicted_idx=0, confidence=0.9),
            CaseHOLDGrade(correct=False, predicted_idx=-1, confidence=0.1),  # abstention
        ]
        result = compute_confidence_analysis(grades)
        total_counted = sum(b["total"] for b in result.values())
        assert total_counted == 1  # only the non-abstention


class TestCitationGrounding:
    def test_exact_match(self):
        assert verify_citation_grounding(
            "fair market value",
            "These cases teach that fair market value is not to be determined in a rarefied realm",
        )

    def test_case_insensitive(self):
        assert verify_citation_grounding(
            "Fair Market Value",
            "These cases teach that fair market value is not to be determined",
        )

    def test_not_found(self):
        assert not verify_citation_grounding(
            "this phrase is completely different",
            "The court held that damages were appropriate",
        )

    def test_empty_quote(self):
        assert not verify_citation_grounding("", "some context")

    def test_empty_context(self):
        assert not verify_citation_grounding("some quote", "")

    def test_grounding_rate(self):
        grades = [
            CaseHOLDGrade(predicted_idx=0, grounding_verified=True),
            CaseHOLDGrade(predicted_idx=1, grounding_verified=False),
            CaseHOLDGrade(predicted_idx=2, grounding_verified=True),
        ]
        assert compute_citation_grounding_rate(grades) == pytest.approx(2 / 3)

    def test_grounding_rate_excludes_abstentions(self):
        grades = [
            CaseHOLDGrade(predicted_idx=0, grounding_verified=True),
            CaseHOLDGrade(predicted_idx=-1, grounding_verified=False),  # abstention
        ]
        assert compute_citation_grounding_rate(grades) == 1.0


class TestAbstentionRate:
    def test_no_abstentions(self):
        grades = [
            CaseHOLDGrade(predicted_idx=0),
            CaseHOLDGrade(predicted_idx=1),
        ]
        assert compute_abstention_rate(grades) == 0.0

    def test_all_abstentions(self):
        grades = [
            CaseHOLDGrade(predicted_idx=-1),
            CaseHOLDGrade(predicted_idx=-1),
        ]
        assert compute_abstention_rate(grades) == 1.0

    def test_mixed(self):
        grades = [
            CaseHOLDGrade(predicted_idx=0),
            CaseHOLDGrade(predicted_idx=-1),
            CaseHOLDGrade(predicted_idx=2),
            CaseHOLDGrade(predicted_idx=-1),
        ]
        assert compute_abstention_rate(grades) == 0.5

    def test_empty(self):
        assert compute_abstention_rate([]) == 0.0


# ═══════════════════════════════════════════════════════════════
# Prompt Engineering Tests
# ═══════════════════════════════════════════════════════════════


class TestPromptEngineering:
    def test_system_prompt_has_leak_protection(self):
        assert "never reveal" in CASEHOLD_SYSTEM_PROMPT.lower()
        assert "evaluation criteria" in CASEHOLD_SYSTEM_PROMPT.lower()

    def test_system_prompt_has_idk_option(self):
        assert "-1" in CASEHOLD_SYSTEM_PROMPT
        assert "none" in CASEHOLD_SYSTEM_PROMPT.lower()

    def test_system_prompt_no_legal_advice(self):
        assert "never provide legal advice" in CASEHOLD_SYSTEM_PROMPT.lower()

    def test_predict_prompt_has_chain_of_thought(self):
        prompt = build_casehold_prompt(
            "test context (<HOLDING>)",
            ["h0", "h1", "h2", "h3", "h4"],
        )
        assert "Identify the legal issue" in prompt
        assert "For each candidate" in prompt
        assert "Select the best match" in prompt

    def test_predict_prompt_has_supporting_quote(self):
        prompt = build_casehold_prompt(
            "test context (<HOLDING>)",
            ["h0", "h1", "h2", "h3", "h4"],
        )
        assert "supporting_quote" in prompt
        assert "exact phrase" in prompt.lower()

    def test_predict_prompt_has_idk_option(self):
        prompt = build_casehold_prompt(
            "test context (<HOLDING>)",
            ["h0", "h1", "h2", "h3", "h4"],
        )
        assert "-1" in prompt
        assert "none match" in prompt.lower()

    def test_predict_prompt_contains_holdings(self):
        prompt = build_casehold_prompt(
            "context",
            ["alpha", "beta", "gamma", "delta", "epsilon"],
        )
        assert "0: alpha" in prompt
        assert "1: beta" in prompt
        assert "4: epsilon" in prompt

    def test_predict_prompt_contains_context(self):
        prompt = build_casehold_prompt(
            "The court considered whether <HOLDING>",
            ["h0", "h1", "h2", "h3", "h4"],
        )
        assert "The court considered whether <HOLDING>" in prompt


# ═══════════════════════════════════════════════════════════════
# Response Parsing Tests
# ═══════════════════════════════════════════════════════════════


class TestResponseParsing:
    def _import_parser(self):
        from julia.evals.casehold.runner import parse_json_response

        return parse_json_response

    def test_parse_valid_json(self):
        parse = self._import_parser()
        result = parse(
            '{"predicted_idx": 2, "confidence": 0.9, "reasoning": "test", "supporting_quote": "the court held"}'
        )
        assert result is not None
        assert result["predicted_idx"] == 2
        assert result["supporting_quote"] == "the court held"

    def test_parse_markdown_fenced(self):
        parse = self._import_parser()
        result = parse(
            '```json\n{"predicted_idx": 0, "confidence": 0.5, "reasoning": "x", "supporting_quote": "y"}\n```'
        )
        assert result is not None
        assert result["predicted_idx"] == 0

    def test_parse_abstention(self):
        parse = self._import_parser()
        result = parse(
            '{"predicted_idx": -1, "confidence": 0.1, "reasoning": "none match", "supporting_quote": ""}'
        )
        assert result is not None
        assert result["predicted_idx"] == -1

    def test_parse_invalid_json(self):
        parse = self._import_parser()
        assert parse("This is not JSON at all") is None

    def test_parse_json_with_surrounding_text(self):
        parse = self._import_parser()
        result = parse(
            'Here is my analysis:\n{"predicted_idx": 3, "confidence": 0.8, "reasoning": "match"}\nDone.'
        )
        assert result is not None
        assert result["predicted_idx"] == 3


# ═══════════════════════════════════════════════════════════════
# YAML Config Loading Tests
# ═══════════════════════════════════════════════════════════════


class TestConfigLoading:
    def _load_config(self):
        import yaml

        config_path = PROJECT_ROOT / "julia" / "evals" / "casehold" / "config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def test_config_has_name(self):
        config = self._load_config()
        assert config["name"] == "casehold"

    def test_config_has_model(self):
        config = self._load_config()
        assert config["model"]["name"] == "claude-opus-4-6"
        assert config["model"]["temperature"] == 0

    def test_config_targets(self):
        config = self._load_config()
        assert config["targets"]["accuracy"] >= 0.70
        assert config["targets"]["grounding_rate"] >= 0.80
        assert config["targets"]["abstention_rate_max"] <= 0.10

    def test_config_has_measures(self):
        config = self._load_config()
        measure_names = [m["name"] for m in config["measures"]]
        assert "accuracy" in measure_names
        assert "grounding_rate" in measure_names
        assert "abstention_rate" in measure_names
        assert "mean_confidence" in measure_names

    def test_config_has_dimensions(self):
        config = self._load_config()
        dim_names = [d["name"] for d in config["dimensions"]]
        assert "jurisdiction" in dim_names
        assert "confidence_bucket" in dim_names
        assert "model" in dim_names

    def test_config_has_baselines(self):
        config = self._load_config()
        assert "bert_base" in config["baselines"]
        assert config["baselines"]["bert_base"] == pytest.approx(0.714)

    def test_config_has_data_paths(self):
        config = self._load_config()
        assert "primary" in config["data"]
        assert "downloaded" in config["data"]

    def test_config_concurrency(self):
        config = self._load_config()
        assert config["concurrency"]["workers"] > 0
        assert config["concurrency"]["batch_size"] > 0


# ═══════════════════════════════════════════════════════════════
# Task Loading Tests
# ═══════════════════════════════════════════════════════════════


class TestTaskLoading:
    def test_load_from_json(self):
        from julia.evals.casehold.runner import _load_from_json

        data_path = (
            PROJECT_ROOT / "julia" / "evals" / "test_data" / "lexglue" / "casehold_samples.json"
        )
        if not data_path.exists():
            pytest.skip("casehold_samples.json not found")

        tasks = _load_from_json(data_path)
        assert len(tasks) > 0
        assert tasks[0].holdings is not None
        assert len(tasks[0].holdings) == 5
        assert 0 <= tasks[0].gold_idx <= 4

    def test_load_with_jurisdiction_extraction(self):
        from julia.evals.casehold.runner import load_casehold_tasks

        tasks = load_casehold_tasks(max_examples=10)
        if not tasks:
            pytest.skip("No CaseHOLD data available")

        # At least some tasks should have jurisdiction extracted
        jurisdictions = [t.jurisdiction for t in tasks if t.jurisdiction]
        assert len(jurisdictions) > 0
