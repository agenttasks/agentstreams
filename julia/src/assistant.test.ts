/**
 * assistant.test.ts — Tests first (TDD).
 *
 * Covers:
 *   - JuliaSessionBuilder validates required fields and chains correctly
 *   - JuliaSession maintains conversation history across send() calls
 *   - Builder enforces branded type safety for projectIds and matterId
 *   - Static factory JuliaSession.builder() returns a fresh builder
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  ProjectId,
  MatterId,
  isOk,
  isErr,
} from "./types.js";

// ── Mock @anthropic-ai/sdk ────────────────────────────────────

const createMock = vi.fn().mockResolvedValue({
  content: [{ type: "text", text: "Understood, counselor." }],
  model: "claude-opus-4-6",
  usage: { input_tokens: 20, output_tokens: 10 },
});

vi.mock("@anthropic-ai/sdk", () => ({
  default: vi.fn().mockImplementation(() => ({
    messages: { create: createMock },
  })),
}));

import { JuliaSession, JuliaSessionBuilder } from "./assistant.js";

// ── JuliaSession.builder() static factory ────────────────────

describe("JuliaSession.builder()", () => {
  it("returns a JuliaSessionBuilder instance", () => {
    const builder = JuliaSession.builder();
    expect(builder).toBeInstanceOf(JuliaSessionBuilder);
  });

  it("is distinct from a second call (not shared state)", () => {
    const b1 = JuliaSession.builder();
    const b2 = JuliaSession.builder();
    expect(b1).not.toBe(b2);
  });
});

// ── JuliaSessionBuilder chaining ──────────────────────────────

describe("JuliaSessionBuilder chaining", () => {
  it("build() throws when skill is not set", () => {
    expect(() => JuliaSession.builder().build()).toThrow();
  });

  it("build() succeeds when skill is set", () => {
    const session = JuliaSession.builder().skill("review-contract").build();
    expect(session).toBeInstanceOf(JuliaSession);
  });

  it("vault() accepts branded ProjectId values", () => {
    const session = JuliaSession.builder()
      .skill("triage-nda")
      .vault(ProjectId("proj_1"), ProjectId("proj_2"))
      .build();
    expect(session).toBeInstanceOf(JuliaSession);
  });

  it("matter() accepts a branded MatterId", () => {
    const session = JuliaSession.builder()
      .skill("compliance-check")
      .matter(MatterId("matter_xyz"))
      .build();
    expect(session).toBeInstanceOf(JuliaSession);
  });

  it("model() overrides the default model", () => {
    const session = JuliaSession.builder()
      .skill("brief")
      .model("claude-sonnet-4-6")
      .build();
    expect(session).toBeInstanceOf(JuliaSession);
  });

  it("methods return `this` for fluent chaining", () => {
    const builder = JuliaSession.builder();
    const afterSkill = builder.skill("legal-response");
    expect(afterSkill).toBe(builder);

    const afterVault = builder.vault(ProjectId("p1"));
    expect(afterVault).toBe(builder);

    const afterMatter = builder.matter(MatterId("m1"));
    expect(afterMatter).toBe(builder);

    const afterModel = builder.model("claude-opus-4-6");
    expect(afterModel).toBe(builder);
  });
});

// ── JuliaSession.send() ───────────────────────────────────────

describe("JuliaSession.send()", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    createMock.mockResolvedValue({
      content: [{ type: "text", text: "Response text." }],
      model: "claude-opus-4-6",
      usage: { input_tokens: 20, output_tokens: 10 },
    });
  });

  it("returns Ok with a string on success", async () => {
    const session = JuliaSession.builder().skill("review-contract").build();
    const result = await session.send("Review this NDA.");
    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(typeof result.value).toBe("string");
      expect(result.value.length).toBeGreaterThan(0);
    }
  });

  it("accumulates conversation history across multiple sends", async () => {
    const session = JuliaSession.builder().skill("triage-nda").build();

    await session.send("First question.");
    await session.send("Second question.");

    // The third call should include all prior turns in the messages array
    expect(createMock).toHaveBeenCalledTimes(2);
    const secondCallArgs = createMock.mock.calls[1]![0] as {
      messages: Array<{ role: string; content: string }>;
    };
    expect(secondCallArgs.messages.length).toBeGreaterThanOrEqual(3);
    // First user + first assistant + second user
    expect(secondCallArgs.messages[0]!.role).toBe("user");
    expect(secondCallArgs.messages[0]!.content).toBe("First question.");
    expect(secondCallArgs.messages[1]!.role).toBe("assistant");
    expect(secondCallArgs.messages[2]!.role).toBe("user");
    expect(secondCallArgs.messages[2]!.content).toBe("Second question.");
  });

  it("returns Err when API throws", async () => {
    createMock.mockRejectedValueOnce(new Error("network error"));
    const session = JuliaSession.builder().skill("legal-risk-assessment").build();
    const result = await session.send("Will this fail?");
    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("processing_failed");
    }
  });

  it("history does not grow after an error", async () => {
    createMock.mockRejectedValueOnce(new Error("fail"));
    const session = JuliaSession.builder().skill("brief").build();

    const r1 = await session.send("Turn 1 — will fail.");
    expect(isErr(r1)).toBe(true);

    createMock.mockResolvedValueOnce({
      content: [{ type: "text", text: "ok" }],
      model: "claude-opus-4-6",
      usage: { input_tokens: 5, output_tokens: 2 },
    });

    const r2 = await session.send("Turn 2 — should succeed.");
    expect(isOk(r2)).toBe(true);

    // Second call should only have the turn-2 user message (no orphaned turn-1)
    const callArgs = createMock.mock.calls[1]![0] as {
      messages: Array<{ role: string }>;
    };
    expect(callArgs.messages).toHaveLength(1);
    expect(callArgs.messages[0]!.role).toBe("user");
  });
});

// ── getSessionId ──────────────────────────────────────────────

describe("JuliaSession.getSessionId()", () => {
  it("returns undefined before any send", () => {
    const session = JuliaSession.builder().skill("vendor-check").build();
    expect(session.getSessionId()).toBeUndefined();
  });

  it("returns a string session ID after first send", async () => {
    const session = JuliaSession.builder().skill("vendor-check").build();
    await session.send("Hello.");
    const sid = session.getSessionId();
    expect(typeof sid).toBe("string");
    expect(sid!.length).toBeGreaterThan(0);
  });

  it("returns the same session ID across multiple sends", async () => {
    const session = JuliaSession.builder().skill("meeting-briefing").build();
    await session.send("First.");
    const sid1 = session.getSessionId();
    await session.send("Second.");
    const sid2 = session.getSessionId();
    expect(sid1).toBe(sid2);
  });
});
