/**
 * LegalBench benchmark types — Cherny "Programming TypeScript" (O'Reilly 2019) patterns.
 *
 * Branded types (Ch.6 p.172), Result/Option (Ch.7 p.183-185),
 * conditional types (Ch.6 p.163), companion objects (Ch.6 p.160),
 * discriminated unions + totality (Ch.6 p.146-150).
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import type { Result, VaultError } from "./types";
export { Ok, Err, isOk } from "./types";

// ── Branded Types (Cherny Ch.6 p.172) ─────────────────────────
// Nominal typing via intersection with unique symbol. Prevents
// accidentally passing a LegalBenchRunId where a SampleId is expected.

export type LegalBenchSampleId = string & { readonly brand: unique symbol };
export type LegalBenchRunId = string & { readonly brand: unique symbol };

export function LegalBenchSampleId(id: string): LegalBenchSampleId {
  return id as LegalBenchSampleId;
}

export function LegalBenchRunId(id: string): LegalBenchRunId {
  return id as LegalBenchRunId;
}

// ── Answer Types (Discriminated Union, Cherny Ch.6 p.146) ─────
// Totality: switch + assertNever ensures all cases handled.

export type AnswerType =
  | "binary"
  | "multiple_choice"
  | "classification"
  | "extraction";

// ── LegalBench Category ───────────────────────────────────────
// Degenerate dimension from Kimball schema (no separate dim table).

export type LegalBenchCategory =
  | "contract_nli"
  | "cuad"
  | "maud"
  | "learned_hands"
  | "supply_chain_disclosure"
  | "opp115"
  | "diversity_jurisdiction"
  | "rule_application"
  | "core_legal_knowledge"
  | "contract_qa"
  | "rhetorical_understanding"
  | "privacy_policy"
  | "ssla"
  | "sara"
  | "textualism"
  | "citation_prediction"
  | "interpretation"
  | "corporate_lobbying"
  | "court_outcomes"
  | "judicial_ethics"
  | "international_law"
  | "unfair_tos";

// ── LegalBench Task Config ────────────────────────────────────
// Loaded from scripts/legalbench_tasks.json at runtime.

export type LegalBenchTaskConfig = {
  readonly category: LegalBenchCategory;
  readonly hf_config: string;
  readonly text_fields: readonly string[];
  readonly answer_field: string;
  readonly answer_type: AnswerType;
  readonly label_names: readonly string[];
  readonly test_size: number;
  readonly choice_fields?: readonly string[];
};

// ── LegalBench Task (Companion Object, Cherny Ch.6 p.160) ─────
// Same name for type AND namespace: LegalBenchTask.create() + x: LegalBenchTask.

export type LegalBenchTask = {
  readonly id: LegalBenchSampleId;
  readonly task: string;
  readonly category: LegalBenchCategory;
  readonly text: string;
  readonly context: string | null;
  readonly answer: string;
  readonly answerType: AnswerType;
  readonly labelNames: readonly string[];
  readonly hfIndex: number;
  readonly tokenCount: number;
};

export const LegalBenchTask = {
  fromRow(row: Record<string, unknown>): LegalBenchTask {
    return {
      id: LegalBenchSampleId(row.id as string),
      task: row.task as string,
      category: row.category as LegalBenchCategory,
      text: row.text as string,
      context: (row.context as string) ?? null,
      answer: row.answer as string,
      answerType: row.answer_type as AnswerType,
      labelNames: JSON.parse(row.label_names as string),
      hfIndex: row.hf_index as number,
      tokenCount: (row.token_count as number) ?? 0,
    };
  },
};

// ── Eval Response (Conditional Type, Cherny Ch.6 p.163) ────────
// When --verify-citations is used, response includes citationScore.
// Compile-time guarantee: if HasCitations is true, quotesUsed and
// citationScore MUST be present. If false, they are FORBIDDEN.

export type LegalBenchEvalResponse<HasCitations extends boolean> = {
  readonly sampleId: LegalBenchSampleId;
  readonly task: string;
  readonly category: LegalBenchCategory;
  readonly predictedAnswer: string;
  readonly confidence: number;
  readonly reasoning: string;
  readonly durationMs: number;
  readonly inputTokens: number;
  readonly outputTokens: number;
} & (HasCitations extends true
  ? { readonly quotesUsed: string[]; readonly citationScore: number }
  : { readonly quotesUsed?: never; readonly citationScore?: never });

// ── LegalBench Error (Discriminated Union, Cherny Ch.7 p.183) ──
// Typed errors for exhaustive handling via switch + assertNever.

export type LegalBenchError =
  | { type: "task_not_found"; task: string }
  | { type: "parse_failed"; rawOutput: string; reason: string }
  | { type: "hallucinated_label"; predicted: string; validLabels: string[] }
  | { type: "citation_failed"; quote: string; sourceScore: number }
  | { type: "low_confidence"; confidence: number; threshold: number }
  | { type: "database_error"; message: string };

export type LegalBenchResult<T> = Result<T>;

// ── Best-of-N Result ──────────────────────────────────────────
// For borderline cases (confidence < threshold), re-run N times
// and take majority vote.

export type BestOfNResult = {
  readonly sampleId: LegalBenchSampleId;
  readonly attempts: number;
  readonly agreement: number;
  readonly majorityAnswer: string;
  readonly answers: readonly string[];
  readonly isBorderline: boolean;
};

// ── Type Guard (Cherny Ch.6 p.162) ────────────────────────────

export function isBinary(task: LegalBenchTask): task is LegalBenchTask & { answerType: "binary" } {
  return task.answerType === "binary";
}

export function isContractNli(
  task: LegalBenchTask,
): task is LegalBenchTask & { category: "contract_nli" } {
  return task.category === "contract_nli";
}
