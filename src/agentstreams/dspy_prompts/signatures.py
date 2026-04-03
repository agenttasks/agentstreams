"""DSPy signatures for AgentStreams pipeline stages.

Each signature defines a typed input/output contract for a prompt module.
These compose into pipelines: crawl → extract → classify → persist.

Uses DSPy's Signature pattern for programmatic prompt optimization.
When DSPy is not installed, signatures are plain dataclass contracts
that can still drive Claude Agent SDK subagent prompts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ── Signature contracts (work with or without dspy) ─────────


@dataclass
class ClassifyPageSignature:
    """Classify a crawled page into type and topics.

    Input: url, content (first 3000 chars)
    Output: page_type, topics, confidence
    """

    # Inputs
    url: str = ""
    content: str = ""

    # Outputs
    page_type: str = ""
    topics: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class ExtractPatternsSignature:
    """Extract SDK patterns, API surface, and code languages from a page.

    Input: url, content, page_type
    Output: sdk_patterns, api_surface, code_languages, cross_references
    """

    # Inputs
    url: str = ""
    content: str = ""
    page_type: str = ""

    # Outputs
    sdk_patterns: list[str] = field(default_factory=list)
    api_surface: list[str] = field(default_factory=list)
    code_languages: list[str] = field(default_factory=list)
    cross_references: list[str] = field(default_factory=list)


@dataclass
class ValidateEntitySignature:
    """Validate a UDA entity against ontology constraints.

    Input: entity_name, entity_data, ontology_class
    Output: is_valid, violations, suggestions
    """

    # Inputs
    entity_name: str = ""
    entity_data: dict[str, Any] = field(default_factory=dict)
    ontology_class: str = ""

    # Outputs
    is_valid: bool = True
    violations: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class SummarizeCrawlSignature:
    """Summarize crawl results for pipeline reporting.

    Input: domain, page_count, error_count, bloom_stats, top_topics
    Output: summary, recommendations, metrics_snapshot
    """

    # Inputs
    domain: str = ""
    page_count: int = 0
    error_count: int = 0
    bloom_stats: dict[str, Any] = field(default_factory=dict)
    top_topics: list[str] = field(default_factory=list)

    # Outputs
    summary: str = ""
    recommendations: list[str] = field(default_factory=list)
    metrics_snapshot: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerateGraphQLSignature:
    """Generate GraphQL query for UDA entity access.

    Input: entity_name, fields_requested, filters
    Output: query, variables, explanation
    """

    # Inputs
    entity_name: str = ""
    fields_requested: list[str] = field(default_factory=list)
    filters: dict[str, Any] = field(default_factory=dict)

    # Outputs
    query: str = ""
    variables: dict[str, Any] = field(default_factory=dict)
    explanation: str = ""
