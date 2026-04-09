#!/usr/bin/env python3
"""Download CUAD dataset from HuggingFace and optionally store in Neon pgvector + LanceDB.

CUAD (Contract Understanding Atticus Dataset):
  510 contracts, 13K+ expert annotations, 41 clause types.
  Source: https://www.atticusprojectai.org/cuad

Usage:
  uv run julia/evals/cuad/download_cuad.py                    # Download only
  uv run julia/evals/cuad/download_cuad.py --store-neon        # Download + store in Neon pgvector
  uv run julia/evals/cuad/download_cuad.py --store-lancedb     # Download + store in LanceDB
  uv run julia/evals/cuad/download_cuad.py --store-all         # Download + both backends

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = Path(__file__).parent / "data"


def download_cuad() -> list[dict]:
    """Download CUAD from HuggingFace and save to local JSONL."""
    from datasets import load_dataset

    print("Downloading CUAD dataset from HuggingFace...")
    ds = load_dataset("cuad", split="test")

    # CUAD structure: context (contract text), questions (clause type queries),
    # answers (extracted spans per clause type), id, title
    contracts: dict[str, dict] = {}

    for row in ds:
        contract_id = row["id"].rsplit("_", 1)[0] if "_" in row["id"] else row["id"]
        if contract_id not in contracts:
            contracts[contract_id] = {
                "id": contract_id,
                "title": row["title"],
                "context": row["context"],
                "annotations": {},
            }

        # Each row is one question (clause type) for one contract
        question = row["question"]
        answers = row["answers"]
        answer_texts = answers["text"] if answers and "text" in answers else []
        answer_starts = answers["answer_start"] if answers and "answer_start" in answers else []

        contracts[contract_id]["annotations"][question] = {
            "texts": answer_texts,
            "starts": answer_starts,
            "found": len(answer_texts) > 0,
        }

    contract_list = list(contracts.values())
    print(f"Parsed {len(contract_list)} unique contracts")

    # Save contracts
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    contracts_path = DATA_DIR / "contracts.jsonl"
    with open(contracts_path, "w") as f:
        for contract in contract_list:
            f.write(json.dumps(contract) + "\n")
    print(f"Saved {len(contract_list)} contracts to {contracts_path}")

    # Extract and save clause types
    clause_types = set()
    for contract in contract_list:
        clause_types.update(contract["annotations"].keys())

    clause_types_list = sorted(clause_types)
    clause_types_path = DATA_DIR / "clause_types.json"
    with open(clause_types_path, "w") as f:
        json.dump(clause_types_list, f, indent=2)
    print(f"Saved {len(clause_types_list)} clause types to {clause_types_path}")

    return contract_list


async def store_in_neon(contracts: list[dict]) -> None:
    """Store contract chunks in Neon Postgres via pgvector embeddings."""
    from src.embeddings import EmbeddingPipeline, NeonVectorStore
    from src.neon_db import connection_pool

    neon_store = NeonVectorStore(dim=384)
    pipeline = EmbeddingPipeline(neon_store=neon_store, chunk_size=512)

    async with connection_pool() as conn:
        await neon_store.ensure_schema(conn)
        total_records = 0

        for i, contract in enumerate(contracts):
            records = pipeline.embed_page(
                url=f"cuad://{contract['id']}",
                content=contract["context"],
                wing="cuad",
                room=contract["id"],
            )
            count = await pipeline.store_neon(conn, records)
            total_records += count

            if (i + 1) % 50 == 0:
                await conn.commit()
                print(f"  Stored {i + 1}/{len(contracts)} contracts ({total_records} chunks)")

        await conn.commit()
        print(f"Stored {total_records} chunks in Neon pgvector")


def store_in_lancedb(contracts: list[dict]) -> None:
    """Store contract chunks in local LanceDB for hybrid search."""
    from src.embeddings import EmbeddingPipeline, LanceStore

    lance_store = LanceStore(db_path=str(DATA_DIR / ".lancedb"), table_name="cuad_contracts")
    pipeline = EmbeddingPipeline(lance_store=lance_store, chunk_size=512)

    total_records = 0
    for i, contract in enumerate(contracts):
        records = pipeline.embed_page(
            url=f"cuad://{contract['id']}",
            content=contract["context"],
            wing="cuad",
            room=contract["id"],
        )
        count = pipeline.store_local(records)
        total_records += count

        if (i + 1) % 50 == 0:
            print(f"  Stored {i + 1}/{len(contracts)} contracts ({total_records} chunks)")

    print(f"Stored {total_records} chunks in LanceDB at {DATA_DIR / '.lancedb'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download CUAD dataset")
    parser.add_argument("--store-neon", action="store_true", help="Store in Neon pgvector")
    parser.add_argument("--store-lancedb", action="store_true", help="Store in local LanceDB")
    parser.add_argument("--store-all", action="store_true", help="Store in both backends")
    args = parser.parse_args()

    contracts = download_cuad()

    if args.store_all or args.store_neon:
        asyncio.run(store_in_neon(contracts))

    if args.store_all or args.store_lancedb:
        store_in_lancedb(contracts)

    print("Done.")


if __name__ == "__main__":
    main()
