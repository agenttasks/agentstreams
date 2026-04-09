# Harvey AI — Competitive Intelligence Taxonomy

## Source: harvey.ai/sitemap.xml (422 URLs crawled 2026-04-09)

---

## BigLaw Bench (Harvey's Eval Framework)

**Key Metric: Answer Score** = "What % of a lawyer-quality work product does the model complete?"
- Harvey proprietary models: **74%** of expert lawyer-quality work product
- Public foundation models: ~50% answer score
- Foundation models "consistently hallucinate sources" on citation tasks

**Key Metric: Source Score** = "What % of correct statements have an accurate source?"
- Harvey proprietary: high source accuracy (not published exact %)
- Foundation models: dramatically underperform on source verification

**Task Distribution (Transactional):**
- Corporate Strategy & Advising: 28.3%
- Drafting: 24.5%
- Legal Research: 13.2%
- Due Diligence: 11.3%
- Risk Assessment & Compliance: 9.4%

**Task Distribution (Litigation):**
- Analysis of Litigation Filings: 25.5%
- Case Management: 23.4%
- Drafting: 14.9%

**Critique of open benchmarks:** "Multiple-choice or one-size-fits-all benchmarks are insufficient to capture the real billable work that lawyers do."

---

## ELO Score Methodology

**How Harvey measures quality:**
- Head-to-head comparisons evaluated by local legal professionals
- 150-200 point gap = ~70% preference (noticeably better)
- 400+ point gap = >90% preference (fundamental step-change)

**Concrete Results:**
- Harvey Assistant: preferred >70% vs generic foundation models
- EDGAR system: ELO 1695, parity with human expert
- Vault citation quality: 62-97% across implementations
- Vault latency: 11-24 seconds

**Julia Gap:** Julia has no ELO evaluation system. Need to implement:
- Pairwise comparison framework (Julia output vs baseline)
- Local legal professional evaluation pipeline
- Answer Score + Source Score metrics

---

## Spectre (Harvey's Agent Platform)

**Architecture (directly comparable to Julia's pipeline):**
- Durable Runs: persistent run record, short-lived worker processes
- Sandboxes: isolated environments with scoped access
- Harness: assembles context, routes events, manages progress
- Collaboration: Slack/web/CLI all reference same durable run
- Scheduled Runs: first-class objects (not separate background jobs)

**Legal mapping:**
- Repositories → Matters
- Diffs → Document versions
- Sandbox boundaries → Ethical walls
- Credentials → Access controls

**Julia equivalents:**
- Durable Runs → julia_audit_logs (persistent event log)
- Sandboxes → Agent tool grants (least-privilege)
- Harness → pipeline.ts executePipeline()
- Collaboration → MCP server (stdio + future HTTP)
- Scheduled Runs → pg_cron jobs in schema.sql

**Julia Gaps:**
- No Slack integration (Spectre has it)
- No durable run resumption (Julia pipeline is one-shot)
- No ethical wall enforcement (Julia has no matter-level access control)
- No document versioning (Julia vault is append-only, no diff/version tracking)

---

## Harvey Product Surface → Julia Equivalents

| Harvey Feature | Julia Equivalent | Status |
|---|---|---|
| Assistant | completion.ts + assistant.ts | Built |
| Vault | vault.ts (upload, search, review tables) | Built (hash embeddings only) |
| Knowledge | vendored legal skills (9 SKILL.md) | Built |
| Workflow Agents | pipeline.ts (4-agent pipeline) | Built |
| Agent Builder | Not implemented | MISSING |
| Deep Research | Not implemented | MISSING |
| Governance Controls | emotion monitoring + pipeline gates | Built (novel — Harvey lacks emotion gates) |
| Box Integration | Not implemented (plan mentioned Box MCP) | MISSING |
| Mobile | Not applicable (CLI/MCP only) | N/A |
| Multi-Model | completion.ts model parameter | Built (supports any Claude model) |
| Custom Legal Embeddings | hashEmbedding (not semantic) | NEEDS UPGRADE |
| BigLaw Bench | julia/evals/ (8 synthetic scenarios) | NEEDS CUAD/LegalBench |
| ELO Scoring | Not implemented | MISSING |
| File Ingestion System | vault.ts uploadFile + chunkText | Built (basic) |
| MCP | mcp-server.ts (15 tools) | Built |

---

## Harvey Blog Technical Deep Dives

| Post | Date | Key Insight for Julia |
|---|---|---|
| Building Spectre | Apr 7, 2026 | Agent platform arch: durable runs, sandboxes, harness |
| Building an Agent for Document Drafting | Mar 24, 2026 | Complex multi-step document editing workflow |
| BigLaw Bench: Research | Mar 11, 2026 | Eval methodology for legal research quality |
| ELO Scores for Legal AI | Feb 26, 2026 | Pairwise comparison framework, Answer Score + Source Score |
| BigLaw Bench: Global | Feb 18, 2026 | International legal benchmark (multi-jurisdiction) |
| File Ingestion at Scale | Feb 11, 2026 | Vault architecture for large document sets |
| Custom Legal Embeddings (Voyage) | | Domain-specific embeddings vs generic |
| Why Multi-Model | Mar 9, 2026 | Model selection strategy per task type |
| Agent Builder | Mar 5, 2026 | User-configurable agent workflows |
| GPT-5.4 in Harvey | Mar 4, 2026 | Multi-model integration (OpenAI + Anthropic) |
