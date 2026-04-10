"""Scoring functions for CaseHOLD legal holdings evaluation.

Implements:
  - Accuracy: fraction of correctly identified holdings
  - Confidence analysis: accuracy by confidence bucket (high/medium/low)
  - Citation grounding rate: fraction with verified supporting quotes
  - Abstention rate: fraction of "I don't know" responses (predicted_idx=-1)
  - Neon persistence to julia_casehold_eval_runs (Kimball transaction fact)

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any  # noqa: I001

# ── Data Classes ───────────────────────────────────────────────


@dataclass
class CaseHOLDGrade:
    """Score for a single CaseHOLD prediction."""

    example_id: str = ""
    predicted_idx: int = -1
    gold_idx: int = -1
    correct: bool = False
    confidence: float = 0.0
    supporting_quote: str = ""
    grounding_verified: bool = False


# ── Accuracy ───────────────────────────────────────────────────


def compute_casehold_accuracy(grades: list[CaseHOLDGrade]) -> float:
    """Compute accuracy for CaseHOLD predictions.

    Excludes abstentions (predicted_idx == -1) from the denominator.
    """
    attempted = [g for g in grades if g.predicted_idx != -1]
    if not attempted:
        return 0.0
    correct = sum(1 for g in attempted if g.correct)
    return correct / len(attempted)


# ── Confidence Analysis ────────────────────────────────────────


def _confidence_bucket(confidence: float) -> str:
    """Classify confidence into high/medium/low buckets."""
    if confidence > 0.8:
        return "high"
    if confidence >= 0.5:
        return "medium"
    return "low"


def compute_confidence_analysis(grades: list[CaseHOLDGrade]) -> dict[str, Any]:
    """Accuracy breakdown by confidence bucket (high/medium/low).

    Returns dict with per-bucket accuracy, count, and correct count.
    Follows Kimball degenerate dimension pattern — confidence_bucket
    is computed at query time, not stored separately.
    """
    buckets: dict[str, dict[str, int]] = {
        "high": {"correct": 0, "total": 0},
        "medium": {"correct": 0, "total": 0},
        "low": {"correct": 0, "total": 0},
    }

    for g in grades:
        if g.predicted_idx == -1:
            continue
        bucket = _confidence_bucket(g.confidence)
        buckets[bucket]["total"] += 1
        if g.correct:
            buckets[bucket]["correct"] += 1

    result: dict[str, Any] = {}
    for bucket, counts in buckets.items():
        total = counts["total"]
        correct = counts["correct"]
        result[bucket] = {
            "accuracy": correct / total if total > 0 else 0.0,
            "correct": correct,
            "total": total,
        }

    return result


# ── Citation Grounding ─────────────────────────────────────────


def verify_citation_grounding(
    supporting_quote: str,
    citing_prompt: str,
) -> bool:
    """Verify that the supporting quote appears in the citing passage.

    Uses fuzzy substring matching via SequenceMatcher.
    Returns True if the quote matches at >= 80% character level.
    """
    if not supporting_quote or not citing_prompt:
        return False

    norm_quote = " ".join(supporting_quote.split()).lower()
    norm_context = " ".join(citing_prompt.split()).lower()

    # Exact substring match
    if norm_quote in norm_context:
        return True

    # Fuzzy match for minor variations
    matcher = SequenceMatcher(None, norm_quote, norm_context)
    blocks = matcher.get_matching_blocks()
    matched_chars = sum(block.size for block in blocks)
    ratio = matched_chars / max(len(norm_quote), 1)

    return ratio >= 0.8


def compute_citation_grounding_rate(grades: list[CaseHOLDGrade]) -> float:
    """Fraction of predictions with verified supporting quotes.

    Excludes abstentions and errors from the denominator.
    """
    attempted = [g for g in grades if g.predicted_idx != -1]
    if not attempted:
        return 0.0
    verified = sum(1 for g in attempted if g.grounding_verified)
    return verified / len(attempted)


# ── Abstention Rate ────────────────────────────────────────────


def compute_abstention_rate(grades: list[CaseHOLDGrade]) -> float:
    """Fraction of predictions where model said 'I don't know' (idx=-1)."""
    if not grades:
        return 0.0
    abstentions = sum(1 for g in grades if g.predicted_idx == -1)
    return abstentions / len(grades)


# ── Aggregation ────────────────────────────────────────────────


def aggregate_casehold_grades(grades: list[CaseHOLDGrade]) -> dict[str, Any]:
    """Compute all CaseHOLD metrics for a set of grades."""
    return {
        "accuracy": compute_casehold_accuracy(grades),
        "grounding_rate": compute_citation_grounding_rate(grades),
        "abstention_rate": compute_abstention_rate(grades),
        "confidence_analysis": compute_confidence_analysis(grades),
        "total": len(grades),
        "attempted": sum(1 for g in grades if g.predicted_idx != -1),
        "correct": sum(1 for g in grades if g.correct),
        "abstentions": sum(1 for g in grades if g.predicted_idx == -1),
    }


# ── Neon Persistence ──────────────────────────────────────────


async def persist_casehold_result(
    conn,
    *,
    run_id: str,
    example_id: str,
    citing_prompt: str,
    holding_options: list[str],
    predicted_idx: int,
    gold_idx: int,
    correct: bool,
    confidence: float,
    supporting_quote: str | None,
    grounding_verified: bool,
    jurisdiction: str | None,
    reasoning: str | None,
    model: str,
    input_tokens: int | None,
    output_tokens: int | None,
    duration_ms: int | None,
    harness_run_id: int | None = None,
) -> int:
    """Persist a CaseHOLD eval result to julia_casehold_eval_runs.

    Schema: julia/evals/casehold/schema.sql (Kimball transaction fact).
    """
    import json

    row = await (
        await conn.execute(
            """INSERT INTO julia_casehold_eval_runs
               (harness_run_id, run_id, example_id,
                predicted_idx, gold_idx, correct, confidence,
                supporting_quote, grounding_verified,
                jurisdiction, citing_prompt, holding_options, reasoning,
                model, input_tokens, output_tokens, duration_ms)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                harness_run_id,
                run_id,
                example_id,
                predicted_idx,
                gold_idx,
                correct,
                confidence,
                supporting_quote,
                grounding_verified,
                jurisdiction,
                citing_prompt,
                json.dumps(holding_options),
                reasoning,
                model,
                input_tokens,
                output_tokens,
                duration_ms,
            ),
        )
    ).fetchone()
    return row[0]
