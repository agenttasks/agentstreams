#!/usr/bin/env python3
"""Convert non-standard taxonomy files to pipeline-compatible format.

Handles two source formats:
1. PDF-extracted chapter files (## Chapter N: Title + tree-format code blocks)
2. PDF files (extracts text via pymupdf if available, falls back to marker)

Converts to the standard taxonomy format used by extract-patterns.py:
  ---
  source: <origin>
  domain: <domain>
  crawled_at: <timestamp>
  index_hash: <hash>
  page_count: <count>
  ---
  ## Pages
  ### <section-slug>
  URL: <synthetic-url>
  Hash: <content-hash>
  ```
  <content>
  ```

Usage:
  uv run scripts/convert-taxonomy.py taxonomy/kimball-ch01-02.md
  uv run scripts/convert-taxonomy.py taxonomy/kimball-ch01-02.md -o taxonomy/kimball-ch01-02-converted.md
  uv run scripts/convert-taxonomy.py taxonomy/*.md --in-place
  uv run scripts/convert-taxonomy.py taxonomy/document.pdf -o taxonomy/document.md
"""

import argparse
import hashlib
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def content_hash(text: str) -> str:
    """Generate a short content hash."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def slugify(text: str) -> str:
    """Convert a heading to a URL-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower().strip())
    return slug.strip("-")[:60]


def detect_format(text: str) -> str:
    """Detect the format of a taxonomy file."""
    if text.startswith("---"):
        # Check if it has the full pipeline format
        if re.search(r"^### .+$", text, re.MULTILINE) and re.search(r"^URL:", text, re.MULTILINE):
            return "pipeline"  # already compatible
        return "frontmatter-only"

    if re.search(r"^## Chapter \d+", text, re.MULTILINE):
        return "chapter-tree"

    if re.search(r"^## .+$", text, re.MULTILINE):
        return "section-tree"

    return "plain"


def extract_source_info(text: str, file_path: Path) -> dict:
    """Extract source metadata from file content or filename."""
    info = {
        "source": f"file://{file_path.name}",
        "domain": "local",
        "title": file_path.stem,
    }

    # Try to find source line
    source_match = re.search(r"Source:\s*(.+?)(?:\n|$)", text)
    if source_match:
        info["source"] = source_match.group(1).strip()

    # Try to find title
    title_match = re.search(r"^# (.+)$", text, re.MULTILINE)
    if title_match:
        info["title"] = title_match.group(1).strip()

    return info


def convert_chapter_tree(text: str, file_path: Path) -> str:
    """Convert chapter-tree format to pipeline format."""
    info = extract_source_info(text, file_path)
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Split on ## headers (chapters/sections)
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    pages = []

    for section in sections:
        section = section.strip()
        if not section.startswith("## "):
            continue

        # Extract heading
        heading_match = re.match(r"^## (.+)$", section, re.MULTILINE)
        if not heading_match:
            continue
        heading = heading_match.group(1).strip()
        slug = slugify(heading)

        # Extract content (everything after the heading)
        body = section[heading_match.end() :].strip()

        # If content is in a fenced code block, extract it
        code_match = re.search(r"```\n?(.*?)\n?```", body, re.DOTALL)
        if code_match:
            content = code_match.group(1)
        else:
            content = body

        if content.strip():
            pages.append(
                {
                    "slug": slug,
                    "heading": heading,
                    "content": content.strip(),
                    "hash": content_hash(content),
                }
            )

    # Build pipeline-compatible output
    domain = info["domain"]
    base_url = f"https://local.taxonomy/{file_path.stem}"

    lines = [
        "---",
        f"source: {info['source']}",
        f"domain: {domain}",
        f"crawled_at: {now}",
        f"index_hash: {content_hash(text)}",
        f"page_count: {len(pages)}",
        "---",
        "",
        f"# {info['title']}",
        "",
        "## Pages",
    ]

    for page in pages:
        lines.extend(
            [
                "",
                f"### {page['slug']}",
                "",
                f"URL: {base_url}/{page['slug']}",
                f"Hash: {page['hash']}",
                "",
                "```",
                page["content"],
                "```",
            ]
        )

    return "\n".join(lines) + "\n"


def convert_section_tree(text: str, file_path: Path) -> str:
    """Convert section-tree format (## headings without Chapter prefix)."""
    # Same logic as chapter tree — the ## headers are sections
    return convert_chapter_tree(text, file_path)


def convert_plain(text: str, file_path: Path) -> str:
    """Convert plain text to single-page pipeline format."""
    info = extract_source_info(text, file_path)
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    slug = slugify(info["title"])
    h = content_hash(text)

    return f"""---
source: {info["source"]}
domain: {info["domain"]}
crawled_at: {now}
index_hash: {h}
page_count: 1
---

# {info["title"]}

## Pages

### {slug}

URL: https://local.taxonomy/{file_path.stem}/{slug}
Hash: {h}

```
{text.strip()}
```
"""


def convert_pdf(pdf_path: Path) -> str:
    """Extract text from PDF and convert to pipeline format."""
    try:
        import pymupdf  # noqa: F811
    except ImportError:
        print(
            "pymupdf not installed. Install with: uv add pymupdf",
            file=sys.stderr,
        )
        sys.exit(1)

    doc = pymupdf.open(str(pdf_path))
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    title = doc.metadata.get("title", pdf_path.stem) or pdf_path.stem

    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            slug = f"page-{i + 1}"
            pages.append(
                {
                    "slug": slug,
                    "heading": f"Page {i + 1}",
                    "content": text,
                    "hash": content_hash(text),
                }
            )

    doc.close()

    lines = [
        "---",
        f"source: file://{pdf_path.name}",
        "domain: local",
        f"crawled_at: {now}",
        f"index_hash: {content_hash(str(pdf_path))}",
        f"page_count: {len(pages)}",
        "---",
        "",
        f"# {title}",
        "",
        "## Pages",
    ]

    for page in pages:
        lines.extend(
            [
                "",
                f"### {page['slug']}",
                "",
                f"URL: https://local.taxonomy/{pdf_path.stem}/{page['slug']}",
                f"Hash: {page['hash']}",
                "",
                "```",
                page["content"],
                "```",
            ]
        )

    return "\n".join(lines) + "\n"


def is_pipeline_compatible(text: str) -> bool:
    """Check if a file is already in pipeline-compatible format."""
    return detect_format(text) == "pipeline"


def convert_file(file_path: Path) -> str | None:
    """Convert a file to pipeline format. Returns None if already compatible."""
    if file_path.suffix == ".pdf":
        return convert_pdf(file_path)

    text = file_path.read_text(errors="replace")
    fmt = detect_format(text)

    if fmt == "pipeline":
        return None  # already compatible

    if fmt == "chapter-tree":
        return convert_chapter_tree(text, file_path)
    elif fmt == "section-tree":
        return convert_section_tree(text, file_path)
    elif fmt == "plain":
        return convert_plain(text, file_path)
    elif fmt == "frontmatter-only":
        # Has frontmatter but no proper page sections — treat as section tree
        return convert_section_tree(text, file_path)

    return convert_plain(text, file_path)


def main():
    parser = argparse.ArgumentParser(
        description="Convert taxonomy files to pipeline-compatible format"
    )
    parser.add_argument("files", nargs="+", help="Files to convert")
    parser.add_argument("-o", "--output", help="Output file (single file mode only)")
    parser.add_argument("--in-place", action="store_true", help="Overwrite input files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be converted without writing",
    )
    args = parser.parse_args()

    if args.output and len(args.files) > 1:
        print("Error: --output can only be used with a single file", file=sys.stderr)
        sys.exit(1)

    converted = 0
    skipped = 0

    for file_str in args.files:
        file_path = Path(file_str)
        if not file_path.exists():
            print(f"  ✗ {file_path}: not found", file=sys.stderr)
            continue

        result = convert_file(file_path)

        if result is None:
            print(f"  ✓ {file_path.name}: already compatible", file=sys.stderr)
            skipped += 1
            continue

        # Count pages in output
        page_count = result.count("\n### ")

        if args.dry_run:
            print(
                f"  → {file_path.name}: would convert ({page_count} pages)",
                file=sys.stderr,
            )
            converted += 1
            continue

        if args.output:
            out_path = Path(args.output)
        elif args.in_place:
            out_path = file_path
        else:
            # Default: write to same name with -converted suffix
            out_path = file_path.with_stem(file_path.stem + "-converted")

        out_path.write_text(result)
        print(
            f"  ✓ {file_path.name} → {out_path.name} ({page_count} pages)",
            file=sys.stderr,
        )
        converted += 1

    print(
        f"\n{converted} converted, {skipped} already compatible",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
