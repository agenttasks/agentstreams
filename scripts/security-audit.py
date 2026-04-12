#!/usr/bin/env python3
"""Static security audit for the agentstreams codebase.

Scans for vulnerabilities relevant to AI agent ecosystems:
1. Shell injection — unsanitized inputs to subprocess/os.system/eval
2. Prompt injection vectors — crawled content that could manipulate LLM behavior
3. Agent boundary violations — subagent definitions with overly broad tool access
4. Secret leakage — API keys, tokens, credentials in committed files
5. Dependency risks — known risky imports or patterns

Designed as a deterministic, regex-based scanner (no LLM needed).
Runs in CI as a security gate alongside existing validation.

Usage:
  uv run scripts/security-audit.py                    # Audit full codebase
  uv run scripts/security-audit.py --check-only       # Exit 1 on any finding
  uv run scripts/security-audit.py --paths scripts/   # Audit specific paths
"""

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


# ── Finding types ──────────────────────────────────────────


class Finding:
    """A single security finding."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

    def __init__(self, severity: str, category: str, file: Path, line: int, message: str):
        self.severity = severity
        self.category = category
        self.file = file
        self.line = line
        self.message = message

    def __str__(self):
        rel = (
            self.file.relative_to(PROJECT_ROOT)
            if self.file.is_relative_to(PROJECT_ROOT)
            else self.file
        )
        return f"[{self.severity}] {self.category} — {rel}:{self.line} — {self.message}"


# ── Check 1: Shell injection ──────────────────────────────

SHELL_INJECTION_PATTERNS = [
    # Direct shell execution with string formatting
    (r"os\.system\s*\(", "os.system() — use subprocess.run() with shell=False"),
    (r"os\.popen\s*\(", "os.popen() — use subprocess.run() with shell=False"),
    (r"subprocess\.\w+\(.*shell\s*=\s*True", "subprocess with shell=True — pass args as list"),
    (r"eval\s*\(", "eval() — never evaluate untrusted strings"),
    (r"exec\s*\(", "exec() — never execute untrusted code"),
    (r"__import__\s*\(", "__import__() — use importlib for dynamic imports"),
]

# Context patterns that indicate safe usage (in comments, strings describing what NOT to do, regex defs)
SAFE_CONTEXT = re.compile(
    r"(?:never|don.?t|avoid|unsafe|warning|danger|#|\"\"\"|\br['\"]|re\.compile|PATTERNS\s*=)",
    re.IGNORECASE,
)


def check_shell_injection(file: Path, content: str) -> list[Finding]:
    """Scan for unsafe shell execution patterns."""
    # Only check executable code, not documentation
    if file.suffix != ".py":
        return []
    findings = []
    for i, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        # Skip comments and docstrings
        if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
            continue
        for pattern, message in SHELL_INJECTION_PATTERNS:
            if re.search(pattern, line):
                # Check if it's in a safe context (warning/doc)
                if SAFE_CONTEXT.search(line):
                    continue
                findings.append(Finding(Finding.CRITICAL, "shell-injection", file, i, message))
    return findings


# ── Check 2: Prompt injection vectors ─────────────────────

INJECTION_PATTERNS = [
    (r"ignore\s+(?:all\s+)?previous\s+instructions", "Classic prompt injection attempt"),
    (r"you\s+are\s+now\s+(?:a\s+)?(?:DAN|jailbreak)", "Jailbreak pattern"),
    (r"system:\s*you\s+(?:must|should|are)", "Fake system message injection"),
    (r"<\s*(?:system|admin|root)\s*>", "XML tag injection attempting privilege escalation"),
    (r"ANTHROPIC_API_KEY\s*=\s*['\"]sk-", "Hardcoded API key"),
    (r"(?:api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}", "Hardcoded secret value"),
]

# Files where injection patterns are expected (test files, security docs, eval fixtures)
INJECTION_ALLOWLIST = {
    "security-audit.py",  # this file defines the patterns
    "test_security_audit.py",  # tests for this scanner
    "test_validate_skills.py",  # test fixtures with fake API keys
    "test_injection_fixtures.py",  # M10 injection fixture tests
    "evals.md",  # eval frameworks discuss injection patterns
    # M10 injection test fixtures (intentionally contain malicious patterns)
    "injection_classic.md",
    "injection_secrets.md",
    "injection_polyglot.md",
    "injection_agent_boundary.md",
    "injection_agent_write_tools.md",
    "injection_agent_wildcard.md",
}


def check_prompt_injection(file: Path, content: str) -> list[Finding]:
    """Scan for prompt injection vectors in content files."""
    if file.name in INJECTION_ALLOWLIST:
        return []
    findings = []
    for i, line in enumerate(content.splitlines(), 1):
        for pattern, message in INJECTION_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                severity = (
                    Finding.CRITICAL
                    if "API_KEY" in message or "secret" in message.lower()
                    else Finding.HIGH
                )
                findings.append(Finding(severity, "prompt-injection", file, i, message))
    return findings


# ── Check 3: Agent boundary violations ────────────────────

# Tools that should NOT appear in read-only agents
DANGEROUS_TOOLS = {"Write", "Edit", "NotebookEdit"}
# Note: Bash is intentionally excluded — read-only agents like security-auditor
# and test-runner legitimately need Bash for scanning and test execution.

# Required constraints for agent definitions
REQUIRED_AGENT_CONSTRAINTS = {"Read"}  # at minimum, agents should have Read


def check_agent_boundaries(file: Path, content: str) -> list[Finding]:
    """Verify agent definitions have appropriate tool restrictions."""
    if not file.name.endswith(".md") or not str(file).endswith(".claude/agents/" + file.name):
        # Only check files in .claude/agents/
        if ".claude/agents/" not in str(file):
            return []

    findings = []

    # Parse YAML frontmatter
    if not content.startswith("---"):
        findings.append(
            Finding(Finding.MEDIUM, "agent-boundary", file, 1, "Agent missing YAML frontmatter")
        )
        return findings

    frontmatter_end = content.find("---", 3)
    if frontmatter_end == -1:
        return findings

    frontmatter = content[3:frontmatter_end]

    # Check for tools declaration
    tools_match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
    if not tools_match:
        findings.append(
            Finding(
                Finding.HIGH,
                "agent-boundary",
                file,
                1,
                "Agent has no tools restriction — defaults to all tools",
            )
        )
        return findings

    tools = {t.strip() for t in tools_match.group(1).split(",")}

    # Check for dangerous tools in agents that should be read-only
    description_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    description = description_match.group(1).lower() if description_match else ""

    read_only_signals = [
        "read",
        "analyz",
        "extract",
        "inspect",
        "scan",
        "check",
        "validate",
        "audit",
    ]
    write_signals = ["write", "create", "generat", "build", "develop", "optimiz", "migrat"]
    has_write_intent = any(signal in description for signal in write_signals)
    is_read_only_intent = (
        any(signal in description for signal in read_only_signals) and not has_write_intent
    )

    if is_read_only_intent:
        dangerous_found = tools & DANGEROUS_TOOLS
        if dangerous_found:
            findings.append(
                Finding(
                    Finding.HIGH,
                    "agent-boundary",
                    file,
                    1,
                    f"Read-only agent has write tools: {', '.join(sorted(dangerous_found))}",
                )
            )

    # Check for wildcard tool access
    if "*" in tools or "All" in tools:
        findings.append(
            Finding(
                Finding.HIGH,
                "agent-boundary",
                file,
                1,
                "Agent has wildcard tool access — restrict to minimum",
            )
        )

    return findings


# ── Check 4: Secret leakage ──────────────────────────────

SECRET_PATTERNS = [
    (r"sk-ant-[\w-]{20,}", "Anthropic API key"),
    (r"sk-[\w-]{32,}", "Generic API key (sk- prefix)"),
    (r"ghp_[\w]{36}", "GitHub personal access token"),
    (r"gho_[\w]{36}", "GitHub OAuth token"),
    (r"github_pat_[\w]{22}_[\w]{59}", "GitHub fine-grained PAT"),
    (r"xoxb-[\w-]+", "Slack bot token"),
    (r"xoxp-[\w-]+", "Slack user token"),
    (r"eyJ[\w-]+\.eyJ[\w-]+\.[\w-]+", "JWT token"),
    (r"AKIA[\w]{16}", "AWS access key ID"),
    (r"postgres://[\w:]+@[\w.-]+:\d+/\w+", "Database connection string"),
    (r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", "Private key"),
]

SECRET_ALLOWLIST_PATTERNS = [
    r"example",
    r"placeholder",
    r"your[_-]",
    r"<[\w-]+>",  # template variables like <your-key>
    r"\.\.\.",
    r"xxx",
    r"goes-here",
    r"secret-[\w-]+-key",  # placeholder patterns like sk-secret-openai-api-key-goes-here
    r"test[_-]?key",
    r"fake",
    r"dummy",
]


def check_secret_leakage(file: Path, content: str) -> list[Finding]:
    """Scan for hardcoded secrets and credentials."""
    if file.name in INJECTION_ALLOWLIST:
        return []
    # Skip binary-ish files and lockfiles
    if file.suffix in {".lock", ".pdf", ".png", ".jpg", ".gif"}:
        return []

    findings = []
    for i, line in enumerate(content.splitlines(), 1):
        for pattern, message in SECRET_PATTERNS:
            match = re.search(pattern, line)
            if match:
                # Check if it's a placeholder/example
                context = line.lower()
                if any(re.search(ap, context) for ap in SECRET_ALLOWLIST_PATTERNS):
                    continue
                findings.append(Finding(Finding.CRITICAL, "secret-leakage", file, i, message))
    return findings


# ── Check 5: Dependency risks ─────────────────────────────

RISKY_IMPORTS = [
    (r"import\s+pickle\b", "pickle — unsafe deserialization, use json instead"),
    (r"from\s+pickle\s+import", "pickle — unsafe deserialization"),
    (r"import\s+marshal\b", "marshal — unsafe deserialization"),
    (r"yaml\.load\s*\((?!.*Loader)", "yaml.load without SafeLoader — use yaml.safe_load"),
    (r"import\s+shelve\b", "shelve — uses pickle internally"),
    (
        r"from\s+xml\.etree.*import.*parse(?!_sitemap)",
        "XML parsing — ensure defusedxml for untrusted input",
    ),
]


def check_dependency_risks(file: Path, content: str) -> list[Finding]:
    """Scan for risky import patterns."""
    if file.suffix != ".py":
        return []
    findings = []
    for i, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for pattern, message in RISKY_IMPORTS:
            if re.search(pattern, line):
                findings.append(Finding(Finding.MEDIUM, "dependency-risk", file, i, message))
    return findings


# ── Check 6: Crawled content safety ──────────────────────


def check_crawled_content_handling(file: Path, content: str) -> list[Finding]:
    """Verify crawled content is never passed to eval/exec/shell."""
    if file.suffix != ".py":
        return []
    if file.name in {"security-audit.py", "test_security_audit.py"}:
        return []
    findings = []

    # Check if file reads taxonomy/crawled data
    reads_crawl = bool(re.search(r"taxonomy/|crawl|sitemap", content))
    if not reads_crawl:
        return []

    # If it reads crawl data, verify it never evals the content
    for i, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.search(r"eval\s*\(.*content", line) or re.search(r"exec\s*\(.*content", line):
            findings.append(
                Finding(
                    Finding.CRITICAL,
                    "crawl-safety",
                    file,
                    i,
                    "Crawled content passed to eval/exec — never evaluate untrusted data",
                )
            )
        if re.search(r"subprocess.*content|os\.system.*content", line):
            findings.append(
                Finding(
                    Finding.CRITICAL,
                    "crawl-safety",
                    file,
                    i,
                    "Crawled content passed to shell — never execute untrusted data",
                )
            )
    return findings


# ── Scanner orchestrator ──────────────────────────────────

ALL_CHECKS = [
    check_shell_injection,
    check_prompt_injection,
    check_agent_boundaries,
    check_secret_leakage,
    check_dependency_risks,
    check_crawled_content_handling,
]

# File extensions to scan
SCAN_EXTENSIONS = {".py", ".md", ".yml", ".yaml", ".sh", ".toml", ".txt", ".json"}

# Directories to skip
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "vendor", ".pytest_cache"}

# Directories with crawled/generated content — only check for real secrets, skip code-level checks
CRAWLED_CONTENT_DIRS = {"taxonomy"}

# Checks that should NOT run on crawled/generated content (too many false positives from docs)
CODE_LEVEL_CHECKS = {check_shell_injection, check_prompt_injection, check_dependency_risks}


def scan_file(file: Path) -> list[Finding]:
    """Run all checks against a single file."""
    try:
        content = file.read_text(errors="replace")
    except (OSError, UnicodeDecodeError):
        return []

    # Determine if file is in crawled content directory
    is_crawled = any(d in file.parts for d in CRAWLED_CONTENT_DIRS)

    findings = []
    for check in ALL_CHECKS:
        # Skip code-level checks on crawled content (docs mention eval/exec/keys as examples)
        if is_crawled and check in CODE_LEVEL_CHECKS:
            continue
        findings.extend(check(file, content))
    return findings


def scan_directory(root: Path, paths: list[str] | None = None) -> list[Finding]:
    """Scan a directory tree for security findings."""
    findings = []

    if paths:
        # Scan specific paths
        for p in paths:
            target = root / p
            if target.is_file() and target.suffix in SCAN_EXTENSIONS:
                findings.extend(scan_file(target))
            elif target.is_dir():
                for file in sorted(target.rglob("*")):
                    if file.is_file() and file.suffix in SCAN_EXTENSIONS:
                        if not any(skip in file.parts for skip in SKIP_DIRS):
                            findings.extend(scan_file(file))
    else:
        # Scan entire project
        for file in sorted(root.rglob("*")):
            if file.is_file() and file.suffix in SCAN_EXTENSIONS:
                if not any(skip in file.parts for skip in SKIP_DIRS):
                    findings.extend(scan_file(file))

    return findings


# ── Report ────────────────────────────────────────────────


def print_report(findings: list[Finding]) -> None:
    """Print a formatted security report."""
    if not findings:
        print("Security audit: PASS — no findings", file=sys.stderr)
        return

    # Group by severity
    by_severity: dict[str, list[Finding]] = {}
    for f in findings:
        by_severity.setdefault(f.severity, []).append(f)

    print(f"\nSecurity Audit Report — {len(findings)} finding(s)\n", file=sys.stderr)

    for severity in [Finding.CRITICAL, Finding.HIGH, Finding.MEDIUM, Finding.LOW]:
        group = by_severity.get(severity, [])
        if group:
            print(f"{'=' * 60}", file=sys.stderr)
            print(f"{severity} ({len(group)})", file=sys.stderr)
            print(f"{'=' * 60}", file=sys.stderr)
            for f in group:
                print(f"  {f}", file=sys.stderr)
            print(file=sys.stderr)

    # Summary
    crit = len(by_severity.get(Finding.CRITICAL, []))
    high = len(by_severity.get(Finding.HIGH, []))
    med = len(by_severity.get(Finding.MEDIUM, []))
    low = len(by_severity.get(Finding.LOW, []))
    print(
        f"Summary: {crit} critical, {high} high, {med} medium, {low} low",
        file=sys.stderr,
    )


def main():
    parser = argparse.ArgumentParser(description="Static security audit for agentstreams")
    parser.add_argument(
        "--check-only", action="store_true", help="Exit 1 on any CRITICAL or HIGH finding"
    )
    parser.add_argument(
        "--paths", nargs="*", help="Specific paths to scan (relative to project root)"
    )
    parser.add_argument("--root", default=str(PROJECT_ROOT), help="Project root directory")
    args = parser.parse_args()

    root = Path(args.root)
    findings = scan_directory(root, args.paths)
    print_report(findings)

    if args.check_only:
        critical_or_high = [f for f in findings if f.severity in (Finding.CRITICAL, Finding.HIGH)]
        if critical_or_high:
            print(
                f"\nFAILED: {len(critical_or_high)} critical/high finding(s) — fix before merging",
                file=sys.stderr,
            )
            sys.exit(1)
        else:
            print("\nPASSED: no critical or high findings", file=sys.stderr)


if __name__ == "__main__":
    main()
