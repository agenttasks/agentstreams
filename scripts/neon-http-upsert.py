#!/usr/bin/env python3
"""Upsert crawled taxonomy pages into Neon via SQL-over-HTTP.

Workaround for environments where TCP to Neon port 5432 is blocked
but HTTPS goes through the proxy. Parses taxonomy markdown files
produced by crawl-sitemap.py and batch-upserts into the resources table.

Usage:
    uv run scripts/neon-http-upsert.py taxonomy/anthropic-com-full.md
"""

import json
import re
import sys
from pathlib import Path

import httpx

NEON_HOST = "ep-noisy-surf-aju7f7eb-pooler.c-3.us-east-2.aws.neon.tech"
CONN_STRING = f"postgresql://neondb_owner:npg_h15YMtbzqkBj@{NEON_HOST}/neondb?sslmode=require"
SQL_ENDPOINT = f"https://{NEON_HOST}/sql"
BATCH_SIZE = 50


def parse_taxonomy(path: Path) -> list[dict]:
    """Parse a taxonomy markdown file into page records."""
    text = path.read_text()
    pages = []

    # Split on page headers: ### slug\n\nURL: https://...
    page_blocks = re.split(r"\n### ", text)
    for block in page_blocks[1:]:  # skip frontmatter
        lines = block.strip().split("\n")
        slug = lines[0].strip()

        url_match = re.search(r"URL:\s+(https?://\S+)", block)
        hash_match = re.search(r"Hash:\s+(\S+)", block)

        if not url_match:
            continue

        url = url_match.group(1)
        content_hash = hash_match.group(1) if hash_match else None

        # Extract content between ``` fences
        code_match = re.search(r"```\n(.*?)```", block, re.DOTALL)
        content = code_match.group(1).strip() if code_match else ""

        pages.append(
            {
                "slug": slug,
                "url": url,
                "hash": content_hash,
                "content_len": len(content),
            }
        )

    return pages


def neon_sql(client: httpx.Client, query: str, params: list | None = None) -> dict:
    """Execute SQL via Neon's HTTP API."""
    body = {"query": query}
    if params:
        body["params"] = params
    resp = client.post(
        SQL_ENDPOINT,
        json=body,
        headers={
            "Content-Type": "application/json",
            "Neon-Connection-String": CONN_STRING,
        },
    )
    resp.raise_for_status()
    return resp.json()


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/neon-http-upsert.py <taxonomy-file>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    pages = parse_taxonomy(path)
    print(f"Parsed {len(pages)} pages from {path.name}", file=sys.stderr)

    # Get existing URLs from Neon
    with httpx.Client(timeout=30) as client:
        result = neon_sql(client, "SELECT url FROM resources WHERE url LIKE '%anthropic.com%'")
        existing = {row["url"] for row in result["rows"]}
        print(f"Existing anthropic.com resources in Neon: {len(existing)}", file=sys.stderr)

        new_pages = [p for p in pages if p["url"] not in existing]
        update_pages = [p for p in pages if p["url"] in existing]
        print(f"New pages to insert: {len(new_pages)}", file=sys.stderr)
        print(f"Existing pages to update: {len(update_pages)}", file=sys.stderr)

        inserted = 0
        updated = 0

        # Batch insert new pages
        for i in range(0, len(new_pages), BATCH_SIZE):
            batch = new_pages[i : i + BATCH_SIZE]
            for page in batch:
                neon_sql(
                    client,
                    """INSERT INTO resources (type, label, url, content_hash, fetched_at)
                       VALUES ($1, $2, $3, $4, now())
                       ON CONFLICT (url) DO UPDATE SET
                           content_hash = EXCLUDED.content_hash,
                           fetched_at = now()""",
                    ["crawled_page", page["slug"], page["url"], page["hash"]],
                )
                inserted += 1
            print(f"  Inserted {inserted}/{len(new_pages)}...", file=sys.stderr)

        # Update existing pages with fresh hashes
        for page in update_pages:
            neon_sql(
                client,
                """UPDATE resources SET content_hash = $1, fetched_at = now()
                   WHERE url = $2""",
                [page["hash"], page["url"]],
            )
            updated += 1

        # Also enqueue analysis tasks for new pages
        tasks_created = 0
        domain = "www.anthropic.com"
        for page in new_pages:
            priority = 1 if re.search(r"/(research|engineering|news)/", page["url"]) else 0
            neon_sql(
                client,
                """INSERT INTO tasks (queue_name, type, status, priority, skill_name, input)
                   VALUES ($1, $2, 'queued', $3, $4, $5)""",
                [
                    "crawl-analyze",
                    "knowledge_work",
                    priority,
                    "crawl-ingest",
                    json.dumps({"url": page["url"], "domain": domain}),
                ],
            )
            tasks_created += 1

        print(
            f"\nDone: {inserted} inserted, {updated} updated, {tasks_created} tasks created",
            file=sys.stderr,
        )

        # Final count
        result = neon_sql(
            client, "SELECT COUNT(*) as cnt FROM resources WHERE url LIKE '%anthropic.com%'"
        )
        print(f"Total anthropic.com resources now: {result['rows'][0]['cnt']}", file=sys.stderr)

        result = neon_sql(client, "SELECT COUNT(*) as cnt FROM resources")
        print(f"Total resources in Neon: {result['rows'][0]['cnt']}", file=sys.stderr)


if __name__ == "__main__":
    main()
