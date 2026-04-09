/**
 * Julia pipeline orchestration — legal workflow execution.
 *
 * Two pipelines:
 *   1. julia-legal-workflow: intake → research → analysis → draft
 *   2. julia-vault-review: intake → research → parallel file extraction
 *
 * Follows the orchestrator pattern from src/orchestrator.py:
 *   - Steps with same order run in parallel
 *   - Gates check between order groups
 *   - BLOCK verdict or RED risk → abort with human review
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import {
  type Verdict,
  type RiskScore,
  type LegalSkill,
  type ProjectId,
  type MatterId,
  type FileId,
  type ReviewTableId,
  type ReviewColumn,
  type Result,
  type AnalysisResult,
  Ok,
  Err,
  assertNever,
} from "./types.js";

// ── Pipeline Step Types (discriminated union) ────────────────

export type PipelineStepResult =
  | { type: "intake"; skill: LegalSkill; complexity: string }
  | { type: "research"; context: string; citationCount: number }
  | { type: "analysis"; result: AnalysisResult }
  | { type: "draft"; output: string; fileCount: number }
  | { type: "review_extraction"; reviewTableId: ReviewTableId; rowCount: number };

export type GateDecision = "continue" | "human_review" | "abort";

export interface PipelineStep {
  order: number;
  agent: string;
  name: string;
  condition?: (priorResults: PipelineStepResult[]) => boolean;
}

export interface PipelineGate {
  blockOnVerdict: Verdict[];
  blockOnRisk: RiskScore[];
  humanReviewThreshold?: number;
}

export interface PipelineConfig {
  name: string;
  description: string;
  steps: PipelineStep[];
  gate: PipelineGate;
}

// ── Gate Check ───────────────────────────────────────────────

export function checkGate(
  gate: PipelineGate,
  results: PipelineStepResult[],
): GateDecision {
  for (const result of results) {
    if (result.type === "analysis") {
      if (gate.blockOnVerdict.includes(result.result.verdict)) {
        return "abort";
      }
      if (gate.blockOnRisk.includes(result.result.risk_score)) {
        return "human_review";
      }
    }
  }
  return "continue";
}

// ── Pipeline Definitions ─────────────────────────────────────

export const JULIA_LEGAL_WORKFLOW: PipelineConfig = {
  name: "julia-legal-workflow",
  description:
    "End-to-end legal workflow: classify → research → analyze → draft",
  steps: [
    { order: 0, agent: "julia-intake", name: "Classify request" },
    { order: 1, agent: "julia-researcher", name: "Vault search + context" },
    { order: 2, agent: "julia-analyst", name: "Review + risk assessment" },
    // Gate: block on BLOCK verdict or RED risk
    {
      order: 3,
      agent: "julia-drafter",
      name: "Produce deliverable",
      condition: (prior) => {
        // Only draft if analysis didn't block
        const analysis = prior.find((r) => r.type === "analysis");
        if (!analysis || analysis.type !== "analysis") return true;
        return (
          analysis.result.verdict !== "BLOCK" &&
          analysis.result.risk_score !== "RED"
        );
      },
    },
  ],
  gate: {
    blockOnVerdict: ["BLOCK"],
    blockOnRisk: ["RED"],
  },
};

export const JULIA_VAULT_REVIEW: PipelineConfig = {
  name: "julia-vault-review",
  description:
    "Structured review table extraction: intake → research → parallel extraction per file",
  steps: [
    { order: 0, agent: "julia-intake", name: "Classify review request" },
    {
      order: 1,
      agent: "julia-researcher",
      name: "Gather documents from vault",
    },
    // Order 2: parallel extraction per file (handled by executor)
    {
      order: 2,
      agent: "julia-analyst",
      name: "Extract per column per file",
    },
  ],
  gate: {
    blockOnVerdict: ["BLOCK"],
    blockOnRisk: ["RED"],
  },
};

// ── Pipeline Executor ────────────────────────────────────────

export interface PipelineExecutionResult {
  pipeline: string;
  steps: Array<{
    step: PipelineStep;
    result: PipelineStepResult | null;
    gateDecision: GateDecision;
    duration_ms: number;
  }>;
  finalGate: GateDecision;
  total_duration_ms: number;
}

/**
 * Execute a pipeline by walking steps in order.
 *
 * Steps with the same order run concurrently (via Promise.all).
 * After each order group, the gate is checked.
 *
 * The actual agent execution is delegated to the `executeStep` callback,
 * which should call the appropriate Julia module function or Agent SDK query.
 */
export async function executePipeline(
  config: PipelineConfig,
  executeStep: (
    step: PipelineStep,
    priorResults: PipelineStepResult[],
  ) => Promise<PipelineStepResult | null>,
): Promise<Result<PipelineExecutionResult>> {
  const t0 = Date.now();
  const allResults: PipelineStepResult[] = [];
  const stepResults: PipelineExecutionResult["steps"] = [];

  // Group steps by order
  const orderGroups = new Map<number, PipelineStep[]>();
  for (const step of config.steps) {
    const group = orderGroups.get(step.order) ?? [];
    group.push(step);
    orderGroups.set(step.order, group);
  }

  const sortedOrders = [...orderGroups.keys()].sort((a, b) => a - b);

  for (const order of sortedOrders) {
    const group = orderGroups.get(order)!;

    // Filter steps whose conditions are met
    const activeSteps = group.filter(
      (step) => !step.condition || step.condition(allResults),
    );

    // Execute all steps in this order group concurrently
    const groupResults = await Promise.all(
      activeSteps.map(async (step) => {
        const stepT0 = Date.now();
        const result = await executeStep(step, allResults);
        return {
          step,
          result,
          duration_ms: Date.now() - stepT0,
        };
      }),
    );

    // Collect results and check gate
    for (const { step, result, duration_ms } of groupResults) {
      if (result) {
        allResults.push(result);
      }
      const gateDecision = checkGate(config.gate, allResults);
      stepResults.push({ step, result, gateDecision, duration_ms });

      if (gateDecision === "abort") {
        return Ok({
          pipeline: config.name,
          steps: stepResults,
          finalGate: "abort",
          total_duration_ms: Date.now() - t0,
        });
      }

      if (gateDecision === "human_review") {
        return Ok({
          pipeline: config.name,
          steps: stepResults,
          finalGate: "human_review",
          total_duration_ms: Date.now() - t0,
        });
      }
    }
  }

  return Ok({
    pipeline: config.name,
    steps: stepResults,
    finalGate: "continue",
    total_duration_ms: Date.now() - t0,
  });
}
