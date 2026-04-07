"""Tests for src/tracing.py — OpenTelemetry tracing integration."""

from __future__ import annotations

import pytest

import src.tracing
from src.tracing import (
    get_tracer,
    trace_agent_task,
    trace_crawl_pipeline,
    trace_dspy_module,
    trace_embedding,
    trace_span,
)


@pytest.fixture(autouse=True)
def _disable_otel(monkeypatch):
    """Disable OTel exporter for all tests to avoid network calls."""
    monkeypatch.setenv("OTEL_TRACES_ENABLED", "false")
    src.tracing._initialized = False
    src.tracing._tracer = None
    yield
    src.tracing._initialized = False
    src.tracing._tracer = None


class TestTraceSpan:
    def test_yields_span_context(self):
        with trace_span("test_span") as ctx:
            ctx["custom_key"] = "custom_value"
        assert "duration_ms" in ctx
        assert ctx["custom_key"] == "custom_value"

    def test_records_duration(self):
        with trace_span("timed_span") as ctx:
            pass
        assert ctx["duration_ms"] >= 0

    def test_attributes_passed(self):
        with trace_span("attr_span", attributes={"key": "value"}) as ctx:
            pass
        assert "duration_ms" in ctx

    def test_exception_propagates(self):
        try:
            with trace_span("error_span") as ctx:
                raise ValueError("test error")
        except ValueError:
            pass
        assert "duration_ms" in ctx


class TestTraceHelpers:
    def test_crawl_pipeline_span(self):
        with trace_crawl_pipeline("test-crawl", ["example.com"]) as ctx:
            ctx["pages"] = 42
        assert ctx["pages"] == 42

    def test_dspy_module_span(self):
        with trace_dspy_module("ExtractEntities", "ExtractEntities", "claude-sonnet-4-6") as ctx:
            ctx["tokens"] = 1000
        assert ctx["tokens"] == 1000

    def test_dspy_module_with_thinking(self):
        with trace_dspy_module(
            "AlignToOntology", "AlignToOntology", "claude-opus-4-6", "extended"
        ) as ctx:
            ctx["thinking_tokens"] = 15000
        assert ctx["thinking_tokens"] == 15000

    def test_embedding_span(self):
        with trace_embedding("lancedb", wing="docs", room="tool-use", chunk_count=10) as ctx:
            ctx["stored"] = 10
        assert ctx["stored"] == 10

    def test_agent_task_span(self):
        with trace_agent_task("task-001", "crawl", "claude-sonnet-4-6") as ctx:
            ctx["status"] = "completed"
        assert ctx["status"] == "completed"


class TestTracerInit:
    def test_disabled_when_env_false(self):
        tracer = get_tracer()
        assert tracer is None

    def test_span_works_without_tracer(self):
        with trace_span("no_tracer_span") as ctx:
            ctx["data"] = "works"
        assert ctx["data"] == "works"
        assert ctx["duration_ms"] >= 0
