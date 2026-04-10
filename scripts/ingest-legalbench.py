#!/usr/bin/env python3
"""Download LegalBench datasets from HuggingFace and store in Neon Postgres + LanceDB.

Pipeline:
  1. Load task registry from scripts/legalbench_tasks.json (162 tasks, 22 categories)
  2. Load dataset via HuggingFace `datasets` library (nguha/legalbench)
  3. Normalize samples into unified format (text, answer, answer_type, label_names)
  4. Chunk text + compute 384-dim hash embeddings (src/embeddings.py)
  5. Upsert into Neon Postgres (julia_legalbench_samples + julia_legalbench_embeddings)
  6. Optionally populate LanceDB local cache
  7. Write local JSON cache for offline eval runs

Requires: `uv sync --extra lexglue` (installs `datasets>=3.0`)
Schema:  `julia/evals/legalbench_schema.sql` must be applied first.
Auth:    CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).

Usage:
  uv run --extra lexglue scripts/ingest-legalbench.py --task all
  uv run --extra lexglue scripts/ingest-legalbench.py --category contract_nli --limit 50
  uv run --extra lexglue scripts/ingest-legalbench.py --task abercrombie --lance
  uv run --extra lexglue scripts/ingest-legalbench.py --list-tasks
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.embeddings import chunk_text, hash_embedding  # noqa: E402

# ---------------------------------------------------------------------------
# Task registry (loaded from JSON, not hardcoded — 162 tasks is too many)
# ---------------------------------------------------------------------------

TASK_REGISTRY_PATH = PROJECT_ROOT / "scripts" / "legalbench_tasks.json"
TASK_REGISTRY: dict[str, dict] = json.loads(TASK_REGISTRY_PATH.read_text())

CATEGORY_MAP: dict[str, list[str]] = {}
for _task_name, _cfg in TASK_REGISTRY.items():
    CATEGORY_MAP.setdefault(_cfg["category"], []).append(_task_name)

ALL_TASKS = sorted(TASK_REGISTRY.keys())
ALL_CATEGORIES = sorted(CATEGORY_MAP.keys())

# ---------------------------------------------------------------------------
# JSON cache directory
# ---------------------------------------------------------------------------

DATA_DIR = PROJECT_ROOT / "julia" / "evals" / "test_data" / "legalbench"


# ---------------------------------------------------------------------------
# HuggingFace loading
# ---------------------------------------------------------------------------


def load_hf_dataset(task: str, split: str, limit: int) -> list[dict]:
    """Load a LegalBench task from HuggingFace and normalize to unified format."""
    from datasets import load_dataset

    config = TASK_REGISTRY[task]

    try:
        ds = load_dataset("nguha/legalbench", config["hf_config"], split=split)
    except Exception:
        if split == "test":
            print(f"  [warn] No '{split}' split for {task}, trying 'train'", file=sys.stderr)
            ds = load_dataset("nguha/legalbench", config["hf_config"], split="train")
        else:
            raise

    samples = []
    for i, row in enumerate(ds):
        if limit and i >= limit:
            break

        # Combine text fields into unified text
        text_parts = []
        metadata: dict = {}
        for field in config["text_fields"]:
            val = row.get(field, "")
            if val:
                text_parts.append(str(val))
                metadata[field] = str(val)

        text = "\n".join(text_parts) if text_parts else str(row.get("text", ""))

        # Build context from additional fields not in text_fields
        context_parts = []
        skip_fields = set(config["text_fields"]) | {"index", "answer", "label", "Unnamed: 0"}
        for col in ds.column_names:
            if col not in skip_fields and col not in config.get("choice_fields", []):
                val = row.get(col, "")
                if val and str(val) not in text_parts:
                    context_parts.append(f"{col}: {val}")

        context = "\n".join(context_parts) if context_parts else None

        # Handle choice fields (scalr-type multiple choice)
        if "choice_fields" in config:
            choices = []
            for cf in config["choice_fields"]:
                choices.append(str(row.get(cf, "")))
            metadata["choices"] = choices

        # Get answer
        answer_field = config["answer_field"]
        answer = str(row.get(answer_field, ""))

        sample = {
            "task": task,
            "category": config["category"],
            "hf_index": i,
            "text": text,
            "context": context,
            "answer": answer,
            "answer_type": config["answer_type"],
            "label_names": config.get("label_names", []),
            "split": split,
            "metadata": metadata,
            "content_hash": hashlib.sha256(text.encode()).hexdigest()[:32],
        }
        samples.append(sample)

    return samples


# ---------------------------------------------------------------------------
# Neon Postgres storage
# ---------------------------------------------------------------------------


async def store_neon(samples: list[dict], skip_embeddings: bool = False) -> int:
    """Store samples and embeddings in Neon Postgres."""
    from src.neon_db import connection_pool

    count = 0
    async with connection_pool() as conn:
        for sample in samples:
            row = await (
                await conn.execute(
                    """INSERT INTO julia_legalbench_samples
                       (id, task, category, hf_index, text, context, answer,
                        answer_type, label_names, split, metadata, content_hash, token_count)
                       VALUES (gen_random_uuid()::text, %s, %s, %s, %s, %s, %s,
                               %s, %s, %s, %s, %s, %s)
                       ON CONFLICT (task, hf_index, split) DO UPDATE SET
                           text = EXCLUDED.text,
                           answer = EXCLUDED.answer,
                           context = EXCLUDED.context
                       RETURNING id""",
                    (
                        sample["task"],
                        sample["category"],
                        sample["hf_index"],
                        sample["text"],
                        sample.get("context"),
                        sample.get("answer"),
                        sample["answer_type"],
                        json.dumps(sample.get("label_names", [])),
                        sample["split"],
                        json.dumps(sample.get("metadata", {})),
                        sample["content_hash"],
                        len(sample["text"].split()),  # approximate token count
                    ),
                )
            ).fetchone()

            if not skip_embeddings and row:
                sample_id = row[0]
                chunks = chunk_text(sample["text"], chunk_size=512, overlap=64)
                for chunk in chunks:
                    vec = hash_embedding(chunk["text"], dim=384)
                    vec_str = "[" + ",".join(str(v) for v in vec) + "]"
                    chunk_hash = hashlib.sha256(chunk["text"].encode()).hexdigest()[:32]

                    await conn.execute(
                        """INSERT INTO julia_legalbench_embeddings
                           (id, sample_id, chunk_index, content, content_hash,
                            embedding, token_count, metadata)
                           VALUES (gen_random_uuid()::text, %s, %s, %s, %s,
                                   %s::vector, %s, %s)
                           ON CONFLICT (sample_id, chunk_index) DO UPDATE SET
                               content = EXCLUDED.content,
                               embedding = EXCLUDED.embedding""",
                        (
                            sample_id,
                            chunk["index"],
                            chunk["text"],
                            chunk_hash,
                            vec_str,
                            len(chunk["text"].split()),
                            json.dumps({}),
                        ),
                    )

            count += 1

        await conn.commit()

    return count


# ---------------------------------------------------------------------------
# LanceDB storage (optional)
# ---------------------------------------------------------------------------


def store_lance(samples: list[dict]) -> int:
    """Store embeddings in LanceDB local cache (follows ingest-lexglue.py pattern)."""
    try:
        from src.embeddings import EmbeddingRecord, LanceStore
    except ImportError:
        print("  [skip] LanceDB not installed (uv sync --extra vector)", file=sys.stderr)
        return 0

    store = LanceStore(db_path=PROJECT_ROOT / ".lancedb" / "legalbench", table_name="legalbench")
    count = 0
    for sample in samples:
        chunks = chunk_text(sample["text"], chunk_size=512, overlap=64)
        for chunk in chunks:
            vec = hash_embedding(chunk["text"], dim=384)
            record = EmbeddingRecord(
                id=f"{sample['task']}_{sample['hf_index']}_{chunk['index']}",
                text=chunk["text"],
                vector=vec,
                metadata={
                    "task": sample["task"],
                    "category": sample["category"],
                    "hf_index": sample["hf_index"],
                },
                wing="legalbench",
                room=sample["task"],
                content_hash=hashlib.sha256(chunk["text"].encode()).hexdigest()[:32],
            )
            store.add(record)
            count += 1

    return count


# ---------------------------------------------------------------------------
# JSON cache storage
# ---------------------------------------------------------------------------


def store_json(task: str, samples: list[dict]) -> Path:
    """Write samples to local JSON cache for offline eval runs."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    json_path = DATA_DIR / f"{task}_samples.json"
    json_path.write_text(json.dumps(samples, indent=2, default=str))
    return json_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Download LegalBench from HuggingFace → Neon + local JSON"
    )
    parser.add_argument(
        "--task",
        default="all",
        help="Task name or 'all' (default: all)",
    )
    parser.add_argument(
        "--category",
        default="",
        help="Filter by category (e.g., contract_nli, cuad, maud)",
    )
    parser.add_argument(
        "--split",
        default="test",
        help="Dataset split (default: test)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit samples per task (0=all)",
    )
    parser.add_argument(
        "--lance",
        action="store_true",
        help="Also store in LanceDB local cache",
    )
    parser.add_argument(
        "--skip-embeddings",
        action="store_true",
        help="Skip pgvector embedding computation",
    )
    parser.add_argument(
        "--skip-neon",
        action="store_true",
        help="Skip Neon Postgres storage (JSON only)",
    )
    parser.add_argument(
        "--list-tasks",
        action="store_true",
        help="List all tasks and categories, then exit",
    )
    args = parser.parse_args()

    # List tasks mode
    if args.list_tasks:
        print(
            f"\nLegalBench Task Registry ({len(ALL_TASKS)} tasks, {len(ALL_CATEGORIES)} categories)\n"
        )
        for cat in ALL_CATEGORIES:
            tasks = CATEGORY_MAP[cat]
            print(f"  {cat} ({len(tasks)} tasks):")
            for t in sorted(tasks):
                cfg = TASK_REGISTRY[t]
                print(f"    {t:<55} {cfg['answer_type']:<20} {cfg['test_size']:>5} samples")
            print()
        return

    # Determine which tasks to ingest
    if args.category:
        if args.category not in CATEGORY_MAP:
            print(f"Unknown category: {args.category}", file=sys.stderr)
            print(f"Valid categories: {', '.join(ALL_CATEGORIES)}", file=sys.stderr)
            sys.exit(1)
        tasks_to_ingest = sorted(CATEGORY_MAP[args.category])
    elif args.task == "all":
        tasks_to_ingest = ALL_TASKS
    else:
        if args.task not in TASK_REGISTRY:
            print(f"Unknown task: {args.task}", file=sys.stderr)
            sys.exit(1)
        tasks_to_ingest = [args.task]

    print(f"\n  Ingesting {len(tasks_to_ingest)} tasks", file=sys.stderr)
    print(f"  Split: {args.split}", file=sys.stderr)
    print(f"  Limit: {args.limit or 'all'}", file=sys.stderr)
    print(f"  Neon: {'skip' if args.skip_neon else 'yes'}", file=sys.stderr)
    print(f"  LanceDB: {'yes' if args.lance else 'no'}", file=sys.stderr)

    total_samples = 0
    total_neon = 0
    total_lance = 0

    for task_name in tasks_to_ingest:
        print(f"\n  [{task_name}] Loading from HuggingFace...", file=sys.stderr)

        try:
            samples = load_hf_dataset(task_name, args.split, args.limit)
        except Exception as e:
            print(f"  [{task_name}] ERROR: {e}", file=sys.stderr)
            continue

        print(f"  [{task_name}] {len(samples)} samples loaded", file=sys.stderr)
        total_samples += len(samples)

        # Store JSON (always)
        json_path = store_json(task_name, samples)
        print(f"  [{task_name}] JSON → {json_path}", file=sys.stderr)

        # Store Neon (unless skipped)
        if not args.skip_neon and samples:
            try:
                neon_count = asyncio.run(store_neon(samples, skip_embeddings=args.skip_embeddings))
                total_neon += neon_count
                print(f"  [{task_name}] Neon → {neon_count} rows", file=sys.stderr)
            except Exception as e:
                print(f"  [{task_name}] Neon ERROR: {e}", file=sys.stderr)

        # Store LanceDB (if requested)
        if args.lance and samples:
            lance_count = store_lance(samples)
            total_lance += lance_count
            if lance_count:
                print(f"  [{task_name}] LanceDB → {lance_count} chunks", file=sys.stderr)

    # Summary
    print("\n  Summary:", file=sys.stderr)
    print(f"    Tasks: {len(tasks_to_ingest)}", file=sys.stderr)
    print(f"    Samples: {total_samples}", file=sys.stderr)
    print(f"    Neon rows: {total_neon}", file=sys.stderr)
    if args.lance:
        print(f"    LanceDB chunks: {total_lance}", file=sys.stderr)


if __name__ == "__main__":
    main()
