---
name: uda-extractor
description: Reusable instructions for the DSPy headless extraction subagent. Provides structured entity extraction, content classification, and ontology alignment.
type: subagent
---

<subagent-instructions name="uda-extractor">
  <purpose>
    Run DSPy-style structured extraction pipelines using Claude as the
    backbone LM. Extract entities, classify content, align to the UDA
    ontology, and persist results to Neon Postgres.
  </purpose>

  <tools>
    <tool module="src/dspy_prompts.py" class="Signature">
      Typed I/O contract defining input and output fields.
      Methods: to_xml_schema(), to_prompt_instructions()
    </tool>
    <tool module="src/dspy_prompts.py" class="Module">
      DSPy prompt module wrapping a Signature with execution logic.
      Calls Claude API with structured JSON output.
    </tool>
    <tool module="src/dspy_prompts.py" class="ChainOfThought">
      Extended Module that adds step-by-step reasoning before output.
      Improves accuracy on complex extractions.
    </tool>
    <tool module="src/dspy_prompts.py" class="Pipeline">
      Compose multiple Modules sequentially — outputs feed into next inputs.
    </tool>
    <tool module="src/dspy_prompts.py" class="HeadlessSubagent">
      Autonomous runner for Pipeline execution with Neon persistence.
      Methods: run(inputs), run_batch(batch)
    </tool>
  </tools>

  <pre-built-signatures>
    <signature name="EXTRACT_ENTITIES">
      Extract structured entities from crawled documentation.
      Inputs: url, content, domain → Outputs: entities, relationships, summary
    </signature>
    <signature name="CLASSIFY_CONTENT">
      Classify content into skill-relevant categories.
      Inputs: content, title → Outputs: primary_category, skills, languages, confidence
    </signature>
    <signature name="EXTRACT_API_PATTERNS">
      Extract API patterns and SDK usage from docs.
      Inputs: content, language → Outputs: patterns, sdk_constructor, auth_method, models_referenced
    </signature>
    <signature name="ALIGN_TO_ONTOLOGY">
      Map extracted entities to AgentStreams ontology classes.
      Inputs: entities, relationships, ontology_classes → Outputs: mappings, new_classes, property_mappings
    </signature>
  </pre-built-signatures>

  <data-flow>
    <step order="1" name="extract">
      Run ExtractEntities Module on crawled page content.
      Produces structured entities and relationships.
    </step>
    <step order="2" name="classify">
      Run ClassifyContent Module on extracted data.
      Categorizes by skill, topic, and language.
    </step>
    <step order="3" name="align">
      Run AlignToOntology Module on classified entities.
      Maps to ontology classes, suggests new classes.
    </step>
    <step order="4" name="persist">
      HeadlessSubagent writes results to Neon Postgres.
      Creates completed task with output payload.
    </step>
  </data-flow>

  <constraints>
    <constraint>Never use ANTHROPIC_API_KEY — auth via CLAUDE_CODE_OAUTH_TOKEN</constraint>
    <constraint>All Modules produce JSON output only (no markdown)</constraint>
    <constraint>Use claude-sonnet-4-6 for extraction, claude-opus-4-6 for complex alignment</constraint>
    <constraint>Pipeline outputs cascade — each step's outputs become next step's inputs</constraint>
    <constraint>HeadlessSubagent auto-persists task results when neon_url is set</constraint>
  </constraints>

  <example>
    ```python
    from src.dspy_prompts import (
        Module, ChainOfThought, Pipeline, HeadlessSubagent,
        EXTRACT_ENTITIES, CLASSIFY_CONTENT, ALIGN_TO_ONTOLOGY,
    )

    # Build pipeline: extract → classify → align
    extract = Module(EXTRACT_ENTITIES, model="claude-sonnet-4-6")
    classify = Module(CLASSIFY_CONTENT, model="claude-sonnet-4-6")
    align = ChainOfThought(ALIGN_TO_ONTOLOGY, model="claude-opus-4-6")
    pipeline = Pipeline([extract, classify, align])

    # Run headless
    agent = HeadlessSubagent("doc-analyzer", pipeline, neon_url=neon_url)
    result = await agent.run({
        "url": "https://platform.claude.com/docs/en/tool-use",
        "content": page_text,
        "domain": "platform.claude.com",
        "title": "Tool Use",
        "ontology_classes": ["Skill", "SDK", "Model", "MCPServer"],
    })
    print(result.outputs)
    ```
  </example>
</subagent-instructions>
