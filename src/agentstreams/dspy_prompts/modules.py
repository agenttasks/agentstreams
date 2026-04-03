"""DSPy prompt modules for headless subagent orchestration.

Each module wraps a signature into an executable prompt that can be
called via Claude Agent SDK or directly with the Anthropic API.

When DSPy is installed, modules support automatic prompt optimization.
Without DSPy, they generate structured XML prompts for Claude subagents.
"""

from __future__ import annotations

import json
from typing import Any

from .signatures import (
    ClassifyPageSignature,
    ExtractPatternsSignature,
    GenerateGraphQLSignature,
    SummarizeCrawlSignature,
    ValidateEntitySignature,
)


def _build_xml_prompt(
    task: str,
    inputs: dict[str, Any],
    output_schema: dict[str, str],
) -> str:
    """Build a structured XML prompt for Claude subagent execution.

    Uses XML tags for structured input/output — Claude excels at following
    XML-structured instructions.
    """
    input_xml = "\n".join(
        f"  <{k}>{json.dumps(v) if isinstance(v, (list, dict)) else v}</{k}>"
        for k, v in inputs.items()
        if v
    )
    output_fields = "\n".join(
        f"  <{k}>{desc}</{k}>" for k, desc in output_schema.items()
    )

    return f"""<task>{task}</task>

<inputs>
{input_xml}
</inputs>

<output_format>
{output_fields}
</output_format>

<instructions>
Analyze the inputs and produce a JSON response matching the output_format fields.
Return ONLY valid JSON with the specified keys. No markdown, no explanation.
</instructions>"""


class ClassifyPageModule:
    """Classify a crawled page into type and topics.

    Generates a structured prompt that a Claude subagent can execute.
    """

    def forward(self, sig: ClassifyPageSignature) -> str:
        """Build the classification prompt."""
        return _build_xml_prompt(
            task="Classify this web page into a type and extract topic tags.",
            inputs={"url": sig.url, "content": sig.content[:3000]},
            output_schema={
                "page_type": "One of: guide, reference, tutorial, blog, changelog, api-doc",
                "topics": "Up to 5 topic tags from: tool-use, streaming, models, agents, mcp, evals, vision, thinking, batch, embeddings",
                "confidence": "Float 0.0-1.0 indicating classification confidence",
            },
        )


class ExtractPatternsModule:
    """Extract SDK patterns and API surface from a page."""

    def forward(self, sig: ExtractPatternsSignature) -> str:
        return _build_xml_prompt(
            task="Extract SDK patterns, API surface, and code languages from this documentation page.",
            inputs={
                "url": sig.url,
                "content": sig.content[:5000],
                "page_type": sig.page_type,
            },
            output_schema={
                "sdk_patterns": "List of SDK constructor/usage patterns found (e.g. 'new Anthropic()', 'anthropic.Anthropic()')",
                "api_surface": "List of API method names, endpoints, model IDs mentioned",
                "code_languages": "List of programming languages with code examples: python, typescript, java, go, ruby, csharp, php, curl",
                "cross_references": "List of URLs referenced by this page",
            },
        )


class ValidateEntityModule:
    """Validate a UDA entity against ontology constraints."""

    def forward(self, sig: ValidateEntitySignature) -> str:
        return _build_xml_prompt(
            task="Validate this UDA entity against its ontology class constraints.",
            inputs={
                "entity_name": sig.entity_name,
                "entity_data": sig.entity_data,
                "ontology_class": sig.ontology_class,
            },
            output_schema={
                "is_valid": "Boolean — true if entity passes all constraints",
                "violations": "List of constraint violations found",
                "suggestions": "List of suggestions to fix violations",
            },
        )


class SummarizeCrawlModule:
    """Summarize crawl results for pipeline reporting."""

    def forward(self, sig: SummarizeCrawlSignature) -> str:
        return _build_xml_prompt(
            task="Summarize these crawl results and provide recommendations.",
            inputs={
                "domain": sig.domain,
                "page_count": sig.page_count,
                "error_count": sig.error_count,
                "bloom_stats": sig.bloom_stats,
                "top_topics": sig.top_topics,
            },
            output_schema={
                "summary": "2-3 sentence summary of the crawl results",
                "recommendations": "List of actionable recommendations for the next crawl",
                "metrics_snapshot": "Dict of key metrics: {pages_per_sec, dedup_ratio, error_rate}",
            },
        )


class GenerateGraphQLModule:
    """Generate a GraphQL query for UDA entity access."""

    def forward(self, sig: GenerateGraphQLSignature) -> str:
        return _build_xml_prompt(
            task="Generate a GraphQL query to access this UDA entity via pg_graphql.",
            inputs={
                "entity_name": sig.entity_name,
                "fields_requested": sig.fields_requested,
                "filters": sig.filters,
            },
            output_schema={
                "query": "GraphQL query string",
                "variables": "GraphQL variables dict",
                "explanation": "Brief explanation of what the query does",
            },
        )


# ── Pipeline composition ────────────────────────────────────


class CrawlAnalysisPipeline:
    """Composed pipeline: classify → extract → summarize.

    Chains DSPy modules into a full analysis pipeline that can be
    executed by a Claude subagent in sequence.
    """

    def __init__(self) -> None:
        self.classify = ClassifyPageModule()
        self.extract = ExtractPatternsModule()
        self.summarize = SummarizeCrawlModule()

    def build_prompts(
        self,
        url: str,
        content: str,
        domain: str = "",
    ) -> list[dict[str, str]]:
        """Build the sequence of prompts for the full pipeline.

        Returns a list of {stage, prompt} dicts that a subagent
        executes in order, passing outputs forward.
        """
        classify_sig = ClassifyPageSignature(url=url, content=content)
        extract_sig = ExtractPatternsSignature(url=url, content=content)
        summarize_sig = SummarizeCrawlSignature(domain=domain, page_count=1)

        return [
            {"stage": "classify", "prompt": self.classify.forward(classify_sig)},
            {"stage": "extract", "prompt": self.extract.forward(extract_sig)},
            {"stage": "summarize", "prompt": self.summarize.forward(summarize_sig)},
        ]
