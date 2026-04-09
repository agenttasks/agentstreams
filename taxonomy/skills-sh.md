---
source: skills.sh sitemap crawl
domain: skills.sh
crawled_at: 2026-04-09T05:00:00Z
index_hash: a1b2c3d4e5f6
page_count: 4000
---

# skills.sh — Agent Skills Directory

URL: https://skills.sh
Platform: Next.js on Vercel
Total skills indexed: 4,000 across 629 GitHub orgs/repos

## Anthropic Plugin Repos (5)

### anthropics/knowledge-work-plugins (106 skills on skills.sh, 119 in repo)

17 plugins: bio-research, cowork-plugin-management, customer-support, data,
design, engineering, enterprise-search, finance, human-resources, legal,
marketing, operations, partner-built, pdf-viewer, product-management,
productivity, sales

Top skills by installs:
```
data-visualization     3.8K
task-management        1.7K
content-creation       1.5K
code-review            1.4K
memory-management      1.4K
competitive-intelligence 1.3K
knowledge-synthesis    1.2K
system-design          1.2K
```

### anthropics/financial-services-plugins (30 skills on skills.sh, 45 in repo)

5 plugins: financial-analysis (core), investment-banking, equity-research,
private-equity, wealth-management

Top skills by installs:
```
earnings-analysis      528
equity-research        517
macro-rates-monitor    412
ppt-template-creator   392
dcf-model              360
```

### anthropics/skills (17 skills)

3 plugins: document-skills, example-skills, claude-api

Skills: frontend-design, skill-creator, pdf, pptx, docx, webapp-testing,
xlsx, canvas-design, mcp-builder, algorithmic-art, doc-coauthoring,
brand-guidelines, web-artifacts-builder, theme-factory, internal-comms,
slack-gif-creator, claude-api

### anthropics/claude-code (9 skills)

agent-development, skill-development, mcp-integration, command-development,
hook-development, plugin-structure, plugin-settings, writing-hookify-rules,
claude-opus-4-5-migration

### anthropics/claude-plugins-official (6 skills)

claude-md-improver, claude-automation-recommender, playground,
build-mcp-app, build-mcp-server, build-mcpb

## Top Community Repos (by skill count)

```
github/awesome-copilot              253
wshobson/agents                     146
sickn33/antigravity-awesome-skills  135
affaan-m/everything-claude-code     120
claude-office-skills/skills         118
googleworkspace/cli                  95
refoundai/lenny-skills               85
supercent-io/skills-template         76
trailofbits/skills                   60
```

## Skill Page Structure

Each skill page at `https://skills.sh/{owner}/{repo}/{slug}` contains:
1. Breadcrumb navigation: `skills / {owner} / {repo} / {slug}`
2. Title (H1): skill slug
3. Installation: `npx skills add https://github.com/{owner}/{repo} --skill {slug}`
4. Summary: bold description + bullet features
5. SKILL.md: full rendered content
6. Sidebar: weekly installs count, GitHub source link

## Installation Commands

```bash
# Knowledge-work plugins
npx skills add anthropics/knowledge-work-plugins

# Financial services plugins
npx skills add anthropics/financial-services-plugins

# Official skills
npx skills add anthropics/skills

# Community marketplace
claude plugin marketplace add anthropics/claude-plugins-community
```
