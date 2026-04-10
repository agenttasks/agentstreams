"""LexGLUE evaluation metrics — micro-F1, macro-F1, accuracy.

Pure-Python implementation using only stdlib (collections.Counter).
No sklearn dependency required.

Supports both single-label (LEDGAR, SCOTUS, ContractNLI, CaseHOLD) and
multi-label (UNFAIR-ToS, ECtHR-A/B, EUR-Lex) classification tasks.

Auth: N/A (no API calls — pure computation).
"""

from __future__ import annotations

from collections import Counter


def _precision_recall_f1(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    """Compute precision, recall, F1 from counts."""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def accuracy(y_true: list[str], y_pred: list[str]) -> float:
    """Exact-match accuracy for single-label classification.

    Used for ContractNLI, SCOTUS, and CaseHOLD tasks.
    """
    if not y_true:
        return 0.0
    correct = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == p)
    return correct / len(y_true)


def micro_f1(y_true: list[str], y_pred: list[str], labels: list[str] | None = None) -> float:
    """Micro-averaged F1 for single-label classification.

    Aggregates TP/FP/FN across all classes before computing F1.
    Used for LEDGAR and ECtHR-A tasks.
    """
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p == label)
        fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t != label and p == label)
        fn = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p != label)
        total_tp += tp
        total_fp += fp
        total_fn += fn

    _, _, f1 = _precision_recall_f1(total_tp, total_fp, total_fn)
    return f1


def macro_f1(y_true: list[str], y_pred: list[str], labels: list[str] | None = None) -> float:
    """Macro-averaged F1 for single-label classification.

    Computes F1 per class then averages. Used for UNFAIR-ToS task.
    """
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))

    f1_scores = []
    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p == label)
        fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t != label and p == label)
        fn = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p != label)
        _, _, f1 = _precision_recall_f1(tp, fp, fn)
        f1_scores.append(f1)

    return sum(f1_scores) / len(f1_scores) if f1_scores else 0.0


def multilabel_micro_f1(
    y_true_sets: list[set[str]],
    y_pred_sets: list[set[str]],
) -> float:
    """Micro-averaged F1 for multi-label classification.

    Each sample has a set of true labels and a set of predicted labels.
    Aggregates TP/FP/FN across all samples and labels.
    Used for UNFAIR-ToS and ECtHR-A multi-label tasks.
    """
    total_tp = 0
    total_fp = 0
    total_fn = 0

    for true_set, pred_set in zip(y_true_sets, y_pred_sets, strict=True):
        total_tp += len(true_set & pred_set)
        total_fp += len(pred_set - true_set)
        total_fn += len(true_set - pred_set)

    _, _, f1 = _precision_recall_f1(total_tp, total_fp, total_fn)
    return f1


def multilabel_macro_f1(
    y_true_sets: list[set[str]],
    y_pred_sets: list[set[str]],
    labels: list[str] | None = None,
) -> float:
    """Macro-averaged F1 for multi-label classification.

    Computes per-label F1 across all samples, then averages.
    Used for UNFAIR-ToS task.
    """
    if labels is None:
        all_labels: set[str] = set()
        for s in y_true_sets:
            all_labels |= s
        for s in y_pred_sets:
            all_labels |= s
        labels = sorted(all_labels)

    f1_scores = []
    for label in labels:
        tp = sum(
            1
            for ts, ps in zip(y_true_sets, y_pred_sets, strict=True)
            if label in ts and label in ps
        )
        fp = sum(
            1
            for ts, ps in zip(y_true_sets, y_pred_sets, strict=True)
            if label not in ts and label in ps
        )
        fn = sum(
            1
            for ts, ps in zip(y_true_sets, y_pred_sets, strict=True)
            if label in ts and label not in ps
        )
        _, _, f1 = _precision_recall_f1(tp, fp, fn)
        f1_scores.append(f1)

    return sum(f1_scores) / len(f1_scores) if f1_scores else 0.0


def classification_report(
    y_true: list[str],
    y_pred: list[str],
    labels: list[str] | None = None,
) -> list[dict[str, str | float | int]]:
    """Per-class precision, recall, F1, and support.

    Returns a list of dicts sorted by label name.
    """
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))

    true_counts = Counter(y_true)
    report = []

    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p == label)
        fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t != label and p == label)
        fn = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p != label)
        precision, recall, f1 = _precision_recall_f1(tp, fp, fn)
        report.append(
            {
                "label": label,
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1": round(f1, 4),
                "support": true_counts.get(label, 0),
            }
        )

    return report
