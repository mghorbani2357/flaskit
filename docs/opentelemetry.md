# OpenTelemetry

Optional. Off by default (`OTEL_ENABLED=false`).

## Traces

When `OTEL_ENABLED=true`, the generated app:

1. Configures a `TracerProvider` with `OTEL_SERVICE_NAME`
2. Exports spans via OTLP (`grpc` by default, or HTTP)
3. Instruments Flask with `opentelemetry-instrumentation-flask`
4. Injects W3C `traceparent` on responses when a valid span is active

Request/response JSON logs include `trace_id` and `span_id` from the active span (stdlib loggers keep their existing fields).

## Logs bridge

When `OTEL_LOGS_ENABLED=true` (defaults to the same as `OTEL_ENABLED`):

- An OpenTelemetry `LoggingHandler` is attached to the app / request / response loggers
- If `LOG_OUTPUT` includes `stream`, a `ConsoleLogExporter` is registered
- File sinks continue via the configured stdlib file handlers (`LOG_OUTPUT` containing `file`)

Dependencies ship in the generated `requirements.txt`. Ensure a collector is reachable at `OTEL_EXPORTER_OTLP_ENDPOINT`.

```bash
export OTEL_ENABLED=true
export OTEL_LOGS_ENABLED=true
export OTEL_SERVICE_NAME=myapi
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export LOG_OUTPUT=stream,file
python app.py
```

If OpenTelemetry packages are missing, the app logs a warning and continues without tracing. All OTel imports live at the **top** of `app.py` (optional `try` / `except ImportError`).
