#!/usr/bin/env python3
"""Unified quality pipeline runner for agentstreams.

Orchestrates the full crawl → extract → validate → security-audit chain
with caching so repeated runs skip expensive crawl steps.

Stages:
  1. crawl    — Fetch sitemap pages into taxonomy markdown (cached)
  2. extract  — Extract patterns from taxonomy into JSONL (cached)
  3. validate — Cross-reference patterns against skill files
  4. security — Run static security audit on codebase
  5. report   — Emit unified summary

Usage:
  uv run scripts/run-pipeline.py                     # Full pipeline
  uv run scripts/run-pipeline.py --skip-crawl        # Use cached taxonomy
  uv run scripts/run-pipeline.py --stages validate security  # Specific stages
  uv run scripts/run-pipeline.py --check-only        # Exit 1 on failures
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
TAXONOMY_DIR = PROJECT_ROOT / "taxonomy"
SKILLS_DIR = PROJECT_ROOT / "skills"
PATTERNS_DIR = PROJECT_ROOT / ".pipeline"

# Default crawl targets
CRAWL_TARGETS = [
    {
        "name": "platform-claude-com",
        "sitemap": "https://platform.claude.com/sitemap.xml",
        "taxonomy": "taxonomy/platform-claude-com-full.md",
        "max_pages": 2000,
    },
    {
        "name": "code-claude-com",
        "sitemap": "https://code.claude.com/docs/sitemap.xml",
        "taxonomy": "taxonomy/code-claude-com-full.md",
        "max_pages": 1000,
    },
]

ALL_STAGES = ["crawl", "extract", "validate", "security", "prompts"]


# ── Stage runners ─────────────────────────────────────────


def run_command(cmd: list[str], description: str) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    print(f"  → {description}...", file=sys.stderr)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(PROJECT_ROOT),
        )
        output = result.stdout + result.stderr
        if result.returncode != 0:
            return False, output
        return True, output
    except subprocess.TimeoutExpired:
        return False, "Command timed out (600s)"
    except FileNotFoundError as e:
        return False, f"Command not found: {e}"


def is_fresh(path: Path, max_age_hours: int = 24) -> bool:
    """Check if a file exists and was modified within max_age_hours."""
    if not path.exists():
        return False
    age_seconds = time.time() - path.stat().st_mtime
    return age_seconds < max_age_hours * 3600


def stage_crawl(skip: bool = False) -> tuple[bool, list[str]]:
    """Stage 1: Crawl sitemaps into taxonomy files."""
    messages = []
    all_ok = True

    for target in CRAWL_TARGETS:
        taxonomy_path = PROJECT_ROOT / target["taxonomy"]

        if skip or is_fresh(taxonomy_path):
            age = ""
            if taxonomy_path.exists():
                hours = (time.time() - taxonomy_path.stat().st_mtime) / 3600
                age = f" ({hours:.0f}h old)"
            messages.append(f"  ✓ {target['name']}: cached{age}")
            continue

        ok, output = run_command(
            [
                "uv",
                "run",
                str(SCRIPTS_DIR / "crawl-sitemap.py"),
                target["sitemap"],
                target["taxonomy"],
                "--max-pages",
                str(target["max_pages"]),
                "--concurrency",
                "20",
            ],
            f"Crawling {target['name']}",
        )

        if ok:
            messages.append(f"  ✓ {target['name']}: crawled")
        else:
            all_ok = False
            messages.append(f"  ✗ {target['name']}: FAILED")
            messages.append(f"    {output[:200]}")

    return all_ok, messages


def stage_extract() -> tuple[bool, list[str]]:
    """Stage 2: Extract patterns from taxonomy files."""
    messages = []
    all_ok = True

    PATTERNS_DIR.mkdir(exist_ok=True)

    for target in CRAWL_TARGETS:
        taxonomy_path = PROJECT_ROOT / target["taxonomy"]
        patterns_path = PATTERNS_DIR / f"{target['name']}.jsonl"

        if not taxonomy_path.exists():
            messages.append(f"  ⊘ {target['name']}: no taxonomy file, skipping")
            continue

        if (
            is_fresh(patterns_path)
            and patterns_path.stat().st_mtime > taxonomy_path.stat().st_mtime
        ):
            messages.append(f"  ✓ {target['name']}: patterns cached")
            continue

        ok, output = run_command(
            [
                "uv",
                "run",
                str(SCRIPTS_DIR / "extract-patterns.py"),
                str(taxonomy_path),
                "--en-only",
                "-o",
                str(patterns_path),
            ],
            f"Extracting patterns from {target['name']}",
        )

        if ok:
            messages.append(f"  ✓ {target['name']}: extracted")
        else:
            all_ok = False
            messages.append(f"  ✗ {target['name']}: FAILED")

    return all_ok, messages


def stage_validate() -> tuple[bool, list[str]]:
    """Stage 3: Validate skills against patterns."""
    messages = []
    all_ok = True

    if not SKILLS_DIR.exists():
        messages.append("  ⊘ No skills/ directory, skipping")
        return True, messages

    # Use the largest patterns file available
    pattern_files = sorted(
        PATTERNS_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_size, reverse=True
    )
    if not pattern_files:
        messages.append("  ⊘ No pattern files, skipping (run extract first)")
        return True, messages

    ok, output = run_command(
        [
            "uv",
            "run",
            str(SCRIPTS_DIR / "validate-patterns.py"),
            str(pattern_files[0]),
            str(SKILLS_DIR),
        ],
        "Validating skills against patterns",
    )

    if ok:
        # Count findings from output
        actionable = output.count("MEDIUM") + output.count("HIGH")
        messages.append(f"  ✓ Skills validated ({actionable} actionable findings)")
    else:
        all_ok = False
        messages.append("  ✗ Validation FAILED")

    # Include the output summary
    for line in output.splitlines():
        if any(kw in line for kw in ["Total:", "INFO", "LOW", "MEDIUM", "HIGH"]):
            messages.append(f"    {line.strip()}")

    return all_ok, messages


def stage_security() -> tuple[bool, list[str]]:
    """Stage 4: Run security audit."""
    messages = []

    ok, output = run_command(
        [
            "uv",
            "run",
            str(SCRIPTS_DIR / "security-audit.py"),
            "--check-only",
            "--paths",
            "scripts/",
            ".claude/",
        ],
        "Running security audit",
    )

    if ok:
        messages.append("  ✓ Security audit passed")
    else:
        messages.append("  ✗ Security audit FAILED")
        for line in output.splitlines():
            if "CRITICAL" in line or "HIGH" in line:
                messages.append(f"    {line.strip()}")

    return ok, messages


def stage_prompts() -> tuple[bool, list[str]]:
    """Stage 5: Validate agentic prompt integrations."""
    messages = []

    # Check that prompt sources exist
    ok_sources, output_sources = run_command(
        [
            "uv",
            "run",
            str(SCRIPTS_DIR / "render_prompts.py"),
            "--validate",
        ],
        "Validating prompt source files",
    )

    if ok_sources:
        messages.append(f"  ✓ Prompt sources: {output_sources.strip()}")
    else:
        messages.append("  ✗ Prompt sources FAILED")
        return False, messages

    # Check that all integration points exist
    ok_integrations, output_integrations = run_command(
        [
            "uv",
            "run",
            str(SCRIPTS_DIR / "apply_prompts.py"),
            "--check",
        ],
        "Validating prompt integrations",
    )

    if ok_integrations:
        messages.append(f"  ✓ Integrations: {output_integrations.strip()}")
    else:
        messages.append("  ✗ Integration check FAILED")
        for line in output_integrations.splitlines():
            if "ERROR" in line:
                messages.append(f"    {line.strip()}")
        return False, messages

    return True, messages


# ── Pipeline orchestrator ─────────────────────────────────

STAGE_RUNNERS = {
    "crawl": stage_crawl,
    "extract": stage_extract,
    "validate": stage_validate,
    "security": stage_security,
    "prompts": stage_prompts,
}


def run_pipeline(
    stages: list[str],
    skip_crawl: bool = False,
    check_only: bool = False,
) -> tuple[bool, dict[str, tuple[bool, list[str]]]]:
    """Run selected pipeline stages. Returns (all_ok, stage_results)."""
    results: dict[str, tuple[bool, list[str]]] = {}
    all_ok = True

    for stage in stages:
        runner = STAGE_RUNNERS.get(stage)
        if not runner:
            results[stage] = (False, [f"  ✗ Unknown stage: {stage}"])
            all_ok = False
            continue

        start = time.time()
        if stage == "crawl":
            ok, messages = runner(skip=skip_crawl)
        else:
            ok, messages = runner()
        elapsed = time.time() - start

        messages.append(f"  ⏱ {elapsed:.1f}s")
        results[stage] = (ok, messages)
        if not ok:
            all_ok = False

    return all_ok, results


def print_pipeline_report(results: dict[str, tuple[bool, list[str]]]) -> None:
    """Print unified pipeline report."""
    print(f"\n{'=' * 60}", file=sys.stderr)
    print("AgentStreams Quality Pipeline", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    for stage, (ok, messages) in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"\n[{status}] {stage.upper()}", file=sys.stderr)
        for msg in messages:
            print(msg, file=sys.stderr)

    all_ok = all(ok for ok, _ in results.values())
    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"Pipeline: {'PASS' if all_ok else 'FAIL'}", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)


# ── Main ─────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Unified quality pipeline runner")
    parser.add_argument(
        "--stages",
        nargs="*",
        default=ALL_STAGES,
        choices=ALL_STAGES,
        help="Stages to run (default: all)",
    )
    parser.add_argument("--skip-crawl", action="store_true", help="Use cached taxonomy files")
    parser.add_argument("--check-only", action="store_true", help="Exit 1 on any failure")
    args = parser.parse_args()

    all_ok, results = run_pipeline(args.stages, args.skip_crawl, args.check_only)
    print_pipeline_report(results)

    if args.check_only and not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
