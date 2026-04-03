"""Tests for DSPy prompt modules and signatures."""

import json

from agentstreams.dspy_prompts.modules import (
    ClassifyPageModule,
    CrawlAnalysisPipeline,
    ExtractPatternsModule,
    GenerateGraphQLModule,
    SummarizeCrawlModule,
    ValidateEntityModule,
)
from agentstreams.dspy_prompts.signatures import (
    ClassifyPageSignature,
    ExtractPatternsSignature,
    GenerateGraphQLSignature,
    SummarizeCrawlSignature,
    ValidateEntitySignature,
)


def test_classify_page_prompt():
    module = ClassifyPageModule()
    sig = ClassifyPageSignature(
        url="https://platform.claude.com/docs/en/tool-use",
        content="Tool use allows Claude to interact with external tools...",
    )
    prompt = module.forward(sig)
    assert "<task>" in prompt
    assert "<inputs>" in prompt
    assert "<output_format>" in prompt
    assert "page_type" in prompt
    assert "topics" in prompt


def test_extract_patterns_prompt():
    module = ExtractPatternsModule()
    sig = ExtractPatternsSignature(
        url="https://platform.claude.com/docs/en/sdk-python",
        content="import anthropic\nclient = anthropic.Anthropic()\n...",
        page_type="reference",
    )
    prompt = module.forward(sig)
    assert "sdk_patterns" in prompt
    assert "api_surface" in prompt
    assert "code_languages" in prompt


def test_validate_entity_prompt():
    module = ValidateEntityModule()
    sig = ValidateEntitySignature(
        entity_name="Model",
        entity_data={"model_id": "claude-opus-4-6", "family": "Claude 4.6"},
        ontology_class="as:Model",
    )
    prompt = module.forward(sig)
    assert "is_valid" in prompt
    assert "violations" in prompt


def test_summarize_crawl_prompt():
    module = SummarizeCrawlModule()
    sig = SummarizeCrawlSignature(
        domain="platform.claude.com",
        page_count=150,
        error_count=3,
        bloom_stats={"count": 150, "fill_ratio": 0.002},
        top_topics=["tool-use", "agents", "mcp"],
    )
    prompt = module.forward(sig)
    assert "summary" in prompt
    assert "recommendations" in prompt


def test_generate_graphql_prompt():
    module = GenerateGraphQLModule()
    sig = GenerateGraphQLSignature(
        entity_name="Skill",
        fields_requested=["name", "description"],
        filters={"name": "crawl-ingest"},
    )
    prompt = module.forward(sig)
    assert "query" in prompt
    assert "variables" in prompt


def test_crawl_analysis_pipeline():
    pipeline = CrawlAnalysisPipeline()
    prompts = pipeline.build_prompts(
        url="https://example.com/page",
        content="This is a guide about agents...",
        domain="example.com",
    )
    assert len(prompts) == 3
    assert prompts[0]["stage"] == "classify"
    assert prompts[1]["stage"] == "extract"
    assert prompts[2]["stage"] == "summarize"
    # Each prompt should have XML structure
    for p in prompts:
        assert "<task>" in p["prompt"]
        assert "<inputs>" in p["prompt"]


def test_prompt_xml_structure():
    """All prompts should have well-formed XML-ish structure."""
    module = ClassifyPageModule()
    sig = ClassifyPageSignature(url="https://example.com", content="test")
    prompt = module.forward(sig)

    # Check opening and closing tags match
    for tag in ["task", "inputs", "output_format", "instructions"]:
        assert f"<{tag}>" in prompt
        assert f"</{tag}>" in prompt
