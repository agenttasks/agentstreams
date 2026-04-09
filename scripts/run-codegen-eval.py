#!/usr/bin/env python3
"""Parallel A/B code generation eval runner.

Saturates all available CPU cores by running model API calls concurrently
and performing code validation (AST parse, lint, execution) in parallel
worker processes. Inspired by Anthropic's infrastructure noise research:
controls hardware variables to isolate model capability differences.

Usage:
  uv run scripts/run-codegen-eval.py                    # Full A/B suite
  uv run scripts/run-codegen-eval.py --models sonnet    # Sonnet only
  uv run scripts/run-codegen-eval.py --lang python      # Python tasks only
  uv run scripts/run-codegen-eval.py --samples 3        # 3 samples per task
  uv run scripts/run-codegen-eval.py --dry-run          # Show tasks, don't run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from multiprocessing import cpu_count
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import importlib.util

_provider_path = PROJECT_ROOT / "evals" / "codegen-ab" / "provider.py"
_spec = importlib.util.spec_from_file_location("codegen_ab_provider", _provider_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
extract_code_block = _mod.extract_code_block
validate_code = _mod.validate_code

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

MODEL_VARIANTS = {
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-6",
}


@dataclass
class EvalTask:
    task_id: str
    description: str
    prompt: str
    language: str
    difficulty: str
    model_key: str
    model_id: str
    sample_idx: int


@dataclass
class EvalResult:
    task_id: str
    model_key: str
    model_id: str
    language: str
    difficulty: str
    sample_idx: int
    latency_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    syntax_valid: bool = False
    lint_issue_count: int = 0
    executes: bool | None = None
    code_length: int = 0
    error: str | None = None


# ---------------------------------------------------------------------------
# API caller (I/O bound — thread pool)
# ---------------------------------------------------------------------------


def call_model(task: EvalTask) -> tuple[EvalTask, str, dict]:
    """Call Claude API for a single task. Returns (task, generated_code, metadata)."""
    import anthropic

    api_key = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
    if not api_key:
        return task, "", {"error": "No CLAUDE_CODE_OAUTH_TOKEN"}

    client = anthropic.Anthropic(api_key=api_key)
    t0 = time.monotonic()

    try:
        response = client.messages.create(
            model=task.model_id,
            max_tokens=4096,
            temperature=0,
            messages=[{"role": "user", "content": task.prompt}],
        )
        output = response.content[0].text
        latency_ms = int((time.monotonic() - t0) * 1000)
        code = extract_code_block(output, task.language)
        return task, code, {
            "latency_ms": latency_ms,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
    except Exception as e:
        return task, "", {"error": str(e)}


# ---------------------------------------------------------------------------
# Code validator (CPU bound — process pool)
# ---------------------------------------------------------------------------


def validate_task(args: tuple[EvalTask, str, dict]) -> EvalResult:
    """Validate generated code in a worker process."""
    task, code, meta = args

    result = EvalResult(
        task_id=task.task_id,
        model_key=task.model_key,
        model_id=task.model_id,
        language=task.language,
        difficulty=task.difficulty,
        sample_idx=task.sample_idx,
    )

    if "error" in meta:
        result.error = meta["error"]
        return result

    result.latency_ms = meta.get("latency_ms", 0)
    result.input_tokens = meta.get("input_tokens", 0)
    result.output_tokens = meta.get("output_tokens", 0)
    result.code_length = len(code)

    if code:
        validation = validate_code(code, task.language)
        result.syntax_valid = validation["syntax_valid"]
        result.lint_issue_count = len(validation["lint_issues"])
        result.executes = validation.get("executes")

    return result


# ---------------------------------------------------------------------------
# Task loading
# ---------------------------------------------------------------------------


def load_tasks(
    languages: list[str],
    models: list[str],
    samples: int,
) -> list[EvalTask]:
    """Load task definitions and expand into (task × model × sample) matrix."""
    tasks = []
    data_dir = PROJECT_ROOT / "evals" / "codegen-ab" / "test_data"

    for lang in languages:
        task_file = data_dir / f"{lang}_tasks.json"
        if not task_file.exists():
            print(f"  [skip] {task_file} not found", file=sys.stderr)
            continue

        task_defs = json.loads(task_file.read_text())
        for tdef in task_defs:
            for model_key in models:
                model_id = MODEL_VARIANTS[model_key]
                for s in range(samples):
                    tasks.append(
                        EvalTask(
                            task_id=tdef["id"],
                            description=tdef["description"],
                            prompt=tdef["prompt"],
                            language=tdef.get("language", lang),
                            difficulty=tdef.get("difficulty", "medium"),
                            model_key=model_key,
                            model_id=model_id,
                            sample_idx=s,
                        )
                    )

    return tasks


# ---------------------------------------------------------------------------
# Result analysis
# ---------------------------------------------------------------------------


def analyze_results(results: list[EvalResult]) -> dict:
    """Compute A/B comparison metrics."""
    from collections import defaultdict

    by_model = defaultdict(list)
    for r in results:
        by_model[r.model_key].append(r)

    summary = {}
    for model_key, model_results in by_model.items():
        total = len(model_results)
        errors = sum(1 for r in model_results if r.error)
        valid = [r for r in model_results if not r.error]

        syntax_pass = sum(1 for r in valid if r.syntax_valid)
        lint_clean = sum(1 for r in valid if r.lint_issue_count == 0)
        executes = sum(1 for r in valid if r.executes is True)
        exec_tested = sum(1 for r in valid if r.executes is not None)

        avg_latency = sum(r.latency_ms for r in valid) / max(len(valid), 1)
        avg_tokens = sum(r.output_tokens for r in valid) / max(len(valid), 1)
        avg_code_len = sum(r.code_length for r in valid) / max(len(valid), 1)

        summary[model_key] = {
            "model": MODEL_VARIANTS[model_key],
            "total_tasks": total,
            "errors": errors,
            "syntax_pass_rate": syntax_pass / max(len(valid), 1),
            "lint_clean_rate": lint_clean / max(len(valid), 1),
            "execution_pass_rate": executes / max(exec_tested, 1) if exec_tested else None,
            "avg_latency_ms": int(avg_latency),
            "avg_output_tokens": int(avg_tokens),
            "avg_code_length": int(avg_code_len),
        }

    # A/B delta
    keys = list(summary.keys())
    if len(keys) == 2:
        a, b = keys
        summary["delta"] = {
            "syntax_pass_rate": summary[b]["syntax_pass_rate"] - summary[a]["syntax_pass_rate"],
            "lint_clean_rate": summary[b]["lint_clean_rate"] - summary[a]["lint_clean_rate"],
            "latency_diff_ms": summary[b]["avg_latency_ms"] - summary[a]["avg_latency_ms"],
            "token_diff": summary[b]["avg_output_tokens"] - summary[a]["avg_output_tokens"],
        }
        if summary[a]["execution_pass_rate"] is not None and summary[b]["execution_pass_rate"] is not None:
            summary["delta"]["execution_pass_rate"] = (
                summary[b]["execution_pass_rate"] - summary[a]["execution_pass_rate"]
            )

    return summary


def print_report(results: list[EvalResult], summary: dict) -> None:
    """Print formatted A/B comparison report."""
    print("\n" + "=" * 72)
    print("  CODE GENERATION A/B EVAL REPORT")
    print("=" * 72)

    ncpu = cpu_count()
    print(f"\n  Hardware: {ncpu} CPU cores, {os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') // (1024**3)} GB RAM")
    print(f"  Tasks: {len(results)} total executions")

    for model_key, metrics in summary.items():
        if model_key == "delta":
            continue
        m = metrics
        print(f"\n  ── {model_key.upper()} ({m['model']}) ──")
        print(f"  Tasks: {m['total_tasks']}  Errors: {m['errors']}")
        print(f"  Syntax pass rate:    {m['syntax_pass_rate']:.1%}")
        print(f"  Lint clean rate:     {m['lint_clean_rate']:.1%}")
        if m["execution_pass_rate"] is not None:
            print(f"  Execution pass rate: {m['execution_pass_rate']:.1%}")
        print(f"  Avg latency:         {m['avg_latency_ms']} ms")
        print(f"  Avg output tokens:   {m['avg_output_tokens']}")
        print(f"  Avg code length:     {m['avg_code_length']} chars")

    if "delta" in summary:
        d = summary["delta"]
        print(f"\n  ── DELTA (Opus - Sonnet) ──")
        print(f"  Syntax pass:    {d['syntax_pass_rate']:+.1%}")
        print(f"  Lint clean:     {d['lint_clean_rate']:+.1%}")
        if "execution_pass_rate" in d:
            print(f"  Execution pass: {d['execution_pass_rate']:+.1%}")
        print(f"  Latency diff:   {d['latency_diff_ms']:+d} ms")
        print(f"  Token diff:     {d['token_diff']:+d}")

    print("\n" + "=" * 72)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Parallel A/B codegen eval runner")
    parser.add_argument(
        "--models",
        nargs="+",
        default=["sonnet", "opus"],
        choices=["sonnet", "opus"],
        help="Model variants to test (default: both)",
    )
    parser.add_argument(
        "--lang",
        nargs="+",
        default=["python", "typescript"],
        choices=["python", "typescript"],
        help="Languages to test (default: both)",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=1,
        help="Samples per task per model (default: 1)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show tasks without running")
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "evals" / "codegen-ab" / "results.json"),
        help="Output JSON path",
    )
    args = parser.parse_args()

    tasks = load_tasks(args.lang, args.models, args.samples)
    print(f"\n  Loaded {len(tasks)} eval tasks", file=sys.stderr)
    print(f"  Models: {args.models}", file=sys.stderr)
    print(f"  Languages: {args.lang}", file=sys.stderr)
    print(f"  Samples per task: {args.samples}", file=sys.stderr)
    print(f"  CPU cores: {cpu_count()}", file=sys.stderr)

    if args.dry_run:
        for t in tasks:
            print(f"  [{t.model_key}] {t.task_id} ({t.language}) sample={t.sample_idx}")
        return

    # Phase 1: API calls (I/O bound — thread pool, one thread per API call)
    # Limit concurrency to avoid rate limiting
    api_concurrency = min(4, len(tasks))
    print(f"\n  Phase 1: API calls ({api_concurrency} concurrent)...", file=sys.stderr)

    api_results: list[tuple[EvalTask, str, dict]] = []
    with ThreadPoolExecutor(max_workers=api_concurrency) as pool:
        futures = {pool.submit(call_model, task): task for task in tasks}
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            api_results.append(result)
            task = result[0]
            status = "error" if "error" in result[2] else "ok"
            print(
                f"  [{i+1}/{len(tasks)}] {task.model_key}/{task.task_id} — {status}",
                file=sys.stderr,
            )

    # Phase 2: Code validation (CPU bound — process pool, saturate all cores)
    ncpu = cpu_count()
    print(f"\n  Phase 2: Validation ({ncpu} CPU workers)...", file=sys.stderr)

    eval_results: list[EvalResult] = []
    with ProcessPoolExecutor(max_workers=ncpu) as pool:
        futures = {pool.submit(validate_task, ar): ar for ar in api_results}
        for future in as_completed(futures):
            eval_results.append(future.result())

    # Phase 3: Analysis
    summary = analyze_results(eval_results)
    print_report(eval_results, summary)

    # Write results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hardware": {
            "cpu_cores": cpu_count(),
            "ram_gb": os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") // (1024**3),
        },
        "config": {
            "models": args.models,
            "languages": args.lang,
            "samples": args.samples,
        },
        "summary": summary,
        "results": [asdict(r) for r in eval_results],
    }
    output_path.write_text(json.dumps(output_data, indent=2))
    print(f"\n  Results written to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
