import logging


class OtelTraceIdFilter(logging.Filter):
    """Adds trace_id and span_id (hex) for log correlation with Grafana Tempo / Loki."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = ""
        record.span_id = ""
        try:
            from opentelemetry import trace

            span = trace.get_current_span()
            ctx = span.get_span_context() if span is not None else None
            if ctx is not None and ctx.is_valid:
                record.trace_id = format(ctx.trace_id, "032x")
                record.span_id = format(ctx.span_id, "016x")
        except Exception:
            pass
        return True
