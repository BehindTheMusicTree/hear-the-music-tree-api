import logging
import os
import sys


def _parse_int_env(var_name: str, default: int) -> int:
    raw = (os.getenv(var_name) or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _parse_float_env(var_name: str, default: float) -> float:
    raw = (os.getenv(var_name) or "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _build_sampler():
    from opentelemetry.sdk.trace.sampling import ALWAYS_OFF, ALWAYS_ON, ParentBasedTraceIdRatio

    sampler_name = (os.getenv("OTEL_TRACES_SAMPLER") or "parentbased_traceidratio").strip().lower()
    if sampler_name == "always_off":
        return ALWAYS_OFF
    if sampler_name == "always_on":
        return ALWAYS_ON

    ratio = _parse_float_env("OTEL_TRACES_SAMPLER_ARG", 1.0)
    if ratio <= 0:
        return ALWAYS_OFF
    if ratio >= 1:
        return ALWAYS_ON
    return ParentBasedTraceIdRatio(ratio)


def setup_otel() -> None:
    """Configure OTLP export and Django/HTTP/DB instrumentation when endpoint is set."""
    if "pytest" in sys.argv[0]:
        return
    if os.getenv("OTEL_SDK_DISABLED", "").lower() in ("1", "true", "yes"):
        return

    endpoint = (os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT") or "").strip()
    if not endpoint:
        return

    service_name = (os.getenv("OTEL_SERVICE_NAME") or "htmt-api").strip()
    deployment_environment = (os.getenv("OTEL_DEPLOYMENT_ENV") or os.getenv("ENV") or "unknown").strip()
    service_version = (os.getenv("OTEL_SERVICE_VERSION") or os.getenv("APP_VERSION") or "unknown").strip()

    max_attribute_length = _parse_int_env("OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT", 2048)
    schedule_delay_ms = _parse_int_env("OTEL_BSP_SCHEDULE_DELAY_MS", 5000)
    max_queue_size = _parse_int_env("OTEL_BSP_MAX_QUEUE_SIZE", 2048)
    max_export_batch_size = _parse_int_env("OTEL_BSP_MAX_EXPORT_BATCH_SIZE", 512)
    export_timeout_ms = _parse_int_env("OTEL_BSP_EXPORT_TIMEOUT_MS", 30000)

    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.trace.span_limits import SpanLimits

    from api.logging.OtelSensitiveSpanProcessor import OtelSensitiveSpanProcessor

    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": service_version,
            "deployment.environment": deployment_environment,
        }
    )
    provider = TracerProvider(
        resource=resource,
        sampler=_build_sampler(),
        span_limits=SpanLimits(max_attribute_length=max_attribute_length),
    )
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=endpoint),
            schedule_delay_millis=schedule_delay_ms,
            max_queue_size=max_queue_size,
            max_export_batch_size=max_export_batch_size,
            export_timeout_millis=export_timeout_ms,
        )
    )
    provider.add_span_processor(OtelSensitiveSpanProcessor())
    trace.set_tracer_provider(provider)

    DjangoInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()
    RequestsInstrumentor().instrument()

    logging.getLogger(__name__).debug(
        "OpenTelemetry enabled service=%s env=%s version=%s endpoint=%s",
        service_name,
        deployment_environment,
        service_version,
        endpoint,
    )
