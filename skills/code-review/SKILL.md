---
name: code-review
description: "Automated multi-agent PR review for knowledge-work codebases. TRIGGER when: user asks to review a PR, review code changes, catch bugs before merge, or run code review. DO NOT TRIGGER for: security-specific audits (use /security-review), general code questions, or single-file reviews."
---

# Code Review Skill

Automated PR review that catches logic errors, security vulnerabilities, and regressions using multi-agent analysis across the 14-layer knowledge-work architecture.

## Review Pipeline

```
PR diff → harmlessness-screen → parallel analysis → synthesis → verdict
                                    │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            code-generator    security-auditor   architecture-reviewer
            (correctness)     (vulnerabilities)  (design patterns)
```

## How to Use

1. Use the /review slash command in a Claude Code session
2. Or run the codegen eval: `agentstreams eval codegen --models sonnet`
3. Or run promptfoo suites: `agentstreams eval promptfoo`

## Review Checklist

For each file changed:

### Correctness (code-generator agent)
- Logic errors and off-by-one mistakes
- Missing error handling at system boundaries
- Type mismatches (Python: mypy/pyright, TypeScript: tsc)
- Untested edge cases

### Security (security-auditor agent)
- OWASP Top 10 vulnerabilities
- Hardcoded secrets or credentials
- ANTHROPIC_API_KEY never used (must use CLAUDE_CODE_OAUTH_TOKEN)
- Prompt injection vectors in user-facing prompts
- Unsafe subprocess calls

### Architecture (architecture-reviewer agent)
- Follows MemPalace wing/hall/tunnel conventions
- Agent tool grants match least-privilege principle
- No recursive agent spawning (only coordinator may use Agent tool)
- Cross-references in skills point to files that actually exist
- Model names use hyphen format (claude-opus-4-6, not dots)

### Knowledge-Work Specific
- Layer boundaries respected (L1 circuits don't depend on L8 evals)
- Prompt templates in SKILL.md files are syntactically valid
- MCP server configs have proper authentication
- Neon queries use parameterized statements (no SQL injection)

## Output Format

```json
{
  "verdict": "PASS | NEEDS_REMEDIATION | BLOCK",
  "severity": "none | low | medium | high | critical",
  "issues": [
    {
      "file": "src/cli.py",
      "line": 42,
      "severity": "medium",
      "category": "correctness",
      "agent": "code-generator",
      "message": "Missing error handling for subprocess.run timeout",
      "suggestion": "Add try/except subprocess.TimeoutExpired"
    }
  ],
  "summary": "One-sentence summary of review findings"
}
```

## Defaults

- Model: claude-opus-4-6 for security-auditor, claude-sonnet-4-6 for others
- Max files per review: 50
- Timeout per agent: 120 seconds
- Parallel agents: 3 (one per review dimension)
