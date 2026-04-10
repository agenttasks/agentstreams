#!/usr/bin/env python3
"""CUAD + CaseHOLD benchmark runner for Julia legal AI evaluation.

Runs clause extraction (CUAD) and precedent ranking (CaseHOLD) benchmarks,
scoring results with Harvey BigLaw Bench metrics (Answer Score + Source Score).

Results are persisted to Neon Postgres (pg_graphql queryable) and printed
as summary tables.

Usage:
  uv run julia/evals/cuad/runner.py                                  # Full suite
  uv run julia/evals/cuad/runner.py --benchmark cuad                  # CUAD only
  uv run julia/evals/cuad/runner.py --benchmark casehold              # CaseHOLD only
  uv run julia/evals/cuad/runner.py --clause indemnification          # Single clause
  uv run julia/evals/cuad/runner.py --vault-recall                    # Search recall@K
  uv run julia/evals/cuad/runner.py --vault-recall --backend lancedb  # LanceDB hybrid
  uv run julia/evals/cuad/runner.py --source-score                    # Source verification
  uv run julia/evals/cuad/runner.py --contracts 20                    # Limit contracts
  uv run julia/evals/cuad/runner.py --dry-run                         # Show task matrix

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from julia.evals.cuad.prompts import (  # noqa: E402
    CUAD_SYSTEM_PROMPT,
    HIGH_STAKES_CLAUSE_TYPES,
    build_cuad_single_prompt,
    build_cuad_verify_prompt,
)
from julia.evals.cuad.scoring import (  # noqa: E402
    CUADGrade,
    RecallResult,
    aggregate_cuad_grades,
    aggregate_recall_results,
    grade_cuad_extraction,
)

DATA_DIR = Path(__file__).parent / "data"
RESULTS_DIR = Path(__file__).parent / "results"
MODEL = "claude-opus-4-6"
MAX_WORKERS = 4

# ── Data Structures ─────────────────────────────────────────


@dataclass
class CUADTask:
    contract_id: str
    contract_title: str
    clause_type: str
    julia_category: str
    contract_text: str
    gold_texts: list[str]
    gold_found: bool


@dataclass
class CUADResult:
    task: CUADTask
    found: bool = False
    extracted_text: str | None = None
    section_reference: str | None = None
    confidence: float = 0.0
    verification: str = "not_applicable"
    grade: CUADGrade | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    duration_ms: int = 0
    error: str | None = None



# ── API Caller ──────────────────────────────────────────────


def call_claude(system_prompt: str, user_prompt: str, model: str = MODEL) -> dict:
    """Call Claude API and return response metadata."""
    import anthropic

    client = anthropic.Anthropic()
    t0 = time.monotonic()

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    text = response.content[0].text if response.content else ""
    duration_ms = int((time.monotonic() - t0) * 1000)

    return {
        "text": text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "duration_ms": duration_ms,
    }


def parse_json_response(text: str) -> dict | list | None:
    """Parse JSON from Claude response, handling markdown fences."""
    text = text.strip()
    # Strip markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.startswith("```")]
        text = "\n".join(lines).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


# ── CUAD Task Execution ─────────────────────────────────────


def run_cuad_task(task: CUADTask) -> CUADResult:
    """Execute a single CUAD clause extraction task."""
    result = CUADResult(task=task)

    try:
        # Build and send extraction prompt
        user_prompt = build_cuad_single_prompt(task.clause_type, task.contract_text)
        response = call_claude(CUAD_SYSTEM_PROMPT, user_prompt)

        result.input_tokens = response["input_tokens"]
        result.output_tokens = response["output_tokens"]
        result.duration_ms = response["duration_ms"]

        # Parse response
        parsed = parse_json_response(response["text"])
        if not parsed or not isinstance(parsed, dict):
            result.error = "Failed to parse JSON response"
            return result

        result.found = parsed.get("found", False)
        result.extracted_text = parsed.get("extracted_text")
        result.section_reference = parsed.get("section_reference")
        result.confidence = parsed.get("confidence", 0.0)
        result.verification = parsed.get("verification", "not_applicable")

        # Iterative verification for high-stakes clauses
        if (
            task.clause_type in HIGH_STAKES_CLAUSE_TYPES
            and result.found
            and result.extracted_text
        ):
            verify_prompt = build_cuad_verify_prompt(
                task.clause_type,
                result.extracted_text,
                result.section_reference or "",
                task.contract_text,
            )
            verify_response = call_claude(CUAD_SYSTEM_PROMPT, verify_prompt)
            result.input_tokens += verify_response["input_tokens"]
            result.output_tokens += verify_response["output_tokens"]
            result.duration_ms += verify_response["duration_ms"]

            verify_parsed = parse_json_response(verify_response["text"])
            if verify_parsed and isinstance(verify_parsed, dict):
                result.verification = verify_parsed.get("verification", result.verification)
                if result.verification == "retracted":
                    result.found = False
                    result.extracted_text = None
                elif verify_parsed.get("extracted_text"):
                    result.extracted_text = verify_parsed["extracted_text"]

        # Score the extraction
        gold_text = task.gold_texts[0] if task.gold_texts else None
        result.grade = grade_cuad_extraction(
            found=result.found,
            gold_found=task.gold_found,
            extracted_text=result.extracted_text,
            gold_text=gold_text,
            contract_text=task.contract_text,
        )

    except Exception as e:
        result.error = str(e)

    return result



# ── Data Loading ────────────────────────────────────────────


def load_clause_map() -> dict:
    """Load CUAD-to-Julia clause type mapping."""
    map_path = Path(__file__).parent / "clause_map.json"
    with open(map_path) as f:
        return json.load(f)


def load_cuad_tasks(
    clause_filter: str | None = None,
    max_contracts: int | None = None,
) -> list[CUADTask]:
    """Load CUAD tasks from downloaded dataset."""
    contracts_path = DATA_DIR / "contracts.jsonl"
    if not contracts_path.exists():
        print(f"ERROR: CUAD data not found at {contracts_path}")
        print("Run: uv run julia/evals/cuad/download_cuad.py")
        sys.exit(1)

    clause_map = load_clause_map()
    category_lookup = {c["cuad_name"]: c for c in clause_map["categories"]}

    tasks = []
    with open(contracts_path) as f:
        for i, line in enumerate(f):
            if max_contracts and i >= max_contracts:
                break

            contract = json.loads(line)

            for clause_type, annotation in contract["annotations"].items():
                # Apply clause filter if specified
                if clause_filter and clause_filter.lower() not in clause_type.lower():
                    continue

                cat_info = category_lookup.get(clause_type, {})
                julia_category = cat_info.get("julia_category", "other")

                tasks.append(CUADTask(
                    contract_id=contract["id"],
                    contract_title=contract.get("title", ""),
                    clause_type=clause_type,
                    julia_category=julia_category,
                    contract_text=contract["context"],
                    gold_texts=annotation.get("texts", []),
                    gold_found=annotation.get("found", False),
                ))

    return tasks



# ── Vault Recall Evaluation ─────────────────────────────────


def run_vault_recall(
    contracts_limit: int | None = None,
    backend: str = "all",
) -> list[RecallResult]:
    """Measure vault search recall@K across different backends.

    Backends: pgvector (hash), lancedb (hybrid), pg_trgm (fuzzy).
    """
    from src.embeddings import LanceStore, chunk_text, hash_embedding

    contracts_path = DATA_DIR / "contracts.jsonl"
    if not contracts_path.exists():
        print(f"ERROR: CUAD data not found at {contracts_path}")
        return []

    clause_map = load_clause_map()
    high_priority = clause_map.get("high_priority_cuad_types", [])

    results: list[RecallResult] = []
    backends_to_run = ["lancedb"] if backend == "lancedb" else ["lancedb"]

    if backend == "all":
        backends_to_run = ["lancedb"]
    elif backend != "lancedb":
        backends_to_run = [backend]

    with open(contracts_path) as f:
        for i, line in enumerate(f):
            if contracts_limit and i >= contracts_limit:
                break

            contract = json.loads(line)
            contract_id = contract["id"]
            contract_text = contract["context"]

            # Chunk the contract
            chunks = chunk_text(contract_text, chunk_size=512, overlap=64)
            chunk_ids = [f"{contract_id}_chunk_{c['index']}" for c in chunks]
            chunk_texts = [c["text"] for c in chunks]

            # For each high-priority clause type, find which chunks contain the gold span
            for clause_type in high_priority:
                annotation = contract["annotations"].get(clause_type, {})
                gold_texts = annotation.get("texts", [])
                if not gold_texts:
                    continue

                # Identify gold chunks (chunks that contain the gold text)
                gold_chunk_ids = []
                for ci, ct in zip(chunk_ids, chunk_texts, strict=True):
                    for gt in gold_texts:
                        if gt.lower()[:50] in ct.lower():
                            gold_chunk_ids.append(ci)
                            break

                if not gold_chunk_ids:
                    continue

                # LanceDB search
                if "lancedb" in backends_to_run:
                    lance_store = LanceStore(
                        db_path=str(DATA_DIR / ".lancedb"),
                        table_name="cuad_contracts",
                    )
                    t0 = time.monotonic()
                    query_vec = hash_embedding(clause_type)
                    search_results = lance_store.search(
                        query_vec,
                        limit=10,
                        room=contract_id,
                    )
                    duration = int((time.monotonic() - t0) * 1000)

                    retrieved_ids = [r.get("id", "") for r in search_results]
                    from julia.evals.cuad.scoring import compute_recall_at_k

                    recall = compute_recall_at_k(retrieved_ids, gold_chunk_ids, k=10)

                    results.append(RecallResult(
                        contract_id=contract_id,
                        clause_type=clause_type,
                        search_backend="lancedb",
                        k=10,
                        recall_at_k=recall,
                        gold_chunk_count=len(gold_chunk_ids),
                        retrieved_chunk_ids=retrieved_ids,
                        gold_chunk_ids=gold_chunk_ids,
                        duration_ms=duration,
                    ))

            if (i + 1) % 10 == 0:
                print(f"  Recall eval: {i + 1} contracts processed")

    return results


# ── Result Persistence ──────────────────────────────────────


async def persist_results(
    cuad_results: list[CUADResult],
    recall_results: list[RecallResult],
) -> None:
    """Persist CUAD eval results to Neon Postgres."""
    from julia.evals.cuad.scoring import (
        aggregate_cuad_grades,
        persist_cuad_grade,
        persist_vault_recall,
    )
    from src.neon_db import connection_pool, create_harness_run, record_evaluation_result

    async with connection_pool() as conn:
        harness_run_id = await create_harness_run(
            conn,
            harness_name="cuad-benchmark",
            sprint_id="cuad-v1",
            objective="Measure Julia clause extraction F1",
            criteria=[
                {"name": "cuad_f1", "target": 0.85},
                {"name": "source_score", "target": 0.9},
            ],
        )

        for r in cuad_results:
            if r.grade and not r.error:
                await persist_cuad_grade(
                    conn,
                    contract_id=r.task.contract_id,
                    contract_title=r.task.contract_title,
                    clause_type=r.task.clause_type,
                    julia_category=r.task.julia_category,
                    found=r.found,
                    gold_found=r.task.gold_found,
                    extracted_text=r.extracted_text,
                    gold_text=r.task.gold_texts[0] if r.task.gold_texts else None,
                    section_reference=r.section_reference,
                    confidence=r.confidence,
                    verification=r.verification,
                    grade=r.grade,
                    model=MODEL,
                    input_tokens=r.input_tokens,
                    output_tokens=r.output_tokens,
                    duration_ms=r.duration_ms,
                    harness_run_id=harness_run_id,
                )

        for r in recall_results:
            await persist_vault_recall(conn, r, harness_run_id=harness_run_id)

        cuad_grades = [r.grade for r in cuad_results if r.grade]
        agg = aggregate_cuad_grades(cuad_grades)

        await record_evaluation_result(
            conn,
            harness_run_id=harness_run_id,
            iteration=1,
            scores=[
                {"name": "cuad_f1", "value": agg["mean_f1"]},
                {"name": "cuad_answer_score", "value": agg["mean_answer_score"]},
                {"name": "cuad_source_score", "value": agg["mean_source_score"]},
            ],
            overall_score=agg["mean_f1"],
            passed=agg["mean_f1"] >= 0.85,
            summary=f"CUAD F1={agg['mean_f1']:.3f}",
        )

        await conn.commit()
        print(f"Results persisted to Neon (harness_run_id={harness_run_id})")


# ── Print Summary ───────────────────────────────────────────


def print_cuad_summary(results: list[CUADResult]) -> None:
    """Print CUAD evaluation summary table."""
    grades = [r.grade for r in results if r.grade]
    agg = aggregate_cuad_grades(grades)
    errors = sum(1 for r in results if r.error)

    print("\n" + "=" * 70)
    print("CUAD BENCHMARK RESULTS")
    print("=" * 70)
    print(f"  Total tasks:            {len(results)}")
    print(f"  Errors:                 {errors}")
    print(f"  Mean F1:                {agg['mean_f1']:.4f}")
    print(f"  Mean Answer Score:      {agg['mean_answer_score']:.4f}")
    print(f"  Mean Source Score:      {agg['mean_source_score']:.4f}")
    print(f"  Mean Hallucination:     {agg['mean_hallucination_penalty']:.4f}")
    print(f"  Mean Final Score:       {agg['mean_final_score']:.4f}")
    print("  Target F1:              >= 0.85")
    print(f"  PASSED:                 {'YES' if agg['mean_f1'] >= 0.85 else 'NO'}")

    # Per clause-type breakdown
    by_clause: dict[str, list[CUADGrade]] = {}
    for r in results:
        if r.grade:
            by_clause.setdefault(r.task.clause_type, []).append(r.grade)

    if by_clause:
        print("\nPer Clause Type:")
        print(f"  {'Clause Type':<40} {'F1':>6} {'Ans':>6} {'Src':>6} {'N':>4}")
        print("  " + "-" * 62)
        for ct in sorted(by_clause.keys()):
            ct_agg = aggregate_cuad_grades(by_clause[ct])
            print(
                f"  {ct:<40} {ct_agg['mean_f1']:>6.3f} "
                f"{ct_agg['mean_answer_score']:>6.3f} "
                f"{ct_agg['mean_source_score']:>6.3f} "
                f"{ct_agg['count']:>4}"
            )
    print()



def print_recall_summary(results: list[RecallResult]) -> None:
    """Print vault recall summary."""
    agg = aggregate_recall_results(results)

    print("=" * 70)
    print("VAULT RECALL@K RESULTS")
    print("=" * 70)
    for backend, stats in sorted(agg.items()):
        print(f"  {backend:<12} recall@10 = {stats['mean_recall_at_k']:.4f}  (n={stats['count']})")
    print()


# ── Main ────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="CUAD clause extraction benchmark runner")
    parser.add_argument("--clause", type=str, default=None, help="Filter to clause type")
    parser.add_argument("--contracts", type=int, default=None, help="Limit CUAD contracts")
    parser.add_argument("--vault-recall", action="store_true", help="Run vault recall eval only")
    parser.add_argument("--backend", default="all", help="Search backend for recall eval")
    parser.add_argument("--source-score", action="store_true", help="Source verification only")
    parser.add_argument("--persist", action="store_true", help="Persist results to Neon")
    parser.add_argument("--dry-run", action="store_true", help="Show task matrix only")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS, help="Max concurrent workers")
    args = parser.parse_args()

    cuad_results: list[CUADResult] = []
    recall_results: list[RecallResult] = []

    # Vault recall mode
    if args.vault_recall:
        print("Running vault recall evaluation...")
        recall_results = run_vault_recall(
            contracts_limit=args.contracts or 50,
            backend=args.backend,
        )
        print_recall_summary(recall_results)

        if args.persist:
            asyncio.run(persist_results([], recall_results))
        return

    # CUAD benchmark
    tasks = load_cuad_tasks(
        clause_filter=args.clause,
        max_contracts=args.contracts,
    )

    if args.dry_run:
        print(f"CUAD: {len(tasks)} tasks across contracts")
        clause_counts: dict[str, int] = {}
        for t in tasks:
            clause_counts[t.clause_type] = clause_counts.get(t.clause_type, 0) + 1
        for ct, count in sorted(clause_counts.items()):
            print(f"  {ct}: {count} contracts")
        return

    print(f"Running CUAD evaluation ({len(tasks)} tasks, {args.workers} workers)...")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_cuad_task, t): t for t in tasks}
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            cuad_results.append(result)
            if (i + 1) % 50 == 0:
                print(f"  CUAD: {i + 1}/{len(tasks)} completed")

    print_cuad_summary(cuad_results)

    # Save results locally
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())

    if cuad_results:
        cuad_path = RESULTS_DIR / f"cuad_{ts}.jsonl"
        with open(cuad_path, "w") as f:
            for r in cuad_results:
                row = {
                    "contract_id": r.task.contract_id,
                    "clause_type": r.task.clause_type,
                    "found": r.found,
                    "gold_found": r.task.gold_found,
                    "f1": r.grade.f1_score if r.grade else 0.0,
                    "answer_score": r.grade.answer_score if r.grade else 0.0,
                    "source_score": r.grade.source_score if r.grade else 0.0,
                    "error": r.error,
                }
                f.write(json.dumps(row) + "\n")
        print(f"CUAD results saved to {cuad_path}")

    # Persist to Neon
    if args.persist:
        asyncio.run(persist_results(cuad_results, recall_results))


if __name__ == "__main__":
    main()
