"""CaseHOLD dataset ingestion — HuggingFace → Neon Postgres + LanceDB.

Downloads the CaseHOLD dataset (53K+ legal holdings) from HuggingFace,
extracts jurisdiction metadata, generates hash embeddings, and persists
to Neon Postgres 18 (pgvector) and LanceDB (local vector store).

Usage:
    python -m julia.evals.casehold.ingest
    python -m julia.evals.casehold.ingest --export-sample --sample-size 100

Auth: NEON_DATABASE_URL from env (never hardcoded).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.progress import Progress

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.embeddings import EmbeddingRecord, LanceStore, hash_embedding  # noqa: E402
from src.neon_db import connection_pool  # noqa: E402

from .config import extract_jurisdiction  # noqa: E402

console = Console()

# ── HuggingFace Download ───────────────────────────────────


def download_casehold() -> list[dict]:
    """Download CaseHOLD dataset from HuggingFace.

    Downloads CSV files from casehold/casehold repo using huggingface_hub.
    The dataset uses a legacy loading script incompatible with datasets>=3.0,
    so we download the raw CSV files directly.

    CSV format: index, citing_prompt, holding_0..holding_4, score_0..score_4, label
    """
    import csv

    from huggingface_hub import hf_hub_download

    console.print("[bold]Downloading CaseHOLD from HuggingFace...[/bold]")

    splits = {
        "test": "data/all/test.csv",
        "train": "data/all/train.csv",
        "validation": "data/all/val.csv",
    }

    examples = []
    for split_name, csv_path in splits.items():
        try:
            local_path = hf_hub_download(
                "casehold/casehold", csv_path, repo_type="dataset"
            )
        except Exception as e:
            console.print(f"[yellow]Skipping {split_name}: {e}[/yellow]")
            continue

        with open(local_path) as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if len(row) < 13:
                    continue
                idx = row[0]
                citing_prompt = row[1]
                holdings = [row[2], row[3], row[4], row[5], row[6]]
                label = int(row[12])
                jurisdiction = extract_jurisdiction(citing_prompt)
                content_hash = hashlib.sha256(citing_prompt.encode()).hexdigest()

                examples.append({
                    "id": f"casehold_{split_name}_{idx}",
                    "citing_prompt": citing_prompt,
                    "holdings": holdings,
                    "label": label,
                    "jurisdiction": jurisdiction,
                    "court": "",
                    "content_hash": content_hash,
                    "split": split_name,
                })

        console.print(f"  {split_name}: {sum(1 for e in examples if e['split'] == split_name)} rows")

    console.print(f"[green]Downloaded {len(examples)} examples across all splits[/green]")
    return examples


# ── Neon Postgres Ingestion ────────────────────────────────


async def ingest_to_neon(examples: list[dict], batch_size: int = 500) -> int:
    """Ingest CaseHOLD examples into Neon Postgres with pgvector embeddings.

    Uses ON CONFLICT (id) DO NOTHING for idempotent inserts.
    Generates 384-dim hash embeddings for the citing_prompt.
    """
    count = 0
    async with connection_pool() as conn:
        with Progress(console=console) as progress:
            task = progress.add_task("Ingesting to Neon...", total=len(examples))

            for i in range(0, len(examples), batch_size):
                batch = examples[i : i + batch_size]
                for ex in batch:
                    embedding = hash_embedding(ex["citing_prompt"])
                    vec_str = "[" + ",".join(str(v) for v in embedding) + "]"
                    holdings_json = json.dumps(ex["holdings"])

                    await conn.execute(
                        """INSERT INTO casehold_examples
                           (id, citing_prompt, holdings, label, jurisdiction, court,
                            embedding, content_hash, metadata)
                           VALUES (%s, %s, %s::jsonb, %s, %s, %s,
                                   %s::vector, %s, %s::jsonb)
                           ON CONFLICT (id) DO NOTHING""",
                        (
                            ex["id"],
                            ex["citing_prompt"],
                            holdings_json,
                            ex["label"],
                            ex["jurisdiction"],
                            ex["court"],
                            vec_str,
                            ex["content_hash"],
                            json.dumps({"split": ex.get("split", "test")}),
                        ),
                    )
                    count += 1

                await conn.commit()
                progress.update(task, advance=len(batch))

    console.print(f"[green]Ingested {count} examples to Neon Postgres[/green]")
    return count


# ── LanceDB Ingestion ─────────────────────────────────────


def ingest_to_lance(examples: list[dict], db_path: str = ".lancedb") -> int:
    """Ingest CaseHOLD examples into LanceDB local vector store.

    Uses wing='evals', room='casehold' for mempalace taxonomy.
    """
    store = LanceStore(db_path=db_path, table_name="casehold", dim=384)

    records = [
        EmbeddingRecord(
            id=ex["id"],
            text=ex["citing_prompt"],
            vector=hash_embedding(ex["citing_prompt"]),
            wing="evals",
            room="casehold",
            source_url=f"hf://casehold/casehold/{ex.get('split', 'test')}",
            content_hash=ex["content_hash"],
            metadata={
                "holdings": ex["holdings"],
                "label": ex["label"],
                "jurisdiction": ex["jurisdiction"],
            },
        )
        for ex in examples
    ]

    count = store.add(records)
    console.print(f"[green]Ingested {count} examples to LanceDB ({db_path})[/green]")
    return count


# ── Sample Export ──────────────────────────────────────────


def export_sample(examples: list[dict], output_path: Path, n: int = 100) -> None:
    """Export a stratified sample of CaseHOLD examples as JSON fixture.

    Stratifies by jurisdiction to ensure coverage.
    """
    # Group by jurisdiction
    by_jurisdiction: dict[str, list[dict]] = {}
    for ex in examples:
        j = ex["jurisdiction"] or "unknown"
        by_jurisdiction.setdefault(j, []).append(ex)

    # Sample proportionally from each jurisdiction
    sample = []
    total = len(examples)
    for _jurisdiction, group in sorted(by_jurisdiction.items()):
        proportion = len(group) / total
        group_n = max(1, round(proportion * n))
        sample.extend(group[:group_n])

    # Trim or pad to exact n
    sample = sample[:n]

    # Clean for export (remove split, keep essentials)
    export = [
        {
            "id": ex["id"],
            "citing_prompt": ex["citing_prompt"],
            "holdings": ex["holdings"],
            "label": ex["label"],
            "jurisdiction": ex["jurisdiction"],
            "court": ex["court"],
        }
        for ex in sample
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(export, indent=2) + "\n")
    console.print(f"[green]Exported {len(export)} examples to {output_path}[/green]")


# ── Main ───────────────────────────────────────────────────


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="CaseHOLD dataset ingestion")
    parser.add_argument(
        "--export-sample",
        action="store_true",
        help="Export a stratified sample as JSON fixture",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=100,
        help="Number of examples in the sample (default: 100)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "julia" / "evals" / "test_data" / "casehold_sample.json",
        help="Output path for sample JSON",
    )
    parser.add_argument(
        "--skip-neon",
        action="store_true",
        help="Skip Neon Postgres ingestion",
    )
    parser.add_argument(
        "--skip-lance",
        action="store_true",
        help="Skip LanceDB ingestion",
    )
    parser.add_argument(
        "--lance-path",
        type=str,
        default=".lancedb",
        help="LanceDB database path (default: .lancedb)",
    )
    args = parser.parse_args()

    # Download dataset
    examples = download_casehold()

    # Export sample if requested
    if args.export_sample:
        export_sample(examples, args.output, args.sample_size)

    # Ingest to backends
    if not args.skip_neon:
        try:
            asyncio.run(ingest_to_neon(examples))
        except Exception as e:
            console.print(f"[yellow]Neon ingestion skipped: {e}[/yellow]")

    if not args.skip_lance:
        try:
            ingest_to_lance(examples, db_path=args.lance_path)
        except Exception as e:
            console.print(f"[yellow]LanceDB ingestion skipped: {e}[/yellow]")

    console.print("[bold green]CaseHOLD ingestion complete.[/bold green]")


if __name__ == "__main__":
    main()
