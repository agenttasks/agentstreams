#!/usr/bin/env python3
"""Download CaseHOLD dataset from HuggingFace.

CaseHOLD (Case Holdings On Legal Decisions):
  53K case law holdings, multiple-choice format (5 options per question).
  Evaluates precedent ranking and citation quality.
  Source: https://huggingface.co/datasets/casehold/casehold

Usage:
  uv run julia/evals/casehold/download_casehold.py
  uv run julia/evals/casehold/download_casehold.py --split test --limit 1000

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def download_casehold(split: str = "test", limit: int | None = None) -> list[dict]:
    """Download CaseHOLD from HuggingFace via direct CSV download.

    The casehold/casehold dataset uses a legacy loading script that is
    no longer supported by the datasets library. We download the CSV
    directly via huggingface_hub.
    """
    from huggingface_hub import hf_hub_download

    token = os.environ.get("HUGGINGFACE_API_TOKEN") or os.environ.get("HF_TOKEN")

    print(f"Downloading CaseHOLD dataset (split={split}) from HuggingFace...")
    csv_path = hf_hub_download(
        repo_id="casehold/casehold",
        filename=f"data/all/{split}.csv",
        repo_type="dataset",
        token=token,
    )

    # CaseHOLD CSV uses numeric column headers:
    # col 0 = citing_prompt, cols 1-5 = holding options, col 11 = label (0-4)
    # "Unnamed: 0" = example_id
    examples = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit and i >= limit:
                break

            example_id = row.get("Unnamed: 0", str(i))
            examples.append(
                {
                    "id": str(example_id),
                    "citing_prompt": row["0"],
                    "holding_0": row["1"],
                    "holding_1": row["2"],
                    "holding_2": row["3"],
                    "holding_3": row["4"],
                    "holding_4": row["5"],
                    "label": int(row["11"]),
                }
            )

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
