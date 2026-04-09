# Financial Services Plugins

Plugins that turn Claude into a specialist for financial services — investment
banking, equity research, private equity, and wealth management. Built for
[Claude Cowork](https://claude.com/product/cowork), also compatible with
[Claude Code](https://claude.com/product/claude-code).

Source: [github.com/anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins)

## Plugins

| Plugin | Type | Skills | Connectors |
|--------|------|--------|------------|
| **financial-analysis** | Core | 11 | Daloopa, Morningstar, S&P Global, FactSet, Moody's, MT Newswires, Aiera, LSEG, PitchBook, Chronograph, Egnyte |
| **investment-banking** | Add-on | 9 | — |
| **equity-research** | Add-on | 9 | — |
| **private-equity** | Add-on | 10 | — |
| **wealth-management** | Add-on | 6 | — |
| **partner-built/lseg** | Partner | 8 | LSEG |
| **partner-built/spglobal** | Partner | 5 | S&P Global |
| **claude-in-office** | Office | 1 | Microsoft 365 |

**45 skills, 38 commands, 11 MCP integrations**

## Installation

```bash
claude plugin marketplace add anthropics/financial-services-plugins
claude plugin install financial-analysis@financial-services-plugins
claude plugin install equity-research@financial-services-plugins
```
