---
name: review-security
description: "Security review for skill PRs — auth violations, hardcoded secrets, unsafe code patterns, credential exposure"
trigger: "reviewing PR diffs for auth violations, hardcoded secrets, unsafe code patterns, or credential exposure"
---

# Security Review

Analyze the PR diff for security issues in the crawl-ingest skill files.

## Checks

### 1. Auth Violations
- `ANTHROPIC_API_KEY` must NEVER appear in code or config
- Exception: the single "never use" warning in SKILL.md
- All auth must use `CLAUDE_CODE_OAUTH_TOKEN`
- Check: curl examples, GitHub Actions configs, environment variable references

### 2. Hardcoded Credentials
- No API keys, tokens, passwords, or secrets in any example code
- No real URLs with auth parameters
- No `.env` files or credential patterns committed

### 3. Unsafe Shell Patterns
- Unquoted `$variables` in shell scripts (word splitting, glob expansion)
- `eval` usage
- Command injection via string interpolation in curl/bash examples
- Missing `set -euo pipefail` in shell scripts

### 4. Injection Vectors
- SQL injection in SQLite examples (string concatenation instead of parameterized queries)
- XSS in HTML handling examples
- SSRF in crawler URL handling (following redirects to internal networks)
- Path traversal in file read/write patterns

### 5. Unsafe Dependencies
- Known vulnerable package versions
- Packages from untrusted sources

## Output

Return a structured JSON verdict:
```json
{
  "safe": true,
  "severity": "none",
  "issues": [],
  "blockers": []
}
```

Severity levels: `none`, `low`, `medium`, `high`, `critical`

Any `high` or `critical` issue sets `safe: false` and must go into `blockers`.
