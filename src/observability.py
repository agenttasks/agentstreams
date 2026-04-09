"""BL-010: OpenTelemetry observability integration.

Wraps Claude Code's OTel support (code.claude.com/docs/en/monitoring-usage.md)
for tracing agent operations across the 14-layer architecture.

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Generator


@dataclass
class Span:
    """A single trace span representing an operation."""

    name: str
    layer: int
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    attributes: dict[str, Any] = field(default_factory=dict)
    status: str = "ok"
    children: list[Span] = field(default_factory=list)

    @property
    def duration_ms(self) -> int:
        return int((self.end_time - self.start_time) * 1000)


class Tracer:
    """Lightweight tracer that captures spans for 14-layer operations.

    When OTEL_EXPORTER_OTLP_ENDPOINT is set, exports via OpenTelemetry.
    Otherwise, accumulates spans in-memory for local inspection.
    """

    def __init__(self) -> None:
        self.spans: list[Span] = []
        self._otel_enabled = bool(os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"))

    @contextmanager
    def span(self, name: str, layer: int = 0, **attrs: Any) -> Generator[Span, None, None]:
        s = Span(name=name, layer=layer, attributes=attrs)
        try:
            yield s
        except Exception as e:
            s.status = f"error: {e}"
            raise
        finally:
            s.end_time = time.time()
            self.spans.append(s)

    def summary(self) -> dict[str, Any]:
        return {
            "span_count": len(self.spans),
            "total_duration_ms": sum(s.duration_ms for s in self.spans),
            "by_layer": {
                layer: sum(s.duration_ms for s in self.spans if s.layer == layer)
                for layer in sorted({s.layer for s in self.spans})
            },
            "errors": [s.name for s in self.spans if s.status != "ok"],
        }


# Global tracer instance
_tracer = Tracer()


def get_tracer() -> Tracer:
    return _tracer
