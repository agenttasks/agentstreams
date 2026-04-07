---
name: frontend-design
description: "Frontend design with React/Vite/Tailwind using GAN-inspired iterative evaluation. TRIGGER when: user asks to design UI components, create React pages, build design systems, or produce high-quality frontend artifacts with iterative refinement. DO NOT TRIGGER for: backend API work, data pipelines, or simple static HTML without design requirements."
---

# Frontend Design: React + Vite + Tailwind with Iterative Evaluation

Design and build high-quality frontend interfaces using a GAN-inspired harness
that iterates between a generator (produces code) and an evaluator (grades design
quality) until acceptance criteria are met.

## Defaults

- Stack: React + Vite + Tailwind CSS
- Use `claude-sonnet-4-6` for generation, `claude-opus-4-6` for complex design decisions
- Iterative evaluation via `src/harness.py` HarnessRunner
- 4 grading criteria: design quality, originality, craft, functionality
- Max 5 iterations per sprint, 0.7 acceptance threshold

---

## Grading Criteria

From Anthropic's frontend aesthetics cookbook:

| Criterion | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| **Design Quality** | 1.0 | 0.7 | Does the design feel like a coherent whole? Colors, typography, layout, imagery combine to create a distinct mood and identity. |
| **Originality** | 0.8 | 0.6 | Evidence of custom design decisions. Unmodified stock components or telltale AI patterns (purple gradients over white cards) fail here. |
| **Craft** | 1.0 | 0.7 | Technical execution: typography hierarchy, spacing consistency, color harmony, contrast ratios. Competence check. |
| **Functionality** | 1.0 | 0.7 | Usability independent of aesthetics. Can users find actions, complete tasks, navigate without guessing? |

Design quality and originality are emphasized over craft and functionality because
Claude already scores well on technical competence by default.

---

## Harness Architecture

The GAN-inspired loop from Anthropic's harness design blog:

```
User Request
    ↓
Planner → SprintContract (objective + criteria + thresholds)
    ↓
┌─────────────────────────────────────────┐
│  Generator produces React/Vite/Tailwind │
│           ↓                             │
│  Evaluator grades against criteria      │
│           ↓                             │
│  Score < threshold? → feedback → retry  │
│  Score ≥ threshold? → accept            │
└─────────────────────────────────────────┘
    ↓
Final artifact + evaluation trace
```

### Using the Harness

```python
from src.harness import HarnessRunner, frontend_design_harness

config = frontend_design_harness()
runner = HarnessRunner(config)
result = await runner.run("Build a landing page for a Dutch art museum")
```

---

## Design Principles

1. **Visual hierarchy** — guide the eye with size, weight, color, and spacing
2. **Whitespace** — generous spacing creates breathing room and elegance
3. **Typography** — limit to 2 fonts maximum; establish clear heading/body/caption hierarchy
4. **Color** — build a cohesive palette (3-5 colors); use contrast ratios for accessibility
5. **Layout** — use CSS grid/flexbox for responsive structure; avoid fixed pixel widths
6. **Motion** — subtle transitions enhance UX; avoid gratuitous animation
7. **Accessibility** — semantic HTML, ARIA labels, keyboard navigation, screen reader support

## Anti-Patterns

- Purple gradients over white cards (AI slop signal)
- Unmodified component library defaults
- Generic hero sections with stock photography
- Identical spacing and sizing everywhere
- Over-reliance on drop shadows and rounded corners
- Rainbow color schemes without cohesion

---

## Programmatic Tools (src/)

| Module | Class/Function | Purpose |
|--------|---------------|---------|
| `src/harness.py` | `HarnessRunner` | GAN-inspired iterative evaluation loop |
| `src/harness.py` | `frontend_design_harness()` | Pre-configured harness with 4 criteria |
| `src/harness.py` | `SprintContract` | Negotiated acceptance criteria |
| `src/harness.py` | `EvaluationResult` | Graded output with scores and feedback |
| `src/dspy_prompts.py` | `EVALUATE_DESIGN` | DSPy signature for design evaluation |
| `src/neon_db.py` | `create_harness_run` | Persist harness execution to Neon |

## Agents

| Agent | Role |
|-------|------|
| `.claude/agents/frontend-generator.md` | Produces React/Vite/Tailwind artifacts, iterates on feedback |
| `.claude/agents/frontend-evaluator.md` | Grades designs against criteria, calibrated skeptical |

See `.claude/subagents/frontend-design.md` for structured execution instructions.
