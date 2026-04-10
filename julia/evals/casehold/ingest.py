"""CaseHOLD dataset ingestion — HuggingFace → Neon Postgres + LanceDB.

Downloads the CaseHOLD dataset (53K+ legal holdings) from HuggingFace,
extracts jurisdiction metadata, generates hash embeddings, and persists
to Neon Postgres 18 (pgvector) and LanceDB (local vector store).

Supports two Neon ingestion modes:
  - psycopg (default): async connection via NEON_DATABASE_URL
  - HTTP SQL API (--http): batch multi-row INSERT via Neon pooler HTTP endpoint,
    useful when direct Postgres connections are unavailable (e.g., in sandboxed envs).
    Batches 100 rows per HTTP request (53K rows = ~530 requests = ~2 min).

Usage:
    python -m julia.evals.casehold.ingest
    python -m julia.evals.casehold.ingest --http             # HTTP SQL API mode
    python -m julia.evals.casehold.ingest --export-sample --sample-size 100

Auth: NEON_DATABASE_URL from env (never hardcoded).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
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
            local_path = hf_hub_download("casehold/casehold", csv_path, repo_type="dataset")
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

                examples.append(
                    {
                        "id": f"casehold_{split_name}_{idx}",
                        "citing_prompt": citing_prompt,
                        "holdings": holdings,
                        "label": label,
                        "jurisdiction": jurisdiction,
                        "court": "",
                        "content_hash": content_hash,
                        "split": split_name,
                    }
                )

        console.print(
            f"  {split_name}: {sum(1 for e in examples if e['split'] == split_name)} rows"
        )

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


# ── Neon HTTP SQL Batch Ingestion ──────────────────────────


def _get_neon_http_config() -> tuple[str, dict[str, str]]:
    """Build Neon HTTP SQL API endpoint and headers from project env vars.

    Precedence:
    1. NEON_HTTP_HOST + NEON_HTTP_CONN (CLAUDE.md standard)
    2. NEON_DATABASE_URL (CLAUDE.md standard, parsed for host)
    3. DATABASE_URL (non-standard fallback for CI/sandboxed envs)
    """
    http_host = os.environ.get("NEON_HTTP_HOST")
    http_conn = os.environ.get("NEON_HTTP_CONN")

    if http_host and http_conn:
        url = f"https://{http_host}/sql"
        headers = {
            "Neon-Connection-String": http_conn,
            "Content-Type": "application/json",
        }
        return url, headers

    # Fallback: parse host from connection string
    db_url = os.environ.get("NEON_DATABASE_URL") or os.environ.get("DATABASE_URL", "")
    if not db_url:
        raise ValueError("Set NEON_HTTP_HOST + NEON_HTTP_CONN, or NEON_DATABASE_URL")

    match = re.search(r"@([\w.-]+)", db_url)
    if not match:
        raise ValueError(f"Cannot extract host from: {db_url[:40]}...")
    host = match.group(1)

    url = f"https://{host}/sql"
    headers = {
        "Neon-Connection-String": db_url,
        "Content-Type": "application/json",
    }
    return url, headers


def ingest_to_neon_http(examples: list[dict], batch_size: int = 100) -> int:
    """Ingest via Neon HTTP SQL API with multi-row INSERT batches.

    Constructs multi-row VALUES clauses (batch_size rows per HTTP request).
    53K rows at batch_size=100 = ~530 HTTP calls = ~2 minutes.
    Idempotent via ON CONFLICT (id) DO NOTHING.
    """
    import httpx

    url, headers = _get_neon_http_config()
    count = 0
    errors = 0

    with Progress(console=console) as progress:
        task = progress.add_task("Ingesting to Neon (HTTP)...", total=len(examples))

        for i in range(0, len(examples), batch_size):
            batch = examples[i : i + batch_size]

            # Build multi-row VALUES with positional params ($1, $2, ...)
            # 9 columns per row
            values_clauses = []
            params: list = []
            for j, ex in enumerate(batch):
                embedding = hash_embedding(ex["citing_prompt"])
                vec_str = "[" + ",".join(str(v) for v in embedding) + "]"
                offset = j * 9
                values_clauses.append(
                    f"(${offset + 1}, ${offset + 2}, ${offset + 3}::jsonb, ${offset + 4}, "
                    f"${offset + 5}, ${offset + 6}, ${offset + 7}::vector, ${offset + 8}, "
                    f"${offset + 9}::jsonb)"
                )
                params.extend(
                    [
                        ex["id"],
                        ex["citing_prompt"],
                        json.dumps(ex["holdings"]),
                        ex["label"],
                        ex["jurisdiction"],
                        ex.get("court", ""),
                        vec_str,
                        ex["content_hash"],
                        json.dumps({"split": ex.get("split", "test")}),
                    ]
                )

            query = (
                "INSERT INTO casehold_examples "
                "(id, citing_prompt, holdings, label, jurisdiction, court, "
                "embedding, content_hash, metadata) VALUES "
                + ", ".join(values_clauses)
                + " ON CONFLICT (id) DO NOTHING"
            )

            body = json.dumps({"query": query, "params": params})
            try:
                resp = httpx.post(url, headers=headers, content=body, timeout=60)
                if resp.status_code == 200:
                    count += len(batch)
                else:
                    errors += 1
                    if errors <= 3:
                        err = json.loads(resp.text).get("message", resp.text[:100])
                        console.print(f"  [red]Batch error: {err}[/red]")
            except httpx.TimeoutException:
                errors += 1
                if errors <= 3:
                    console.print(f"  [red]Batch timeout at row {i}[/red]")

            progress.update(task, advance=len(batch))

    console.print(
        f"[green]Ingested {count} examples to Neon via HTTP ({errors} batch errors)[/green]"
    )
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
        "--http",
        action="store_true",
        help="Use Neon HTTP SQL API for batch ingestion (no direct Postgres needed)",
    )
    parser.add_argument(
        "--http-batch-size",
        type=int,
        default=100,
        help="Rows per HTTP request when using --http (default: 100)",
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
        if args.http:
            try:
                ingest_to_neon_http(examples, batch_size=args.http_batch_size)
            except Exception as e:
                console.print(f"[yellow]Neon HTTP ingestion failed: {e}[/yellow]")
        else:
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
