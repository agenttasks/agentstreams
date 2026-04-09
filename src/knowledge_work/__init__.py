"""knowledge_work — 8-layer abstraction over anthropics/knowledge-work-plugins.

Layers (bottom → top):

    ┌─────────────────────────────────────────────────────────────┐
    │  8. knowledge-work-evals      Eval harness + A/B scoring   │
    │  7. knowledge-work-harness    Managed Agent runtime loop    │
    │  6. knowledge-work-subagents  Subagent orchestration        │
    │  5. knowledge-work-subtasks   Subtask decomposition         │
    │  4. knowledge-work-tasks      Task definition + routing     │
    │  3. knowledge-work-prompts    Prompt engineering layer      │
    │  2. knowledge-work-tracers    Circuit tracing + attribution │
    │  1. knowledge-work-circuits   Feature circuits + topology   │
    └─────────────────────────────────────────────────────────────┘
              ↕                              ↕
    vendors/knowledge-work-plugins    vendors/circuit-tracer

Glossary:
    circuit  — A set of features across model layers that work together
               to complete a task. Represented as an attribution graph
               where nodes are interpretable features (from SAEs/transcoders)
               and edges carry direct-effect weights quantifying causal
               influence between features.

    feature  — An interpretable unit of neural network computation,
               extracted from superposed representations via sparse
               autoencoders (SAEs) or transcoders. A feature might
               represent "Python function definition" or "financial
               terminology" or "empathetic tone."

    tracer   — The circuit-tracing algorithm: replace MLPs with
               transcoders, compute attribution between features,
               prune to significant paths, visualize.

    task     — A discrete unit of knowledge work (e.g., "draft outreach
               email", "review contract", "analyze dataset"). Maps to
               a SKILL.md in knowledge-work-plugins.

    subtask  — A decomposed step within a task (e.g., "research prospect"
               → "find company info" + "check recent news" + "identify
               decision makers").

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from src.knowledge_work.circuits import Circuit, CircuitTopology, FeatureNode
from src.knowledge_work.evals import ABComparison, EvalResult, EvalSuite
from src.knowledge_work.harness import HarnessConfig, HarnessLoop
from src.knowledge_work.prompts import PromptRegistry, PromptTemplate
from src.knowledge_work.registry import EcosystemRegistry, Layer, Org, RepoEntry
from src.knowledge_work.subagents import SubagentPool, SubagentSpec
from src.knowledge_work.subtasks import Subtask, SubtaskGraph
from src.knowledge_work.tasks import Task, TaskRouter
from src.knowledge_work.tracers import TracerConfig, TracerResult, trace_circuit

__all__ = [
    # Layer 1: Circuits
    "Circuit",
    "CircuitTopology",
    "FeatureNode",
    # Layer 2: Tracers
    "TracerConfig",
    "TracerResult",
    "trace_circuit",
    # Layer 3: Prompts
    "PromptTemplate",
    "PromptRegistry",
    # Layer 4: Tasks
    "Task",
    "TaskRouter",
    # Layer 5: Subtasks
    "Subtask",
    "SubtaskGraph",
    # Layer 6: Subagents
    "SubagentSpec",
    "SubagentPool",
    # Layer 7: Harness
    "HarnessConfig",
    "HarnessLoop",
    # Layer 8: Evals
    "EvalSuite",
    "EvalResult",
    "ABComparison",
    # Registry
    "EcosystemRegistry",
    "RepoEntry",
    "Org",
    "Layer",
]
