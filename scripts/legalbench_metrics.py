"""LegalBench evaluation metrics — category F1, citation precision, Best-of-N agreement.

Extends scripts/lexglue_metrics.py with LegalBench-specific scoring.
Reuses compute_source_score() from julia/evals/cuad/scoring.py for citation verification.

Pure-Python implementation using only stdlib + existing project modules.

Auth: N/A (no API calls — pure computation).
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lexglue_metrics import (  # noqa: E402
    accuracy,
    classification_report,
    macro_f1,
    micro_f1,
)

# Re-export for convenience
__all__ = [
    "accuracy",
    "micro_f1",
    "macro_f1",
    "classification_report",
    "category_accuracy",
    "category_f1",
    "binary_accuracy",
    "citation_precision",
    "citation_recall",
    "best_of_n_agreement_rate",
    "compute_citation_score",
]


def category_accuracy(
    results_by_category: dict[str, list[tuple[str, str]]],
) -> dict[str, float]:
    """Compute accuracy per category.

    Args:
        results_by_category: {category: [(gold, predicted), ...]}

    Returns:
        {category: accuracy}
    """
    out: dict[str, float] = {}
    for cat, pairs in results_by_category.items():
        if not pairs:
            out[cat] = 0.0
            continue
        y_true = [p[0] for p in pairs]
        y_pred = [p[1] for p in pairs]
        out[cat] = accuracy(y_true, y_pred)
    return out


def category_f1(
    results_by_category: dict[str, list[tuple[str, str]]],
) -> dict[str, float]:
    """Compute micro-F1 per category across all tasks in that category.

    Args:
        results_by_category: {category: [(gold, predicted), ...]}

    Returns:
        {category: micro_f1_score}
    """
    out: dict[str, float] = {}
    for cat, pairs in results_by_category.items():
        if not pairs:
            out[cat] = 0.0
            continue
        y_true = [p[0] for p in pairs]
        y_pred = [p[1] for p in pairs]
        out[cat] = micro_f1(y_true, y_pred)
    return out


def binary_accuracy(
    gold: list[str],
    predicted: list[str],
) -> float:
    """Accuracy specifically for binary Yes/No tasks.

    Contract NLI primary metric (target >= 85%, Harvey baseline: 74% Answer Score).
    Normalizes case before comparison.
    """
    if not gold:
        return 0.0
    correct = sum(
        1 for g, p in zip(gold, predicted, strict=True) if g.strip().lower() == p.strip().lower()
    )
    return correct / len(gold)


def compute_citation_score(
    quotes: list[str],
    source_text: str,
) -> float:
    """Verify that cited quotes appear in the source document.

    Reuses compute_source_score() from julia/evals/cuad/scoring.py
    which implements SequenceMatcher-based fuzzy substring matching.

    Returns mean source score across all quotes (0.0 if no quotes).
    """
    if not quotes:
        return 0.0

    sys.path.insert(0, str(PROJECT_ROOT / "julia" / "evals" / "cuad"))
    from scoring import compute_source_score  # noqa: E402

    scores = [compute_source_score(q, source_text) for q in quotes]
    return sum(scores) / len(scores)


def citation_precision(
    all_quotes: list[list[str]],
    all_sources: list[str],
    threshold: float = 0.5,
) -> float:
    """Fraction of cited quotes that are verified in the source document.

    A quote is "verified" if compute_source_score >= threshold.

    Args:
        all_quotes: list of quote lists (one per sample)
        all_sources: list of source texts (one per sample)
        threshold: minimum source score to consider a quote verified

    Returns:
        Precision: verified_quotes / total_quotes
    """
    total = 0
    verified = 0

    sys.path.insert(0, str(PROJECT_ROOT / "julia" / "evals" / "cuad"))
    from scoring import compute_source_score  # noqa: E402

    for quotes, source in zip(all_quotes, all_sources, strict=True):
        for quote in quotes:
            total += 1
            score = compute_source_score(quote, source)
            if score >= threshold:
                verified += 1

    return verified / total if total > 0 else 0.0


def citation_recall(
    results_with_quotes: int,
    total_results: int,
) -> float:
    """Fraction of predictions that include at least one citation.

    Measures whether the model is grounding its answers in the text.
    """
    if total_results == 0:
        return 0.0
    return results_with_quotes / total_results


def best_of_n_agreement_rate(
    agreements: list[float],
) -> float:
    """Mean agreement rate for Best-of-N predictions.

    Agreement = fraction of N attempts that agree with the majority vote.
    1.0 = unanimous, 0.33 = only 1 of 3 agrees.

    Args:
        agreements: list of agreement ratios (one per borderline sample)
    """
    if not agreements:
        return 0.0
    return sum(agreements) / len(agreements)


def aggregate_legalbench_metrics(
    y_true: list[str],
    y_pred: list[str],
    categories: list[str],
    answer_types: list[str],
) -> dict:
    """Compute comprehensive metrics for a LegalBench eval run.

    Returns a dict with overall, per-category, and per-answer-type breakdowns.
    """
    # Overall
    overall_acc = accuracy(y_true, y_pred)
    overall_f1 = micro_f1(y_true, y_pred)

    # Per category
    by_cat: dict[str, list[tuple[str, str]]] = {}
    for g, p, cat in zip(y_true, y_pred, categories, strict=True):
        by_cat.setdefault(cat, []).append((g, p))
    cat_acc = category_accuracy(by_cat)
    cat_f1 = category_f1(by_cat)

    # Per answer type
    by_type: dict[str, list[tuple[str, str]]] = {}
    for g, p, at in zip(y_true, y_pred, answer_types, strict=True):
        by_type.setdefault(at, []).append((g, p))
    type_acc = {t: accuracy([x[0] for x in pairs], [x[1] for x in pairs]) for t, pairs in by_type.items()}

    return {
        "overall_accuracy": round(overall_acc * 100, 2),
        "overall_micro_f1": round(overall_f1 * 100, 2),
        "per_category_accuracy": {k: round(v * 100, 2) for k, v in cat_acc.items()},
        "per_category_f1": {k: round(v * 100, 2) for k, v in cat_f1.items()},
        "per_answer_type_accuracy": {k: round(v * 100, 2) for k, v in type_acc.items()},
        "total_samples": len(y_true),
    }
