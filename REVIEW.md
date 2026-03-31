# Code Review Configuration

## Focus Areas

### Security (blocking)
- Hardcoded secrets, API keys, or credentials in code examples
- `ANTHROPIC_API_KEY` usage outside of "never use" warnings
- Unsafe shell patterns: unquoted variables, `eval`, command injection vectors
- SQL injection in SQLite examples
- SSRF patterns in crawler configurations
- Path traversal in file handling examples

### Consistency (blocking)
- Version numbers must match across SKILL.md, READMEs, package-matrix.md, and setup scripts
- Package names must be correct (e.g., `@modelcontextprotocol/sdk` not `@anthropic-ai/mcp`)
- Model names must use hyphen format (`claude-opus-4-6`, not `claude-opus-4.6` or date suffixes)
- Star counts for the same repo must be identical everywhere
- SDK constructor patterns must match actual APIs

### Accuracy (warning)
- Import paths and method names in code snippets
- Cross-references in "Further Reading" must point to existing files
- MCP SDK availability noted in every language README

## Ignore

- Markdown formatting style preferences (heading levels, list styles)
- Comment density in documentation files
- Line length in markdown prose
- Opinions about package version freshness (versions go stale; that's expected)
