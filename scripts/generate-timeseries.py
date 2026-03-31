#!/usr/bin/env python3
"""Generate 2 weeks of simulated metric_values data for Atlas chart rendering.

Atlas data model alignment:
  ArrayTimeSeq(DsType, startMillis, stepMillis, Array[Double])
  - step = 60_000ms (1 minute)
  - duration = 14 days = 20_160 steps
  - Each metric has multiple tag combinations (dimensions)

Output: SQL INSERT statements for Neon metric_values table.
Usage: python scripts/generate-timeseries.py > scripts/timeseries-seed.sql
"""

import math
import random
import json
from datetime import datetime, timedelta, timezone

# ── Config ────────────────────────────────────────────────────

STEP_SECONDS = 60
DAYS = 14
TOTAL_STEPS = DAYS * 24 * 60  # 20_160

# End = midnight UTC today, Start = 14 days ago
END = datetime(2026, 3, 31, 0, 0, 0, tzinfo=timezone.utc)
START = END - timedelta(days=DAYS)

random.seed(42)  # Reproducible

# ── Metric definitions with tag combinations ──────────────────

METRICS = {
    "agentstreams.pipeline.duration": {
        "type": "timer",
        "tags_combos": [
            {"skill": "crawl-ingest", "language": "python", "stage": "extract"},
            {"skill": "crawl-ingest", "language": "python", "stage": "transform"},
            {"skill": "crawl-ingest", "language": "python", "stage": "load"},
            {"skill": "crawl-ingest", "language": "typescript", "stage": "extract"},
            {"skill": "crawl-ingest", "language": "typescript", "stage": "transform"},
            {"skill": "crawl-ingest", "language": "typescript", "stage": "load"},
            {"skill": "data-pipeline", "language": "python", "stage": "extract"},
            {"skill": "data-pipeline", "language": "python", "stage": "load"},
        ],
    },
    "agentstreams.api.requests": {
        "type": "counter",
        "tags_combos": [
            {"model": "claude-opus-4-6", "skill": "crawl-ingest", "status": "200"},
            {"model": "claude-opus-4-6", "skill": "crawl-ingest", "status": "429"},
            {"model": "claude-sonnet-4-6", "skill": "api-client", "status": "200"},
            {"model": "claude-sonnet-4-6", "skill": "api-client", "status": "429"},
            {"model": "claude-haiku-4-5-20251001", "skill": "data-pipeline", "status": "200"},
        ],
    },
    "agentstreams.api.tokens": {
        "type": "counter",
        "tags_combos": [
            {"model": "claude-opus-4-6", "skill": "crawl-ingest", "direction": "input"},
            {"model": "claude-opus-4-6", "skill": "crawl-ingest", "direction": "output"},
            {"model": "claude-sonnet-4-6", "skill": "api-client", "direction": "input"},
            {"model": "claude-sonnet-4-6", "skill": "api-client", "direction": "output"},
            {"model": "claude-haiku-4-5-20251001", "skill": "data-pipeline", "direction": "input"},
            {"model": "claude-haiku-4-5-20251001", "skill": "data-pipeline", "direction": "output"},
        ],
    },
    "agentstreams.api.cost": {
        "type": "distribution_summary",
        "tags_combos": [
            {"model": "claude-opus-4-6", "skill": "crawl-ingest"},
            {"model": "claude-sonnet-4-6", "skill": "api-client"},
            {"model": "claude-haiku-4-5-20251001", "skill": "data-pipeline"},
        ],
    },
    "agentstreams.eval.score": {
        "type": "gauge",
        "tags_combos": [
            {"skill": "crawl-ingest", "eval_suite": "crawl-ingest-extraction", "assertion_type": "contains"},
            {"skill": "crawl-ingest", "eval_suite": "crawl-ingest-extraction", "assertion_type": "cost"},
            {"skill": "crawl-ingest", "eval_suite": "crawl-ingest-extraction", "assertion_type": "is-json"},
        ],
    },
    "agentstreams.crawl.pages": {
        "type": "counter",
        "tags_combos": [
            {"domain": "docs.anthropic.com", "status": "success", "is_new": "true"},
            {"domain": "docs.anthropic.com", "status": "success", "is_new": "false"},
            {"domain": "docs.anthropic.com", "status": "error", "is_new": "true"},
            {"domain": "github.com", "status": "success", "is_new": "true"},
            {"domain": "github.com", "status": "success", "is_new": "false"},
        ],
    },
    "agentstreams.crawl.dedup": {
        "type": "gauge",
        "tags_combos": [
            {"method": "bloom"},
            {"method": "simhash"},
            {"method": "exact"},
        ],
    },
}


# ── Value generators per metric type ──────────────────────────


def hour_of_day(step: int) -> float:
    """Return fractional hour (0-24) for a given step."""
    minutes = step % (24 * 60)
    return minutes / 60.0


def daily_wave(step: int, base: float, amplitude: float) -> float:
    """Sinusoidal daily pattern peaking mid-afternoon."""
    h = hour_of_day(step)
    return base + amplitude * math.sin(math.pi * (h - 6) / 12)


def gen_counter(step: int, tags: dict) -> float:
    """Counter: rate per minute with daily cycle + noise.

    Atlas plots counters as rate, so we emit per-minute counts.
    """
    # Higher rate during business hours
    base_rate = 5.0
    if tags.get("status") == "429":
        base_rate = 0.3  # Rate-limits are rare
    elif tags.get("is_new") == "false":
        base_rate = 15.0  # Re-crawls more frequent
    elif tags.get("direction") == "output":
        base_rate = 2.0  # Output tokens less frequent

    rate = daily_wave(step, base_rate, base_rate * 0.6)
    rate = max(0, rate + random.gauss(0, base_rate * 0.1))

    # Occasional spike (1% chance)
    if random.random() < 0.01:
        rate *= random.uniform(3, 8)

    return round(rate, 2)


def gen_timer(step: int, tags: dict) -> float:
    """Timer: duration in seconds with stage-dependent baseline."""
    stage_base = {"extract": 2.5, "transform": 0.8, "load": 1.2}
    base = stage_base.get(tags.get("stage", ""), 1.0)

    # Slower at night (batch jobs)
    h = hour_of_day(step)
    if 2 <= h <= 6:
        base *= 1.5

    val = base + random.gauss(0, base * 0.2)
    # Occasional slow request
    if random.random() < 0.005:
        val *= random.uniform(5, 20)

    return round(max(0.01, val), 4)


def gen_gauge(step: int, tags: dict) -> float:
    """Gauge: instantaneous value."""
    if "method" in tags:
        # Bloom filter FPR: low baseline with drift
        bases = {"bloom": 0.02, "simhash": 0.08, "exact": 0.0}
        base = bases.get(tags["method"], 0.05)
        # Gradual drift upward over 2 weeks (bloom fills up)
        drift = (step / TOTAL_STEPS) * 0.01 if tags["method"] == "bloom" else 0
        val = base + drift + random.gauss(0, base * 0.1 + 0.001)
        return round(max(0, min(1, val)), 6)
    else:
        # Eval score: high baseline with occasional dips
        base = 0.85
        if tags.get("assertion_type") == "cost":
            base = 0.92
        elif tags.get("assertion_type") == "is-json":
            base = 0.95
        val = base + random.gauss(0, 0.03)
        # Eval runs every ~6 hours, flat between runs
        if step % 360 > 10:
            return round(max(0, min(1, val)), 4)
        # During eval run, actual measurement
        val = base + random.gauss(0, 0.05)
        return round(max(0, min(1, val)), 4)


def gen_distribution(_step: int, tags: dict) -> float:
    """Distribution summary: cost per request in USD."""
    model_costs = {
        "claude-opus-4-6": 0.075,
        "claude-sonnet-4-6": 0.015,
        "claude-haiku-4-5-20251001": 0.005,
    }
    base = model_costs.get(tags.get("model", ""), 0.02)
    val = base + random.gauss(0, base * 0.3)
    return round(max(0.001, val), 6)


GENERATORS = {
    "counter": gen_counter,
    "timer": gen_timer,
    "gauge": gen_gauge,
    "distribution_summary": gen_distribution,
}


# ── SQL generation ────────────────────────────────────────────


def escape_sql(s: str) -> str:
    return s.replace("'", "''")


def main():
    # Downsample: emit every 5 minutes instead of every 1 minute
    # to keep data volume manageable (20_160 / 5 = 4_032 per series)
    # Atlas can interpolate between points at query time
    SAMPLE_INTERVAL = 5  # every 5th step

    print("-- ═══════════════════════════════════════════════════════════")
    print("-- AgentStreams — 2-week time-series seed data")
    print(f"-- Generated: {datetime.now(timezone.utc).isoformat()}")
    print(f"-- Range: {START.isoformat()} → {END.isoformat()}")
    print(f"-- Step: {STEP_SECONDS * SAMPLE_INTERVAL}s ({SAMPLE_INTERVAL}-minute intervals)")
    print("-- Atlas alignment: ArrayTimeSeq(DsType, startMillis=..., stepMillis=300000)")
    print("-- ═══════════════════════════════════════════════════════════")
    print()
    print("-- Clear existing sample data (idempotent)")
    print("DELETE FROM metric_values;")
    print()

    total_rows = 0

    for metric_name, config in METRICS.items():
        metric_type = config["type"]
        gen = GENERATORS[metric_type]

        print(f"-- ── {metric_name} ({metric_type}) ──")
        print()

        for tags in config["tags_combos"]:
            tags_json = json.dumps(tags, sort_keys=True)
            tag_label = ", ".join(f"{k}={v}" for k, v in sorted(tags.items()))
            print(f"-- Tags: {tag_label}")

            # Batch inserts for performance (500 values per INSERT)
            batch = []
            batch_size = 500

            for step in range(0, TOTAL_STEPS, SAMPLE_INTERVAL):
                ts = START + timedelta(seconds=step * STEP_SECONDS)
                value = gen(step, tags)
                ts_str = ts.strftime("%Y-%m-%d %H:%M:%S+00")
                batch.append(
                    f"('{escape_sql(metric_name)}', {value}, "
                    f"'{escape_sql(tags_json)}', '{ts_str}')"
                )
                total_rows += 1

                if len(batch) >= batch_size:
                    print(
                        "INSERT INTO metric_values "
                        "(metric_name, value, tags, recorded_at) VALUES"
                    )
                    print(",\n".join(batch) + ";")
                    print()
                    batch = []

            if batch:
                print(
                    "INSERT INTO metric_values "
                    "(metric_name, value, tags, recorded_at) VALUES"
                )
                print(",\n".join(batch) + ";")
                print()

        print()

    print(f"-- Total rows inserted: {total_rows}")
    print(f"-- Series count: {sum(len(c['tags_combos']) for c in METRICS.values())}")
    print(
        f"-- Points per series: {TOTAL_STEPS // SAMPLE_INTERVAL} "
        f"(every {SAMPLE_INTERVAL} min over {DAYS} days)"
    )


if __name__ == "__main__":
    main()
