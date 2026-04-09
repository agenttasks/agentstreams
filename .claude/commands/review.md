Review code changes for correctness, security, and architecture issues. Run the code-review skill with the security-auditor, code-generator, and architecture-reviewer agents in parallel.

Check:
1. Logic errors and missing error handling
2. OWASP vulnerabilities and hardcoded secrets
3. ANTHROPIC_API_KEY never used (must use CLAUDE_CODE_OAUTH_TOKEN)
4. MemPalace conventions respected
5. Agent tool grants follow least privilege
6. Model names use hyphen format (claude-opus-4-6)

Output a structured verdict: PASS, NEEDS_REMEDIATION, or BLOCK.
