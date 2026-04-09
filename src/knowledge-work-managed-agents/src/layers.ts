/**
 * 14-layer type definitions and registry.
 *
 * Each layer has an ID, name, and a check() function that returns
 * a LayerResult with pass/fail and evidence. The registry is the
 * backbone that the agent, session, and router all reference.
 */

export interface LayerResult {
  layer: number;
  name: string;
  pass: boolean;
  score: number; // 0.0 - 1.0
  evidence: string[];
  metadata: Record<string, unknown>;
}

export interface Layer {
  id: number;
  name: string;
  description: string;
  /** Repos from the ecosystem registry that feed this layer */
  repos: string[];
}

/**
 * The 14-layer registry — maps layer IDs to metadata.
 * Half-integer layers (1.5, 2.5, 7.5) sit between their neighbors.
 */
export const LAYER_REGISTRY: Record<number, Layer> = {
  0: {
    id: 0,
    name: "training",
    description: "RLHF, Constitutional AI, character formation, preference data",
    repos: [
      "anthropics/hh-rlhf",
      "anthropics/claude-constitution",
      "safety-research/open-source-alignment-faking",
    ],
  },
  1: {
    id: 1,
    name: "circuits",
    description: "Feature nodes, topology, cross-layer similarity",
    repos: [
      "decoderesearch/SAELens",
      "decoderesearch/circuit-tracer",
      "safety-research/persona_vectors",
      "safety-research/assistant-axis",
    ],
  },
  1.5: {
    id: 1.5,
    name: "steering",
    description:
      "Activation steering, persona vectors, feature interventions",
    repos: [
      "safety-research/persona_vectors",
      "safety-research/assistant-axis",
      "decoderesearch/circuit-tracer",
    ],
  },
  2: {
    id: 2,
    name: "tracers",
    description: "Circuit tracing, attribution graphs, pruning",
    repos: [
      "decoderesearch/circuit-tracer",
      "safety-research/petri",
      "safety-research/auditing-agents",
    ],
  },
  2.5: {
    id: 2.5,
    name: "reasoning",
    description:
      "Scratchpad faithfulness, encoded content, unfaithful thinking detection",
    repos: [
      "safety-research/petri",
      "safety-research/lie-detector",
      "safety-research/trusted-monitor",
    ],
  },
  3: {
    id: 3,
    name: "prompts",
    description: "PromptRegistry, SKILL.md templates, A/B variants",
    repos: [
      "anthropics/prompt-eng-interactive-tutorial",
      "anthropics/claude-cookbooks",
      "safety-research/inoculation-prompting",
    ],
  },
  4: {
    id: 4,
    name: "tasks",
    description: "Task catalog, routing, domain mapping",
    repos: [
      "anthropics/skills",
      "anthropics/knowledge-work-plugins",
      "anthropics/financial-services-plugins",
      "modelcontextprotocol/registry",
    ],
  },
  5: {
    id: 5,
    name: "subtasks",
    description: "DAG decomposition, topological execution, parallelism",
    repos: ["anthropics/knowledge-work-plugins"],
  },
  6: {
    id: 6,
    name: "subagents",
    description: "Subagent pool, tool grants, cattle-not-pets",
    repos: [
      "anthropics/claude-agent-sdk-python",
      "anthropics/claude-agent-sdk-typescript",
    ],
  },
  7: {
    id: 7,
    name: "harness",
    description: "Agent runtime loop, session log, brain/hands decoupling",
    repos: [
      "anthropics/claude-code",
      "modelcontextprotocol/servers",
      "modelcontextprotocol/ext-apps",
    ],
  },
  7.5: {
    id: 7.5,
    name: "behavioral_safety",
    description:
      "6-dimension behavioral audit, reward hacking, scope creep, track covering",
    repos: [
      "safety-research/bloom",
      "safety-research/impossiblebench",
      "safety-research/SCONE-bench",
      "safety-research/SHADE-Arena",
      "safety-research/auditing-agents",
    ],
  },
  8: {
    id: 8,
    name: "evals",
    description: "Benchmarking, A/B testing, scoring",
    repos: [
      "anthropics/evals",
      "anthropics/claude-code-security-review",
      "safety-research/bloom",
      "modelcontextprotocol/inspector",
    ],
  },
  9: {
    id: 9,
    name: "welfare",
    description:
      "Model affect measurement, distress detection, psychological assessment",
    repos: [
      "safety-research/persona_vectors",
      "safety-research/assistant-axis",
      "anthropics/claude-constitution",
    ],
  },
  10: {
    id: 10,
    name: "governance",
    description: "RSP, ASL levels, release decisions, access control",
    repos: [
      "anthropics/model-cards",
      "anthropics/evals",
      "anthropics/political-neutrality-eval",
    ],
  },
};

/** All layer IDs sorted ascending */
export const LAYER_IDS = Object.keys(LAYER_REGISTRY)
  .map(Number)
  .sort((a, b) => a - b);
