# Claude Agent SDK V2 — Knowledge Work Sessions

TypeScript patterns for running knowledge-work agents using the V2
Agent SDK (`@anthropic-ai/claude-agent-sdk`). These patterns complement
the Messages API integration in `sdk-integration.md` by adding
session management, multi-turn conversations, and resumable workflows.

## Installation

```bash
npm install @anthropic-ai/claude-agent-sdk
```

## One-Shot Skill Execution

For single-turn skill invocations (e.g., "analyze this data"):

```typescript
import { unstable_v2_prompt } from "@anthropic-ai/claude-agent-sdk";

// Run a data-analyst skill
const result = await unstable_v2_prompt(
  "Analyze the Q1 revenue data in data/q1-2026.csv and produce a variance report",
  { model: "claude-opus-4-6" }
);

if (result.subtype === "success") {
  console.log(result.result);
}
```

## Multi-Turn Knowledge Work Session

For workflows that require multiple exchanges (research → analysis → report):

```typescript
import { unstable_v2_createSession } from "@anthropic-ai/claude-agent-sdk";

await using session = unstable_v2_createSession({
  model: "claude-opus-4-6",
});

// Turn 1: Research phase (enterprise-search-agent skills)
await session.send(
  "Search for recent competitive intelligence on Acme Corp — " +
  "funding rounds, product launches, leadership changes"
);
for await (const msg of session.stream()) {
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log("[Research]", text);
  }
}

// Turn 2: Analysis phase (data-analyst skills)
await session.send(
  "Now analyze the competitive data and produce a SWOT matrix"
);
for await (const msg of session.stream()) {
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log("[Analysis]", text);
  }
}

// Turn 3: Report phase (marketing-agent skills)
await session.send(
  "Format the SWOT analysis as a competitive brief for the sales team"
);
for await (const msg of session.stream()) {
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log("[Report]", text);
  }
}
```

## Resumable Compliance Review

For long-running compliance workflows that may span multiple sessions:

```typescript
import {
  unstable_v2_createSession,
  unstable_v2_resumeSession,
  type SDKMessage,
} from "@anthropic-ai/claude-agent-sdk";

function getAssistantText(msg: SDKMessage): string | null {
  if (msg.type !== "assistant") return null;
  return msg.message.content
    .filter((block) => block.type === "text")
    .map((block) => block.text)
    .join("");
}

// Phase 1: Initial contract review
const session = unstable_v2_createSession({
  model: "claude-opus-4-6",
});

await session.send(
  "Review the vendor contract in contracts/acme-saas-2026.pdf " +
  "for compliance risks, data protection clauses, and liability gaps"
);

let sessionId: string | undefined;
const findings: string[] = [];

for await (const msg of session.stream()) {
  sessionId = msg.session_id;
  const text = getAssistantText(msg);
  if (text) findings.push(text);
}

console.log("Session ID for resume:", sessionId);
session.close();

// Store sessionId in your database for later...

// Phase 2: Resume and ask follow-up questions
await using resumed = unstable_v2_resumeSession(sessionId!, {
  model: "claude-opus-4-6",
});

await resumed.send(
  "Based on your review, which clauses need remediation before signing? " +
  "Produce a verdict: PASS, NEEDS_REMEDIATION, or BLOCK"
);

for await (const msg of resumed.stream()) {
  const text = getAssistantText(msg);
  if (text) console.log("[Verdict]", text);
}
```

## Pipeline Pattern: Research → Insight → Report

Maps to the `research-to-report` pipeline from `src/knowledge_agents.py`:

```typescript
import { unstable_v2_createSession } from "@anthropic-ai/claude-agent-sdk";

interface PipelineResult {
  research: string;
  insight: string;
  report: string;
}

async function researchToReport(topic: string): Promise<PipelineResult> {
  await using session = unstable_v2_createSession({
    model: "claude-opus-4-6",
  });

  const results: PipelineResult = { research: "", insight: "", report: "" };

  // Step 1: Research (enterprise-search-agent)
  await session.send(`Research: ${topic}`);
  for await (const msg of session.stream()) {
    if (msg.type === "assistant") {
      results.research += msg.message.content
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join("");
    }
  }

  // Step 2: Insight (data-analyst)
  await session.send("Analyze the research and extract key insights with data support");
  for await (const msg of session.stream()) {
    if (msg.type === "assistant") {
      results.insight += msg.message.content
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join("");
    }
  }

  // Step 3: Report (marketing-agent)
  await session.send("Format as a structured report with executive summary");
  for await (const msg of session.stream()) {
    if (msg.type === "assistant") {
      results.report += msg.message.content
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join("");
    }
  }

  return results;
}

// Usage
const result = await researchToReport("AI agent frameworks market landscape 2026");
console.log(result.report);
```

## Auth

The Agent SDK reads `CLAUDE_CODE_OAUTH_TOKEN` from the environment
automatically. Never use `ANTHROPIC_API_KEY`.

## See Also

- `sdk-integration.md` — Direct Messages API patterns (streaming, structured outputs)
- `src/knowledge_agents.py` — Python skill catalog and pipeline definitions
- `src/knowledge_subagents.py` — Claude Code CLI subagent generator
- `src/plugin_bridge.py` — Cowork plugin → ManagedAgentConfig bridge
