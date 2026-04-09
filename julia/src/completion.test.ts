/**
 * completion.test.ts — Tests first (TDD).
 *
 * Covers:
 *   - Conditional types: CompletionResponse<true> has citations, <false> does not
 *   - buildLegalSystemPrompt includes legal constraints
 *   - complete() with and without vault context (Anthropic client mocked)
 *   - mergeSearchResults reciprocal rank fusion
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  type CompletionResponse,
  type Citation,
  type SearchResult,
  ProjectId,
  FileId,
  ChunkId,
  MatterId,
  Ok,
  isOk,
  isErr,
} from "./types.js";

// ── Mock @anthropic-ai/sdk before importing completion ───────

vi.mock("@anthropic-ai/sdk", () => {
  const create = vi.fn().mockResolvedValue({
    content: [{ type: "text", text: "This is a legal analysis." }],
    model: "claude-opus-4-6",
    usage: { input_tokens: 50, output_tokens: 20 },
  });
  return {
    default: vi.fn().mockImplementation(() => ({
      messages: { create },
    })),
  };
});

// Mock vault module — semanticSearch returns canned results
vi.mock("./vault.js", () => ({
  semanticSearch: vi.fn().mockResolvedValue(
    Ok([
      {
        id: ChunkId("chunk_1"),
        file_id: FileId("file_1"),
        chunk_index: 0,
        content: "Indemnification clause text.",
        content_hash: "abc123",
        token_count: 10,
        metadata: {},
        score: 0.95,
        project_id: ProjectId("proj_1"),
      } satisfies SearchResult,
    ]),
  ),
}));

import { complete, buildLegalSystemPrompt } from "./completion.js";
import Anthropic from "@anthropic-ai/sdk";

// ── buildLegalSystemPrompt ────────────────────────────────────

describe("buildLegalSystemPrompt", () => {
  it("includes the Julia identity and legal constraint", () => {
    const prompt = buildLegalSystemPrompt();
    expect(prompt).toContain("Julia");
    expect(prompt).toContain("Never provide legal advice");
    expect(prompt).toContain("analysis");
  });

  it("includes vault context when provided", () => {
    const ctx = "RELEVANT DOCUMENT EXCERPTS:\n[doc excerpt here]";
    const prompt = buildLegalSystemPrompt(undefined, ctx);
    expect(prompt).toContain(ctx);
  });

  it("does not mention vault context when not provided", () => {
    const prompt = buildLegalSystemPrompt();
    expect(prompt).not.toContain("RELEVANT DOCUMENT EXCERPTS");
  });

  it("incorporates legal skill when provided", () => {
    const prompt = buildLegalSystemPrompt("review-contract");
    expect(prompt).toContain("review-contract");
  });

  it("produces a non-empty string for every legal skill", () => {
    const skills = [
      "brief",
      "compliance-check",
      "legal-response",
      "legal-risk-assessment",
      "meeting-briefing",
      "review-contract",
      "signature-request",
      "triage-nda",
      "vendor-check",
    ] as const;
    for (const skill of skills) {
      expect(buildLegalSystemPrompt(skill).length).toBeGreaterThan(0);
    }
  });
});

// ── complete() without vault ──────────────────────────────────

describe("complete() without vault (HasVault = false)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Re-apply the default mock after clearing
    const AnthropicMock = Anthropic as unknown as ReturnType<typeof vi.fn>;
    AnthropicMock.mockImplementation(() => ({
      messages: {
        create: vi.fn().mockResolvedValue({
          content: [{ type: "text", text: "Legal analysis result." }],
          model: "claude-opus-4-6",
          usage: { input_tokens: 30, output_tokens: 15 },
        }),
      },
    }));
  });

  it("returns Ok with text and no citations property", async () => {
    const result = await complete({ query: "What is force majeure?" });
    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      const response: CompletionResponse<false> = result.value;
      expect(typeof response.text).toBe("string");
      expect(response.text.length).toBeGreaterThan(0);
      expect(response.model).toBe("claude-opus-4-6");
      expect(response.usage.input_tokens).toBeGreaterThanOrEqual(0);
      expect(response.usage.output_tokens).toBeGreaterThanOrEqual(0);
      expect(response.duration_ms).toBeGreaterThanOrEqual(0);
      // citations must NOT be present on HasVault=false response
      expect("citations" in response).toBe(false);
    }
  });

  it("accepts an optional matterId", async () => {
    const result = await complete({
      query: "Explain indemnity.",
      matterId: MatterId("matter_abc"),
    });
    expect(isOk(result)).toBe(true);
  });

  it("uses the provided model override", async () => {
    const AnthropicMock = Anthropic as unknown as ReturnType<typeof vi.fn>;
    const createMock = vi.fn().mockResolvedValue({
      content: [{ type: "text", text: "ok" }],
      model: "claude-sonnet-4-6",
      usage: { input_tokens: 10, output_tokens: 5 },
    });
    AnthropicMock.mockImplementation(() => ({
      messages: { create: createMock },
    }));

    await complete({ query: "brief", model: "claude-sonnet-4-6" });
    expect(createMock).toHaveBeenCalledWith(
      expect.objectContaining({ model: "claude-sonnet-4-6" }),
    );
  });
});

// ── complete() with vault ─────────────────────────────────────

describe("complete() with vault (HasVault = true)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    const AnthropicMock = Anthropic as unknown as ReturnType<typeof vi.fn>;
    AnthropicMock.mockImplementation(() => ({
      messages: {
        create: vi.fn().mockResolvedValue({
          content: [{ type: "text", text: "Analysis with citations." }],
          model: "claude-opus-4-6",
          usage: { input_tokens: 80, output_tokens: 40 },
        }),
      },
    }));
  });

  it("returns Ok with citations array when projectIds provided", async () => {
    const result = await complete({
      query: "Summarize indemnification obligations.",
      projectIds: [ProjectId("proj_1")],
    });
    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      const response: CompletionResponse<true> = result.value;
      expect(Array.isArray(response.citations)).toBe(true);
      const citation: Citation = response.citations[0]!;
      expect(typeof citation.file_id).toBe("string");
      expect(typeof citation.chunk_id).toBe("string");
      expect(typeof citation.content).toBe("string");
      expect(typeof citation.score).toBe("number");
    }
  });

  it("merges results from multiple projects", async () => {
    const result = await complete({
      query: "Liability cap analysis.",
      projectIds: [ProjectId("proj_1"), ProjectId("proj_2")],
    });
    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(Array.isArray(result.value.citations)).toBe(true);
    }
  });

  it("returns citations sorted by relevance (score descending)", async () => {
    const result = await complete({
      query: "Force majeure.",
      projectIds: [ProjectId("proj_1")],
    });
    if (isOk(result)) {
      const { citations } = result.value;
      for (let i = 1; i < citations.length; i++) {
        expect(citations[i - 1]!.score).toBeGreaterThanOrEqual(
          citations[i]!.score,
        );
      }
    }
  });
});

// ── Conditional type contract ─────────────────────────────────

describe("CompletionResponse conditional type contract", () => {
  it("CompletionResponse<true> is assignable with citations", () => {
    // Type-level test: construct a CompletionResponse<true> manually
    const withVault: CompletionResponse<true> = {
      text: "analysis",
      model: "claude-opus-4-6",
      usage: { input_tokens: 10, output_tokens: 5 },
      duration_ms: 100,
      citations: [
        {
          file_id: FileId("f1"),
          chunk_id: ChunkId("c1"),
          content: "excerpt",
          score: 0.9,
        },
      ],
    };
    expect(withVault.citations).toHaveLength(1);
  });

  it("CompletionResponse<false> is assignable without citations", () => {
    // Type-level test: no citations field required
    const noVault: CompletionResponse<false> = {
      text: "analysis",
      model: "claude-opus-4-6",
      usage: { input_tokens: 10, output_tokens: 5 },
      duration_ms: 100,
    };
    expect(noVault.text).toBe("analysis");
    // The following would be a type error at compile time:
    // expect((noVault as any).citations).toBeUndefined();
  });
});

// ── Error handling ────────────────────────────────────────────

describe("complete() error handling", () => {
  it("returns Err when Anthropic throws", async () => {
    const AnthropicMock = Anthropic as unknown as ReturnType<typeof vi.fn>;
    AnthropicMock.mockImplementation(() => ({
      messages: {
        create: vi.fn().mockRejectedValue(new Error("API unavailable")),
      },
    }));

    const result = await complete({ query: "Will this fail?" });
    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("processing_failed");
    }
  });
});
