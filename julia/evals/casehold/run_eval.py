"""CaseHOLD legal holdings benchmark runner.

Loads examples from Neon Postgres (or local JSON sample), runs Julia-style
legal analysis prompts against Claude, measures accuracy, and persists
results to casehold_eval_results.

Prompt engineering:
- Allow "I don't know" responses (reduce hallucinations)
- Chain-of-thought verification (identify issue → evaluate → select → verify)
- Direct quote grounding (extract supporting phrase from context)
- Prompt leak protection (scan for rubric keywords)

Usage:
    python -m julia.evals.casehold.run_eval
    python -m julia.evals.casehold.run_eval --samples 20 --model claude-sonnet-4-6
    python -m julia.evals.casehold.run_eval --full --jurisdiction federal --citation-audit

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
      NEON_DATABASE_URL for database access (optional).
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import anthropic
from rich.console import Console
from rich.table import Table

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from .config import (  # noqa: E402
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_MODEL,
    DEFAULT_SAMPLE_SIZE,
    DEFAULT_WORKERS,
    MAX_TOKENS,
    OUTPUT_SCHEMA,
    PROMPT_LEAK_KEYWORDS,
    SYSTEM_PROMPT,
    TARGET_ACCURACY,
    TEMPERATURE,
    USER_PROMPT_TEMPLATE,
    format_holdings,
)

console = Console()

# ── Data Loading ───────────────────────────────────────────


def load_examples_from_json(
    path: Path | None = None,
    jurisdiction: str = "",
    samples: int = 0,
) -> list[dict]:
    """Load CaseHOLD examples from local JSON fixture."""
    if path is None:
        path = PROJECT_ROOT / "julia" / "evals" / "test_data" / "casehold_sample.json"

    if not path.exists():
        console.print(f"[red]Sample file not found: {path}[/red]")
        console.print("Run: python -m julia.evals.casehold.ingest --export-sample")
        sys.exit(1)

    examples = json.loads(path.read_text())

    if jurisdiction:
        examples = [e for e in examples if e.get("jurisdiction") == jurisdiction]

    if samples > 0:
        examples = examples[:samples]

    return examples


async def load_examples_from_neon(
    jurisdiction: str = "",
    samples: int = 0,
) -> list[dict]:
    """Load CaseHOLD examples from Neon Postgres."""
    from src.neon_db import connection_pool

    query = "SELECT id, citing_prompt, holdings, label, jurisdiction, court FROM casehold_examples"
    conditions = []
    params: list[Any] = []

    if jurisdiction:
        conditions.append("jurisdiction = %s")
        params.append(jurisdiction)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id"

    if samples > 0:
        query += " LIMIT %s"
        params.append(samples)

    async with connection_pool() as conn:
        rows = await (await conn.execute(query, tuple(params))).fetchall()

    return [
        {
            "id": row[0],
            "citing_prompt": row[1],
            "holdings": row[2] if isinstance(row[2], list) else json.loads(row[2]),
            "label": row[3],
            "jurisdiction": row[4],
            "court": row[5],
        }
        for row in rows
    ]


# ── Model Interaction ─────────────────────────────────────


def get_client() -> anthropic.Anthropic:
    """Create Anthropic client using CLAUDE_CODE_OAUTH_TOKEN."""
    return anthropic.Anthropic()


def call_model(
    client: anthropic.Anthropic,
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Call Claude API and return response with usage metadata."""
    start_ms = time.monotonic_ns() // 1_000_000

    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    duration_ms = (time.monotonic_ns() // 1_000_000) - start_ms
    text = response.content[0].text if response.content else ""

    return {
        "text": text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "duration_ms": duration_ms,
    }


# ── Output Parsing & Validation ────────────────────────────


def parse_output(text: str) -> dict | None:
    """Parse JSON output from model response.

    Handles markdown code fences and extracts the first JSON object.
    """
    # Strip markdown code fences
    cleaned = re.sub(r"```(?:json)?\s*\n?", "", text)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON object in the text
        match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return None


def validate_output(parsed: dict) -> list[str]:
    """Validate parsed output against OUTPUT_SCHEMA. Returns list of errors."""
    errors = []

    for field_name in OUTPUT_SCHEMA["required"]:
        if field_name not in parsed:
            errors.append(f"Missing required field: {field_name}")

    if "selected_holding" in parsed:
        val = parsed["selected_holding"]
        if not isinstance(val, int) or val < -1 or val > 4:
            errors.append(f"selected_holding must be integer -1 to 4, got {val}")

    if "confidence" in parsed:
        val = parsed["confidence"]
        if not isinstance(val, (int, float)) or val < 0 or val > 1:
            errors.append(f"confidence must be number 0 to 1, got {val}")

    for field_name in ["question_id", "reasoning", "supporting_quote"]:
        if field_name in parsed and not isinstance(parsed[field_name], str):
            errors.append(f"{field_name} must be string, got {type(parsed[field_name]).__name__}")

    return errors


def check_prompt_leak(text: str) -> list[str]:
    """Check for prompt leak keywords in model output."""
    found = []
    text_lower = text.lower()
    for keyword in PROMPT_LEAK_KEYWORDS:
        if keyword.lower() in text_lower:
            found.append(keyword)
    return found


def check_citation_grounded(supporting_quote: str, citing_prompt: str) -> bool:
    """Check if the supporting quote appears in the citing prompt.

    Uses fuzzy matching: the quote (lowered, stripped) must be a substring
    of the citing prompt (lowered).
    """
    if not supporting_quote or not citing_prompt:
        return False
    quote = supporting_quote.lower().strip()
    context = citing_prompt.lower()
    # Exact substring match
    if quote in context:
        return True
    # Fuzzy: check if at least 80% of words overlap
    quote_words = set(quote.split())
    context_words = set(context.split())
    if not quote_words:
        return False
    overlap = len(quote_words & context_words) / len(quote_words)
    return overlap >= 0.8


# ── Single Example Evaluation ─────────────────────────────


def evaluate_single(
    client: anthropic.Anthropic,
    example: dict,
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Evaluate a single CaseHOLD example. Returns result dict."""
    prompt = USER_PROMPT_TEMPLATE.format(
        citing_prompt=example["citing_prompt"],
        holdings_formatted=format_holdings(example["holdings"]),
        question_id=example["id"],
    )

    try:
        response = call_model(client, SYSTEM_PROMPT, prompt, model)
    except Exception as e:
        return {
            "example_id": example["id"],
            "selected_holding": -1,
            "correct": False,
            "confidence": 0.0,
            "reasoning": "",
            "supporting_quote": "",
            "citation_grounded": False,
            "duration_ms": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "raw_output": "",
            "error": str(e),
            "parse_error": True,
            "prompt_leak": [],
        }

    raw_output = response["text"]
    parsed = parse_output(raw_output)

    if parsed is None:
        return {
            "example_id": example["id"],
            "selected_holding": -1,
            "correct": False,
            "confidence": 0.0,
            "reasoning": "",
            "supporting_quote": "",
            "citation_grounded": False,
            "duration_ms": response["duration_ms"],
            "input_tokens": response["input_tokens"],
            "output_tokens": response["output_tokens"],
            "raw_output": raw_output,
            "error": "Failed to parse JSON from model output",
            "parse_error": True,
            "prompt_leak": check_prompt_leak(raw_output),
        }

    validation_errors = validate_output(parsed)
    selected = parsed.get("selected_holding", -1)
    confidence = parsed.get("confidence", 0.0)
    reasoning = parsed.get("reasoning", "")
    supporting_quote = parsed.get("supporting_quote", "")
    correct = selected == example["label"]
    grounded = check_citation_grounded(supporting_quote, example["citing_prompt"])

    return {
        "example_id": example["id"],
        "selected_holding": selected,
        "correct": correct,
        "confidence": confidence,
        "reasoning": reasoning,
        "supporting_quote": supporting_quote,
        "citation_grounded": grounded,
        "duration_ms": response["duration_ms"],
        "input_tokens": response["input_tokens"],
        "output_tokens": response["output_tokens"],
        "raw_output": raw_output,
        "error": "; ".join(validation_errors) if validation_errors else "",
        "parse_error": False,
        "prompt_leak": check_prompt_leak(raw_output),
    }


# ── Batch Evaluation ──────────────────────────────────────


def run_eval(
    examples: list[dict],
    model: str = DEFAULT_MODEL,
    workers: int = DEFAULT_WORKERS,
) -> list[dict]:
    """Run CaseHOLD eval on a batch of examples using ThreadPoolExecutor."""
    client = get_client()
    results: list[dict] = []

    console.print(f"[bold]Running CaseHOLD eval: {len(examples)} examples, model={model}[/bold]")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_idx = {
            executor.submit(evaluate_single, client, ex, model): i
            for i, ex in enumerate(examples)
        }

        for completed, future in enumerate(as_completed(future_to_idx), 1):
            result = future.result()
            results.append(result)

            if completed % 10 == 0 or completed == len(examples):
                correct_so_far = sum(1 for r in results if r["correct"])
                acc = correct_so_far / len(results) if results else 0
                console.print(
                    f"  [{completed}/{len(examples)}] "
                    f"accuracy={acc:.1%} "
                    f"({correct_so_far}/{len(results)} correct)"
                )

    return results


# ── Result Persistence ────────────────────────────────────


async def persist_results(run_id: str, results: list[dict], model: str) -> int:
    """Persist evaluation results to Neon Postgres."""
    from src.neon_db import connection_pool

    count = 0
    async with connection_pool() as conn:
        for r in results:
            await conn.execute(
                """INSERT INTO casehold_eval_results
                   (run_id, example_id, model, selected_holding, correct,
                    confidence, reasoning, supporting_quote, citation_grounded,
                    duration_ms, input_tokens, output_tokens, raw_output)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    run_id,
                    r["example_id"],
                    model,
                    r["selected_holding"],
                    r["correct"],
                    r["confidence"],
                    r["reasoning"],
                    r["supporting_quote"],
                    r["citation_grounded"],
                    r["duration_ms"],
                    r["input_tokens"],
                    r["output_tokens"],
                    r["raw_output"],
                ),
            )
            count += 1
        await conn.commit()

    return count


# ── Metrics Computation ───────────────────────────────────


def compute_metrics(
    results: list[dict],
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> dict[str, Any]:
    """Compute accuracy, per-jurisdiction metrics, and citation audit stats."""
    total = len(results)
    if total == 0:
        return {"total": 0, "accuracy": 0.0}

    correct = sum(1 for r in results if r["correct"])
    accuracy = correct / total

    # Per-jurisdiction accuracy
    by_jurisdiction: dict[str, list[dict]] = {}
    for r in results:
        # Need to look up jurisdiction from examples... use a fallback
        j = r.get("jurisdiction", "unknown")
        by_jurisdiction.setdefault(j, []).append(r)

    jurisdiction_accuracy = {}
    for j, group in sorted(by_jurisdiction.items()):
        j_correct = sum(1 for r in group if r["correct"])
        jurisdiction_accuracy[j] = {
            "total": len(group),
            "correct": j_correct,
            "accuracy": j_correct / len(group) if group else 0,
        }

    # Confidence distribution
    low_confidence = sum(1 for r in results if r["confidence"] < confidence_threshold)
    high_confidence = total - low_confidence
    high_conf_correct = sum(
        1 for r in results if r["confidence"] >= confidence_threshold and r["correct"]
    )
    high_conf_accuracy = high_conf_correct / high_confidence if high_confidence > 0 else 0

    # Citation grounding
    grounded = sum(1 for r in results if r["citation_grounded"])
    grounding_rate = grounded / total

    # Parse errors
    parse_errors = sum(1 for r in results if r.get("parse_error", False))

    # Prompt leaks
    prompt_leaks = sum(1 for r in results if r.get("prompt_leak"))

    # Token usage
    total_input = sum(r["input_tokens"] for r in results)
    total_output = sum(r["output_tokens"] for r in results)
    total_duration = sum(r["duration_ms"] for r in results)

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "target_accuracy": TARGET_ACCURACY,
        "passes_target": accuracy >= TARGET_ACCURACY,
        "jurisdiction_accuracy": jurisdiction_accuracy,
        "confidence_threshold": confidence_threshold,
        "low_confidence_count": low_confidence,
        "high_confidence_count": high_confidence,
        "high_confidence_accuracy": high_conf_accuracy,
        "citation_grounding_rate": grounding_rate,
        "citation_grounded_count": grounded,
        "parse_errors": parse_errors,
        "prompt_leaks": prompt_leaks,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_duration_ms": total_duration,
        "avg_duration_ms": total_duration / total if total > 0 else 0,
    }


# ── Report Printing ───────────────────────────────────────


def print_report(metrics: dict, model: str) -> None:
    """Print evaluation report using Rich tables."""
    console.print()

    # Overall results
    status = "[green]PASS[/green]" if metrics["passes_target"] else "[red]FAIL[/red]"
    table = Table(title=f"CaseHOLD Benchmark Results ({model})")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Total Examples", str(metrics["total"]))
    table.add_row("Correct", str(metrics["correct"]))
    table.add_row("Accuracy", f"{metrics['accuracy']:.1%}")
    table.add_row("Target (BERT baseline)", f"{metrics['target_accuracy']:.0%}")
    table.add_row("Status", status)
    table.add_row("", "")
    table.add_row("Citation Grounding Rate", f"{metrics['citation_grounding_rate']:.1%}")
    table.add_row(
        f"High Confidence (>={metrics['confidence_threshold']})",
        f"{metrics['high_confidence_count']}/{metrics['total']}",
    )
    table.add_row("High Confidence Accuracy", f"{metrics['high_confidence_accuracy']:.1%}")
    table.add_row("Parse Errors", str(metrics["parse_errors"]))
    table.add_row("Prompt Leaks", str(metrics["prompt_leaks"]))
    table.add_row("", "")
    table.add_row("Total Input Tokens", f"{metrics['total_input_tokens']:,}")
    table.add_row("Total Output Tokens", f"{metrics['total_output_tokens']:,}")
    table.add_row("Avg Duration", f"{metrics['avg_duration_ms']:.0f}ms")

    console.print(table)

    # Per-jurisdiction breakdown (if multiple jurisdictions)
    jurisdiction_data = metrics.get("jurisdiction_accuracy", {})
    if len(jurisdiction_data) > 1:
        j_table = Table(title="Per-Jurisdiction Accuracy")
        j_table.add_column("Jurisdiction", style="bold")
        j_table.add_column("Total", justify="right")
        j_table.add_column("Correct", justify="right")
        j_table.add_column("Accuracy", justify="right")

        for j, stats in sorted(jurisdiction_data.items()):
            j_table.add_row(
                j or "unknown",
                str(stats["total"]),
                str(stats["correct"]),
                f"{stats['accuracy']:.1%}",
            )

        console.print(j_table)


# ── Main ───────────────────────────────────────────────────


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="CaseHOLD legal holdings benchmark")
    parser.add_argument(
        "--jurisdiction",
        type=str,
        default="",
        help="Filter by jurisdiction (e.g., delaware, federal)",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        help=f"Flag answers below this confidence (default: {DEFAULT_CONFIDENCE_THRESHOLD})",
    )
    parser.add_argument(
        "--citation-audit",
        action="store_true",
        help="Verify citation grounding in report",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=0,
        help="Number of samples (0 = all available)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Model to evaluate (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Use full dataset from Neon Postgres (requires ingest)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Concurrent API workers (default: {DEFAULT_WORKERS})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Path to write results JSON",
    )
    args = parser.parse_args()

    # Load examples
    if args.full:
        console.print("[bold]Loading from Neon Postgres...[/bold]")
        examples = asyncio.run(
            load_examples_from_neon(
                jurisdiction=args.jurisdiction,
                samples=args.samples or 0,
            )
        )
    else:
        console.print("[bold]Loading from local sample...[/bold]")
        examples = load_examples_from_json(
            jurisdiction=args.jurisdiction,
            samples=args.samples if args.samples > 0 else DEFAULT_SAMPLE_SIZE,
        )

    if not examples:
        console.print("[red]No examples found. Check your filters or run ingest first.[/red]")
        sys.exit(1)

    console.print(f"Loaded {len(examples)} examples")

    # Attach jurisdiction to results for per-jurisdiction metrics
    jurisdiction_map = {ex["id"]: ex.get("jurisdiction", "") for ex in examples}

    # Run evaluation
    results = run_eval(examples, model=args.model, workers=args.workers)

    # Attach jurisdiction to results
    for r in results:
        r["jurisdiction"] = jurisdiction_map.get(r["example_id"], "")

    # Compute and print metrics
    metrics = compute_metrics(results, confidence_threshold=args.confidence_threshold)
    print_report(metrics, model=args.model)

    # Citation audit details
    if args.citation_audit:
        console.print("\n[bold]Citation Audit Details[/bold]")
        ungrounded = [r for r in results if not r["citation_grounded"]]
        if ungrounded:
            for r in ungrounded[:10]:
                console.print(f"  [red]UNGROUNDED[/red] {r['example_id']}")
                console.print(f"    Quote: {r['supporting_quote'][:100]}...")
            if len(ungrounded) > 10:
                console.print(f"  ... and {len(ungrounded) - 10} more")
        else:
            console.print("  [green]All citations grounded![/green]")

    # Persist to Neon if using full dataset
    if args.full:
        run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%S") + f"_{args.model}"
        try:
            count = asyncio.run(persist_results(run_id, results, args.model))
            console.print(f"\n[green]Persisted {count} results to Neon (run_id={run_id})[/green]")
        except Exception as e:
            console.print(f"\n[yellow]Result persistence skipped: {e}[/yellow]")

    # Write results JSON
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_data = {
            "run_id": datetime.now(UTC).isoformat(),
            "model": args.model,
            "metrics": metrics,
            "results": results,
        }
        output_path.write_text(json.dumps(output_data, indent=2, default=str) + "\n")
        console.print(f"\n[green]Results written to {output_path}[/green]")

    # Exit with non-zero if below target
    if not metrics["passes_target"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
