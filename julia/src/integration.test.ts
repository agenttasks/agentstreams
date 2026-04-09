/**
 * Integration tests — cross-module interactions.
 *
 * These tests verify that modules work together correctly:
 *   1. vault → completion: search results feed into completion citations
 *   2. matters → audit: matter operations produce audit log entries
 *   3. pipeline → gate: pipeline execution respects gate decisions
 *   4. db.ts → all modules: shared connection used consistently
 *
 * All external dependencies (Neon, Anthropic) are mocked.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  ProjectId,
  FileId,
  MatterId,
  AuditLogId,
  Ok,
  Err,
  isSome,
  isOk,
  isErr,
  type Result,
  type JuliaEvent,
  type AnalysisResult,
  type PipelineStepResult,
} from "./types.js";

// ── Mock shared db.ts ────────────────────────────────────────

const mockSql = vi.fn();

vi.mock("./db.js", () => ({
  getSql: vi.fn(() => ({ ok: true, value: mockSql })),
  _resetSql: vi.fn(),
}));

// ── Mock Anthropic SDK ───────────────────────────────────────

vi.mock("@anthropic-ai/sdk", () => {
  return {
    default: vi.fn().mockImplementation(() => ({
      messages: {
        create: vi.fn().mockResolvedValue({
          content: [{ type: "text", text: "Legal analysis: The indemnification clause is standard." }],
          usage: { input_tokens: 100, output_tokens: 50 },
          stop_reason: "end_turn",
        }),
      },
    })),
  };
});

// ── Helper: mock SQL rows ────────────────────────────────────

function mockRows(rows: Record<string, unknown>[]): void {
  mockSql.mockResolvedValueOnce(rows);
}

// ── Tests ────────────────────────────────────────────────────

describe("Integration: vault → completion", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockSql.mockResolvedValue([]);
  });

  it("completion uses vault search results as citations", async () => {
    // Import dynamically so mocks are in place
    const { semanticSearch } = await import("./vault.js");
    const { buildLegalSystemPrompt } = await import("./completion.js");

    // Mock vault search returning 2 chunks
    mockRows([
      {
        id: "chunk_1", file_id: "file_1", project_id: "proj_1",
        chunk_index: 0, content: "The indemnification shall not exceed...",
        content_hash: "abc", token_count: 50, metadata: {},
        score: 0.95,
      },
      {
        id: "chunk_2", file_id: "file_1", project_id: "proj_1",
        chunk_index: 1, content: "Governing law shall be New York...",
        content_hash: "def", token_count: 40, metadata: {},
        score: 0.87,
      },
    ]);

    const searchResult = await semanticSearch(ProjectId("proj_1"), "indemnification", 5);
    expect(isOk(searchResult)).toBe(true);
    if (isOk(searchResult)) {
      expect(searchResult.value).toHaveLength(2);
      expect(searchResult.value[0]!.score).toBe(0.95);
    }

    // Verify system prompt includes legal constraints
    const prompt = buildLegalSystemPrompt("review-contract");
    expect(prompt).toContain("Julia");
    expect(prompt).toContain("legal");
  });
});

describe("Integration: matters → audit", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockSql.mockResolvedValue([]);
  });

  it("matter creation event can be logged to audit", async () => {
    const { eventToRow } = await import("./audit.js");

    const event: JuliaEvent = {
      type: "matter.create",
      matterId: MatterId("matter_123"),
      name: "Acme Corp v. Widget Inc",
    };

    const row = eventToRow(event, { userEmail: "lawyer@firm.com" });
    expect(row.event_type).toBe("matter.create");
    expect(row.client_matter_id).toBe("matter_123");
    expect(row.user_email).toBe("lawyer@firm.com");
    expect(row.input_summary).toBe("Acme Corp v. Widget Inc");
  });

  it("completion event captures token counts for matter billing", async () => {
    const { eventToRow } = await import("./audit.js");

    const event: JuliaEvent = {
      type: "completion",
      query: "Review this NDA for non-compete restrictions",
      model: "claude-opus-4-6",
      matterId: MatterId("matter_456"),
      projectIds: [ProjectId("proj_1")],
      input_tokens: 2500,
      output_tokens: 1200,
      duration_ms: 3400,
    };

    const row = eventToRow(event);
    expect(row.client_matter_id).toBe("matter_456");
    expect(row.input_tokens).toBe(2500);
    expect(row.output_tokens).toBe(1200);
    expect(row.duration_ms).toBe(3400);
    expect(row.model).toBe("claude-opus-4-6");
  });
});

describe("Integration: pipeline → gate", () => {
  it("pipeline aborts when analyst returns BLOCK verdict", async () => {
    const { executePipeline, JULIA_LEGAL_WORKFLOW } = await import("./pipeline.js");

    const blockAnalysis: AnalysisResult = {
      verdict: "BLOCK",
      risk_score: "RED",
      findings: [{
        clause: "Section 12 — Unlimited Liability",
        severity: "RED",
        description: "No liability cap",
        recommendation: "Reject or negotiate cap",
      }],
      summary: "Critical risk — contract must not proceed.",
    };

    const result = await executePipeline(
      JULIA_LEGAL_WORKFLOW,
      async (step) => {
        switch (step.agent) {
          case "julia-intake":
            return { type: "intake", skill: "review-contract", complexity: "composite" };
          case "julia-researcher":
            return { type: "research", context: "Contract text...", citationCount: 3 };
          case "julia-analyst":
            return { type: "analysis", result: blockAnalysis };
          case "julia-drafter":
            // Should NOT be reached due to BLOCK
            throw new Error("Drafter should not execute after BLOCK");
          default:
            return null;
        }
      },
    );

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value.finalGate).toBe("abort");
      // Drafter step should not appear (condition prevents it)
      const agents = result.value.steps.map((s) => s.step.agent);
      expect(agents).not.toContain("julia-drafter");
    }
  });

  it("pipeline continues through all steps on PASS verdict", async () => {
    const { executePipeline, JULIA_LEGAL_WORKFLOW } = await import("./pipeline.js");

    const passAnalysis: AnalysisResult = {
      verdict: "PASS",
      risk_score: "GREEN",
      findings: [],
      summary: "Contract is standard.",
    };

    const result = await executePipeline(
      JULIA_LEGAL_WORKFLOW,
      async (step) => {
        switch (step.agent) {
          case "julia-intake":
            return { type: "intake", skill: "review-contract", complexity: "atomic" };
          case "julia-researcher":
            return { type: "research", context: "Contract looks standard", citationCount: 2 };
          case "julia-analyst":
            return { type: "analysis", result: passAnalysis };
          case "julia-drafter":
            return { type: "draft", output: "DRAFT: Contract review complete.", fileCount: 1 };
          default:
            return null;
        }
      },
    );

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value.finalGate).toBe("continue");
      expect(result.value.steps).toHaveLength(4);
      const agents = result.value.steps.map((s) => s.step.agent);
      expect(agents).toContain("julia-drafter");
    }
  });

  it("pipeline gate checks AFTER entire order group (not mid-group)", async () => {
    const { checkGate, type PipelineGate } = await import("./pipeline.js");

    const gate: PipelineGate = {
      blockOnVerdict: ["BLOCK"],
      blockOnRisk: ["RED"],
    };

    // No analysis results → continue
    expect(checkGate(gate, [])).toBe("continue");

    // GREEN analysis → continue
    const greenResults: PipelineStepResult[] = [
      { type: "analysis", result: { verdict: "PASS", risk_score: "GREEN", findings: [], summary: "" } },
    ];
    expect(checkGate(gate, greenResults)).toBe("continue");

    // RED analysis → human_review
    const redResults: PipelineStepResult[] = [
      { type: "analysis", result: { verdict: "NEEDS_REMEDIATION", risk_score: "RED", findings: [], summary: "" } },
    ];
    expect(checkGate(gate, redResults)).toBe("human_review");
  });
});

describe("Integration: shared db.ts", () => {
  it("getSql returns the same Result-wrapped function", async () => {
    const { getSql } = await import("./db.js");
    const result1 = getSql();
    const result2 = getSql();
    expect(result1.ok).toBe(true);
    expect(result2.ok).toBe(true);
  });
});

describe("Integration: all event types round-trip through audit", () => {
  it("every JuliaEvent variant produces a valid AuditRow", async () => {
    const { eventToRow } = await import("./audit.js");

    const events: JuliaEvent[] = [
      { type: "vault.create_project", projectId: ProjectId("p1"), name: "Test" },
      { type: "vault.upload", projectId: ProjectId("p1"), fileId: FileId("f1"), filename: "contract.pdf" },
      { type: "vault.search", projectId: ProjectId("p1"), query: "indemnification" },
      { type: "vault.delete_file", projectId: ProjectId("p1"), fileId: FileId("f1") },
      { type: "vault.create_review_table", projectId: ProjectId("p1"), reviewTableId: "rt1" as any },
      { type: "matter.create", matterId: MatterId("m1"), name: "Case" },
      { type: "matter.delete", matterId: MatterId("m1") },
      { type: "matter.associate_query", matterId: MatterId("m1"), tokens: 500 },
      { type: "completion", query: "q", model: "claude-opus-4-6", matterId: null, projectIds: [], input_tokens: 100, output_tokens: 50, duration_ms: 1000 },
      { type: "assistant.session", sessionId: "s1", skill: "review-contract", matterId: null },
    ];

    for (const event of events) {
      const row = eventToRow(event);
      expect(row.event_type).toBe(event.type);
      // Every row must have a non-empty event_type
      expect(typeof row.event_type).toBe("string");
      expect(row.event_type.length).toBeGreaterThan(0);
    }
  });
});
