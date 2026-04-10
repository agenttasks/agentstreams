"""OpenTelemetry tracing for AgentStreams UDA pipelines.

Instruments crawl, extract, embed, and agent task pipelines with
distributed traces exportable to any OTLP-compatible backend
(Jaeger, Grafana Tempo, Honeycomb, Datadog, etc.).

Trace hierarchy:
    pipeline span (root)
    ├── crawl span
    │   ├── sitemap_parse span
    │   ├── fetch_page span (per URL)
    │   └── persist span
    ├── extract span
    │   ├── dspy_module span (per signature)
    │   └── thinking span (extended/adaptive)
    └── embed span
        ├── chunk span
        └── store span (lance / pgvector)

Environment:
    OTEL_EXPORTER_OTLP_ENDPOINT: OTLP endpoint (default: http://localhost:4318)
    OTEL_SERVICE_NAME: Service name (default: agentstreams)
    OTEL_TRACES_ENABLED: Set to "false" to disable (default: true)
    OTEL_LOG_USER_PROMPTS: Include user prompts in spans (default: false)
    OTEL_LOG_TOOL_DETAILS: Include tool call details in spans (default: false)
    OTEL_LOG_TOOL_CONTENT: Include tool result content in spans (default: false)
"""

from __future__ import annotations

import os
import time
from collections.abc import Generator
from contextlib import AbstractContextManager, contextmanager
from typing import Any

# Lazy imports to avoid hard dependency
_tracer = None
_initialized = False

# 2.1.101 OTEL logging flags — control sensitive span attributes
_log_prompts = False
_log_tool_details = False
_log_tool_content = False

# Attribute keywords by category — each gated by its own flag
_PROMPT_KEYWORDS = {"prompt", "user_input", "request"}
_TOOL_DETAIL_KEYWORDS = {"tool", "function", "method", "action"}
_TOOL_CONTENT_KEYWORDS = {"content", "output", "text", "body", "response", "result"}


def _should_log_attribute(key: str) -> bool:
    """Check if a sensitive span attribute should be logged.

    Each flag controls its own category:
    - OTEL_LOG_USER_PROMPTS → prompt, user_input, request
    - OTEL_LOG_TOOL_DETAILS → tool, function, method, action
    - OTEL_LOG_TOOL_CONTENT → content, output, text, body, response, result

    Non-sensitive attributes (e.g. duration_ms, model, status) always pass.
    """
    key_lower = key.lower()
    if any(kw in key_lower for kw in _PROMPT_KEYWORDS):
        return _log_prompts
    if any(kw in key_lower for kw in _TOOL_DETAIL_KEYWORDS):
        return _log_tool_details
    if any(kw in key_lower for kw in _TOOL_CONTENT_KEYWORDS):
        return _log_tool_content
    return True  # Non-sensitive attributes always logged


def _init_tracer():
    """Initialize the OTel tracer provider. Idempotent."""
    global _tracer, _initialized, _log_prompts, _log_tool_details, _log_tool_content
    if _initialized:
        return
    _initialized = True

    # Parse 2.1.101 logging flags
    _log_prompts = os.environ.get("OTEL_LOG_USER_PROMPTS", "false").lower() == "true"
    _log_tool_details = os.environ.get("OTEL_LOG_TOOL_DETAILS", "false").lower() == "true"
    _log_tool_content = os.environ.get("OTEL_LOG_TOOL_CONTENT", "false").lower() == "true"

    if os.environ.get("OTEL_TRACES_ENABLED", "true").lower() == "false":
        return

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        service_name = os.environ.get("OTEL_SERVICE_NAME", "agentstreams")
        resource = Resource.create({"service.name": service_name})

        provider = TracerProvider(resource=resource)
        endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
        exporter = OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces")
        provider.add_span_processor(BatchSpanProcessor(exporter))

        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer("agentstreams", "0.1.0")
    except ImportError:
        pass  # OTel packages not installed — tracing disabled


def get_tracer():
    """Get the AgentStreams OTel tracer. Returns None if tracing disabled."""
    _init_tracer()
    return _tracer


@contextmanager
def trace_span(
    name: str,
    *,
    attributes: dict[str, Any] | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Context manager for tracing a span.

    Works whether OTel is installed or not — when disabled, yields
    a simple dict that collects timing without exporting.

    Usage:
        with trace_span("crawl_page", attributes={"url": url}) as span_ctx:
            result = await fetch(url)
            span_ctx["status_code"] = 200
    """
    tracer = get_tracer()
    span_ctx: dict[str, Any] = {"start_time": time.monotonic()}

    if tracer is not None:
        with tracer.start_as_current_span(name) as span:
            if attributes:
                for k, v in attributes.items():
                    if not _should_log_attribute(k):
                        continue
                    span.set_attribute(k, str(v) if not isinstance(v, (int, float, bool)) else v)
            try:
                yield span_ctx
            except Exception as e:
                span.set_attribute("error", True)
                span.set_attribute("error.message", str(e))
                raise
            finally:
                elapsed = time.monotonic() - span_ctx["start_time"]
                span.set_attribute("duration_ms", int(elapsed * 1000))
                for k, v in span_ctx.items():
                    if k != "start_time":
                        if not _should_log_attribute(k):
                            continue
                        span.set_attribute(
                            k,
                            str(v) if not isinstance(v, (int, float, bool)) else v,
                        )
    else:
        try:
            yield span_ctx
        finally:
            span_ctx["duration_ms"] = int((time.monotonic() - span_ctx["start_time"]) * 1000)


def trace_crawl_pipeline(
    pipeline_name: str,
    domains: list[str],
) -> AbstractContextManager[dict[str, Any]]:
    """Create a root span for a crawl pipeline."""
    return trace_span(
        "crawl_pipeline",
        attributes={
            "pipeline.name": pipeline_name,
            "pipeline.domains": ",".join(domains),
            "pipeline.type": "crawl",
        },
    )


def trace_dspy_module(
    module_name: str,
    signature_name: str,
    model: str,
    thinking_type: str = "",
) -> AbstractContextManager[dict[str, Any]]:
    """Create a span for a DSPy module execution."""
    attrs = {
        "dspy.module": module_name,
        "dspy.signature": signature_name,
        "dspy.model": model,
    }
    if thinking_type:
        attrs["dspy.thinking_type"] = thinking_type
    return trace_span("dspy_module", attributes=attrs)


def trace_embedding(
    backend: str,
    wing: str = "",
    room: str = "",
    chunk_count: int = 0,
) -> AbstractContextManager[dict[str, Any]]:
    """Create a span for an embedding operation."""
    return trace_span(
        "embedding",
        attributes={
            "embedding.backend": backend,
            "embedding.wing": wing,
            "embedding.room": room,
            "embedding.chunks": chunk_count,
        },
    )


def trace_agent_task(
    task_id: str,
    task_type: str,
    model: str,
) -> AbstractContextManager[dict[str, Any]]:
    """Create a span for an Agent SDK task execution."""
    return trace_span(
        "agent_task",
        attributes={
            "agent.task_id": task_id,
            "agent.task_type": task_type,
            "agent.model": model,
        },
    )


def trace_harness_run(
    harness_name: str,
    sprint_id: str,
    max_iterations: int = 5,
) -> AbstractContextManager[dict[str, Any]]:
    """Create a root span for a GAN-inspired harness run."""
    return trace_span(
        "harness_run",
        attributes={
            "harness.name": harness_name,
            "harness.sprint_id": sprint_id,
            "harness.max_iterations": max_iterations,
        },
    )
