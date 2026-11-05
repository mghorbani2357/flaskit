# Configuration

Generated `config.py` is **flat** (no classes). Every setting is an `UPPER_CASE` name read from the environment.

Values in `.env.example` are documentation only unless you export them yourself (or use a loader such as your shell / process manager). The app reads **`os.environ`**.

## API / Swagger

| Variable | Default | Notes |
|----------|---------|-------|
| `API_TITLE` | init project name | Swagger title |
| `API_DESCRIPTION` | `{name} API` | OpenAPI description |
| `API_VERSION` | `1.0.0` | Also set from Docker `DOCKER_TAG` |
| `OPENAPI_VERSION` | `3.0.3` | |
| `BASE_PATH` | `/` | Path prefix for routes; also OpenAPI `servers` when not empty/`/` |
| `DOCS_PATH` | `/docs` | Swagger UI mount |

## Runtime

| Variable | Default | Notes |
|----------|---------|-------|
| `ENV` / `FLASK_ENV` | `development` | `production` / `prod` → bjoern |
| `DEBUG` | true in development | Flask debug flag |
| `HOST` | `127.0.0.1` | Docker sets `0.0.0.0` |
| `PORT` | `5000` | Docker sets `80` |
| `BJOERN_REUSE_PORT` | `true` | Linux `SO_REUSEPORT` |
| `STATIC_CACHE_MAX_AGE` | `604800` | Browser cache TTL (seconds) for `/assets/statics/` |
| `SECRET_KEY` | `change-me` | Change in real deployments |

## Auth (Swagger Authorize)

| Variable | Default |
|----------|---------|
| `AUTH_SCHEME` | `bearer` (`apiKey` also supported) |
| `AUTH_HEADER` | `Authorization` |
| `AUTH_BEARER_FORMAT` | `JWT` |
| `AUTH_SECURITY_NAME` | `httpAuth` |

## Logging

See [Logging](logging.md) for the full list (`LOG_LEVEL`, `LOG_OUTPUT`, per-logger names/files, rotation, redaction).

## OpenTelemetry

| Variable | Default |
|----------|---------|
| `OTEL_ENABLED` | `false` |
| `OTEL_SERVICE_NAME` | project name |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc` (`http` / `http/protobuf` also accepted) |

## `BASE_PATH` behavior

- Path-like values (`/`, `/api`) are joined with each module `URL_PREFIX` for routing.
- Absolute `http(s)://...` values are **not** prepended to Flask routes; use them when you only need a Swagger server URL.
- OpenAPI `servers` (and the Swagger Servers dropdown) appear only when `BASE_PATH` is set to something other than empty or `/`.
