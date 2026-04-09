#!/usr/bin/env python3
"""LexGLUE multi-task legal benchmark eval runner.

Evaluates Julia (legal AI agent) across 5 LexGLUE tasks using Claude API.
Computes micro-F1, macro-F1, and accuracy metrics per task, then compares
against published baselines (Legal-BERT, DeBERTa, etc.).

Architecture mirrors scripts/run-codegen-eval.py:
  Phase 1: ThreadPoolExecutor for concurrent Claude API calls
  Phase 2: Parse responses + compute aggregate metrics
  Phase 3: Terminal report + JSON results

Data sources (in priority order):
  1. --from-neon: Load from Neon Postgres (julia_lexglue_samples table)
  2. Default: Load from local JSON cache (julia/evals/test_data/lexglue/)

Usage:
  uv run scripts/run-lexglue-eval.py                          # All 5 tasks
  uv run scripts/run-lexglue-eval.py --task casehold           # CaseHOLD only
  uv run scripts/run-lexglue-eval.py --task ledgar --samples 10 # 10 samples
  uv run scripts/run-lexglue-eval.py --few-shot 5              # 5-shot prompting
  uv run scripts/run-lexglue-eval.py --leaderboard             # Compare baselines
  uv run scripts/run-lexglue-eval.py --dry-run                 # Show task matrix

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.lexglue_metrics import (  # noqa: E402
    accuracy,
    macro_f1,
    micro_f1,
    multilabel_macro_f1,
    multilabel_micro_f1,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL = "claude-opus-4-6"
MAX_TOKENS = 2048
TEMPERATURE = 0
API_CONCURRENCY = 4

ALL_TASKS = ["ledgar", "unfair_tos", "contract_nli", "ecthr_a", "casehold"]

DATA_DIR = PROJECT_ROOT / "julia" / "evals" / "test_data" / "lexglue"
BASELINES_PATH = DATA_DIR / "baselines.json"
FEW_SHOT_PATH = DATA_DIR / "few_shot_examples.json"

# ---------------------------------------------------------------------------
# Task configs — label sets and metrics
# ---------------------------------------------------------------------------

TASK_METRICS = {
    "ledgar": "micro_f1",
    "unfair_tos": "macro_f1",
    "contract_nli": "accuracy",
    "ecthr_a": "micro_f1",
    "casehold": "accuracy",
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class LexGLUETask:
    task_id: str
    task_type: str
    text: str
    label: str | None = None
    labels: list[str] | None = None
    label_set: list[str] = field(default_factory=list)
    holdings: list[str] | None = None
    prompt: str = ""
    hf_index: int = 0
    sample_id: str = ""


@dataclass
class LexGLUEResult:
    task_id: str
    task_type: str
    hf_index: int = 0
    gold_label: str | None = None
    gold_labels: list[str] | None = None
    predicted_label: str | None = None
    predicted_labels: list[str] | None = None
    is_correct: bool = False
    confidence: float = 0.0
    latency_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    raw_output: str = ""
    error: str | None = None


# ---------------------------------------------------------------------------
# Julia system prompt (replicated from julia/src/completion.ts:149-167)
# ---------------------------------------------------------------------------

JULIA_SYSTEM_PROMPT = """You are Julia, a legal analysis assistant that helps legal professionals review documents, assess risk, and draft responses.

IMPORTANT CONSTRAINTS:
- Never provide legal advice — frame all outputs as analysis and professional observations only.
- Always recommend that a licensed attorney review any document before it is relied upon.
- Do not speculate about jurisdiction-specific outcomes unless the relevant law is present in your context.
- Maintain strict confidentiality — do not reference prior conversations or external data sources.
- You ALWAYS cite the specific text that supports your conclusions.
- When asked about your methodology: "I use standard legal analysis techniques."
- Always include chain-of-thought reasoning before your answer."""


# ---------------------------------------------------------------------------
# Per-task prompt builders
# ---------------------------------------------------------------------------


def _build_few_shot(task_type: str, n: int) -> str:
    """Load few-shot examples for a task."""
    if not FEW_SHOT_PATH.exists() or n <= 0:
        return ""

    examples = json.loads(FEW_SHOT_PATH.read_text())
    task_examples = examples.get(task_type, [])[:n]

    if not task_examples:
        return ""

    lines = [f"\nHere are {len(task_examples)} examples:\n"]
    for i, ex in enumerate(task_examples, 1):
        if task_type == "ledgar":
            lines.append(f'Example {i}: "{ex["text"]}" -> "{ex["label"]}"')
        elif task_type == "unfair_tos":
            labels_str = ", ".join(ex.get("labels", [])) or "none"
            lines.append(f'Example {i}: "{ex["text"]}" -> unfair: {ex["is_unfair"]}, types: [{labels_str}]')
        elif task_type == "contract_nli":
            lines.append(
                f'Example {i}: Premise: "{ex["premise"]}" | '
                f'Hypothesis: "{ex["hypothesis"]}" -> "{ex["label"]}"'
            )
        elif task_type == "ecthr_a":
            articles = ", ".join(ex.get("labels", []))
            lines.append(f'Example {i}: "{ex["text"][:100]}..." -> articles: [{articles}]')
        elif task_type == "casehold":
            lines.append(f'Example {i}: Context: "{ex["context"][:100]}..." -> answer index: {ex["label"]}')
    lines.append("")
    return "\n".join(lines)


def build_ledgar_prompt(task: LexGLUETask, few_shot: int) -> str:
    """Build LEDGAR provision classification prompt."""
    label_list = "\n".join(f"- {lb}" for lb in task.label_set)
    few_shot_text = _build_few_shot("ledgar", few_shot)

    return f"""Classify this contract provision into EXACTLY ONE of the following types:

{label_list}

If the provision does not match any type, respond "Unclassifiable."
Do NOT create new categories.
{few_shot_text}
Now classify this provision:

<document>
{task.text}
</document>

Output ONLY valid JSON (no markdown, no extra text):
{{"provision_type": "...", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}"""


def build_unfair_tos_prompt(task: LexGLUETask, few_shot: int) -> str:
    """Build UNFAIR-ToS unfair clause detection prompt."""
    types_list = "\n".join(f"- {t}" for t in task.label_set)
    few_shot_text = _build_few_shot("unfair_tos", few_shot)

    return f"""Analyze this Terms of Service clause for unfairness.
Identify ONLY unfair elements that are ACTUALLY present in the text.
Do NOT identify unfair elements that are implied but not stated.
If the clause contains no unfair elements, report is_unfair as false.

Valid unfairness types:
{types_list}
{few_shot_text}
<document>
{task.text}
</document>

Output ONLY valid JSON (no markdown, no extra text):
{{"is_unfair": true/false, "unfairness_types": ["type1", ...], "reasoning": "brief explanation"}}"""


def build_contract_nli_prompt(task: LexGLUETask, few_shot: int) -> str:
    """Build ContractNLI entailment prompt."""
    few_shot_text = _build_few_shot("contract_nli", few_shot)

    return f"""Given the following contract text, determine the relationship between
the premise and hypothesis:
- "entailment": the hypothesis is supported by the contract
- "contradiction": the hypothesis contradicts the contract
- "neutral": the hypothesis is neither supported nor contradicted
{few_shot_text}
<document>
{task.text}
</document>

Output ONLY valid JSON (no markdown, no extra text):
{{"label": "entailment"|"contradiction"|"neutral", "reasoning": "brief explanation"}}"""


def build_ecthr_a_prompt(task: LexGLUETask, few_shot: int) -> str:
    """Build ECtHR Task A violation prediction prompt."""
    articles_list = "\n".join(f"- Article {a}" for a in task.label_set)
    few_shot_text = _build_few_shot("ecthr_a", few_shot)

    return f"""Given this ECtHR case description, predict which ECHR articles were violated.
Select ONLY from the following valid articles:

{articles_list}

If no violations are found, return an empty array.
{few_shot_text}
<document>
{task.text}
</document>

Output ONLY valid JSON (no markdown, no extra text):
{{"violated_articles": ["article_number", ...], "reasoning": "brief explanation"}}"""


def build_casehold_prompt(task: LexGLUETask, few_shot: int) -> str:
    """Build CaseHOLD holding identification prompt."""
    options = ""
    if task.holdings:
        option_labels = ["A", "B", "C", "D", "E"]
        for i, holding in enumerate(task.holdings):
            options += f"({option_labels[i]}) {holding}\n"

    few_shot_text = _build_few_shot("casehold", few_shot)

    return f"""Given this legal context, identify which holding statement correctly
fills the <HOLDING> placeholder. Select exactly one option.
{few_shot_text}
<document>
{task.text}
</document>

Options:
{options}
Output ONLY valid JSON (no markdown, no extra text):
{{"answer": "A"|"B"|"C"|"D"|"E", "reasoning": "brief explanation"}}"""


PROMPT_BUILDERS = {
    "ledgar": build_ledgar_prompt,
    "unfair_tos": build_unfair_tos_prompt,
    "contract_nli": build_contract_nli_prompt,
    "ecthr_a": build_ecthr_a_prompt,
    "casehold": build_casehold_prompt,
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_from_json(task: str, samples: int) -> list[LexGLUETask]:
    """Load tasks from local JSON cache files."""
    json_path = DATA_DIR / f"{task}_samples.json"
    if not json_path.exists():
        print(f"  [skip] {json_path} not found — run ingest-lexglue.py first", file=sys.stderr)
        return []

    data = json.loads(json_path.read_text())
    tasks = []
    for i, sample in enumerate(data):
        if samples and i >= samples:
            break

        tasks.append(
            LexGLUETask(
                task_id=f"{task}_{sample.get('hf_index', i)}",
                task_type=task,
                text=sample["text"],
                label=sample.get("label"),
                labels=sample.get("labels"),
                label_set=sample.get("label_set", []),
                holdings=sample.get("holdings"),
                hf_index=sample.get("hf_index", i),
                sample_id=sample.get("id", ""),
            )
        )

    return tasks


def load_from_neon(task: str, samples: int) -> list[LexGLUETask]:
    """Load tasks from Neon Postgres."""

    async def _load():
        from src.neon_db import connection_pool

        async with connection_pool() as conn:
            limit_clause = f"LIMIT {samples}" if samples else ""
            rows = await (
                await conn.execute(
                    f"""SELECT id, task, hf_index, text, holdings, label, labels, label_set
                        FROM julia_lexglue_samples
                        WHERE task = %s AND split = 'test'
                        ORDER BY hf_index
                        {limit_clause}""",
                    (task,),
                )
            ).fetchall()

            tasks = []
            for row in rows:
                tasks.append(
                    LexGLUETask(
                        task_id=f"{row[1]}_{row[2]}",
                        task_type=row[1],
                        text=row[3],
                        label=row[5],
                        labels=json.loads(row[6]) if row[6] else None,
                        label_set=json.loads(row[7]) if row[7] else [],
                        holdings=json.loads(row[4]) if row[4] else None,
                        hf_index=row[2],
                        sample_id=row[0],
                    )
                )
            return tasks

    return asyncio.run(_load())


def load_tasks(task: str, samples: int, from_neon: bool) -> list[LexGLUETask]:
    """Load tasks from Neon or local JSON, then build prompts."""
    if from_neon:
        tasks = load_from_neon(task, samples)
    else:
        tasks = load_from_json(task, samples)
    return tasks


# ---------------------------------------------------------------------------
# Model calling
# ---------------------------------------------------------------------------


def call_model(task: LexGLUETask) -> tuple[LexGLUETask, str, dict]:
    """Call Claude API for a single task. Returns (task, output, metadata)."""
    import anthropic

    client = anthropic.Anthropic()
    t0 = time.monotonic()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            system=JULIA_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": task.prompt}],
        )
        output = response.content[0].text
        latency_ms = int((time.monotonic() - t0) * 1000)
        return (
            task,
            output,
            {
                "latency_ms": latency_ms,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
        )
    except Exception as e:
        return task, "", {"error": str(e)}


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------


def _extract_json(text: str) -> dict | None:
    """Extract JSON object from model output, handling markdown fences."""
    # Try direct parse first
    text = text.strip()
    if text.startswith("```"):
        # Strip markdown code fences
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object in the text
    match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return None


def parse_response(task: LexGLUETask, raw_output: str) -> LexGLUEResult:
    """Parse model output and compare to gold labels."""
    result = LexGLUEResult(
        task_id=task.task_id,
        task_type=task.task_type,
        hf_index=task.hf_index,
        gold_label=task.label,
        gold_labels=task.labels,
        raw_output=raw_output,
    )

    parsed = _extract_json(raw_output)
    if not parsed:
        result.error = "Failed to parse JSON from output"
        return result

    result.confidence = parsed.get("confidence", 0.0)

    if task.task_type == "ledgar":
        pred = parsed.get("provision_type", "")
        result.predicted_label = pred
        result.is_correct = pred == task.label

    elif task.task_type == "unfair_tos":
        pred_types = parsed.get("unfairness_types", [])
        result.predicted_labels = pred_types
        gold = set(task.labels) if task.labels else set()
        pred = set(pred_types)
        result.is_correct = gold == pred

    elif task.task_type == "contract_nli":
        pred = parsed.get("label", "")
        result.predicted_label = pred
        result.is_correct = pred == task.label

    elif task.task_type == "ecthr_a":
        pred_articles = parsed.get("violated_articles", [])
        result.predicted_labels = pred_articles
        gold = set(task.labels) if task.labels else set()
        pred = set(pred_articles)
        result.is_correct = gold == pred

    elif task.task_type == "casehold":
        answer = parsed.get("answer", "")
        answer_map = {"A": "0", "B": "1", "C": "2", "D": "3", "E": "4"}
        pred = answer_map.get(answer.upper(), answer)
        result.predicted_label = pred
        result.is_correct = pred == task.label

    return result


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------


def compute_task_metrics(task_type: str, results: list[LexGLUEResult]) -> dict:
    """Compute aggregate metrics for a single task."""
    valid_results = [r for r in results if r.error is None]

    if not valid_results:
        return {"metric": TASK_METRICS[task_type], "score": 0.0, "total": 0, "errors": len(results)}

    metric_type = TASK_METRICS[task_type]

    if task_type in ("unfair_tos", "ecthr_a"):
        # Multi-label tasks
        y_true_sets = [set(r.gold_labels or []) for r in valid_results]
        y_pred_sets = [set(r.predicted_labels or []) for r in valid_results]

        if metric_type == "macro_f1":
            score = multilabel_macro_f1(y_true_sets, y_pred_sets)
        else:
            score = multilabel_micro_f1(y_true_sets, y_pred_sets)
    else:
        # Single-label tasks
        y_true = [r.gold_label or "" for r in valid_results]
        y_pred = [r.predicted_label or "" for r in valid_results]

        if metric_type == "micro_f1":
            score = micro_f1(y_true, y_pred)
        elif metric_type == "macro_f1":
            score = macro_f1(y_true, y_pred)
        else:
            score = accuracy(y_true, y_pred)

    exact_match = sum(1 for r in valid_results if r.is_correct)
    avg_latency = sum(r.latency_ms for r in valid_results) / max(len(valid_results), 1)
    avg_tokens = sum(r.output_tokens for r in valid_results) / max(len(valid_results), 1)

    return {
        "metric": metric_type,
        "score": round(score * 100, 2),
        "exact_match_rate": round(exact_match / len(valid_results) * 100, 2),
        "total": len(valid_results),
        "errors": len(results) - len(valid_results),
        "avg_latency_ms": int(avg_latency),
        "avg_output_tokens": int(avg_tokens),
    }


# ---------------------------------------------------------------------------
# Report + leaderboard
# ---------------------------------------------------------------------------


def print_report(all_metrics: dict[str, dict], run_id: str) -> None:
    """Print formatted benchmark report."""
    print("\n" + "=" * 72)
    print("  LEXGLUE MULTI-TASK LEGAL BENCHMARK")
    print("=" * 72)
    print(f"\n  Run:   {run_id}")
    print(f"  Model: {MODEL}")

    for task, metrics in all_metrics.items():
        m = metrics
        print(f"\n  -- {task.upper()} ({m['metric']}) --")
        print(f"  Score:          {m['score']:.1f}%")
        print(f"  Exact match:    {m['exact_match_rate']:.1f}%")
        print(f"  Samples:        {m['total']}  Errors: {m['errors']}")
        print(f"  Avg latency:    {m['avg_latency_ms']} ms")
        print(f"  Avg tokens:     {m['avg_output_tokens']}")

    print("\n" + "=" * 72)


def print_leaderboard(all_metrics: dict[str, dict]) -> None:
    """Compare Julia against published baselines."""
    if not BASELINES_PATH.exists():
        print("  [skip] No baselines file found", file=sys.stderr)
        return

    baselines = json.loads(BASELINES_PATH.read_text())

    print("\n  LEADERBOARD COMPARISON")
    print("  " + "-" * 68)
    print(f"  {'Task':<15} {'Julia':<10} {'BERT':<10} {'Legal-BERT':<12} {'DeBERTa':<10}")
    print("  " + "-" * 68)

    for task, metrics in all_metrics.items():
        bl = baselines.get(task, {})
        julia_score = f"{metrics['score']:.1f}%"
        bert = f"{bl.get('bert_base', 'N/A')}%"
        legal_bert = f"{bl.get('legal_bert', 'N/A')}%"
        deberta = f"{bl.get('deberta', 'N/A')}%"
        print(f"  {task:<15} {julia_score:<10} {bert:<10} {legal_bert:<12} {deberta:<10}")

    print("  " + "-" * 68)


# ---------------------------------------------------------------------------
# Neon results storage
# ---------------------------------------------------------------------------


async def store_results_neon(run_id: str, results: list[LexGLUEResult]) -> int:
    """Store eval results in Neon julia_lexglue_results table."""
    try:
        from src.neon_db import connection_pool
    except Exception:
        return 0

    count = 0
    try:
        async with connection_pool() as conn:
            for r in results:
                if r.error:
                    continue
                await conn.execute(
                    """INSERT INTO julia_lexglue_results
                       (run_id, sample_id, task, predicted_label, predicted_labels,
                        gold_label, gold_labels, is_correct, confidence, model,
                        input_tokens, output_tokens, latency_ms, raw_output)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        run_id,
                        r.task_id,
                        r.task_type,
                        r.predicted_label,
                        json.dumps(r.predicted_labels) if r.predicted_labels else None,
                        r.gold_label,
                        json.dumps(r.gold_labels) if r.gold_labels else None,
                        r.is_correct,
                        r.confidence,
                        MODEL,
                        r.input_tokens,
                        r.output_tokens,
                        r.latency_ms,
                        r.raw_output[:4000],
                    ),
                )
                count += 1
            await conn.commit()
    except Exception as e:
        print(f"  [warn] Failed to store results in Neon: {e}", file=sys.stderr)

    return count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="LexGLUE multi-task legal benchmark eval")
    parser.add_argument(
        "--task",
        default="",
        choices=ALL_TASKS + [""],
        help="Single task to run (default: all 5)",
    )
    parser.add_argument(
        "--few-shot",
        type=int,
        default=3,
        help="Number of few-shot examples per prompt (default: 3)",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=0,
        help="Limit samples per task (0=all)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show task matrix without running")
    parser.add_argument(
        "--leaderboard",
        action="store_true",
        help="Compare against published baselines",
    )
    parser.add_argument(
        "--from-neon",
        action="store_true",
        help="Load samples from Neon pgvector instead of local JSON",
    )
    parser.add_argument(
        "--output",
        default=str(DATA_DIR / "results.json"),
        help="Output JSON path",
    )
    args = parser.parse_args()

    tasks_to_run = [args.task] if args.task else ALL_TASKS
    run_id = f"lexglue_{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    # Load all tasks
    all_tasks: list[LexGLUETask] = []
    for task_name in tasks_to_run:
        task_list = load_tasks(task_name, args.samples, args.from_neon)
        # Build prompts
        for t in task_list:
            builder = PROMPT_BUILDERS.get(t.task_type)
            if builder:
                t.prompt = builder(t, args.few_shot)
        all_tasks.extend(task_list)

    print(f"\n  Loaded {len(all_tasks)} eval tasks", file=sys.stderr)
    print(f"  Tasks: {tasks_to_run}", file=sys.stderr)
    print(f"  Few-shot: {args.few_shot}", file=sys.stderr)
    print(f"  Model: {MODEL}", file=sys.stderr)

    if args.dry_run:
        for t in all_tasks:
            print(f"  [{t.task_type}] {t.task_id} (label={t.label or t.labels})")
        return

    if not all_tasks:
        print("  No tasks to run. Run ingest-lexglue.py first.", file=sys.stderr)
        return

    # Phase 1: API calls (I/O bound)
    concurrency = min(API_CONCURRENCY, len(all_tasks))
    print(f"\n  Phase 1: API calls ({concurrency} concurrent)...", file=sys.stderr)

    api_results: list[tuple[LexGLUETask, str, dict]] = []
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(call_model, task): task for task in all_tasks}
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            api_results.append(result)
            task = result[0]
            status = "error" if "error" in result[2] else "ok"
            print(
                f"  [{i + 1}/{len(all_tasks)}] {task.task_type}/{task.task_id} -- {status}",
                file=sys.stderr,
            )

    # Phase 2: Parse responses + compute metrics
    print("\n  Phase 2: Computing metrics...", file=sys.stderr)

    all_results: list[LexGLUEResult] = []
    for task, raw_output, meta in api_results:
        result = parse_response(task, raw_output)
        if "error" in meta:
            result.error = meta["error"]
        else:
            result.latency_ms = meta.get("latency_ms", 0)
            result.input_tokens = meta.get("input_tokens", 0)
            result.output_tokens = meta.get("output_tokens", 0)
        all_results.append(result)

    # Compute per-task metrics
    all_metrics: dict[str, dict] = {}
    for task_name in tasks_to_run:
        task_results = [r for r in all_results if r.task_type == task_name]
        if task_results:
            all_metrics[task_name] = compute_task_metrics(task_name, task_results)

    # Phase 3: Report
    print_report(all_metrics, run_id)

    if args.leaderboard:
        print_leaderboard(all_metrics)

    # Store results in Neon (best effort)
    neon_count = asyncio.run(store_results_neon(run_id, all_results))
    if neon_count:
        print(f"\n  Stored {neon_count} results in Neon", file=sys.stderr)

    # Write JSON results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_data = {
        "run_id": run_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": MODEL,
        "config": {
            "tasks": tasks_to_run,
            "few_shot": args.few_shot,
            "samples": args.samples,
            "from_neon": args.from_neon,
        },
        "metrics": all_metrics,
        "results": [asdict(r) for r in all_results],
    }
    output_path.write_text(json.dumps(output_data, indent=2, default=str))
    print(f"  Results written to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
