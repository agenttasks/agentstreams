## Summary

<!-- 1-3 bullet points describing what this PR does and why -->

-

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Refactor (no functional change)
- [ ] Agent config change (`.claude/agents/` or `.claude/subagents/`)
- [ ] Webapp change (`webapp/`)
- [ ] CI/CD or workflow change (`.github/`)
- [ ] Documentation
- [ ] Dependency update

## Checklist

### Required (all PRs)

- [ ] `make ci` passes locally (lint, test, build, validate)
- [ ] No `ANTHROPIC_API_KEY` usage (auth flows through `CLAUDE_CODE_OAUTH_TOKEN`)
- [ ] No hardcoded credentials or secrets
- [ ] Model names use hyphen format (`claude-opus-4-6`, `claude-sonnet-4-6`)

### If modifying agents

- [ ] No agent has `Agent` in tools (only `coordinator` may spawn subagents)
- [ ] Read-only agents have `disallowedTools: Edit, Write`
- [ ] Model assignment follows hierarchy (opus/sonnet/haiku)
- [ ] Inoculation block present for security-critical agents
- [ ] `src/orchestrator.py` updated to match frontmatter changes
- [ ] `opus-orchestrator.md` subagent roster updated

### If modifying webapp

- [ ] `cd webapp && npx tsc --noEmit` passes
- [ ] `cd webapp && npx next build` produces static export
- [ ] No `dangerouslySetInnerHTML` or XSS vectors

### If modifying safety-research references

- [ ] Star counts consistent across files
- [ ] Repo URLs valid (`github.com/safety-research/...`)
- [ ] Pip-installable packages added to `pyproject.toml [safety]` if applicable

## Test plan

<!-- How to verify these changes work -->

-

## Related

<!-- Link to issues, other PRs, or safety-research repos if relevant -->
