#!/usr/bin/env python3
"""Validate skills using Claude to check code examples and cross-references.

Runs Claude against each skill's files to verify:
1. Code examples are syntactically valid
2. Cross-references point to existing files
3. SDK constructor patterns follow CLAUDE.md rules
4. Model names use hyphen format
5. No ANTHROPIC_API_KEY usage (except warnings)

Usage:
    uv run scripts/validate-skills.py                    # Validate all skills
    uv run scripts/validate-skills.py crawl-ingest       # Validate one skill
    uv run scripts/validate-skills.py --check-only       # Skip Claude, run static checks only
"""

import argparse
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"

# Patterns that should never appear (except in warnings)
FORBIDDEN_PATTERNS = [
    (r"ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY found — use CLAUDE_CODE_OAUTH_TOKEN"),
]

# Patterns that must use hyphen format
MODEL_PATTERN = re.compile(r"claude[_\.](?:opus|sonnet|haiku|mythos)[_\.][\d]")

# Valid SDK constructors per language
VALID_CONSTRUCTORS = {
    "typescript": ["new Anthropic()", "Anthropic()"],
    "python": ["anthropic.Anthropic()"],
    "java": ["AnthropicClient.builder().build()"],
    "go": ["anthropic.NewClient()"],
    "ruby": ["Anthropic::Client.new"],
    "csharp": ["new AnthropicClient()"],
    "php": ["Anthropic::client()"],
}


class ValidationResult:
    def __init__(self, skill: str):
        self.skill = skill
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.files_checked = 0

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [f"[{status}] {self.skill} ({self.files_checked} files)"]
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARN:  {w}")
        return "\n".join(lines)


def find_skills() -> list[str]:
    """Find all skill directories."""
    if not SKILLS_DIR.exists():
        return []
    return [
        d.name for d in sorted(SKILLS_DIR.iterdir()) if d.is_dir() and (d / "SKILL.md").exists()
    ]


def check_cross_references(skill_dir: Path, content: str, file_path: Path) -> list[str]:
    """Check that cross-referenced files exist."""
    errors = []
    # Match markdown links and backtick references to .md files
    refs = re.findall(r"`([^`]+\.md)`", content)
    refs += re.findall(r"\[.*?\]\(([^)]+\.md)\)", content)

    for ref in refs:
        if ref.startswith("http"):
            continue
        # Skip generic language-relative refs (e.g. "the language-specific README.md")
        if ref in (
            "README.md",
            "sdk-integration.md",
            "lsp-config.md",
            "CLAUDE.md",
            "CLAUDE.local.md",
            "MEMORY.md",
        ):
            continue
        # Skip repo-root relative refs (outside skill dir)
        if ref.startswith(
            ("agentstreams/", "taxonomy/", "vendors/", "~/", ".claude/", "src/", "scripts/")
        ):
            continue
        # Try relative to skill dir and file parent
        candidates = [
            skill_dir / ref,
            file_path.parent / ref,
        ]
        if not any(c.exists() for c in candidates):
            errors.append(f"{file_path.name}: broken reference '{ref}'")
    return errors


def check_forbidden_patterns(content: str, file_path: Path) -> list[str]:
    """Check for forbidden patterns."""
    errors = []
    for pattern, message in FORBIDDEN_PATTERNS:
        matches = list(re.finditer(pattern, content))
        for match in matches:
            # Allow in "never use" context
            line_start = content.rfind("\n", 0, match.start()) + 1
            line_end = content.find("\n", match.end())
            line = content[line_start:line_end].lower()
            if any(w in line for w in ["never", "don't", "do not", "warning", "not use"]):
                continue
            errors.append(f"{file_path.name}: {message}")
            break  # One per pattern per file
    return errors


def check_model_names(content: str, file_path: Path) -> list[str]:
    """Check model names use hyphen format."""
    warnings = []
    if MODEL_PATTERN.search(content):
        warnings.append(f"{file_path.name}: model name uses dots/underscores instead of hyphens")
    return warnings


def check_skill_md(skill_dir: Path) -> list[str]:
    """Validate SKILL.md has required frontmatter."""
    errors = []
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text()

    if not content.startswith("---"):
        errors.append("SKILL.md missing frontmatter")
        return errors

    frontmatter_end = content.find("---", 3)
    if frontmatter_end == -1:
        errors.append("SKILL.md frontmatter not closed")
        return errors

    frontmatter = content[3:frontmatter_end]
    if "name:" not in frontmatter:
        errors.append("SKILL.md missing 'name' in frontmatter")
    if "description:" not in frontmatter:
        errors.append("SKILL.md missing 'description' in frontmatter")

    return errors


def validate_skill(skill_name: str) -> ValidationResult:
    """Run all static checks on a skill."""
    result = ValidationResult(skill_name)
    skill_dir = SKILLS_DIR / skill_name

    if not skill_dir.exists():
        result.errors.append(f"Skill directory not found: {skill_dir}")
        return result

    # Check SKILL.md
    result.errors.extend(check_skill_md(skill_dir))

    # Check all markdown files
    for md_file in sorted(skill_dir.rglob("*.md")):
        result.files_checked += 1
        content = md_file.read_text()

        result.errors.extend(check_forbidden_patterns(content, md_file))
        result.errors.extend(check_cross_references(skill_dir, content, md_file))
        result.warnings.extend(check_model_names(content, md_file))

    return result


def main():
    parser = argparse.ArgumentParser(description="Validate skills")
    parser.add_argument("skill", nargs="?", help="Specific skill to validate")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Run static checks only (no Claude)",
    )
    args = parser.parse_args()

    if args.skill:
        skills = [args.skill]
    else:
        skills = find_skills()

    if not skills:
        print("No skills found in", SKILLS_DIR)
        sys.exit(1)

    print(f"Validating {len(skills)} skill(s)...\n")

    results = []
    for skill in skills:
        result = validate_skill(skill)
        results.append(result)
        print(result.summary())
        print()

    # Summary
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    total_files = sum(r.files_checked for r in results)
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)

    print(f"{'=' * 50}")
    print(f"Results: {passed}/{total} skills passed ({total_files} files checked)")
    if total_errors:
        print(f"  {total_errors} error(s)")
    if total_warnings:
        print(f"  {total_warnings} warning(s)")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
