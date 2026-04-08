"""DSPy headless subagent prompting for structured extraction.

Implements DSPy-style programmatic prompt optimization using Claude
as the backbone LM. Provides typed Signatures, Modules, and a headless
subagent runner that executes extraction pipelines without interactive UI.

UDA pattern: prompts are ontology-defined (as:Prompt), their execution
produces DataContainers that map to Neon tables via mappings.ttl.

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

# ── Signature definitions (DSPy-style typed I/O) ────────────


@dataclass
class Field:
    """A typed field in a DSPy Signature."""

    name: str
    description: str
    field_type: str = "str"  # str, int, float, bool, list, dict
    required: bool = True
    default: Any = None


@dataclass
class Signature:
    """DSPy-style typed signature defining input/output schema.

    Signatures are the contract between prompt modules:
    inputs define what the module receives, outputs define
    what it must produce.

    Example:
        ExtractEntities = Signature(
            name="ExtractEntities",
            doc="Extract named entities from text",
            inputs=[Field("text", "Source text to analyze")],
            outputs=[Field("entities", "List of entities", "list")]
        )
    """

    name: str
    doc: str
    inputs: list[Field] = field(default_factory=list)
    outputs: list[Field] = field(default_factory=list)

    def to_xml_schema(self) -> str:
        """Render signature as XML task schema for Claude prompting."""
        lines = [f'<task name="{self.name}">']
        lines.append(f"  <description>{self.doc}</description>")
        lines.append("  <inputs>")
        for f in self.inputs:
            req = ' required="true"' if f.required else ""
            lines.append(f'    <field name="{f.name}" type="{f.field_type}"{req}>')
            lines.append(f"      {f.description}")
            lines.append("    </field>")
        lines.append("  </inputs>")
        lines.append("  <outputs>")
        for f in self.outputs:
            lines.append(f'    <field name="{f.name}" type="{f.field_type}">')
            lines.append(f"      {f.description}")
            lines.append("    </field>")
        lines.append("  </outputs>")
        lines.append("</task>")
        return "\n".join(lines)

    def to_prompt_instructions(self) -> str:
        """Generate structured prompt instructions from signature."""
        input_desc = "\n".join(f"- {f.name} ({f.field_type}): {f.description}" for f in self.inputs)
        output_desc = "\n".join(
            f"- {f.name} ({f.field_type}): {f.description}" for f in self.outputs
        )
        return (
            f"## Task: {self.name}\n\n"
            f"{self.doc}\n\n"
            f"### Inputs\n{input_desc}\n\n"
            f"### Required Outputs (respond as JSON)\n{output_desc}"
        )


# ── Module definitions (DSPy-style composable prompt programs) ─


@dataclass
class Prediction:
    """Result of a module execution."""

    outputs: dict[str, Any]
    raw_response: str = ""
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    thinking_tokens: int = 0
    thinking_text: str = ""

    def __getattr__(self, name: str) -> Any:
        if name in self.outputs:
            return self.outputs[name]
        raise AttributeError(f"No output field '{name}'")


class Module:
    """DSPy-style prompt module with typed I/O.

    Wraps a Signature with execution logic. Can be composed
    into pipelines via the >> operator.

    Args:
        signature: The typed I/O contract.
        model: Claude model to use (default: claude-sonnet-4-6).
        system_prompt: Optional system-level instructions.
        temperature: Sampling temperature.
        max_tokens: Max output tokens.
    """

    def __init__(
        self,
        signature: Signature,
        *,
        model: str = "claude-sonnet-4-6",
        system_prompt: str = "",
        temperature: float = 0.0,
        max_tokens: int = 4096,
    ):
        self.signature = signature
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _build_messages(self, inputs: dict[str, Any]) -> list[dict]:
        """Build Claude API messages from signature and inputs."""
        instructions = self.signature.to_prompt_instructions()
        input_text = "\n".join(f"**{k}**: {v}" for k, v in inputs.items())
        user_content = f"{instructions}\n\n---\n\n### Input Values\n{input_text}"

        return [{"role": "user", "content": user_content}]

    async def __call__(self, **inputs: Any) -> Prediction:
        """Execute the module with given inputs.

        Uses the Anthropic SDK with CLAUDE_CODE_OAUTH_TOKEN auth.
        """
        import anthropic

        client = anthropic.Anthropic()
        messages = self._build_messages(inputs)
        system = self.system_prompt or (
            "You are a structured extraction agent. "
            "Respond ONLY with valid JSON matching the output schema. "
            "No commentary, no markdown fences — just the JSON object."
        )

        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system,
            messages=messages,
        )

        raw_text = response.content[0].text
        outputs = self._parse_json_output(raw_text)

        return Prediction(
            outputs=outputs,
            raw_response=raw_text,
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    @staticmethod
    def _parse_json_output(text: str) -> dict[str, Any]:
        """Parse JSON from model output, handling markdown fences."""
        # Strip markdown code fences if present
        cleaned = re.sub(r"^```(?:json)?\n?", "", text.strip())
        cleaned = re.sub(r"\n?```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"raw": text}


class ChainOfThought(Module):
    """DSPy ChainOfThought module — adds reasoning before extraction.

    Instructs the model to think step-by-step before producing
    structured output, improving accuracy on complex extractions.
    """

    def _build_messages(self, inputs: dict[str, Any]) -> list[dict]:
        instructions = self.signature.to_prompt_instructions()
        input_text = "\n".join(f"**{k}**: {v}" for k, v in inputs.items())
        user_content = (
            f"{instructions}\n\n---\n\n### Input Values\n{input_text}\n\n"
            "Think step-by-step in a `reasoning` field, then provide the output fields."
        )
        return [{"role": "user", "content": user_content}]


class ExtendedThinking(Module):
    """DSPy module using Claude's extended thinking (budget_tokens).

    Enables a dedicated thinking budget for complex reasoning before
    generating structured output. The thinking is visible in the response
    and tracked in Prediction.thinking_tokens / thinking_text.

    Budget guidelines (from skills/context-window/shared/extended-thinking.md):
        Simple: 2,000-5,000 | Medium: 5,000-15,000
        Complex: 15,000-50,000 | Maximum: 50,000-128,000

    Args:
        signature: Typed I/O contract.
        budget_tokens: Thinking token budget.
        model: Must be claude-opus-4-6 or claude-sonnet-4-6.
    """

    def __init__(
        self,
        signature: Signature,
        *,
        budget_tokens: int = 10_000,
        model: str = "claude-opus-4-6",
        system_prompt: str = "",
        max_tokens: int = 16_384,
    ):
        super().__init__(
            signature,
            model=model,
            system_prompt=system_prompt,
            temperature=1.0,  # required for extended thinking
            max_tokens=max_tokens,
        )
        self.budget_tokens = budget_tokens

    async def __call__(self, **inputs: Any) -> Prediction:
        """Execute with extended thinking enabled."""
        import anthropic

        client = anthropic.Anthropic()
        messages = self._build_messages(inputs)
        system = self.system_prompt or (
            "You are a structured extraction agent with deep reasoning capability. "
            "Think carefully through each step. "
            "After thinking, respond ONLY with valid JSON matching the output schema."
        )

        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=1.0,
            thinking={
                "type": "enabled",
                "budget_tokens": self.budget_tokens,
            },
            system=system,
            messages=messages,
        )

        # Extract thinking and text blocks separately
        thinking_text = ""
        raw_text = ""
        for block in response.content:
            if block.type == "thinking":
                thinking_text = block.thinking
            elif block.type == "text":
                raw_text = block.text

        outputs = self._parse_json_output(raw_text)
        thinking_tokens = getattr(response.usage, "thinking_tokens", 0) or 0

        return Prediction(
            outputs=outputs,
            raw_response=raw_text,
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            thinking_tokens=thinking_tokens,
            thinking_text=thinking_text,
        )


class AdaptiveThinking(Module):
    """DSPy module using Claude's adaptive thinking mode.

    Adaptive thinking (Claude 4.6) automatically decides how much
    reasoning to apply based on task complexity. Unlike ExtendedThinking
    with a fixed budget, adaptive mode self-calibrates.

    Use for:
    - Architecture decisions where complexity varies
    - Ontology alignment where some entities are trivial, others complex
    - Pipeline design where the model should decide when to think deeply

    Args:
        signature: Typed I/O contract.
        model: Must support adaptive thinking (claude-opus-4-6, claude-sonnet-4-6).
    """

    def __init__(
        self,
        signature: Signature,
        *,
        model: str = "claude-opus-4-6",
        system_prompt: str = "",
        max_tokens: int = 16_384,
    ):
        super().__init__(
            signature,
            model=model,
            system_prompt=system_prompt,
            temperature=1.0,  # required for thinking modes
            max_tokens=max_tokens,
        )

    async def __call__(self, **inputs: Any) -> Prediction:
        """Execute with adaptive thinking."""
        import anthropic

        client = anthropic.Anthropic()
        messages = self._build_messages(inputs)
        system = self.system_prompt or (
            "You are a structured extraction agent with adaptive reasoning. "
            "Apply as much reasoning as the task requires — simple lookups need none, "
            "complex ontology alignment needs deep analysis. "
            "Respond with valid JSON matching the output schema."
        )

        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=1.0,
            thinking={"type": "adaptive"},
            system=system,
            messages=messages,
        )

        thinking_text = ""
        raw_text = ""
        for block in response.content:
            if block.type == "thinking":
                thinking_text = block.thinking
            elif block.type == "text":
                raw_text = block.text

        outputs = self._parse_json_output(raw_text)
        thinking_tokens = getattr(response.usage, "thinking_tokens", 0) or 0

        return Prediction(
            outputs=outputs,
            raw_response=raw_text,
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            thinking_tokens=thinking_tokens,
            thinking_text=thinking_text,
        )


class Pipeline:
    """Compose multiple modules into a sequential pipeline.

    Each module's outputs become the next module's inputs.

    Example:
        pipeline = Pipeline([extract_module, classify_module, summarize_module])
        result = await pipeline(text="...")
    """

    def __init__(self, modules: list[Module]):
        self.modules = modules

    async def __call__(self, **inputs: Any) -> Prediction:
        current_inputs = inputs
        last_prediction: Prediction | None = None
        total_in_tokens = 0
        total_out_tokens = 0

        for module in self.modules:
            last_prediction = await module(**current_inputs)
            total_in_tokens += last_prediction.input_tokens
            total_out_tokens += last_prediction.output_tokens
            # Feed outputs as inputs to next module
            current_inputs = {**current_inputs, **last_prediction.outputs}

        if last_prediction is None:
            return Prediction(outputs={})
        last_prediction.input_tokens = total_in_tokens
        last_prediction.output_tokens = total_out_tokens
        return last_prediction


# ── Headless Subagent Runner ────────────────────────────────


class HeadlessSubagent:
    """Headless DSPy subagent for autonomous structured extraction.

    Runs a pipeline of modules without interactive UI, persisting
    results to Neon Postgres. Designed for batch processing and
    background task execution.

    Args:
        name: Subagent identifier (maps to as:Prompt ontology).
        pipeline: Pipeline of modules to execute.
        neon_url: Neon connection string for result persistence.
    """

    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        *,
        neon_url: str = "",
    ):
        self.name = name
        self.pipeline = pipeline
        self.neon_url = neon_url or os.environ.get("NEON_DATABASE_URL", "")

    async def run(self, inputs: dict[str, Any]) -> Prediction:
        """Execute the subagent pipeline and optionally persist results."""
        prediction = await self.pipeline(**inputs)

        if self.neon_url:
            await self._persist_result(inputs, prediction)

        return prediction

    async def _persist_result(self, inputs: dict[str, Any], prediction: Prediction) -> None:
        """Persist extraction result to Neon as a completed task."""
        from src.neon_db import complete_task, connection_pool, enqueue_task

        async with connection_pool(self.neon_url) as conn:
            task_id = await enqueue_task(
                conn,
                queue_name=f"dspy:{self.name}",
                task_type="knowledge_work",
                skill_name="agentic-prompts",
                task_input=inputs,
            )
            await complete_task(
                conn,
                task_id,
                output={
                    "prediction": prediction.outputs,
                    "model": prediction.model,
                    "tokens": {
                        "input": prediction.input_tokens,
                        "output": prediction.output_tokens,
                    },
                },
            )
            await conn.commit()

    async def run_batch(self, batch: list[dict[str, Any]]) -> list[Prediction]:
        """Execute the subagent on a batch of inputs."""
        return [await self.run(inputs) for inputs in batch]


# ── Pre-built Signatures ────────────────────────────────────

# Entity extraction from crawled pages
EXTRACT_ENTITIES = Signature(
    name="ExtractEntities",
    doc="Extract structured entities from crawled documentation page content.",
    inputs=[
        Field("url", "Source URL of the crawled page"),
        Field("content", "Plain text content of the page"),
        Field("domain", "Domain the page belongs to"),
    ],
    outputs=[
        Field("entities", "List of extracted entities with type and description", "list"),
        Field("relationships", "Relationships between entities", "list"),
        Field("summary", "One-paragraph summary of the page"),
    ],
)

# Classify crawled content by topic
CLASSIFY_CONTENT = Signature(
    name="ClassifyContent",
    doc="Classify crawled content into skill-relevant categories.",
    inputs=[
        Field("content", "Plain text content to classify"),
        Field("title", "Page title"),
    ],
    outputs=[
        Field("primary_category", "Main category (api, sdk, tool, concept, tutorial, reference)"),
        Field("skills", "Relevant skill names from ontology", "list"),
        Field("languages", "Programming languages mentioned", "list"),
        Field("confidence", "Classification confidence 0.0-1.0", "float"),
    ],
)

# Extract API patterns from documentation
EXTRACT_API_PATTERNS = Signature(
    name="ExtractAPIPatterns",
    doc="Extract API usage patterns, code samples, and SDK constructor calls.",
    inputs=[
        Field("content", "Documentation page content"),
        Field("language", "Target programming language"),
    ],
    outputs=[
        Field("patterns", "List of API patterns with name, code, and description", "list"),
        Field("sdk_constructor", "SDK constructor call if mentioned"),
        Field("auth_method", "Authentication method described"),
        Field("models_referenced", "Claude model IDs referenced", "list"),
    ],
)

# Ontology alignment — map extracted data to UDA ontology
ALIGN_TO_ONTOLOGY = Signature(
    name="AlignToOntology",
    doc="Map extracted entities to AgentStreams ontology classes and properties.",
    inputs=[
        Field("entities", "List of extracted entities", "list"),
        Field("relationships", "List of entity relationships", "list"),
        Field("ontology_classes", "Available ontology classes", "list"),
    ],
    outputs=[
        Field("mappings", "Entity-to-class mappings with confidence", "list"),
        Field("new_classes", "Suggested new ontology classes", "list"),
        Field("property_mappings", "Property-to-column mappings", "list"),
    ],
)

# Evaluate a design artifact against sprint contract criteria
EVALUATE_DESIGN = Signature(
    name="EvaluateDesign",
    doc="Grade a frontend design artifact against sprint contract criteria.",
    inputs=[
        Field("artifact_description", "Description of the generated artifact"),
        Field("criteria", "List of evaluation criteria with descriptions", "list"),
        Field("contract_objective", "The sprint contract objective"),
    ],
    outputs=[
        Field("scores", "List of criterion scores with name, score 0-1, feedback", "list"),
        Field("overall_score", "Composite score 0.0-1.0", "float"),
        Field("passed", "Whether the artifact passes all threshold criteria", "bool"),
        Field("summary", "1-paragraph evaluation summary"),
        Field("strategy_recommendation", "Either 'refine' or 'pivot'"),
    ],
)

# Negotiate sprint contract criteria
NEGOTIATE_CONTRACT = Signature(
    name="NegotiateContract",
    doc="Negotiate sprint contract criteria between generator and evaluator.",
    inputs=[
        Field("request", "Original user request"),
        Field("proposed_criteria", "Planner's proposed criteria", "list"),
    ],
    outputs=[
        Field("accepted_criteria", "Finalized criteria with thresholds", "list"),
        Field("max_iterations", "Agreed maximum iterations", "int"),
        Field("acceptance_threshold", "Overall passing threshold", "float"),
    ],
)
