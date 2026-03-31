#!/usr/bin/env python3
"""Extract structured patterns from crawled taxonomy markdown files.

Reads taxonomy files produced by crawl-sitemap.py and extracts:
- Page type (guide, reference, tutorial, blog, changelog, api-doc)
- Topic tags (tool-use, streaming, models, agents, mcp, evals, etc.)
- API surface (method names, model IDs, endpoint paths)
- Code languages detected in content
- SDK constructor patterns
- Cross-reference links to other documentation pages

Usage:
  uv run scripts/extract-patterns.py <taxonomy_file> [options]

Examples:
  uv run scripts/extract-patterns.py taxonomy/anthropic-blog.md
  uv run scripts/extract-patterns.py taxonomy/code-claude-com-full.md --en-only
  uv run scripts/extract-patterns.py taxonomy/platform-claude-com-full.md -o patterns/platform.jsonl
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── Page type classifiers ──────────────────────────────────

PAGE_TYPE_SIGNALS = {
    "blog": [r"Published\s+\w+\s+\d+,?\s+\d{4}", r"engineering/", r"research/"],
    "reference": [r"Parameters\b", r"Returns?\b.*\btype\b", r"Endpoint", r"api-reference"],
    "changelog": [r"changelog", r"what.?s.new", r"release.notes"],
    "tutorial": [r"step\s+\d", r"tutorial", r"getting.started", r"quickstart"],
    "guide": [r"guide", r"how.to", r"best.practices", r"overview"],
    "api-doc": [r"api\.anthropic\.com", r"messages\.create", r"completions"],
}


def classify_page_type(url: str, content: str) -> str:
    """Classify a page into a type based on URL and content signals."""
    text = (url + "\n" + content[:3000]).lower()
    scores: dict[str, int] = {}
    for ptype, patterns in PAGE_TYPE_SIGNALS.items():
        score = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
        if score > 0:
            scores[ptype] = score
    if not scores:
        return "guide"  # default
    return max(scores, key=scores.get)


# ── Topic extraction ───────────────────────────────────────

TOPIC_KEYWORDS = {
    "tool-use": [
        r"\btool.?use\b",
        r"\btool.?calling\b",
        r"\bfunction.?calling\b",
        r"\btool search\b",
    ],
    "streaming": [r"\bstreaming\b", r"\bserver.sent.events\b", r"\bSSE\b"],
    "models": [
        r"\bclaude.opus\b",
        r"\bclaude.sonnet\b",
        r"\bclaude.haiku\b",
        r"\bmodel.?selection\b",
    ],
    "agents": [r"\bagent\b", r"\bsub.?agent\b", r"\borchestrat\b", r"\bagentic\b"],
    "mcp": [r"\bMCP\b", r"\bmodel.context.protocol\b", r"\bmcp.?server\b"],
    "evals": [r"\beval\b", r"\bbenchmark\b", r"\bSWE.?bench\b", r"\bBrowseComp\b"],
    "prompting": [r"\bprompt.?engineering\b", r"\bsystem.prompt\b", r"\bprompt.?caching\b"],
    "vision": [r"\bvision\b", r"\bimage\b", r"\bmultimodal\b", r"\bPDF\b"],
    "embeddings": [r"\bembedding\b", r"\bvoyage\b", r"\bvector\b"],
    "context-window": [r"\bcontext.window\b", r"\btoken.?count\b", r"\bcontext.?length\b"],
    "safety": [r"\bsafety\b", r"\bguardrail\b", r"\bcontent.?filter\b", r"\bharmful\b"],
    "code-execution": [r"\bcode.?execution\b", r"\bsandbox\b", r"\bcomputer.?use\b"],
    "retrieval": [r"\bretrieval\b", r"\bRAG\b", r"\bcontextual.retrieval\b"],
    "claude-code": [r"\bclaude.code\b", r"\bCLI\b", r"\bclaude.?code.?best\b"],
    "hooks": [r"\bhook\b", r"\bpre.?commit\b", r"\bpost.?tool\b"],
    "memory": [r"\bmemory\b", r"\bCLAUDE\.md\b", r"\bauto.?memory\b"],
    "parallel": [r"\bparallel\b", r"\bconcurren\b", r"\basync\b"],
    "auth": [r"\bOAuth\b", r"\bauth\b", r"\bAPI.?key\b", r"\btoken\b"],
    "batch": [r"\bbatch\b", r"\bmessage.?batch\b"],
    "extended-thinking": [r"\bextended.?thinking\b", r"\bthink.?tool\b", r"\badaptive.?think\b"],
}


def extract_topics(content: str, max_topics: int = 5) -> list[str]:
    """Extract up to max_topics from content based on keyword signals."""
    text = content[:10000].lower()
    scores: dict[str, int] = {}
    for topic, patterns in TOPIC_KEYWORDS.items():
        score = sum(len(re.findall(p, text, re.IGNORECASE)) for p in patterns)
        if score > 0:
            scores[topic] = score
    return sorted(scores, key=scores.get, reverse=True)[:max_topics]


# ── API surface extraction ─────────────────────────────────

API_PATTERNS = [
    # Anthropic API methods
    r"(?:client|anthropic)\.\w+\.\w+(?:\.\w+)?",  # client.messages.create
    # Model IDs
    r"claude-(?:opus|sonnet|haiku)-[\w.-]+",
    # HTTP methods + paths
    r"(?:GET|POST|PUT|DELETE|PATCH)\s+/\w[\w/{}.-]*",
    # REST endpoints
    r"/v\d/\w[\w/{}.-]*",
]


def extract_api_surface(content: str) -> list[str]:
    """Extract API method names, model IDs, and endpoints."""
    found: set[str] = set()
    for pattern in API_PATTERNS:
        matches = re.findall(pattern, content[:20000])
        found.update(m.strip() for m in matches)
    return sorted(found)[:20]  # cap at 20


# ── Code language detection ────────────────────────────────

LANG_SIGNALS = {
    "python": [r"\bimport\s+anthropic\b", r"\bfrom\s+anthropic\b", r"\.py\b", r"python"],
    "typescript": [r"\bimport\s+Anthropic\b", r"from\s+['\"]@anthropic", r"\.ts\b", r"typescript"],
    "javascript": [r"\brequire\(['\"]@anthropic", r"\.js\b", r"javascript"],
    "java": [r"\bAnthropicClient\b", r"\.java\b", r"\bjava\b"],
    "go": [r"\banthropic\.NewClient\b", r"\.go\b", r"\bpackage\s+main\b"],
    "ruby": [r"\bAnthropic::Client\b", r"\.rb\b", r"\bruby\b"],
    "csharp": [r"\bnew\s+AnthropicClient\b", r"\.cs\b", r"\bcsharp\b"],
    "php": [r"\bAnthropic::client\b", r"\.php\b", r"\bphp\b"],
    "curl": [r"\bcurl\b.*api\.anthropic", r"\bcurl\s+-"],
    "bash": [r"\bbash\b", r"\bset\s+-euo\b", r"#!/bin/bash"],
}


def detect_code_languages(content: str) -> list[str]:
    """Detect programming languages mentioned or demonstrated."""
    text = content[:20000]
    found = []
    for lang, patterns in LANG_SIGNALS.items():
        if any(re.search(p, text, re.IGNORECASE) for p in patterns):
            found.append(lang)
    return sorted(found)


# ── SDK pattern extraction ─────────────────────────────────

SDK_PATTERNS = [
    r"new\s+Anthropic\(\)",
    r"anthropic\.Anthropic\(\)",
    r"AnthropicClient\.builder\(\)\.build\(\)",
    r"anthropic\.NewClient\(\)",
    r"Anthropic::Client\.new",
    r"new\s+AnthropicClient\(\)",
    r"Anthropic::client\(\)",
    r"client\.messages\.create",
    r"client\.completions\.create",
    r"messages\.create",
    r"client\.beta\.\w+",
    r"StreamableHTTPServerTransport",
    r"StdioServerTransport",
]


def extract_sdk_patterns(content: str) -> list[str]:
    """Extract SDK constructor and method patterns."""
    found: set[str] = set()
    for pattern in SDK_PATTERNS:
        matches = re.findall(pattern, content[:20000])
        found.update(matches)
    return sorted(found)


# ── Link extraction ────────────────────────────────────────


def extract_links(content: str, base_domain: str) -> list[str]:
    """Extract cross-reference links to documentation pages."""
    url_pattern = r"https?://[\w.-]+(?:/[\w./-]*)*"
    urls = re.findall(url_pattern, content[:20000])
    # Filter to same domain or known doc domains
    doc_domains = {base_domain, "code.claude.com", "platform.claude.com", "docs.anthropic.com"}
    links: set[str] = set()
    for url in urls:
        for domain in doc_domains:
            if domain in url:
                links.add(url)
                break
    return sorted(links)[:20]


# ── Taxonomy parser ────────────────────────────────────────

PAGE_SECTION_RE = re.compile(r"^### (.+)$", re.MULTILINE)


def parse_taxonomy_pages(text: str) -> list[dict]:
    """Parse taxonomy markdown into individual page records."""
    pages = []
    sections = PAGE_SECTION_RE.split(text)

    # sections[0] is frontmatter/header, then alternating slug/content
    for i in range(1, len(sections), 2):
        slug = sections[i].strip()
        body = sections[i + 1] if i + 1 < len(sections) else ""

        # Extract URL and content
        url_match = re.search(r"URL:\s*(https?://\S+)", body)
        url = url_match.group(1) if url_match else ""

        # Content is between ``` fences
        content_match = re.search(r"```\n(.*?)\n```", body, re.DOTALL)
        content = content_match.group(1) if content_match else body

        if url:
            pages.append({"slug": slug, "url": url, "content": content})

    return pages


def extract_domain(text: str) -> str:
    """Extract domain from taxonomy frontmatter."""
    match = re.search(r"^domain:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


# ── Main ─────────────────────────────────────────────────


def analyze_page(page: dict, domain: str) -> dict:
    """Extract all patterns from a single page."""
    url = page["url"]
    content = page["content"]

    return {
        "url": url,
        "slug": page["slug"],
        "page_type": classify_page_type(url, content),
        "topics": extract_topics(content),
        "api_surface": extract_api_surface(content),
        "code_langs": detect_code_languages(content),
        "sdk_patterns": extract_sdk_patterns(content),
        "links": extract_links(content, domain),
    }


def main():
    parser = argparse.ArgumentParser(description="Extract patterns from crawled taxonomy")
    parser.add_argument("taxonomy_file", help="Path to taxonomy markdown file")
    parser.add_argument("-o", "--output", help="Output JSONL file (default: stdout)")
    parser.add_argument("--en-only", action="store_true", help="Only process English pages (/en/)")
    parser.add_argument("--max-pages", type=int, default=0, help="Max pages to process (0=all)")
    parser.add_argument("--summary", action="store_true", help="Print summary stats to stderr")
    args = parser.parse_args()

    text = Path(args.taxonomy_file).read_text()
    domain = extract_domain(text)
    pages = parse_taxonomy_pages(text)

    if args.en_only:
        pages = [p for p in pages if "/en/" in p["url"]]

    if args.max_pages > 0:
        pages = pages[: args.max_pages]

    print(f"Processing {len(pages)} pages from {domain}...", file=sys.stderr)

    out = open(args.output, "w") if args.output else sys.stdout  # noqa: SIM115

    # Aggregate stats
    type_counts: dict[str, int] = {}
    topic_counts: dict[str, int] = {}
    lang_counts: dict[str, int] = {}
    total_api = 0
    total_sdk = 0
    total_links = 0

    for page in pages:
        result = analyze_page(page, domain)
        out.write(json.dumps(result) + "\n")

        # Accumulate stats
        ptype = result["page_type"]
        type_counts[ptype] = type_counts.get(ptype, 0) + 1
        for topic in result["topics"]:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        for lang in result["code_langs"]:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        total_api += len(result["api_surface"])
        total_sdk += len(result["sdk_patterns"])
        total_links += len(result["links"])

    if args.output:
        out.close()

    if args.summary or args.output:
        print(f"\n{'=' * 60}", file=sys.stderr)
        print(f"Pattern Extraction Summary — {domain}", file=sys.stderr)
        print(f"{'=' * 60}", file=sys.stderr)
        print(f"Pages analyzed: {len(pages)}", file=sys.stderr)
        print("\nPage types:", file=sys.stderr)
        for ptype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {ptype}: {count}", file=sys.stderr)
        print("\nTop topics:", file=sys.stderr)
        for topic, count in sorted(topic_counts.items(), key=lambda x: -x[1])[:15]:
            print(f"  {topic}: {count}", file=sys.stderr)
        print("\nCode languages:", file=sys.stderr)
        for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
            print(f"  {lang}: {count}", file=sys.stderr)
        print(f"\nAPI surface entries: {total_api}", file=sys.stderr)
        print(f"SDK patterns: {total_sdk}", file=sys.stderr)
        print(f"Cross-references: {total_links}", file=sys.stderr)
        print(f"{'=' * 60}", file=sys.stderr)


if __name__ == "__main__":
    main()
