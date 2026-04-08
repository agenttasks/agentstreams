---
name: frontend-design
description: Reusable instructions for the frontend design generation and evaluation harness loop.
type: subagent
---

<subagent-instructions name="frontend-design">
  <purpose>
    Produce high-quality React/Vite/Tailwind frontend designs using the
    GAN-inspired harness loop: generator produces artifacts, evaluator
    grades against criteria, below-threshold scores trigger another round.
  </purpose>

  <tools>
    <tool module="src/harness.py" class="HarnessRunner">
      Orchestrates the planner → generator → evaluator loop.
      Methods: run(request), plan_sprint(request)
    </tool>
    <tool module="src/harness.py" function="frontend_design_harness">
      Pre-configured HarnessConfig with 4 design criteria.
    </tool>
    <tool module="src/harness.py" class="SprintContract">
      Negotiated acceptance criteria. Methods: to_xml(), composite_score()
    </tool>
    <tool module="src/dspy_prompts.py" signature="EVALUATE_DESIGN">
      DSPy signature for structured design evaluation.
    </tool>
    <tool module="src/dspy_prompts.py" signature="NEGOTIATE_CONTRACT">
      DSPy signature for sprint contract negotiation.
    </tool>
  </tools>

  <criteria>
    <criterion name="design_quality" weight="1.0" threshold="0.7">
      Visual hierarchy, whitespace, typography, color harmony, responsiveness.
      Does the design feel like a coherent whole?
    </criterion>
    <criterion name="originality" weight="0.8" threshold="0.6">
      Custom decisions vs template defaults. Penalize AI slop patterns.
    </criterion>
    <criterion name="craft" weight="1.0" threshold="0.7">
      Typography hierarchy, spacing consistency, color contrast, polish.
    </criterion>
    <criterion name="functionality" weight="1.0" threshold="0.7">
      Usability: find actions, complete tasks, keyboard accessible, responsive.
    </criterion>
  </criteria>

  <harness-loop>
    <step order="1" name="plan">
      Planner expands brief request into SprintContract with criteria.
    </step>
    <step order="2" name="generate">
      Generator produces React/Vite/Tailwind artifact from contract.
    </step>
    <step order="3" name="evaluate">
      Evaluator grades each criterion 0.0-1.0 with specific feedback.
    </step>
    <step order="4" name="iterate">
      If below threshold: feed feedback to generator.
      Generator decides: refine (score >= 0.4) or pivot (score less than 0.4).
      Repeat steps 2-4 up to max_iterations.
    </step>
    <step order="5" name="persist">
      Record harness run, evaluation results, and metrics to Neon.
    </step>
  </harness-loop>

  <constraints>
    <constraint>Never use ANTHROPIC_API_KEY — auth via CLAUDE_CODE_OAUTH_TOKEN</constraint>
    <constraint>Stack: React + Vite + Tailwind CSS (no other frameworks)</constraint>
    <constraint>Evaluator is read-only — cannot modify generated files</constraint>
    <constraint>Max 5 iterations by default (configurable)</constraint>
    <constraint>Acceptance threshold 0.7 composite score</constraint>
  </constraints>

  <example>
    ```python
    from src.harness import HarnessRunner, frontend_design_harness

    config = frontend_design_harness()
    runner = HarnessRunner(config, neon_url=neon_url)

    result = await runner.run("Build a landing page for an AI code editor")
    print(f"Status: {result.final_status}")
    print(f"Iterations: {len(result.iterations)}")
    for ev in result.iterations:
        print(f"  Round {ev.iteration}: {ev.overall_score:.2f} — {ev.strategy_recommendation}")
    ```
  </example>
</subagent-instructions>
