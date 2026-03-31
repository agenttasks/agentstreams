# agentstreams

## Project

Multi-language skill system for Claude Code. Skills provide web crawling, Anthropic SDK integration, bloom filter deduplication, programmatic prompts (DSPy), LSP code intelligence, and evals — across 8 languages (TypeScript, Python, Java, Go, Ruby, C#, PHP, cURL).

## Auth

**Never use `ANTHROPIC_API_KEY`**. All auth flows through `CLAUDE_CODE_OAUTH_TOKEN`.

For SDK constructors:
- TypeScript: `new Anthropic()` (reads env automatically)
- Python: `anthropic.Anthropic()` (reads env automatically)
- Java: `AnthropicClient.builder().build()` (reads env automatically)
- Go: `anthropic.NewClient()` (reads env automatically)
- Ruby: `Anthropic::Client.new` (reads env automatically)
- C#: `new AnthropicClient()` (reads env automatically)
- PHP: `Anthropic::client()` (reads env automatically)
- cURL: `-H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN"`

## Review Criteria

When reviewing PRs, check:
- Model names use hyphen format: `claude-opus-4-6`, `claude-sonnet-4-6` (never dots or date suffixes)
- Versions are consistent across `SKILL.md`, language READMEs, `package-matrix.md`, and setup scripts
- Cross-references in "Further Reading" sections point to files that actually exist
- Every language README mentions its MCP SDK availability
- Star counts are consistent across files for the same repositories
- SDK constructor patterns match the actual SDK API for each language
- No `ANTHROPIC_API_KEY` anywhere except "never use" warnings

## Code Style

- Markdown: ATX headings, fenced code blocks with language tags
- Shell scripts: `set -euo pipefail`
- No trailing whitespace
- Python managed with `uv` exclusively — no `npm`/`node_modules`/`package.json` in this repo

## Stack

- Python only for executable code (managed with `uv`)
- Claude Code CLI with `CLAUDE_CODE_OAUTH_TOKEN` (Pro Max)
- Agent SDK: `claude-agent-sdk` run locally via scripts
