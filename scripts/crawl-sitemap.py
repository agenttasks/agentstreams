#!/usr/bin/env python3
"""Async parallel sitemap crawler for the AgentStreams UDA taxonomy.

Parses sitemap XML, fans out concurrent HTTP fetches with aiohttp,
writes taxonomy markdown + optionally upserts into Neon Postgres.

Usage:
  uv run scripts/crawl-sitemap.py <sitemap_url> <output_file> [options]

Examples:
  # Crawl platform.claude.com English pages
  uv run scripts/crawl-sitemap.py \\
    https://platform.claude.com/sitemap.xml \\
    taxonomy/platform-claude-com-full.md --concurrency 20

  # Crawl specific blog posts
  uv run scripts/crawl-sitemap.py \\
    https://www.anthropic.com/sitemap.xml \\
    taxonomy/anthropic-blog.md \\
    --urls https://www.anthropic.com/engineering/building-effective-agents
"""

import argparse
import asyncio
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
from spiders import HTMLToText, content_hash, html_to_text  # shared base module

# UDA integration: import src/ modules when available
_src_available = False
try:
    from src.neon_db import connection_pool as _neon_pool  # noqa: F401
    from src.neon_db import enqueue_task, upsert_resource  # noqa: F401

    _src_available = True
except ImportError:
    pass

__all__ = ["HTMLToText", "content_hash", "html_to_text"]  # re-export for tests

# ── Constants ────────────────────────────────────────────────

DEFAULT_CONCURRENCY = 20
DEFAULT_RATE_DELAY = 0.05  # 50ms between requests
TRUNCATE_BYTES = 50_000
USER_AGENT = "agentstreams-crawler/2.0 (async sitemap crawler)"


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1] or "index"


# ── Sitemap XML parser ──────────────────────────────────────


def parse_sitemap_xml(xml_text: str) -> list[str]:
    """Extract URLs from sitemap XML (handles both urlset and sitemapindex)."""
    urls: list[str] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return urls

    # Strip namespace for easier parsing
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    # Check if this is a sitemap index
    for sitemap in root.findall(f"{ns}sitemap"):
        loc = sitemap.find(f"{ns}loc")
        if loc is not None and loc.text:
            urls.append(loc.text.strip())

    # Or a regular urlset
    for url_elem in root.findall(f"{ns}url"):
        loc = url_elem.find(f"{ns}loc")
        if loc is not None and loc.text:
            urls.append(loc.text.strip())

    return urls


async def fetch_sitemap_urls(session: aiohttp.ClientSession, sitemap_url: str) -> list[str]:
    """Fetch and parse a sitemap, following sitemap index references."""
    try:
        async with session.get(sitemap_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            xml_text = await resp.text()
    except Exception as e:
        print(f"Error fetching sitemap {sitemap_url}: {e}", file=sys.stderr)
        return []

    urls = parse_sitemap_xml(xml_text)

    # If any URLs point to other sitemaps, fetch those too
    sub_sitemaps = [u for u in urls if u.endswith(".xml")]
    if sub_sitemaps:
        page_urls = [u for u in urls if not u.endswith(".xml")]
        for sub_url in sub_sitemaps:
            sub_urls = await fetch_sitemap_urls(session, sub_url)
            page_urls.extend(sub_urls)
        return page_urls

    return urls


# ── Core async fetcher ───────────────────────────────────────


async def fetch_page(
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    url: str,
    rate_delay: float,
) -> dict:
    """Fetch a single page with rate limiting."""
    async with sem:
        await asyncio.sleep(rate_delay)
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                raw = await resp.text(errors="replace")

            # Convert HTML to text
            if "<html" in raw[:500].lower() or "<!doctype" in raw[:500].lower():
                text = html_to_text(raw)
            else:
                text = raw

            # Truncate
            if len(text) > TRUNCATE_BYTES:
                text = text[:TRUNCATE_BYTES] + "\n\n[... truncated at 50KB ...]\n"

            return {
                "url": url,
                "content": text.strip(),
                "hash": content_hash(text),
                "error": None,
            }
        except Exception as e:
            return {"url": url, "content": None, "hash": None, "error": str(e)}


# ── Neon writer ──────────────────────────────────────────────


async def write_to_neon(
    neon_url: str,
    results: list[dict],
    domain: str,
    priority_pattern: re.Pattern | None,
) -> tuple[int, int]:
    """Upsert resources and create analysis tasks in Neon. Returns (resources, tasks) counts.

    Uses src/neon_db.py typed data access functions when available,
    falling back to inline psycopg for backwards compatibility.
    """
    resources_count = 0
    tasks_count = 0

    if _src_available:
        # UDA path: use src/neon_db.py typed functions
        async with _neon_pool(neon_url) as conn:
            for r in results:
                if r["error"] or not r["content"]:
                    continue
                await upsert_resource(
                    conn,
                    resource_type="crawled_page",
                    label=slug_from_url(r["url"]),
                    url=r["url"],
                    content_hash=r["hash"],
                )
                resources_count += 1

                priority = 1 if (priority_pattern and priority_pattern.search(r["url"])) else 0
                await enqueue_task(
                    conn,
                    queue_name="crawl-analyze",
                    task_type="knowledge_work",
                    skill_name="crawl-ingest",
                    task_input={"url": r["url"], "domain": domain},
                    priority=priority,
                )
                tasks_count += 1
            await conn.commit()
    else:
        # Legacy path: inline psycopg
        import psycopg

        async with await psycopg.AsyncConnection.connect(neon_url) as conn:
            for r in results:
                if r["error"] or not r["content"]:
                    continue
                await conn.execute(
                    """INSERT INTO resources (type, label, url, content_hash, fetched_at)
                       VALUES ('crawled_page', %s, %s, %s, now())
                       ON CONFLICT (url) DO UPDATE
                       SET content_hash = EXCLUDED.content_hash,
                           fetched_at = now()""",
                    (slug_from_url(r["url"]), r["url"], r["hash"]),
                )
                resources_count += 1

                priority = 1 if (priority_pattern and priority_pattern.search(r["url"])) else 0
                await conn.execute(
                    """INSERT INTO tasks (queue_name, type, status, input, priority)
                       VALUES ('crawl-analyze', 'knowledge_work', 'queued', %s, %s)""",
                    (json.dumps({"url": r["url"], "domain": domain}), priority),
                )
                tasks_count += 1
            await conn.commit()

    return resources_count, tasks_count


# ── Taxonomy markdown writer ─────────────────────────────────


def write_taxonomy(
    results: list[dict],
    output_path: str,
    sitemap_url: str,
    domain: str,
) -> None:
    """Write crawl results as taxonomy markdown with frontmatter."""
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    success = [r for r in results if not r["error"]]
    errors = [r for r in results if r["error"]]

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, "w") as f:
        # Frontmatter
        f.write("---\n")
        f.write(f"source: {sitemap_url}\n")
        f.write(f"domain: {domain}\n")
        f.write(f"crawled_at: {now}\n")
        f.write(f"page_count: {len(success)}\n")
        f.write(f"error_count: {len(errors)}\n")
        f.write("crawler: crawl-sitemap.py (async, aiohttp)\n")
        f.write("---\n\n")

        f.write(f"# {domain} — Sitemap Crawl Taxonomy\n\n")
        f.write(f"Source: `{sitemap_url}`\n")
        f.write(f"Crawled: {now}\n")
        f.write(f"Pages: {len(success)} fetched, {len(errors)} errors\n\n")

        # Pages
        f.write("## Pages\n\n")
        for r in sorted(success, key=lambda x: x["url"]):
            slug = slug_from_url(r["url"])
            f.write(f"### {slug}\n\n")
            f.write(f"URL: {r['url']}\n")
            f.write(f"Hash: {r['hash']}\n\n")
            f.write("```\n")
            f.write(r["content"])
            f.write("\n```\n\n")

        # Error summary
        if errors:
            f.write("## Errors\n\n")
            for r in errors:
                f.write(f"- {r['url']}: {r['error']}\n")
            f.write("\n")

        f.write(f"---\n\nCrawl complete: {len(success)} pages fetched, {len(errors)} errors\n")


# ── Main ─────────────────────────────────────────────────────


async def main_async(args: argparse.Namespace) -> None:
    domain = args.domain or urlparse(args.sitemap_url).netloc
    priority_pattern = re.compile(args.priority_pattern) if args.priority_pattern else None

    headers = {"User-Agent": USER_AGENT}
    async with aiohttp.ClientSession(headers=headers) as session:
        # Resolve URL list
        if args.urls:
            urls = args.urls
            print(f"Using {len(urls)} explicit URLs", file=sys.stderr)
        else:
            print(f"Fetching sitemap: {args.sitemap_url}", file=sys.stderr)
            urls = await fetch_sitemap_urls(session, args.sitemap_url)
            print(f"Found {len(urls)} URLs in sitemap", file=sys.stderr)

        # Apply max-pages limit
        urls = urls[: args.max_pages]

        # Filter by priority pattern if --priority-only
        if args.priority_only and priority_pattern:
            urls = [u for u in urls if priority_pattern.search(u)]
            print(f"Filtered to {len(urls)} priority URLs", file=sys.stderr)

        if not urls:
            print("No URLs to crawl", file=sys.stderr)
            return

        # Fan out fetches
        sem = asyncio.Semaphore(args.concurrency)
        start_time = asyncio.get_event_loop().time()

        print(
            f"Crawling {len(urls)} pages (concurrency={args.concurrency})...",
            file=sys.stderr,
        )

        tasks = [fetch_page(session, sem, url, args.rate_delay) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten exceptions into error results
        final_results = []
        for i, r in enumerate(results):
            if isinstance(r, Exception):
                final_results.append(
                    {"url": urls[i], "content": None, "hash": None, "error": str(r)}
                )
            else:
                final_results.append(r)

        elapsed = asyncio.get_event_loop().time() - start_time
        success = sum(1 for r in final_results if not r["error"])
        errors = sum(1 for r in final_results if r["error"])

        print(
            f"Fetched {success} pages, {errors} errors in {elapsed:.1f}s "
            f"({success / elapsed:.1f} pages/sec)",
            file=sys.stderr,
        )

        # Emit metrics
        print(
            json.dumps(
                {
                    "metric": "agentstreams.crawl.pages",
                    "tags": {"domain": domain, "status": "summary"},
                    "value": success,
                    "elapsed_s": round(elapsed, 2),
                    "errors": errors,
                }
            ),
            file=sys.stderr,
        )

    # Write taxonomy markdown
    write_taxonomy(final_results, args.output_file, args.sitemap_url, domain)
    print(f"Wrote {args.output_file}", file=sys.stderr)

    # Write to Neon if configured
    neon_url = args.neon_url or ""
    if not neon_url:
        import os

        neon_url = os.environ.get("NEON_DATABASE_URL", "")

    if neon_url:
        print("Writing to Neon...", file=sys.stderr)
        try:
            res_count, task_count = await write_to_neon(
                neon_url, final_results, domain, priority_pattern
            )
            print(
                f"Neon: {res_count} resources upserted, {task_count} tasks created",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Neon write error: {e}", file=sys.stderr)
    else:
        print("No NEON_DATABASE_URL — skipping Neon writes", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Async parallel sitemap crawler")
    parser.add_argument("sitemap_url", help="URL of the sitemap.xml")
    parser.add_argument("output_file", help="Output taxonomy markdown file")
    parser.add_argument("--urls", nargs="*", help="Explicit URLs (skip sitemap parsing)")
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--rate-delay", type=float, default=DEFAULT_RATE_DELAY)
    parser.add_argument("--max-pages", type=int, default=2000)
    parser.add_argument("--priority-pattern", default="/en/", help="Regex for priority URLs")
    parser.add_argument("--priority-only", action="store_true", help="Only crawl priority URLs")
    parser.add_argument("--neon-url", help="Neon connection string (or NEON_DATABASE_URL env)")
    parser.add_argument("--domain", help="Override detected domain")
    args = parser.parse_args()

    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
