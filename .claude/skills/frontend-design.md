---
name: frontend-design
description: "Frontend design with React/Vite/Tailwind using GAN-inspired iterative evaluation"
trigger: "user asks to design frontend components, create React pages, build design systems, produce high-quality UI with iterative refinement, or improve frontend aesthetics"
---

Read `skills/frontend-design/SKILL.md` for the full skill definition with design
principles, grading criteria, and harness architecture.

## UDA Programmatic Tools (src/)

| Module | Class/Function | Purpose |
|--------|---------------|---------|
| `src/harness.py` | `HarnessRunner`, `frontend_design_harness()` | GAN-inspired iterative evaluation loop |
| `src/harness.py` | `SprintContract`, `EvaluationResult` | Contract negotiation and graded output |
| `src/dspy_prompts.py` | `EVALUATE_DESIGN`, `NEGOTIATE_CONTRACT` | DSPy signatures for design evaluation |
| `src/neon_db.py` | `create_harness_run`, `record_evaluation_result` | Persist harness runs to Neon |
| `src/tracing.py` | `trace_harness_run` | OTel distributed tracing for harness |

See `.claude/subagents/frontend-design.md` for structured execution instructions.
