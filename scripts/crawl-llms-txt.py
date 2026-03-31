#!/usr/bin/env python3
"""Crawl an llms.txt index and fetch each linked page into a taxonomy markdown file.

Usage:
  python3 scripts/crawl-llms-txt.py <llms_txt_url> <output_file> [--pages URL1 URL2 ...]

Examples:
  # Crawl full index
  python3 scripts/crawl-llms-txt.py https://code.claude.com/docs/llms.txt taxonomy/code-claude-com.md

  # Crawl specific pages only
  python3 scripts/crawl-llms-txt.py https://code.claude.com/docs/llms.txt taxonomy/code-claude-com.md \
    --pages https://code.claude.com/docs/en/tools-reference https://code.claude.com/docs/en/sub-agents

Output format:
  Markdown file with frontmatter, index section, and full content of each crawled page.
"""

import argparse
import hashlib
import re
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path


class HTMLToText(HTMLParser):
    """Minimal HTML-to-text converter that strips tags and extracts text content."""

    def __init__(self):
        super().__init__()
        self._text = []
        self._skip = False
        self._skip_tags = {"script", "style", "nav", "footer", "header"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True
        if tag in ("br", "p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr"):
            self._text.append("\n")
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self._text.append(f" [{value}] ")

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False
        if tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "table"):
            self._text.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self._text.append(data)

    def get_text(self):
        return "".join(self._text)


def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch a URL and return its text content."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "agentstreams-crawler/1.0 (taxonomy builder)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")

    # If it looks like HTML, strip tags
    if "<html" in raw[:500].lower() or "<!doctype" in raw[:500].lower():
        parser = HTMLToText()
        parser.feed(raw)
        return parser.get_text()
    return raw


def extract_urls(text: str, base_url: str) -> list[str]:
    """Extract URLs from llms.txt content. Handles both absolute and relative URLs."""
    urls = []
    for line in text.splitlines():
        line = line.strip()
        # Match markdown links [text](url) or bare URLs
        for match in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", line):
            url = match.group(2)
            if url.startswith("http"):
                urls.append(url)
            elif url.startswith("/"):
                # Resolve relative URL
                from urllib.parse import urlparse

                parsed = urlparse(base_url)
                urls.append(f"{parsed.scheme}://{parsed.netloc}{url}")
        # Also match bare .md URLs
        if line.endswith(".md") and "/" in line:
            if line.startswith("http"):
                urls.append(line)
            elif line.startswith("/"):
                from urllib.parse import urlparse

                parsed = urlparse(base_url)
                urls.append(f"{parsed.scheme}://{parsed.netloc}{line}")
        # Match lines that are just URLs
        if line.startswith("http://") or line.startswith("https://"):
            url = line.split()[0]  # Take first token only
            if url not in urls:
                urls.append(url)
    return urls


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def main():
    parser = argparse.ArgumentParser(description="Crawl llms.txt and build taxonomy")
    parser.add_argument("llms_txt_url", help="URL of the llms.txt file")
    parser.add_argument("output_file", help="Output markdown file path")
    parser.add_argument("--pages", nargs="*", help="Specific page URLs to crawl (instead of all)")
    parser.add_argument(
        "--max-pages", type=int, default=100, help="Max pages to crawl (default: 100)"
    )
    args = parser.parse_args()

    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    from urllib.parse import urlparse

    source_domain = urlparse(args.llms_txt_url).netloc

    print(f"Fetching index: {args.llms_txt_url}")
    try:
        index_text = fetch_url(args.llms_txt_url)
    except urllib.error.URLError as e:
        print(f"Error fetching index: {e}", file=sys.stderr)
        sys.exit(1)

    index_hash = content_hash(index_text)

    # Determine which pages to crawl
    if args.pages:
        page_urls = args.pages
    else:
        page_urls = extract_urls(index_text, args.llms_txt_url)

    page_urls = page_urls[: args.max_pages]
    print(f"Found {len(page_urls)} pages to crawl")

    # Build output
    out = Path(args.output_file)
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, "w") as f:
        # Frontmatter
        f.write("---\n")
        f.write(f"source: {args.llms_txt_url}\n")
        f.write(f"domain: {source_domain}\n")
        f.write(f"crawled_at: {now}\n")
        f.write(f"index_hash: {index_hash}\n")
        f.write(f"page_count: {len(page_urls)}\n")
        f.write("---\n\n")

        # Index section
        f.write(f"# {source_domain} — Documentation Taxonomy\n\n")
        f.write(f"Source: `{args.llms_txt_url}`\n")
        f.write(f"Crawled: {now}\n\n")

        f.write("## Index\n\n")
        f.write("```\n")
        # Write first 100 lines of index
        for line in index_text.splitlines()[:100]:
            f.write(f"{line}\n")
        f.write("```\n\n")

        # Crawl each page
        f.write("## Pages\n\n")
        success = 0
        errors = 0
        for i, url in enumerate(page_urls):
            slug = urlparse(url).path.rstrip("/").split("/")[-1] or "index"
            print(f"  [{i + 1}/{len(page_urls)}] {slug}...")

            try:
                content = fetch_url(url)
                page_hash = content_hash(content)
                # Truncate very long pages
                if len(content) > 50000:
                    content = content[:50000] + "\n\n[... truncated at 50KB ...]\n"
                f.write(f"### {slug}\n\n")
                f.write(f"URL: {url}\n")
                f.write(f"Hash: {page_hash}\n\n")
                f.write("```\n")
                f.write(content.strip())
                f.write("\n```\n\n")
                success += 1
            except Exception as e:
                f.write(f"### {slug}\n\n")
                f.write(f"URL: {url}\n")
                f.write(f"Error: {e}\n\n")
                errors += 1
                print(f"    Error: {e}")

        f.write(f"---\n\nCrawl complete: {success} pages fetched, {errors} errors\n")

    print(f"\nDone: {out} ({success} pages, {errors} errors)")


if __name__ == "__main__":
    main()
