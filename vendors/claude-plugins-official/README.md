# Vendored: anthropics/skills

> Upstream: https://github.com/anthropics/skills
> Marketplace name: `anthropic-agent-skills`
> Vendored on: 2026-04-09

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks.

## Repository Structure

```
.claude-plugin/
  marketplace.json          # Plugin marketplace manifest (3 plugins, 17 skills)
skills/
  algorithmic-art/          # Generative art via p5.js (templates/)
  brand-guidelines/         # Anthropic brand identity standards
  canvas-design/            # Visual art in PDF/PNG (canvas-fonts/)
  claude-api/               # Claude API/SDK docs
  doc-coauthoring/          # Structured doc co-authoring workflow
  docx/                     # Word document operations (scripts/)
  frontend-design/          # Production-grade UI design guidance
  internal-comms/           # Internal company communications (examples/)
  mcp-builder/              # MCP server development guide (reference/ scripts/)
  pdf/                      # PDF operations (scripts/, forms.md, reference.md)
  pptx/                     # PowerPoint operations (scripts/, editing.md, pptxgenjs.md)
  skill-creator/            # Build new skills (agents/ assets/ eval-viewer/ references/ scripts/)
  slack-gif-creator/        # Animated GIFs for Slack (core/)
  theme-factory/            # Theme styling toolkit (themes/, theme-showcase.pdf)
  web-artifacts-builder/    # React/Tailwind claude.ai artifacts (scripts/)
  webapp-testing/           # Playwright web testing (examples/ scripts/)
  xlsx/                     # Spreadsheet operations (scripts/)
spec/
  agent-skills-spec.md      # -> https://agentskills.io/specification
template/
  SKILL.md                  # Blank skill template
```

## Marketplace Plugins

The marketplace.json defines three installable plugins:

### document-skills
Proprietary document processing suite (source-available, not open source):
- `xlsx` - Spreadsheet creation/editing/analysis
- `docx` - Word document operations
- `pptx` - PowerPoint presentation operations
- `pdf` - PDF creation/reading/manipulation

### example-skills
Open source (Apache 2.0) examples demonstrating various capabilities:
- `algorithmic-art` - Generative art via p5.js
- `brand-guidelines` - Anthropic brand styling
- `canvas-design` - Visual art creation
- `doc-coauthoring` - Documentation workflow
- `frontend-design` - Production UI design
- `internal-comms` - Company communications
- `mcp-builder` - MCP server development
- `skill-creator` - Skill authoring tool
- `slack-gif-creator` - Animated GIFs for Slack
- `theme-factory` - Theme styling system
- `web-artifacts-builder` - React/shadcn artifacts
- `webapp-testing` - Playwright testing toolkit

### claude-api
Claude API and SDK documentation skill:
- `claude-api` - Multi-language SDK reference (TS, Python, Java, Go, Ruby, C#, PHP, cURL)

## Installation (Claude Code)

```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
/plugin install claude-api@anthropic-agent-skills
```

## Vendor Notes

This is a stub vendor -- SKILL.md files contain summarized metadata and descriptions extracted from the upstream repo. Subdirectories for scripts, templates, references, and examples are created as empty placeholders matching the upstream structure. Full file contents (scripts, templates, reference docs, etc.) are not included and should be fetched from upstream if needed.

## Third-Party Dependencies

- imageio 2.37.0 (BSD 2-Clause)
- imageio-ffmpeg 0.6.0 (BSD 2-Clause)
- FFmpeg 7.0.2 (GPLv3)
- Pillow 11.3.0 (MIT-CMU / HPND)
- 24 fonts (SIL Open Font License v1.1)
