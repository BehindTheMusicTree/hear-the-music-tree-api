from opentelemetry.sdk.trace import ReadableSpan, Span
from opentelemetry.sdk.trace.export import SpanProcessor


class OtelSensitiveSpanProcessor(SpanProcessor):
    """Redacts high-risk span attributes before export."""

    _SENSITIVE_KEYS = {
        "http.request.header.authorization",
        "http.response.header.set-cookie",
        "db.statement",
        "url.full",
    }

    def on_start(self, span: Span, parent_context=None) -> None:
        return

    def on_end(self, span: ReadableSpan) -> None:
        for key in self._SENSITIVE_KEYS:
            if key in span.attributes:
                span.set_attribute(key, "[redacted]")

    def shutdown(self) -> None:
        return

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True
