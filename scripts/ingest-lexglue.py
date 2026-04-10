#!/usr/bin/env python3
"""Download LexGLUE datasets from HuggingFace and store in Neon Postgres + LanceDB.

Pipeline:
  1. Load dataset via HuggingFace `datasets` library
  2. Normalize samples into unified format (text, label(s), label_set)
  3. Chunk text + compute 384-dim hash embeddings (src/embeddings.py)
  4. Upsert into Neon Postgres (julia_lexglue_samples + julia_lexglue_embeddings)
  5. Optionally populate LanceDB local cache
  6. Write local JSON cache for offline eval runs

Requires: `uv sync --extra lexglue` (installs `datasets>=2.14.0`)
Schema:  `julia/evals/lexglue_schema.sql` must be applied first.
Auth:    CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).

Usage:
  uv run --extra lexglue scripts/ingest-lexglue.py --task all
  uv run --extra lexglue scripts/ingest-lexglue.py --task casehold --limit 50
  uv run --extra lexglue scripts/ingest-lexglue.py --task ledgar --lance
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
# LexGLUE task configs
# ---------------------------------------------------------------------------

TASK_CONFIGS = {
    "ledgar": {
        "hf_name": "ledgar",
        "label_type": "single",
        "label_field": "label",
        "text_field": "text",
        "label_names": [
            "Adjustments",
            "Agreements",
            "Amendments",
            "Anti-Dilution",
            "Applicable Laws",
            "Approvals",
            "Arbitration",
            "Assignments",
            "Audits",
            "Base Salary",
            "Benefits",
            "Board Composition",
            "Brokers",
            "Buy-Sell",
            "Capitalization",
            "Change of Control",
            "Closing Conditions",
            "Closings",
            "Compliance",
            "Conditions Precedent",
            "Confidential Information",
            "Confidentiality",
            "Consent",
            "Consideration",
            "Cooperation",
            "Costs",
            "Counterparts",
            "Covenants",
            "Definitions",
            "Deliveries",
            "Directors",
            "Disclosure",
            "Dispute Resolution",
            "Distributions",
            "Dividends",
            "Due Diligence",
            "Duration",
            "Effectiveness",
            "Employment",
            "Entire Agreement",
            "Equity",
            "Events of Default",
            "Exclusivity",
            "Execution",
            "Exercise",
            "Exhibits",
            "Expenses",
            "Fees",
            "Force Majeure",
            "Further Assurances",
            "General",
            "Governing Law",
            "Guarantees",
            "Headings",
            "Indemnification",
            "Insurance",
            "Integration",
            "Interest Rate",
            "Intellectual Property",
            "Interpretation",
            "Jurisdictions",
            "Landlord",
            "Leases",
            "Liability",
            "Limitations",
            "Loans",
            "Maintenance",
            "Management",
            "Merger",
            "Modifications",
            "No Conflicts",
            "No Waiver",
            "Non-Competition",
            "Non-Disparagement",
            "Non-Solicitation",
            "Notices",
            "Options",
            "Ownership",
            "Parties",
            "Payments",
            "Permits",
            "Pricing",
            "Procedures",
            "Property",
            "Purchase",
            "Redemption",
            "Registration Rights",
            "Reimbursement",
            "Remedies",
            "Renewal",
            "Rent",
            "Representations",
            "Resignation",
            "Restrictions",
            "Returns",
            "Schedules",
            "Security",
            "Severability",
            "Stock Options",
            "Successors",
            "Tax",
            "Termination",
            "Terms",
            "Title",
            "Transfers",
            "Voting",
            "Waiver",
            "Warranties",
        ],
    },
    "unfair_tos": {
        "hf_name": "unfair_tos",
        "label_type": "multi",
        "label_field": "labels",
        "text_field": "text",
        "label_names": [
            "limitation_of_liability",
            "unilateral_termination",
            "unilateral_change",
            "content_removal",
            "jurisdiction",
            "choice_of_law",
            "arbitration",
            "contract_by_using",
        ],
    },
    "scotus": {
        "hf_name": "scotus",
        "label_type": "single",
        "label_field": "label",
        "text_field": "text",
        "label_names": [
            "Criminal Procedure",
            "Civil Rights",
            "First Amendment",
            "Due Process",
            "Privacy",
            "Attorneys",
            "Unions",
            "Economic Activity",
            "Judicial Power",
            "Federalism",
            "Interstate Relations",
            "Federal Taxation",
            "Miscellaneous",
            "Private Action",
        ],
    },
    "ecthr_a": {
        "hf_name": "ecthr_a",
        "label_type": "multi",
        "label_field": "labels",
        "text_field": "text",
        "label_names": [
            "2",
            "3",
            "5",
            "6",
            "8",
            "9",
            "10",
            "11",
            "13",
            "14",
            "P1-1",
        ],
    },
    "casehold": {
        "hf_name": "case_hold",
        "label_type": "single",
        "label_field": "label",
        "text_field": "context",
        "holdings_field": "endings",
        "label_names": ["0", "1", "2", "3", "4"],
    },
    "contract_nli": {
        "hf_dataset": "kiddothe2b/contract-nli",
        "hf_name": "contractnli_a",
        "label_type": "single",
        "label_field": "label",
        "text_field": "premise",
        "hypothesis_field": "hypothesis",
        "label_names": ["contradiction", "entailment", "neutral"],
    },
    "ecthr_b": {
        "hf_name": "ecthr_b",
        "label_type": "multi",
        "label_field": "labels",
        "text_field": "text",
        "label_names": [
            "2",
            "3",
            "5",
            "6",
            "8",
            "9",
            "10",
            "11",
            "14",
            "P1-1",
        ],
    },
    "eurlex": {
        "hf_name": "eurlex",
        "label_type": "multi",
        "label_field": "labels",
        "text_field": "text",
        "label_names": [
            "100163",
            "100168",
            "100169",
            "100170",
            "100171",
            "100172",
            "100173",
            "100174",
            "100175",
            "100176",
            "100177",
            "100179",
            "100180",
            "100183",
            "100184",
            "100185",
            "100186",
            "100187",
            "100189",
            "100190",
            "100191",
            "100192",
            "100193",
            "100194",
            "100195",
            "100196",
            "100197",
            "100198",
            "100199",
            "100200",
            "100201",
            "100202",
            "100204",
            "100205",
            "100206",
            "100207",
            "100212",
            "100214",
            "100215",
            "100220",
            "100221",
            "100222",
            "100223",
            "100224",
            "100226",
            "100227",
            "100229",
            "100230",
            "100231",
            "100232",
            "100233",
            "100234",
            "100235",
            "100237",
            "100238",
            "100239",
            "100240",
            "100241",
            "100242",
            "100243",
            "100244",
            "100245",
            "100246",
            "100247",
            "100248",
            "100249",
            "100250",
            "100252",
            "100253",
            "100254",
            "100255",
            "100256",
            "100257",
            "100258",
            "100259",
            "100260",
            "100261",
            "100262",
            "100263",
            "100264",
            "100265",
            "100266",
            "100268",
            "100269",
            "100270",
            "100271",
            "100272",
            "100273",
            "100274",
            "100275",
            "100276",
            "100277",
            "100278",
            "100279",
            "100280",
            "100281",
            "100282",
            "100283",
            "100284",
            "100285",
        ],
    },
}

ALL_TASKS = list(TASK_CONFIGS.keys())


# ---------------------------------------------------------------------------
# HuggingFace loading
# ---------------------------------------------------------------------------


def load_hf_dataset(task: str, split: str, limit: int) -> list[dict]:
    """Load a LexGLUE task from HuggingFace and normalize to unified format."""
    from datasets import load_dataset

    config = TASK_CONFIGS[task]
    hf_dataset = config.get("hf_dataset", "lex_glue")
    hf_name = config["hf_name"]
    try:
        ds = load_dataset(hf_dataset, hf_name, split=split)
    except Exception:
        # Some datasets may not have test split — try validation
        if split == "test":
            print(f"  [warn] No '{split}' split for {task}, trying 'validation'", file=sys.stderr)
            ds = load_dataset(hf_dataset, hf_name, split="validation")
        else:
            raise

    samples = []
    for i, row in enumerate(ds):
        if limit and i >= limit:
            break

        text = row[config["text_field"]]
        if isinstance(text, list):
            text = " ".join(text)

        sample = {
            "task": task,
            "hf_index": i,
            "text": text,
            "label_set": config["label_names"],
            "split": split,
            "metadata": {},
        }

        # Handle hypothesis for ContractNLI
        if "hypothesis_field" in config:
            hypothesis = row[config["hypothesis_field"]]
            sample["text"] = f"Premise: {text}\nHypothesis: {hypothesis}"
            sample["metadata"]["premise"] = text
            sample["metadata"]["hypothesis"] = hypothesis

        # Handle holdings for CaseHOLD
        if "holdings_field" in config:
            holdings = row[config["holdings_field"]]
            sample["holdings"] = holdings

        # Handle labels
        if config["label_type"] == "single":
            raw_label = row[config["label_field"]]
            if isinstance(raw_label, int):
                sample["label"] = config["label_names"][raw_label]
            else:
                sample["label"] = str(raw_label)
            sample["labels"] = None
        else:
            raw_labels = row[config["label_field"]]
            if isinstance(raw_labels, list) and all(isinstance(x, int) for x in raw_labels):
                sample["labels"] = [config["label_names"][x] for x in raw_labels]
            else:
                sample["labels"] = [str(x) for x in raw_labels]
            sample["label"] = None

        sample["content_hash"] = hashlib.sha256(sample["text"].encode()).hexdigest()[:32]
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
            # Upsert sample
            await conn.execute(
                """INSERT INTO julia_lexglue_samples
                   (id, task, hf_index, text, holdings, label, labels,
                    label_set, split, metadata, content_hash)
                   VALUES (gen_random_uuid()::text, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (task, hf_index, split) DO UPDATE SET
                       text = EXCLUDED.text,
                       label = EXCLUDED.label,
                       labels = EXCLUDED.labels""",
                (
                    sample["task"],
                    sample["hf_index"],
                    sample["text"],
                    json.dumps(sample.get("holdings")) if sample.get("holdings") else None,
                    sample.get("label"),
                    json.dumps(sample.get("labels")) if sample.get("labels") else None,
                    json.dumps(sample["label_set"]),
                    sample["split"],
                    json.dumps(sample.get("metadata", {})),
                    sample["content_hash"],
                ),
            )

            # Embed and store chunks
            if not skip_embeddings:
                # Get the sample ID back
                row = await (
                    await conn.execute(
                        """SELECT id FROM julia_lexglue_samples
                           WHERE task = %s AND hf_index = %s AND split = %s""",
                        (sample["task"], sample["hf_index"], sample["split"]),
                    )
                ).fetchone()

                if row:
                    sample_id = row[0]
                    chunks = chunk_text(sample["text"], chunk_size=512, overlap=64)
                    for chunk in chunks:
                        vec = hash_embedding(chunk["text"], dim=384)
                        vec_str = "[" + ",".join(str(v) for v in vec) + "]"
                        chunk_hash = hashlib.sha256(chunk["text"].encode()).hexdigest()[:32]

                        await conn.execute(
                            """INSERT INTO julia_lexglue_embeddings
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
                                json.dumps(
                                    {"char_start": chunk["start"], "char_end": chunk["end"]}
                                ),
                            ),
                        )

            count += 1

        await conn.commit()

    return count


# ---------------------------------------------------------------------------
# LanceDB local cache
# ---------------------------------------------------------------------------


def store_lance(samples: list[dict]) -> int:
    """Store embeddings in LanceDB local cache."""
    from src.embeddings import EmbeddingRecord, LanceStore

    store = LanceStore(db_path=PROJECT_ROOT / ".lancedb" / "lexglue", table_name="lexglue")
    records = []

    for sample in samples:
        chunks = chunk_text(sample["text"], chunk_size=512, overlap=64)
        for chunk in chunks:
            vec = hash_embedding(chunk["text"], dim=384)
            record_id = hashlib.sha256(
                f"{sample['task']}:{sample['hf_index']}:{chunk['index']}".encode()
            ).hexdigest()[:16]

            records.append(
                EmbeddingRecord(
                    id=record_id,
                    text=chunk["text"],
                    vector=vec,
                    wing="lexglue",
                    room=sample["task"],
                    source_url=f"hf://lex_glue/{sample['task']}/{sample['hf_index']}",
                    content_hash=hashlib.sha256(chunk["text"].encode()).hexdigest()[:32],
                    metadata={
                        "task": sample["task"],
                        "hf_index": sample["hf_index"],
                        "chunk_index": chunk["index"],
                    },
                )
            )

    return store.add(records) if records else 0


# ---------------------------------------------------------------------------
# Local JSON cache
# ---------------------------------------------------------------------------


def write_json_cache(task: str, samples: list[dict]) -> Path:
    """Write samples to local JSON file for offline eval runs."""
    out_dir = PROJECT_ROOT / "julia" / "evals" / "test_data" / "lexglue"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{task}_samples.json"
    out_path.write_text(json.dumps(samples, indent=2, default=str))
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Download LexGLUE from HuggingFace and store in Neon + LanceDB"
    )
    parser.add_argument(
        "--task",
        default="all",
        choices=ALL_TASKS + ["all"],
        help="Which LexGLUE task to ingest (default: all)",
    )
    parser.add_argument(
        "--split",
        default="test",
        choices=["test", "validation", "train"],
        help="HuggingFace dataset split (default: test)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max samples per task (0=all)",
    )
    parser.add_argument(
        "--lance",
        action="store_true",
        help="Also populate LanceDB local cache",
    )
    parser.add_argument(
        "--skip-embeddings",
        action="store_true",
        help="Skip pgvector embedding (store metadata only)",
    )
    parser.add_argument(
        "--skip-neon",
        action="store_true",
        help="Skip Neon storage (local JSON + LanceDB only)",
    )
    args = parser.parse_args()

    tasks = ALL_TASKS if args.task == "all" else [args.task]

    for task in tasks:
        print(f"\n  Loading {task} from HuggingFace (split={args.split})...", file=sys.stderr)
        samples = load_hf_dataset(task, args.split, args.limit)
        print(f"  Loaded {len(samples)} samples", file=sys.stderr)

        # Write local JSON cache (always)
        json_path = write_json_cache(task, samples)
        print(f"  JSON cache: {json_path}", file=sys.stderr)

        # Store in Neon
        if not args.skip_neon:
            print("  Storing in Neon Postgres...", file=sys.stderr)
            neon_count = asyncio.run(store_neon(samples, skip_embeddings=args.skip_embeddings))
            print(f"  Neon: {neon_count} samples stored", file=sys.stderr)

        # Store in LanceDB
        if args.lance:
            print("  Storing in LanceDB...", file=sys.stderr)
            lance_count = store_lance(samples)
            print(f"  LanceDB: {lance_count} records stored", file=sys.stderr)

    print(f"\n  Done. Ingested {len(tasks)} task(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
