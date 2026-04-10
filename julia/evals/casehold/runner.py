#!/usr/bin/env python3
"""CaseHOLD legal holdings benchmark runner.

Evaluates Julia's ability to identify correct legal holdings from
case law citations. 53K+ holdings, 5-way multiple choice.

Features:
  - Chain-of-thought prompting with citation grounding
  - Jurisdiction filtering (--jurisdiction delaware)
  - Confidence threshold flagging (--confidence-threshold 0.8)
  - Citation grounding audit (--citation-audit)
  - Neon Postgres persistence (Kimball fact table)
  - YAML-driven eval config (config.yaml)

Usage:
  uv run julia/evals/casehold/runner.py                           # Full suite
  uv run julia/evals/casehold/runner.py --examples 1000           # 1000 examples
  uv run julia/evals/casehold/runner.py --jurisdiction delaware   # Delaware only
  uv run julia/evals/casehold/runner.py --citation-audit          # Grounding audit
  uv run julia/evals/casehold/runner.py --confidence-threshold 0.8 # Flag low conf
  uv run julia/evals/casehold/runner.py --dry-run                 # Show task matrix

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from julia.evals.casehold.prompts import (  # noqa: E402
    CASEHOLD_SYSTEM_PROMPT,
    build_casehold_prompt,
    extract_jurisdiction,
)
from julia.evals.casehold.scoring import (  # noqa: E402
    CaseHOLDGrade,
    aggregate_casehold_grades,
    verify_citation_grounding,
)

# ── Config ─────────────────────────────────────────────────────

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def load_config() -> dict[str, Any]:
    """Load eval config from YAML file."""
    import yaml

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f)
    # Defaults if config.yaml is missing
    return {
        "model": {"name": "claude-opus-4-6", "temperature": 0, "max_tokens": 4096},
        "targets": {"accuracy": 0.70, "grounding_rate": 0.80, "abstention_rate_max": 0.05},
        "concurrency": {"workers": 4, "batch_size": 50},
        "baselines": {"bert_base": 0.714, "legal_bert": 0.753, "deberta": 0.760},
        "data": {
            "primary": "julia/evals/test_data/lexglue/casehold_samples.json",
            "downloaded": "julia/evals/casehold/data/casehold.jsonl",
        },
    }


CONFIG = load_config()
MODEL = CONFIG.get("model", {}).get("name", "claude-opus-4-6")
MAX_WORKERS = CONFIG.get("concurrency", {}).get("workers", 4)
TARGET_ACCURACY = CONFIG.get("targets", {}).get("accuracy", 0.70)

# ── Data Structures ────────────────────────────────────────────


@dataclass
class CaseHOLDTask:
    example_id: str
    citing_prompt: str
    holdings: list[str]
    gold_idx: int
    jurisdiction: str | None = None


@dataclass
class CaseHOLDResult:
    task: CaseHOLDTask
    predicted_idx: int = -1
    correct: bool = False
    confidence: float = 0.0
    reasoning: str = ""
    supporting_quote: str = ""
    grounding_verified: bool = False
    input_tokens: int = 0
    output_tokens: int = 0
    duration_ms: int = 0
    error: str | None = None


# ── API Caller ─────────────────────────────────────────────────


def call_claude(system_prompt: str, user_prompt: str, model: str = MODEL) -> dict:
    """Call Claude API and return response metadata."""
    import anthropic

    client = anthropic.Anthropic()
    t0 = time.monotonic()

    response = client.messages.create(
        model=model,
        max_tokens=CONFIG.get("model", {}).get("max_tokens", 4096),
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


def parse_json_response(text: str) -> dict | None:
    """Parse JSON from Claude response, handling markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.startswith("```")]
        text = "\n".join(lines).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON object from surrounding text
    import re

    match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return None


# ── Task Execution ─────────────────────────────────────────────


def run_casehold_task(task: CaseHOLDTask) -> CaseHOLDResult:
    """Execute a single CaseHOLD prediction task."""
    result = CaseHOLDResult(task=task)

    try:
        user_prompt = build_casehold_prompt(task.citing_prompt, task.holdings)
        response = call_claude(CASEHOLD_SYSTEM_PROMPT, user_prompt)

        result.input_tokens = response["input_tokens"]
        result.output_tokens = response["output_tokens"]
        result.duration_ms = response["duration_ms"]

        parsed = parse_json_response(response["text"])
        if not parsed or not isinstance(parsed, dict):
            result.error = "Failed to parse JSON response"
            return result

        result.predicted_idx = parsed.get("predicted_idx", -1)
        result.confidence = parsed.get("confidence", 0.0)
        result.reasoning = parsed.get("reasoning", "")
        result.supporting_quote = parsed.get("supporting_quote", "")

        # Check correctness (abstentions are always incorrect)
        if result.predicted_idx == -1:
            result.correct = False
        else:
            result.correct = result.predicted_idx == task.gold_idx

        # Verify citation grounding
        if result.supporting_quote:
            result.grounding_verified = verify_citation_grounding(
                result.supporting_quote, task.citing_prompt
            )

    except Exception as e:
        result.error = str(e)

    return result


# ── Data Loading ───────────────────────────────────────────────


def load_casehold_tasks(
    max_examples: int | None = None,
    jurisdiction_filter: str | None = None,
) -> list[CaseHOLDTask]:
    """Load CaseHOLD tasks from local data files.

    Tries pre-ingested LexGLUE samples first, falls back to downloaded JSONL.
    Extracts jurisdiction from citing_prompt and optionally filters.
    """
    # Try pre-ingested samples first
    primary_path = PROJECT_ROOT / CONFIG.get("data", {}).get(
        "primary", "julia/evals/test_data/lexglue/casehold_samples.json"
    )
    downloaded_path = PROJECT_ROOT / CONFIG.get("data", {}).get(
        "downloaded", "julia/evals/casehold/data/casehold.jsonl"
    )

    tasks: list[CaseHOLDTask] = []

    if primary_path.exists():
        tasks = _load_from_json(primary_path)
    elif downloaded_path.exists():
        tasks = _load_from_jsonl(downloaded_path)
    else:
        print(f"ERROR: No CaseHOLD data found at {primary_path} or {downloaded_path}")
        print("Run: uv run julia/evals/casehold/download_casehold.py")
        sys.exit(1)

    # Extract jurisdiction
    for task in tasks:
        task.jurisdiction = extract_jurisdiction(task.citing_prompt)

    # Filter by jurisdiction if specified
    if jurisdiction_filter:
        norm_filter = jurisdiction_filter.lower().replace("-", "_").replace(" ", "_")
        tasks = [t for t in tasks if t.jurisdiction and norm_filter in t.jurisdiction]

    # Limit examples
    if max_examples and max_examples > 0:
        tasks = tasks[:max_examples]

    return tasks


def _load_from_json(path: Path) -> list[CaseHOLDTask]:
    """Load from pre-ingested LexGLUE JSON format."""
    data = json.loads(path.read_text())
    tasks = []
    for sample in data:
        holdings = sample.get("holdings", [])
        if not holdings or len(holdings) < 5:
            continue

        label = sample.get("label")
        if label is None:
            continue

        tasks.append(
            CaseHOLDTask(
                example_id=str(sample.get("hf_index", len(tasks))),
                citing_prompt=sample["text"],
                holdings=holdings,
                gold_idx=int(label),
            )
        )
    return tasks


def _load_from_jsonl(path: Path) -> list[CaseHOLDTask]:
    """Load from downloaded HuggingFace JSONL format."""
    tasks = []
    with open(path) as f:
        for line in f:
            ex = json.loads(line)
            try:
                tasks.append(
                    CaseHOLDTask(
                        example_id=ex["id"],
                        citing_prompt=ex["citing_prompt"],
                        holdings=[ex[f"holding_{i}"] for i in range(5)],
                        gold_idx=ex["label"],
                    )
                )
            except KeyError:
                continue  # skip malformed rows
    return tasks


# ── Result Persistence ─────────────────────────────────────────


async def persist_results(
    results: list[CaseHOLDResult],
    run_id: str,
) -> None:
    """Persist eval results to Neon Postgres."""
    from julia.evals.casehold.scoring import persist_casehold_result
    from src.neon_db import connection_pool

    async with connection_pool() as conn:
        for r in results:
            if r.error:
                continue
            await persist_casehold_result(
                conn,
                run_id=run_id,
                example_id=r.task.example_id,
                citing_prompt=r.task.citing_prompt,
                holding_options=r.task.holdings,
                predicted_idx=r.predicted_idx,
                gold_idx=r.task.gold_idx,
                correct=r.correct,
                confidence=r.confidence,
                supporting_quote=r.supporting_quote or None,
                grounding_verified=r.grounding_verified,
                jurisdiction=r.task.jurisdiction,
                reasoning=r.reasoning or None,
                model=MODEL,
                input_tokens=r.input_tokens,
                output_tokens=r.output_tokens,
                duration_ms=r.duration_ms,
            )
        await conn.commit()
        print(f"Results persisted to Neon (run_id={run_id})")


# ── Summary Report ─────────────────────────────────────────────


def print_casehold_summary(
    results: list[CaseHOLDResult],
    confidence_threshold: float | None = None,
    citation_audit: bool = False,
) -> None:
    """Print CaseHOLD evaluation summary with confidence analysis."""
    grades = [
        CaseHOLDGrade(
            example_id=r.task.example_id,
            predicted_idx=r.predicted_idx,
            gold_idx=r.task.gold_idx,
            correct=r.correct,
            confidence=r.confidence,
            supporting_quote=r.supporting_quote,
            grounding_verified=r.grounding_verified,
        )
        for r in results
        if not r.error
    ]

    agg = aggregate_casehold_grades(grades)
    errors = sum(1 for r in results if r.error)

    print("\n" + "=" * 70)
    print("CASEHOLD BENCHMARK RESULTS")
    print("=" * 70)
    print(f"  Total examples:         {len(results)}")
    print(f"  Errors:                 {errors}")
    print(f"  Attempted:              {agg['attempted']}")
    print(f"  Abstentions:            {agg['abstentions']} ({agg['abstention_rate']:.1%})")
    print(f"  Accuracy:               {agg['accuracy']:.4f}")
    print(f"  Correct:                {agg['correct']} / {agg['attempted']}")
    print(f"  Target:                 >= {TARGET_ACCURACY:.0%}")
    print(f"  PASSED:                 {'YES' if agg['accuracy'] >= TARGET_ACCURACY else 'NO'}")

    # Confidence bucket breakdown
    conf = agg["confidence_analysis"]
    print("\n  Confidence Breakdown:")
    print(f"  {'Bucket':<12} {'Accuracy':>10} {'Correct':>10} {'Total':>8}")
    print("  " + "-" * 44)
    for bucket in ("high", "medium", "low"):
        b = conf[bucket]
        if b["total"] > 0:
            print(f"  {bucket:<12} {b['accuracy']:>10.4f} {b['correct']:>10} {b['total']:>8}")

    # Confidence threshold flagging
    if confidence_threshold and confidence_threshold > 0:
        low_conf = [r for r in results if not r.error and r.confidence < confidence_threshold]
        print(f"\n  Low confidence (< {confidence_threshold}):")
        print(f"    Count:     {len(low_conf)}")
        if low_conf:
            low_correct = sum(1 for r in low_conf if r.correct)
            print(f"    Accuracy:  {low_correct / len(low_conf):.4f}")

    # Citation grounding audit
    if citation_audit:
        print("\n  Citation Grounding:")
        print(f"    Grounding rate:       {agg['grounding_rate']:.4f}")
        grounded = sum(1 for g in grades if g.grounding_verified and g.predicted_idx != -1)
        attempted = agg["attempted"]
        print(f"    Verified quotes:      {grounded} / {attempted}")

    # Per-jurisdiction breakdown
    by_jurisdiction: dict[str, list[CaseHOLDGrade]] = {}
    for r in results:
        if not r.error and r.task.jurisdiction:
            by_jurisdiction.setdefault(r.task.jurisdiction, []).append(
                CaseHOLDGrade(
                    correct=r.correct,
                    predicted_idx=r.predicted_idx,
                    gold_idx=r.task.gold_idx,
                    confidence=r.confidence,
                )
            )

    if by_jurisdiction:
        print("\n  Per-Jurisdiction Accuracy (top 10):")
        print(f"  {'Jurisdiction':<25} {'Accuracy':>10} {'N':>6}")
        print("  " + "-" * 43)
        # Sort by count descending, show top 10
        sorted_jurisdictions = sorted(
            by_jurisdiction.items(), key=lambda x: len(x[1]), reverse=True
        )[:10]
        for jur, jur_grades in sorted_jurisdictions:
            attempted_jur = [g for g in jur_grades if g.predicted_idx != -1]
            if attempted_jur:
                jur_acc = sum(1 for g in attempted_jur if g.correct) / len(attempted_jur)
                print(f"  {jur:<25} {jur_acc:>10.4f} {len(attempted_jur):>6}")

    # Baselines comparison
    baselines = CONFIG.get("baselines", {})
    if baselines:
        print("\n  Baselines:")
        for name, score in sorted(baselines.items()):
            marker = " <-- Julia" if name == "julia" else ""
            print(f"    {name:<15} {score:.1%}{marker}")
        print(f"    {'julia':<15} {agg['accuracy']:.1%} <-- this run")

    print()


# ── Main ───────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="CaseHOLD legal holdings benchmark runner")
    parser.add_argument(
        "--examples",
        type=int,
        default=None,
        help="Limit number of examples (default: all)",
    )
    parser.add_argument(
        "--jurisdiction",
        type=str,
        default=None,
        help="Filter by jurisdiction (e.g., delaware, 9th_cir)",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=None,
        help="Flag answers below this confidence threshold",
    )
    parser.add_argument(
        "--citation-audit",
        action="store_true",
        help="Verify citation grounding (supporting_quote in context)",
    )
    parser.add_argument(
        "--persist",
        action="store_true",
        help="Persist results to Neon Postgres",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show task matrix without running eval",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_WORKERS,
        help="Max concurrent API workers",
    )
    args = parser.parse_args()

    run_id = f"casehold_{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    # Load tasks
    tasks = load_casehold_tasks(
        max_examples=args.examples,
        jurisdiction_filter=args.jurisdiction,
    )

    if not tasks:
        print("ERROR: No CaseHOLD tasks loaded.")
        sys.exit(1)

    # Dry run
    if args.dry_run:
        print(f"CaseHOLD: {len(tasks)} examples")
        jurisdictions: dict[str, int] = {}
        for t in tasks:
            jur = t.jurisdiction or "unknown"
            jurisdictions[jur] = jurisdictions.get(jur, 0) + 1
        print("\nJurisdiction distribution:")
        for jur, count in sorted(jurisdictions.items(), key=lambda x: -x[1])[:20]:
            print(f"  {jur:<25} {count:>6}")
        return

    # Run eval
    print(f"Running CaseHOLD evaluation ({len(tasks)} tasks, {args.workers} workers)...")
    results: list[CaseHOLDResult] = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_casehold_task, t): t for t in tasks}
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            results.append(result)
            if (i + 1) % 100 == 0:
                print(f"  CaseHOLD: {i + 1}/{len(tasks)} completed")

    # Summary
    print_casehold_summary(
        results,
        confidence_threshold=args.confidence_threshold,
        citation_audit=args.citation_audit,
    )

    # Save results locally
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    results_path = results_dir / f"casehold_{ts}.jsonl"
    with open(results_path, "w") as f:
        for r in results:
            row = {
                "example_id": r.task.example_id,
                "predicted_idx": r.predicted_idx,
                "gold_idx": r.task.gold_idx,
                "correct": r.correct,
                "confidence": r.confidence,
                "supporting_quote": r.supporting_quote,
                "grounding_verified": r.grounding_verified,
                "jurisdiction": r.task.jurisdiction,
                "error": r.error,
            }
            f.write(json.dumps(row) + "\n")
    print(f"Results saved to {results_path}")

    # Persist to Neon
    if args.persist:
        asyncio.run(persist_results(results, run_id))


if __name__ == "__main__":
    main()
