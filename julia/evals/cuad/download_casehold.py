#!/usr/bin/env python3
"""Download CaseHOLD dataset from HuggingFace.

CaseHOLD (Case Holdings On Legal Decisions):
  53K case law holdings, multiple-choice format (5 options per question).
  Evaluates precedent ranking and citation quality.
  Source: https://huggingface.co/datasets/casehold/casehold

Usage:
  uv run julia/evals/cuad/download_casehold.py
  uv run julia/evals/cuad/download_casehold.py --split test --limit 1000

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def download_casehold(split: str = "test", limit: int | None = None) -> list[dict]:
    """Download CaseHOLD from HuggingFace and save to local JSONL."""
    from datasets import load_dataset

    print(f"Downloading CaseHOLD dataset (split={split}) from HuggingFace...")
    ds = load_dataset("casehold/casehold", "all", split=split)

    examples = []
    for i, row in enumerate(ds):
        if limit and i >= limit:
            break

        examples.append({
            "id": str(row.get("example_id", i)),
            "citing_prompt": row["citing_prompt"],
            "holding_0": row["holding_0"],
            "holding_1": row["holding_1"],
            "holding_2": row["holding_2"],
            "holding_3": row["holding_3"],
            "holding_4": row["holding_4"],
            "label": row["label"],
        })

    print(f"Parsed {len(examples)} CaseHOLD examples")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / "casehold.jsonl"
    with open(output_path, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")
    print(f"Saved {len(examples)} examples to {output_path}")

    return examples


def main() -> None:
    parser = argparse.ArgumentParser(description="Download CaseHOLD dataset")
    parser.add_argument("--split", default="test", help="Dataset split (default: test)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of examples")
    args = parser.parse_args()

    download_casehold(split=args.split, limit=args.limit)
    print("Done.")


if __name__ == "__main__":
    main()
