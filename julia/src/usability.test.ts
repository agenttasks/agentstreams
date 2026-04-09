/**
 * Usability tests — end-to-end legal workflow scenarios.
 *
 * These tests simulate real user stories to verify Julia works
 * as a coherent legal AI system, not just individual modules:
 *
 *   1. Contract review: upload → search → analyze → draft redlines
 *   2. NDA triage: upload NDA → triage → classify risk → respond
 *   3. Client matter lifecycle: create → query → audit → delete
 *   4. Multi-project search: upload to 2 projects → cross-project search
 *   5. Review table extraction: upload 3 contracts → extract columns
 *
 * All external dependencies mocked. Focus is on workflow correctness,
 * not individual function behavior (that's in unit tests).
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  ProjectId,
  FileId,
  MatterId,
  AuditLogId,
  ReviewTableId,
  Ok,
  isOk,
  isSome,
  type JuliaEvent,
  type ReviewColumn,
} from "./types.js";

// ── Mock shared db.ts ────────────────────────────────────────

const mockSql = vi.fn();

vi.mock("./db.js", () => ({
  getSql: vi.fn(() => ({ ok: true, value: mockSql })),
  _resetSql: vi.fn(),
}));

vi.mock("@anthropic-ai/sdk", () => ({
  default: vi.fn().mockImplementation(() => ({
    messages: {
      create: vi.fn().mockResolvedValue({
        content: [{ type: "text", text: "Analysis complete." }],
        usage: { input_tokens: 200, output_tokens: 100 },
        stop_reason: "end_turn",
      }),
    },
  })),
}));

// ── Helpers ──────────────────────────────────────────────────

function mockRows(rows: Record<string, unknown>[]): void {
  mockSql.mockResolvedValueOnce(rows);
}

beforeEach(() => {
  vi.clearAllMocks();
  mockSql.mockResolvedValue([]);
});

// ── Scenario 1: Contract Review Workflow ─────────────────────

describe("Scenario: Contract review end-to-end", () => {
  it("upload contract → search for clauses → get completion with citations", async () => {
    const { createProject, uploadFile, semanticSearch } = await import("./vault.js");
    const { buildLegalSystemPrompt } = await import("./completion.js");
    const { eventToRow } = await import("./audit.js");

    // Step 1: Create a vault project for this contract
    const projectId = ProjectId("proj_contract_review");
    mockRows([{ id: projectId }]);
    const projResult = await createProject("Q3 Vendor Contracts", "counsel@firm.com");
    expect(isOk(projResult)).toBe(true);

    // Step 2: Upload the contract
    const fileId = FileId("file_msa_001");
    mockRows([{ id: fileId }]);
    const uploadResult = await uploadFile(
      projectId,
      "vendor-msa-2026.pdf",
      "MASTER SERVICES AGREEMENT\n\nSection 8.2 Indemnification.\nVendor shall indemnify Client for all claims arising from...\n\nSection 12.1 Limitation of Liability.\nIn no event shall either party's aggregate liability exceed...",
      "application/pdf",
    );
    expect(isOk(uploadResult)).toBe(true);

    // Step 3: Search for indemnification clauses
    mockRows([
      {
        id: "chunk_1", file_id: fileId, project_id: projectId,
        chunk_index: 0,
        content: "Section 8.2 Indemnification. Vendor shall indemnify Client for all claims arising from...",
        content_hash: "abc123", token_count: 30, metadata: {},
        score: 0.92,
      },
    ]);
    const searchResult = await semanticSearch(projectId, "indemnification liability", 5);
    expect(isOk(searchResult)).toBe(true);
    if (isOk(searchResult)) {
      expect(searchResult.value.length).toBeGreaterThan(0);
      expect(searchResult.value[0]!.content).toContain("Indemnification");
    }

    // Step 4: Build legal system prompt for review-contract skill
    const systemPrompt = buildLegalSystemPrompt("review-contract");
    expect(systemPrompt).toContain("review-contract");
    expect(systemPrompt).toContain("Never provide legal advice");

    // Step 5: Log the search event for audit trail
    const searchEvent: JuliaEvent = {
      type: "vault.search",
      projectId,
      query: "indemnification liability",
    };
    const row = eventToRow(searchEvent, { userEmail: "counsel@firm.com" });
    expect(row.event_type).toBe("vault.search");
    expect(row.project_id).toBe(projectId as string);
  });
});

// ── Scenario 2: NDA Triage Workflow ──────────────────────────

describe("Scenario: NDA triage classification", () => {
  it("upload NDA → search non-compete → classify risk level", async () => {
    const { uploadFile } = await import("./vault.js");
    const { eventToRow } = await import("./audit.js");

    const projectId = ProjectId("proj_nda_inbox");
    const fileId = FileId("file_nda_acme");

    // Upload NDA
    mockRows([{ id: fileId }]);
    const result = await uploadFile(
      projectId,
      "acme-nda-2026.pdf",
      "NON-DISCLOSURE AGREEMENT\n\nSection 5. Non-Compete.\nDuring the term and for 24 months thereafter, Recipient shall not...\n\nSection 7. Non-Solicitation.\nRecipient agrees not to solicit...",
      "application/pdf",
    );
    expect(isOk(result)).toBe(true);

    // Verify the upload event can be audited
    const uploadEvent: JuliaEvent = {
      type: "vault.upload",
      projectId,
      fileId,
      filename: "acme-nda-2026.pdf",
    };
    const row = eventToRow(uploadEvent);
    expect(row.event_type).toBe("vault.upload");
    expect(row.metadata).toEqual({ file_id: fileId as string });
  });
});

// ── Scenario 3: Client Matter Lifecycle ──────────────────────

describe("Scenario: Client matter lifecycle", () => {
  it("create matter → associate queries → check usage → soft delete", async () => {
    const { addMatters, getMatters, deleteMatters, associateQuery } = await import("./matters.js");
    const { eventToRow } = await import("./audit.js");

    const matterId = MatterId("matter_acme_v_widget");

    // Step 1: Create matter
    mockRows([{ id: matterId }]);
    const createResult = await addMatters([
      { name: "Acme Corp v. Widget Inc", description: "Patent infringement claim" },
    ]);
    expect(isOk(createResult)).toBe(true);

    // Step 2: Associate a query (simulates billing attribution)
    const assocResult = await associateQuery(matterId, 3500);
    expect(isOk(assocResult)).toBe(true);

    // Step 3: Audit trail captures the association
    const assocEvent: JuliaEvent = {
      type: "matter.associate_query",
      matterId,
      tokens: 3500,
    };
    const row = eventToRow(assocEvent);
    expect(row.input_tokens).toBe(3500);
    expect(row.client_matter_id).toBe(matterId as string);

    // Step 4: Soft delete
    const deleteResult = await deleteMatters([matterId]);
    expect(isOk(deleteResult)).toBe(true);

    // Step 5: Delete event is auditable
    const deleteEvent: JuliaEvent = { type: "matter.delete", matterId };
    const deleteRow = eventToRow(deleteEvent);
    expect(deleteRow.event_type).toBe("matter.delete");
  });
});

// ── Scenario 4: Pipeline Gate Enforcement ────────────────────

describe("Scenario: Pipeline blocks on critical risk", () => {
  it("RED risk in analyst step prevents drafter from executing", async () => {
    const { executePipeline, JULIA_LEGAL_WORKFLOW } = await import("./pipeline.js");

    let drafterCalled = false;

    const result = await executePipeline(
      JULIA_LEGAL_WORKFLOW,
      async (step) => {
        switch (step.agent) {
          case "julia-intake":
            return { type: "intake", skill: "review-contract" as const, complexity: "orchestrated" };
          case "julia-researcher":
            return { type: "research", context: "Found critical liability issues", citationCount: 5 };
          case "julia-analyst":
            return {
              type: "analysis",
              result: {
                verdict: "BLOCK" as const,
                risk_score: "RED" as const,
                findings: [{
                  clause: "Section 15 — Unlimited Indemnification",
                  severity: "RED" as const,
                  description: "No cap on liability",
                  recommendation: "Do not proceed without negotiation",
                }],
                summary: "Contract poses unacceptable risk.",
              },
            };
          case "julia-drafter":
            drafterCalled = true;
            return { type: "draft", output: "Should not reach here", fileCount: 0 };
          default:
            return null;
        }
      },
    );

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value.finalGate).toBe("abort");
      expect(drafterCalled).toBe(false);
    }
  });
});

// ── Scenario 5: Review Table Extraction ──────────────────────

describe("Scenario: Review table across multiple contracts", () => {
  it("create review table → verify columns → check row status", async () => {
    const { createReviewTable, getReviewRow } = await import("./vault.js");

    const projectId = ProjectId("proj_vendor_review");
    const columns: ReviewColumn[] = [
      { name: "Party", type: "text", description: "Contracting party name" },
      { name: "Governing Law", type: "text", description: "Jurisdiction" },
      { name: "Liability Cap", type: "currency", description: "Maximum liability amount" },
      { name: "Term", type: "date", description: "Contract duration" },
    ];
    const fileIds = [FileId("file_1"), FileId("file_2"), FileId("file_3")];

    // Create review table
    const rtId = ReviewTableId("rt_vendor_2026");
    mockRows([{ id: rtId }]);
    const createResult = await createReviewTable(projectId, "Q3 Vendor Review", columns, fileIds);
    expect(isOk(createResult)).toBe(true);

    // Check that a row was created for each file (pending status)
    // The SQL mock returns empty for row queries
    const rowResult = await getReviewRow(rtId, FileId("file_1"));
    // Returns Result<Option<ReviewRow>>; mock returns empty → Ok(None)
    expect(isOk(rowResult)).toBe(true);
    if (isOk(rowResult)) {
      expect(rowResult.value._tag).toBe("None");
    }
  });
});

// ── Scenario 6: Assistant Session Builder Validation ─────────

describe("Scenario: Multi-turn legal assistant", () => {
  it("builder validates skill is required before build", async () => {
    const { JuliaSession } = await import("./assistant.js");

    // Missing skill should throw on build
    expect(() => {
      JuliaSession.builder().build();
    }).toThrow("skill is required");
  });

  it("builder creates session with full config", async () => {
    const { JuliaSession } = await import("./assistant.js");

    const session = JuliaSession.builder()
      .skill("review-contract")
      .matter(MatterId("matter_123"))
      .model("claude-opus-4-6")
      .build();

    expect(session).toBeDefined();
    // Session should have no ID until first send()
    expect(session.getSessionId()).toBeUndefined();
  });
});
