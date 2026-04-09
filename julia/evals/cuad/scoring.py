"""Scoring functions for CUAD clause extraction and CaseHOLD precedent ranking.

Implements Harvey BigLaw Bench dual scoring:
  - Answer Score: Did Julia correctly identify clause presence/absence?
  - Source Score: Is the extracted quote accurate against the source?
  - Hallucination Penalty: Penalty for fabricated clauses not in source text.

Also:
  - Token-level F1 for span extraction (CUAD standard metric)
  - Recall@K for vault search evaluation
  - Accuracy for CaseHOLD multiple-choice

Neon persistence: results are stored in julia_cuad_eval_runs, julia_cuad_vault_recall,
and julia_casehold_eval_runs tables for pg_graphql queryability.

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Any

# ── Data Classes ───────────────────────────────────────────────


@dataclass
class CUADGrade:
    """Harvey-style dual scoring for a single clause extraction."""

    answer_score: float = 0.0
    source_score: float = 0.0
    hallucination_penalty: float = 0.0
    final_score: float = 0.0
    f1_score: float = 0.0


@dataclass
class RecallResult:
    """Recall@K result for a single search query."""

    contract_id: str = ""
    clause_type: str = ""
    search_backend: str = "pgvector"
    k: int = 10
    recall_at_k: float = 0.0
    gold_chunk_count: int = 0
    retrieved_chunk_ids: list[str] = field(default_factory=list)
    gold_chunk_ids: list[str] = field(default_factory=list)
    duration_ms: int = 0


@dataclass
class CaseHOLDGrade:
    """Score for a single CaseHOLD prediction."""

    example_id: str = ""
    predicted_idx: int = -1
    gold_idx: int = -1
    correct: bool = False
    confidence: float = 0.0


# ── Token-Level F1 ─────────────────────────────────────────────


def _tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenizer for F1 computation."""
    return re.findall(r"\w+", text.lower())


def compute_f1(predicted_span: str | None, gold_span: str | None) -> float:
    """Compute token-level F1 between predicted and gold text spans.

    This is the standard CUAD metric: token overlap F1.
    Returns 1.0 if both are None/empty (true negative).
    Returns 0.0 if one is present and the other is not.
    """
    if not predicted_span and not gold_span:
        return 1.0
    if not predicted_span or not gold_span:
        return 0.0

    pred_tokens = _tokenize(predicted_span)
    gold_tokens = _tokenize(gold_span)

    if not pred_tokens and not gold_tokens:
        return 1.0
    if not pred_tokens or not gold_tokens:
        return 0.0

    gold_set = set(gold_tokens)
    pred_set = set(pred_tokens)

    tp = len(gold_set & pred_set)
    if tp == 0:
        return 0.0

    precision = tp / len(pred_set)
    recall = tp / len(gold_set)
    return 2 * precision * recall / (precision + recall)


def compute_exact_match(predicted: str | None, gold: str | None) -> bool:
    """Strict exact string match after normalization."""
    if predicted is None and gold is None:
        return True
    if predicted is None or gold is None:
        return False
    return predicted.strip().lower() == gold.strip().lower()


# ── Source Score (Harvey-style) ────────────────────────────────


def compute_source_score(
    extracted_text: str | None,
    contract_text: str,
) -> float:
    """Verify that extracted text appears in the source contract.

    Uses fuzzy substring matching via SequenceMatcher.
    Returns 1.0 if the extracted text is found verbatim (or very close).
    Returns 0.0 if the text is fabricated.

    For Neon pg_trgm integration, use fuzzy_search() from src/neon_db.py
    when running against the database.
    """
    if not extracted_text:
        return 1.0  # No extraction = no source violation

    # Normalize whitespace for comparison
    norm_extracted = " ".join(extracted_text.split()).lower()
    norm_contract = " ".join(contract_text.split()).lower()

    # Exact substring match (best case)
    if norm_extracted in norm_contract:
        return 1.0

    # Fuzzy match: find best matching region in contract
    # Use SequenceMatcher to find the best substring ratio
    matcher = SequenceMatcher(None, norm_extracted, norm_contract)
    blocks = matcher.get_matching_blocks()

    if not blocks:
        return 0.0

    # Sum matched characters
    matched_chars = sum(block.size for block in blocks)
    ratio = matched_chars / max(len(norm_extracted), 1)

    # Threshold: 90% character match = verified source
    return min(ratio / 0.9, 1.0)


# ── Answer Score ───────────────────────────────────────────────


def compute_answer_score(found: bool, gold_found: bool) -> float:
    """Binary: did Julia correctly identify clause presence/absence?

    1.0 if both agree (true positive or true negative).
    0.0 if they disagree (false positive or false negative).
    """
    return 1.0 if found == gold_found else 0.0


# ── Hallucination Penalty ──────────────────────────────────────


def compute_hallucination_penalty(
    extracted_text: str | None,
    contract_text: str,
    gold_found: bool,
) -> float:
    """Penalty for fabricated clauses not traceable to the source text.

    Hallucination = Julia claims to find a clause (found=True) but either:
      1. The gold annotation says it's not there (false positive), or
      2. The extracted text doesn't appear in the contract (fabricated quote).

    Returns 0.0 (no penalty) to 1.0 (full penalty).
    """
    if not extracted_text:
        return 0.0

    # False positive: Julia found something but gold says nothing exists
    if not gold_found:
        return 1.0

    # Fabricated quote: text not in contract
    source = compute_source_score(extracted_text, contract_text)
    if source < 0.5:
        return 1.0 - source

    return 0.0


# ── Complete CUAD Grading ──────────────────────────────────────


def grade_cuad_extraction(
    *,
    found: bool,
    gold_found: bool,
    extracted_text: str | None,
    gold_text: str | None,
    contract_text: str,
) -> CUADGrade:
    """Compute all CUAD scores for a single clause extraction.

    Combines token-level F1, Harvey Answer Score, Source Score,
    and hallucination penalty into a complete grade.
    """
    answer = compute_answer_score(found, gold_found)
    source = compute_source_score(extracted_text, contract_text)
    hallucination = compute_hallucination_penalty(extracted_text, contract_text, gold_found)
    f1 = compute_f1(extracted_text, gold_text)
    final = answer - hallucination

    return CUADGrade(
        answer_score=answer,
        source_score=source,
        hallucination_penalty=hallucination,
        final_score=max(0.0, final),
        f1_score=f1,
    )


# ── Recall@K ──────────────────────────────────────────────────


def compute_recall_at_k(
    retrieved_chunk_ids: list[str],
    gold_chunk_ids: list[str],
    k: int = 10,
) -> float:
    """Compute recall@K: fraction of gold chunks in the top-K retrieved set.

    Returns 1.0 if all gold chunks are in top-K, 0.0 if none are.
    Returns 1.0 if there are no gold chunks (vacuously true).
    """
    if not gold_chunk_ids:
        return 1.0

    top_k = set(retrieved_chunk_ids[:k])
    gold_set = set(gold_chunk_ids)
    found = len(top_k & gold_set)
    return found / len(gold_set)


# ── CaseHOLD Accuracy ─────────────────────────────────────────


def compute_casehold_accuracy(grades: list[CaseHOLDGrade]) -> float:
    """Compute accuracy for CaseHOLD predictions."""
    if not grades:
        return 0.0
    correct = sum(1 for g in grades if g.correct)
    return correct / len(grades)


# ── Aggregation ────────────────────────────────────────────────


def aggregate_cuad_grades(grades: list[CUADGrade]) -> dict[str, float]:
    """Compute mean scores across all CUAD clause extractions."""
    if not grades:
        return {
            "mean_answer_score": 0.0,
            "mean_source_score": 0.0,
            "mean_hallucination_penalty": 0.0,
            "mean_final_score": 0.0,
            "mean_f1": 0.0,
            "count": 0,
        }

    n = len(grades)
    return {
        "mean_answer_score": sum(g.answer_score for g in grades) / n,
        "mean_source_score": sum(g.source_score for g in grades) / n,
        "mean_hallucination_penalty": sum(g.hallucination_penalty for g in grades) / n,
        "mean_final_score": sum(g.final_score for g in grades) / n,
        "mean_f1": sum(g.f1_score for g in grades) / n,
        "count": n,
    }


def aggregate_recall_results(results: list[RecallResult]) -> dict[str, Any]:
    """Aggregate recall@K results by search backend."""
    by_backend: dict[str, list[float]] = {}
    for r in results:
        by_backend.setdefault(r.search_backend, []).append(r.recall_at_k)

    summary: dict[str, Any] = {}
    for backend, recalls in by_backend.items():
        summary[backend] = {
            "mean_recall_at_k": sum(recalls) / len(recalls),
            "count": len(recalls),
        }
    return summary


# ── Neon Persistence ───────────────────────────────────────────


async def persist_cuad_grade(
    conn,
    *,
    contract_id: str,
    contract_title: str,
    clause_type: str,
    julia_category: str,
    found: bool,
    gold_found: bool,
    extracted_text: str | None,
    gold_text: str | None,
    section_reference: str | None,
    confidence: float | None,
    verification: str,
    grade: CUADGrade,
    model: str,
    input_tokens: int | None,
    output_tokens: int | None,
    duration_ms: int | None,
    harness_run_id: int | None = None,
) -> int:
    """Persist a CUAD eval result to julia_cuad_eval_runs in Neon Postgres."""
    row = await (
        await conn.execute(
            """INSERT INTO julia_cuad_eval_runs
               (harness_run_id, contract_id, contract_title, clause_type,
                julia_category, found, gold_found, extracted_text, gold_text,
                section_reference, confidence, verification,
                answer_score, source_score, f1_score, hallucination_penalty,
                final_score, model, input_tokens, output_tokens, duration_ms)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                       %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                harness_run_id, contract_id, contract_title, clause_type,
                julia_category, found, gold_found, extracted_text, gold_text,
                section_reference, confidence, verification,
                grade.answer_score, grade.source_score, grade.f1_score,
                grade.hallucination_penalty, grade.final_score,
                model, input_tokens, output_tokens, duration_ms,
            ),
        )
    ).fetchone()
    return row[0]


async def persist_vault_recall(conn, result: RecallResult, harness_run_id: int | None = None) -> int:
    """Persist a vault recall result to julia_cuad_vault_recall."""
    row = await (
        await conn.execute(
            """INSERT INTO julia_cuad_vault_recall
               (harness_run_id, contract_id, clause_type, search_backend,
                k, recall_at_k, gold_chunk_count,
                retrieved_chunk_ids, gold_chunk_ids, duration_ms)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                harness_run_id, result.contract_id, result.clause_type,
                result.search_backend, result.k, result.recall_at_k,
                result.gold_chunk_count,
                result.retrieved_chunk_ids, result.gold_chunk_ids,
                result.duration_ms,
            ),
        )
    ).fetchone()
    return row[0]


async def persist_casehold_result(
    conn,
    *,
    example_id: str,
    citing_prompt: str,
    holding_options: list[str],
    predicted_idx: int | None,
    gold_idx: int,
    correct: bool,
    confidence: float | None,
    reasoning: str | None,
    model: str,
    input_tokens: int | None,
    output_tokens: int | None,
    duration_ms: int | None,
    harness_run_id: int | None = None,
) -> int:
    """Persist a CaseHOLD eval result to julia_casehold_eval_runs."""
    row = await (
        await conn.execute(
            """INSERT INTO julia_casehold_eval_runs
               (harness_run_id, example_id, citing_prompt, holding_options,
                predicted_idx, gold_idx, correct, confidence, reasoning,
                model, input_tokens, output_tokens, duration_ms)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                harness_run_id, example_id, citing_prompt, holding_options,
                predicted_idx, gold_idx, correct, confidence, reasoning,
                model, input_tokens, output_tokens, duration_ms,
            ),
        )
    ).fetchone()
    return row[0]
