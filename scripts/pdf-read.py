#!/usr/bin/env python3
"""Download PDFs from URLs with bloom filter deduplication and token-optimized extraction.

Downloads PDFs, checks a session-scoped bloom filter to avoid re-processing,
extracts text via PyMuPDF, and outputs taxonomy-format markdown for selective
reading with minimal token usage.

Usage:
  uv run scripts/pdf-read.py https://example.com/document.pdf
  uv run scripts/pdf-read.py --pages 1-10 https://example.com/large.pdf
  uv run scripts/pdf-read.py --toc https://example.com/document.pdf
  uv run scripts/pdf-read.py --no-cache URL1 URL2 URL3
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.bloom import BloomFilter  # noqa: E402

TAXONOMY_DIR = PROJECT_ROOT / "taxonomy"
CACHE_DIR = PROJECT_ROOT / ".cache" / "pdf"
BLOOM_CACHE = CACHE_DIR / "pdf-bloom.bin"


def url_to_slug(url: str) -> str:
    """Convert URL to filesystem-safe slug."""
    # Strip protocol and trailing slashes
    clean = re.sub(r"^https?://", "", url).rstrip("/")
    # Replace non-alphanumeric with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", clean.lower()).strip("-")
    # Truncate and add hash suffix for uniqueness
    short_hash = hashlib.sha256(url.encode()).hexdigest()[:8]
    return f"{slug[:80]}-{short_hash}"


def parse_page_range(spec: str, total_pages: int) -> list[int]:
    """Parse page range spec like '1-10,15,20-25' into list of 0-indexed page numbers."""
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start_i = max(0, int(start) - 1)
            end_i = min(total_pages, int(end))
            pages.update(range(start_i, end_i))
        else:
            idx = int(part) - 1
            if 0 <= idx < total_pages:
                pages.add(idx)
    return sorted(pages)


def download_pdf(url: str) -> Path:
    """Download PDF to cache directory. Returns path to cached file."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    slug = url_to_slug(url)
    cached_path = CACHE_DIR / f"{slug}.pdf"

    if cached_path.exists():
        print(f"  [cache hit] {cached_path.name}", file=sys.stderr)
        return cached_path

    print(f"  [downloading] {url}", file=sys.stderr)

    # Handle redirects (e.g., Anthropic system card URLs redirect to CDN)
    req = urllib.request.Request(url, headers={"User-Agent": "pdf-read/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        # Follow redirect if content-type indicates HTML (login page)
        content_type = resp.headers.get("Content-Type", "")
        data = resp.read()

        # Check if we got a redirect page instead of a PDF
        if b"%PDF" not in data[:1024] and content_type and "html" in content_type.lower():
            # Try to find redirect URL in the response
            redirect_match = re.search(rb'href=["\']([^"\']+\.pdf[^"\']*)', data)
            if redirect_match:
                redirect_url = redirect_match.group(1).decode("utf-8", errors="replace")
                if not redirect_url.startswith("http"):
                    # Relative URL — resolve against original
                    from urllib.parse import urljoin

                    redirect_url = urljoin(url, redirect_url)
                print(f"  [redirect] {redirect_url}", file=sys.stderr)
                req2 = urllib.request.Request(redirect_url, headers={"User-Agent": "pdf-read/1.0"})
                with urllib.request.urlopen(req2, timeout=60) as resp2:
                    data = resp2.read()

    cached_path.write_bytes(data)
    size_mb = len(data) / (1024 * 1024)
    print(f"  [saved] {cached_path.name} ({size_mb:.1f} MB)", file=sys.stderr)
    return cached_path


def extract_pdf(
    pdf_path: Path,
    page_indices: list[int] | None = None,
) -> dict:
    """Extract text from PDF. Returns structured page data."""
    try:
        import pymupdf
    except ImportError:
        print("pymupdf not installed. Run: uv add pymupdf", file=sys.stderr)
        sys.exit(1)

    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)
    title = doc.metadata.get("title", pdf_path.stem) or pdf_path.stem

    if page_indices is None:
        page_indices = list(range(total_pages))

    pages = []
    for i in page_indices:
        if i >= total_pages:
            continue
        page = doc[i]
        text = page.get_text().strip()
        if text:
            char_count = len(text)
            est_tokens = char_count // 4
            pages.append(
                {
                    "number": i + 1,
                    "text": text,
                    "chars": char_count,
                    "est_tokens": est_tokens,
                }
            )

    doc.close()

    return {
        "title": title,
        "total_pages": total_pages,
        "extracted_pages": len(pages),
        "pages": pages,
        "total_chars": sum(p["chars"] for p in pages),
        "total_est_tokens": sum(p["est_tokens"] for p in pages),
    }


def write_taxonomy(url: str, data: dict, output_dir: Path) -> Path:
    """Write extracted PDF data in taxonomy format for selective reading."""
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = url_to_slug(url)
    out_path = output_dir / f"{slug}.md"
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "---",
        f"source: {url}",
        "domain: pdf",
        f"crawled_at: {now}",
        f"index_hash: {hashlib.sha256(url.encode()).hexdigest()[:12]}",
        f"total_pages: {data['total_pages']}",
        f"extracted_pages: {data['extracted_pages']}",
        f"total_est_tokens: {data['total_est_tokens']}",
        "---",
        "",
        f"# {data['title']}",
        "",
        "## Page Index",
        "",
    ]

    # Page index for quick scanning
    for page in data["pages"]:
        preview = page["text"][:80].replace("\n", " ")
        lines.append(f"- page-{page['number']}: ~{page['est_tokens']} tokens — {preview}...")

    lines.extend(["", "## Pages", ""])

    for page in data["pages"]:
        lines.extend(
            [
                f"### page-{page['number']}",
                "",
                f"<!-- ~{page['est_tokens']} tokens, {page['chars']} chars -->",
                "",
                page["text"],
                "",
            ]
        )

    out_path.write_text("\n".join(lines))
    return out_path


def load_bloom() -> BloomFilter:
    """Load or create the session bloom filter."""
    if BLOOM_CACHE.exists():
        data = BLOOM_CACHE.read_bytes()
        return BloomFilter.from_bytes(data, expected_items=1000, fp_rate=0.01)
    return BloomFilter(expected_items=1000, fp_rate=0.01)


def save_bloom(bloom: BloomFilter) -> None:
    """Persist bloom filter to disk."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    BLOOM_CACHE.write_bytes(bloom.to_bytes())


def print_toc(data: dict) -> None:
    """Print table of contents with token estimates."""
    print(f"# {data['title']}")
    print(f"Total pages: {data['total_pages']}, Extracted: {data['extracted_pages']}")
    print(f"Estimated tokens: ~{data['total_est_tokens']:,}")
    print()
    for page in data["pages"]:
        preview = page["text"][:100].replace("\n", " ")
        print(f"  p{page['number']:>4}  ~{page['est_tokens']:>6} tok  {preview}...")


def print_stats(data: dict) -> None:
    """Print per-page token statistics."""
    print(f"{'Page':>6}  {'Chars':>8}  {'~Tokens':>8}  {'Cumulative':>10}")
    print("-" * 40)
    cumulative = 0
    for page in data["pages"]:
        cumulative += page["est_tokens"]
        print(f"{page['number']:>6}  {page['chars']:>8}  {page['est_tokens']:>8}  {cumulative:>10}")
    print("-" * 40)
    print(f"{'Total':>6}  {data['total_chars']:>8}  {data['total_est_tokens']:>8}")


def process_url(
    url: str,
    bloom: BloomFilter,
    *,
    pages: str | None = None,
    output_dir: Path = TAXONOMY_DIR,
    no_cache: bool = False,
    toc_only: bool = False,
    stats_only: bool = False,
) -> Path | None:
    """Process a single PDF URL. Returns output path or None if skipped."""
    slug = url_to_slug(url)
    cached_taxonomy = output_dir / f"{slug}.md"

    # Bloom filter check
    if not no_cache and url in bloom:
        if cached_taxonomy.exists():
            print(f"  [bloom skip] Already processed: {url}", file=sys.stderr)
            if toc_only or stats_only:
                # Re-extract for display but don't re-download
                pdf_path = CACHE_DIR / f"{slug}.pdf"
                if pdf_path.exists():
                    page_indices = parse_page_range(pages, 99999) if pages else None
                    data = extract_pdf(pdf_path, page_indices)
                    if toc_only:
                        print_toc(data)
                    elif stats_only:
                        print_stats(data)
            return cached_taxonomy
        # Bloom says seen but cache file missing — re-process
        print(f"  [bloom hit, cache miss] Re-extracting: {url}", file=sys.stderr)

    # Download
    pdf_path = download_pdf(url)

    # Extract
    total_pages_for_range = 99999  # Will be clamped inside extract_pdf
    page_indices = parse_page_range(pages, total_pages_for_range) if pages else None
    data = extract_pdf(pdf_path, page_indices)

    if toc_only:
        print_toc(data)
        bloom.add(url)
        save_bloom(bloom)
        return None

    if stats_only:
        print_stats(data)
        bloom.add(url)
        save_bloom(bloom)
        return None

    # Write taxonomy
    out_path = write_taxonomy(url, data, output_dir)
    print(
        f"  [extracted] {out_path.name} "
        f"({data['extracted_pages']} pages, ~{data['total_est_tokens']:,} tokens)",
        file=sys.stderr,
    )

    # Update bloom filter
    bloom.add(url)
    save_bloom(bloom)

    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Download and extract PDFs with bloom filter deduplication"
    )
    parser.add_argument("urls", nargs="+", help="PDF URLs to process")
    parser.add_argument("--pages", help='Page range (e.g., "1-10", "5,10,15-20")')
    parser.add_argument(
        "--output",
        default=str(TAXONOMY_DIR),
        help="Output directory (default: taxonomy/)",
    )
    parser.add_argument("--no-cache", action="store_true", help="Force re-download")
    parser.add_argument("--toc", action="store_true", help="Print table of contents only")
    parser.add_argument("--stats", action="store_true", help="Print per-page token estimates")
    args = parser.parse_args()

    bloom = load_bloom()
    output_dir = Path(args.output)
    results = []

    for url in args.urls:
        print(f"\n Processing: {url}", file=sys.stderr)
        result = process_url(
            url,
            bloom,
            pages=args.pages,
            output_dir=output_dir,
            no_cache=args.no_cache,
            toc_only=args.toc,
            stats_only=args.stats,
        )
        if result:
            results.append(result)

    if results:
        print(f"\n {len(results)} PDFs extracted:", file=sys.stderr)
        for r in results:
            print(f"  {r}", file=sys.stderr)


if __name__ == "__main__":
    main()
