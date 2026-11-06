# Configuration

Generated `config.py` is **flat** (no classes). Every setting is an `UPPER_CASE` name read from `os.environ`.

`.env.example` documents variables; the process must actually export them (shell, Docker, process manager, or a loader you add yourself).

## API / Swagger

| Variable | Default | Notes |
|----------|---------|-------|
| `API_TITLE` | init project name | Swagger title |
| `API_DESCRIPTION` | `{name} API` | OpenAPI description |
| `API_VERSION` | `1.0.0` | Also set from Docker `DOCKER_TAG` |
| `OPENAPI_VERSION` | `3.0.3` | |
| `BASE_PATH` | `/` | Prefix for **routes, docs, and assets**; OpenAPI `servers` when not empty/`/` |
| `DOCS_PATH` | `/docs` | Docs segment joined under `BASE_PATH` |

## Timezone

| Variable | Default | Notes |
|----------|---------|-------|
| `TIMEZONE` | `UTC` | IANA name (`Asia/Tehran`, `Europe/Berlin`, …). Invalid values fall back to UTC. Bundled via `tzdata` for Windows/minimal images. |

Helpers: `config.TZ` (`ZoneInfo`), log fields `timezone` and `tz_offset`.

## Runtime

| Variable | Default | Notes |
|----------|---------|-------|
| `ENV` / `FLASK_ENV` | `development` | `production` / `prod` → bjoern |
| `DEBUG` | true in development | Flask debug |
| `HOST` | `127.0.0.1` | Docker: `0.0.0.0` |
| `PORT` | `5000` | Docker: `80` |
| `BJOERN_REUSE_PORT` | `true` | Linux `SO_REUSEPORT` |
| `STATIC_CACHE_MAX_AGE` | `604800` | Cache-Control for `{BASE_PATH}/assets/statics/` |
| `SECRET_KEY` | `change-me` | Change in real deployments |

## Auth (Swagger Authorize)

| Variable | Default |
|----------|---------|
| `AUTH_SCHEME` | `bearer` (`apiKey` also supported) |
| `AUTH_HEADER` | `Authorization` |
| `AUTH_BEARER_FORMAT` | `JWT` |
| `AUTH_SECURITY_NAME` | `httpAuth` |

## Logging

See [Logging](logging.md) (`LOG_LEVEL`, `LOG_OUTPUT`, per-logger names/files, rotation, redaction).

## OpenTelemetry

| Variable | Default |
|----------|---------|
| `OTEL_ENABLED` | `false` |
| `OTEL_LOGS_ENABLED` | same as `OTEL_ENABLED` |
| `OTEL_SERVICE_NAME` | project name |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc` (`http` / `http/protobuf` accepted) |

## `BASE_PATH` behavior

Helpers in `config.py`:

| Helper | Purpose |
|--------|---------|
| `app_path(*parts)` | Join `BASE_PATH` with segments |
| `route_prefix(blueprint_path)` | Module mount path |
| `docs_url_prefix()` | Docs under `BASE_PATH` |
| `assets_url_path()` | Flask `static_url_path` under `BASE_PATH` |

Examples with `BASE_PATH=/api`:

| Resource | URL |
|----------|-----|
| Module `users` (`URL_PREFIX=/users`) | `/api/users/` |
| Swagger UI | `/api/docs` |
| OpenAPI JSON | `/api/docs/openapi.json` |
| Swagger assets | `/api/assets/swagger-ui/...` |
| Public statics | `/api/assets/statics/...` |

- Path-like values (`/`, `/api`) are prepended to Flask routes and static URLs.
- Absolute `http(s)://...` values are **not** prepended to routes; use them when you only need a Swagger server URL.
- OpenAPI `servers` (and the Swagger Servers dropdown) appear only when `BASE_PATH` is not empty or `/`.

### Examples

=== "Windows cmd"

    ```bat
    set BASE_PATH=/api
    set TIMEZONE=Asia/Tehran
    set PORT=8082
    python app.py
    ```

=== "PowerShell"

    ```powershell
    $env:BASE_PATH="/api"
    $env:TIMEZONE="Asia/Tehran"
    $env:PORT="8082"
    python app.py
    ```

=== "Linux / macOS"

    ```bash
    export BASE_PATH=/api
    export TIMEZONE=Asia/Tehran
    export PORT=8082
    python app.py
    ```
