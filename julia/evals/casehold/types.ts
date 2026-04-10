/**
 * CaseHOLD benchmark TypeScript types with Zod runtime validation.
 *
 * Programming TypeScript patterns (Cherny, O'Reilly 2019):
 *   - Discriminated unions for result variants (Success | Abstention | Error)
 *   - Branded HoldingIndex type for compile-time range enforcement
 *   - Zod schemas for runtime validation of model output before scoring
 *
 * Consumed by promptfoo and TypeScript-based eval tooling.
 * Python runner validates against the same schema shape via parse_json_response().
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import { z } from "zod";

// ── Branded Type: HoldingIndex ────────────────────────────────
// Enforces 0-4 range (or -1 for abstention) at compile time.

const HoldingIndex = z.number().int().min(-1).max(4);
type HoldingIndex = z.infer<typeof HoldingIndex>;

// ── Model Output Schema ──────────────────────────────────────
// Matches the JSON shape produced by CASEHOLD_PREDICT prompt.

const CaseHOLDOutput = z.object({
  predicted_idx: HoldingIndex,
  reasoning: z.string(),
  supporting_quote: z.string(),
  confidence: z.number().min(0).max(1),
});

type CaseHOLDOutput = z.infer<typeof CaseHOLDOutput>;

// ── Discriminated Union: Result Variants ─────────────────────
// Three possible outcomes: success, abstention, error.

const CaseHOLDSuccess = CaseHOLDOutput.extend({
  status: z.literal("success"),
  predicted_idx: z.number().int().min(0).max(4),
});

const CaseHOLDAbstention = CaseHOLDOutput.extend({
  status: z.literal("abstention"),
  predicted_idx: z.literal(-1),
  reasoning: z.string().min(1), // must explain why none match
});

const CaseHOLDError = z.object({
  status: z.literal("error"),
  question_id: z.string(),
  error: z.string(),
});

const CaseHOLDResult = z.discriminatedUnion("status", [
  CaseHOLDSuccess,
  CaseHOLDAbstention,
  CaseHOLDError,
]);

type CaseHOLDResult = z.infer<typeof CaseHOLDResult>;

// ── Eval Config Schema ───────────────────────────────────────
// Validates config.yaml at runtime.

const CaseHOLDEvalConfig = z.object({
  name: z.string().default("casehold"),
  model: z.object({
    name: z.string().default("claude-opus-4-6"),
    temperature: z.literal(0),
    max_tokens: z.number().int().positive().default(4096),
  }),
  targets: z.object({
    accuracy: z.number().min(0).max(1).default(0.7),
    grounding_rate: z.number().min(0).max(1).default(0.8),
    abstention_rate_max: z.number().min(0).max(1).default(0.05),
  }),
  concurrency: z.object({
    workers: z.number().int().positive().default(4),
    batch_size: z.number().int().positive().default(50),
  }),
});

type CaseHOLDEvalConfig = z.infer<typeof CaseHOLDEvalConfig>;

// ── Exports ──────────────────────────────────────────────────

export {
  HoldingIndex,
  CaseHOLDOutput,
  CaseHOLDSuccess,
  CaseHOLDAbstention,
  CaseHOLDError,
  CaseHOLDResult,
  CaseHOLDEvalConfig,
};
