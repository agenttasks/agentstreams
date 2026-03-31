---
name: review-consistency
description: "Cross-file consistency check for crawl-ingest skill PRs. TRIGGER when: reviewing documentation PRs for version mismatches, broken cross-references, inconsistent package names, or missing MCP SDK mentions. DO NOT TRIGGER for: security issues, code logic, or formatting preferences."
---

# Consistency Review

Cross-check all files in `skills/crawl-ingest/` for internal consistency.

## Checks

### 1. Version Alignment
Compare version numbers across these files — they must agree:
- `SKILL.md` tier tables (authoritative source)
- Language-specific `README.md` files (install commands + package tables)
- `references/package-matrix.md` (equivalence matrix)
- `scripts/setup_*.sh` (install scripts)

Key packages to verify:
- Anthropic SDKs (Python, TypeScript, Java, Go, Ruby, C#, PHP)
- Agent SDKs (Python, TypeScript only)
- MCP SDKs (all languages)
- Web crawlers (Crawlee, Scrapy, crawler4j, Colly, Mechanize, Abot, Symfony)
- Bloom filters (bloom-filters, pybloom-live, Guava, bits-and-blooms, bloomer, BloomFilter.NetCore)

### 2. Model Name Format
All model references must use hyphen format:
- `claude-opus-4-6` (correct)
- `claude-sonnet-4-6` (correct)
- `claude-haiku-4-5` (correct)
- `claude-sonnet-4-20250514` (WRONG — date suffix)
- `claude-opus-4.6` (WRONG — dot instead of hyphen)

### 3. Star Counts
The same GitHub repository must show the same star count everywhere.
Check: SKILL.md, package-matrix.md, language READMEs.

### 4. Cross-References
Every path in "Further Reading" sections must resolve to an existing file.
Check with: `ls` or `Glob` for each referenced path.

### 5. SDK Constructor Patterns
Each language's code examples must use the correct constructor:
- TypeScript: `new Anthropic()`
- Python: `anthropic.Anthropic()`
- Java: `AnthropicClient.builder().build()`
- Go: `anthropic.NewClient()`
- Ruby: `Anthropic::Client.new`
- C#: `new AnthropicClient()`
- PHP: `Anthropic::client()`

### 6. MCP SDK Mentions
Every language README must note MCP SDK availability with:
- Package name / import path
- Maintainer (if notable: Google, Microsoft, JetBrains, Spring AI, PHP Foundation)
- Star count

### 7. Feature Completeness Scores
`package-matrix.md` scores must match actual capabilities documented in each language's files.

## Output

Post inline comments on specific lines where inconsistencies exist.
If no issues found, post a single approving comment: "Consistency check passed — no issues found."
