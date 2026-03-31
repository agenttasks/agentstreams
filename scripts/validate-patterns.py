#!/usr/bin/env python3
"""Validate skill files against extracted documentation patterns.

Cross-references patterns extracted from crawled documentation (JSONL)
against skill files to find:
1. Stale model IDs — model names in skills not found in current docs
2. SDK constructor drift — constructor patterns that don't match docs
3. API surface coverage — methods used in skills vs documented methods
4. Topic coverage gaps — doc topics not represented in any skill

Usage:
  uv run scripts/validate-patterns.py <patterns_jsonl> <skills_dir>
  uv run scripts/validate-patterns.py /tmp/platform-patterns.jsonl skills/ --check-only
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── Pattern loading ───────────────────────────────────────


def load_patterns(jsonl_path: str) -> list[dict]:
    """Load pattern records from a JSONL file."""
    patterns = []
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if line:
                patterns.append(json.loads(line))
    return patterns


def aggregate_patterns(patterns: list[dict]) -> dict:
    """Aggregate patterns into summary collections."""
    model_ids: set[str] = set()
    sdk_patterns: set[str] = set()
    api_methods: set[str] = set()
    topics: dict[str, int] = {}
    code_langs: dict[str, int] = {}

    for p in patterns:
        for api in p.get("api_surface", []):
            # Extract model IDs
            if re.match(r"claude-(?:opus|sonnet|haiku)-[\w.-]+", api):
                model_ids.add(api)
            else:
                api_methods.add(api)

        for sdk in p.get("sdk_patterns", []):
            sdk_patterns.add(sdk)

        for topic in p.get("topics", []):
            topics[topic] = topics.get(topic, 0) + 1

        for lang in p.get("code_langs", []):
            code_langs[lang] = code_langs.get(lang, 0) + 1

    return {
        "model_ids": model_ids,
        "sdk_patterns": sdk_patterns,
        "api_methods": api_methods,
        "topics": topics,
        "code_langs": code_langs,
    }


# ── Skill scanning ────────────────────────────────────────


def scan_skill_files(skills_dir: Path) -> dict:
    """Scan skill markdown files for model IDs, SDK patterns, topics."""
    model_ids: set[str] = set()
    sdk_patterns: set[str] = set()
    api_refs: set[str] = set()
    languages: set[str] = set()

    for md_file in skills_dir.rglob("*.md"):
        try:
            content = md_file.read_text()
        except (OSError, UnicodeDecodeError):
            continue

        # Extract model IDs
        for match in re.findall(r"claude-(?:opus|sonnet|haiku)-[\w.-]+", content):
            model_ids.add(match)

        # Extract SDK constructor patterns
        sdk_regexes = [
            r"new\s+Anthropic\(\)",
            r"anthropic\.Anthropic\(\)",
            r"AnthropicClient\.builder\(\)\.build\(\)",
            r"anthropic\.NewClient\(\)",
            r"Anthropic::Client\.new",
            r"new\s+AnthropicClient\(\)",
            r"Anthropic::client\(\)",
        ]
        for pattern in sdk_regexes:
            if re.search(pattern, content):
                for m in re.findall(pattern, content):
                    sdk_patterns.add(m)

        # Extract API method references
        for match in re.findall(r"(?:client|anthropic)\.\w+\.\w+", content):
            api_refs.add(match)

        # Detect language directories
        rel = md_file.relative_to(skills_dir)
        if len(rel.parts) >= 2:
            lang_dir = rel.parts[1]
            known_langs = {
                "python",
                "typescript",
                "javascript",
                "java",
                "go",
                "ruby",
                "csharp",
                "php",
                "curl",
            }
            if lang_dir in known_langs:
                languages.add(lang_dir)

    return {
        "model_ids": model_ids,
        "sdk_patterns": sdk_patterns,
        "api_refs": api_refs,
        "languages": languages,
    }


# ── Validation checks ─────────────────────────────────────


def check_model_ids(doc_models: set[str], skill_models: set[str]) -> list[dict]:
    """Check for stale or unknown model IDs in skills."""
    findings = []

    # Clean up doc models — remove artifacts like "claude-opus-4-6The"
    clean_doc = {m for m in doc_models if not m[-1].isupper()}

    for model in skill_models:
        if model not in clean_doc and clean_doc:
            # Check if it's a known base model (without date suffix)
            base = re.sub(r"-\d{8}$", "", model)
            if base not in clean_doc and model not in clean_doc:
                findings.append(
                    {
                        "severity": "medium",
                        "category": "model-id",
                        "message": f"Model '{model}' in skills not found in current docs",
                    }
                )

    return findings


def check_sdk_constructors(doc_sdks: set[str], skill_sdks: set[str]) -> list[dict]:
    """Check SDK constructor patterns match documentation."""
    findings = []

    # Normalize patterns for comparison
    def normalize(s: str) -> str:
        return re.sub(r"\s+", "", s).lower()

    doc_normalized = {normalize(s): s for s in doc_sdks}
    skill_normalized = {normalize(s): s for s in skill_sdks}

    for norm, original in skill_normalized.items():
        if norm not in doc_normalized and doc_normalized:
            findings.append(
                {
                    "severity": "low",
                    "category": "sdk-constructor",
                    "message": f"SDK pattern '{original}' in skills not found in docs",
                }
            )

    return findings


def check_topic_coverage(
    doc_topics: dict[str, int],
    skills_dir: Path,
) -> list[dict]:
    """Check if major documentation topics are represented in skills."""
    findings = []

    # Read all skill content for topic matching
    all_skill_content = ""
    for md_file in skills_dir.rglob("*.md"):
        try:
            all_skill_content += md_file.read_text().lower() + "\n"
        except (OSError, UnicodeDecodeError):
            continue

    # Topics with significant doc coverage (>10 pages) that should appear in skills
    topic_keywords = {
        "tool-use": ["tool use", "tool calling", "function calling", "tool_use"],
        "streaming": ["streaming", "server-sent events", "stream"],
        "mcp": ["mcp", "model context protocol"],
        "agents": ["agent", "sub-agent", "subagent", "orchestrat"],
        "batch": ["batch", "message batch"],
        "vision": ["vision", "image", "multimodal", "pdf"],
        "extended-thinking": ["extended thinking", "think tool", "thinking"],
        "prompting": ["prompt engineering", "system prompt", "prompt caching"],
    }

    for topic, count in sorted(doc_topics.items(), key=lambda x: -x[1]):
        if count < 10:
            continue
        keywords = topic_keywords.get(topic, [topic.replace("-", " ")])
        found = any(kw in all_skill_content for kw in keywords)
        if not found:
            findings.append(
                {
                    "severity": "info",
                    "category": "topic-coverage",
                    "message": f"Topic '{topic}' ({count} doc pages) not found in skills",
                }
            )

    return findings


def check_language_coverage(
    doc_langs: dict[str, int],
    skill_langs: set[str],
) -> list[dict]:
    """Check if documented languages are represented in skills."""
    findings = []

    # Map doc language names to skill directory names
    lang_map = {
        "python": "python",
        "typescript": "typescript",
        "javascript": "javascript",
        "java": "java",
        "go": "go",
        "ruby": "ruby",
        "csharp": "csharp",
        "php": "php",
        "curl": "curl",
    }

    for doc_lang, count in sorted(doc_langs.items(), key=lambda x: -x[1]):
        if count < 5:
            continue
        skill_dir = lang_map.get(doc_lang)
        if skill_dir and skill_dir not in skill_langs:
            findings.append(
                {
                    "severity": "info",
                    "category": "language-coverage",
                    "message": f"Language '{doc_lang}' ({count} doc pages) missing from skills",
                }
            )

    return findings


# ── Report ────────────────────────────────────────────────


def print_report(
    doc_summary: dict,
    skill_summary: dict,
    findings: list[dict],
) -> None:
    """Print validation report."""
    print(f"\n{'=' * 60}", file=sys.stderr)
    print("Pattern-Driven Skill Validation", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    print("\nDocumentation coverage:", file=sys.stderr)
    print(f"  Model IDs: {len(doc_summary['model_ids'])}", file=sys.stderr)
    print(f"  SDK patterns: {len(doc_summary['sdk_patterns'])}", file=sys.stderr)
    print(f"  API methods: {len(doc_summary['api_methods'])}", file=sys.stderr)
    print(f"  Topics: {len(doc_summary['topics'])}", file=sys.stderr)
    print(f"  Languages: {len(doc_summary['code_langs'])}", file=sys.stderr)

    print("\nSkill coverage:", file=sys.stderr)
    print(f"  Model IDs: {len(skill_summary['model_ids'])}", file=sys.stderr)
    print(f"  SDK patterns: {len(skill_summary['sdk_patterns'])}", file=sys.stderr)
    print(f"  API refs: {len(skill_summary['api_refs'])}", file=sys.stderr)
    print(f"  Languages: {len(skill_summary['languages'])}", file=sys.stderr)

    if not findings:
        print("\n✓ No issues found", file=sys.stderr)
    else:
        by_severity: dict[str, list[dict]] = {}
        for f in findings:
            by_severity.setdefault(f["severity"], []).append(f)

        for severity in ["high", "medium", "low", "info"]:
            group = by_severity.get(severity, [])
            if group:
                print(f"\n{severity.upper()} ({len(group)}):", file=sys.stderr)
                for f in group:
                    print(f"  [{f['category']}] {f['message']}", file=sys.stderr)

    total = len(findings)
    actionable = len([f for f in findings if f["severity"] in ("high", "medium")])
    print(f"\nTotal: {total} findings ({actionable} actionable)", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)


# ── Main ─────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Validate skills against doc patterns")
    parser.add_argument("patterns_jsonl", help="Path to patterns JSONL file")
    parser.add_argument("skills_dir", help="Path to skills directory")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Exit 1 on any high/medium finding",
    )
    args = parser.parse_args()

    patterns = load_patterns(args.patterns_jsonl)
    doc_summary = aggregate_patterns(patterns)
    skills_dir = Path(args.skills_dir)
    skill_summary = scan_skill_files(skills_dir)

    findings = []
    findings.extend(check_model_ids(doc_summary["model_ids"], skill_summary["model_ids"]))
    findings.extend(
        check_sdk_constructors(doc_summary["sdk_patterns"], skill_summary["sdk_patterns"])
    )
    findings.extend(check_topic_coverage(doc_summary["topics"], skills_dir))
    findings.extend(check_language_coverage(doc_summary["code_langs"], skill_summary["languages"]))

    print_report(doc_summary, skill_summary, findings)

    if args.check_only:
        actionable = [f for f in findings if f["severity"] in ("high", "medium")]
        if actionable:
            sys.exit(1)


if __name__ == "__main__":
    main()
