# OpenTelemetry

Optional. Off by default (`OTEL_ENABLED=false`).

When enabled, the generated app:

1. Configures a `TracerProvider` with `OTEL_SERVICE_NAME`
2. Exports spans via OTLP (`grpc` by default, or HTTP)
3. Instruments Flask with `opentelemetry-instrumentation-flask`
4. Injects W3C `traceparent` on responses when a valid span is active

Dependencies are already listed in the generated `requirements.txt`. Ensure an OTLP collector is reachable at `OTEL_EXPORTER_OTLP_ENDPOINT`.

```bash
OTEL_ENABLED=true \
OTEL_SERVICE_NAME=myapi \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
python app.py
```

If OpenTelemetry packages are missing, the app logs a warning and continues without tracing.
