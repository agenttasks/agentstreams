# Financial Services Plugins

This is a marketplace of Claude Cowork plugins for financial services professionals.
Each subdirectory is a standalone plugin.

## Repository Structure

```
├── financial-analysis/    # Core — shared modeling tools + MCP connectors
├── investment-banking/    # CIMs, teasers, merger models, strip profiles
├── equity-research/       # Earnings analysis, coverage initiation, catalysts
├── private-equity/        # Deal sourcing, IC memos, portfolio monitoring
├── wealth-management/     # Client prep, financial plans, rebalancing
├── partner-built/lseg/    # LSEG fixed income, FX, macro analytics
├── partner-built/spglobal/# S&P Global tearsheets, earnings, funding
└── claude-in-office/      # Microsoft 365 add-in deployment wizard
```

## Plugin Structure

Each plugin follows this layout:

```
plugin-name/
├── .claude-plugin/plugin.json
├── commands/
├── skills/
├── hooks/
├── mcp/
└── .claude/
```

## Key Files

- `plugin.json`: Plugin metadata — name, description, version
- `commands/*.md`: Slash commands invoked as `/plugin:command-name`
- `skills/*/SKILL.md`: Detailed knowledge and workflows for specific tasks

## Development Workflow

1. Edit markdown files directly — changes take effect immediately
2. Test commands with `/plugin:command-name` syntax
3. Skills are invoked automatically when their trigger conditions match
