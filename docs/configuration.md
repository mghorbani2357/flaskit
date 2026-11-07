# Configuration (`.env`)

Generated projects use a flat **`.env`** file next to `app.py`. `config.py` loads it with `python-dotenv` (`override=False`), then reads `os.environ`.

| Rule | Meaning |
|------|---------|
| Process env wins | If a variable is already set in the shell/container, `.env` does not override it |
| Empty string | Treated like “unset” → default applies |
| Docker | `.dockerignore` excludes `.env`; pass variables into the container at runtime |

Edit `.env`, restart the process, and the new values apply.

---

## API and OpenAPI

| Variable | Default | What it does |
|----------|---------|--------------|
| `API_TITLE` | folder name from `flaskit init` | Title shown in Swagger UI and OpenAPI `info.title` |
| `API_DESCRIPTION` | `{name} API` | OpenAPI `info.description` |
| `API_VERSION` | `1.0.0` | OpenAPI `info.version`. In Docker, build-arg `DOCKER_TAG` is mapped to this |
| `OPENAPI_VERSION` | `3.0.3` | OpenAPI spec version advertised by Flask-Smorest |
| `BASE_PATH` | `/` | **Prefix for every HTTP surface**: module routes, docs, and `/assets`. Also drives OpenAPI `servers` when not `/` |
| `DOCS_PATH` | `/docs` | Docs path segment under `BASE_PATH` (final URL = `{BASE_PATH}{DOCS_PATH}`) |

### `BASE_PATH` examples

With `BASE_PATH=/api` and a module `URL_PREFIX=/users`:

| Resource | URL |
|----------|-----|
| Users API | `/api/users/` |
| Swagger UI | `/api/docs` |
| OpenAPI JSON | `/api/docs/openapi.json` |
| Swagger UI assets | `/api/assets/swagger-ui/...` |
| Files in `assets/statics/` | `/api/assets/statics/...` |

Notes:

- Path-like values (`/`, `/api`) are joined onto Flask routes and `static_url_path`.
- Absolute `http(s)://…` values are **not** prepended to routes; use them only when you need a public server URL in the OpenAPI document.
- The Swagger **Servers** dropdown appears only when `BASE_PATH` is set to something other than empty or `/`.

Helpers in `config.py`: `app_path()`, `route_prefix()`, `docs_url_prefix()`, `assets_url_path()`.

---

## Timezone

| Variable | Default | What it does |
|----------|---------|--------------|
| `TIMEZONE` | `UTC` | IANA timezone for log payloads (`timezone`, `tz_offset`). Examples: `UTC`, `Asia/Tehran`, `Europe/Berlin` |
| `TZ` | (unset) | Fallback if `TIMEZONE` is unset (common in containers). `TIMEZONE` wins when both are set |

Invalid names fall back to `UTC`. `config.TZ` is a `ZoneInfo` instance used by the app.

---

## Server and runtime

| Variable | Default | What it does |
|----------|---------|--------------|
| `ENV` | `development` | Runtime mode. `development` / `dev` → Flask built-in server. `production` / `prod` → **bjoern** (intended for Docker/Linux) |
| `FLASK_ENV` | (unset) | Used only if `ENV` is unset (legacy Flask name) |
| `DEBUG` | `true` when `ENV` is development | Flask debug reloader / debugger. Keep `false` in production |
| `HOST` | `127.0.0.1` | Bind address. Docker image defaults to `0.0.0.0` |
| `PORT` | `5000` | Bind port. Docker image defaults to `80` |
| `BJOERN_REUSE_PORT` | `true` | Passes `reuse_port` to bjoern (`SO_REUSEPORT` on Linux) |
| `SECRET_KEY` | `change-me` | Flask secret (sessions, extensions). **Change in every real deployment** |
| `FLASK_APP` | `app:create_app` | Used by the `flask` CLI (`flask --app …`). Optional if you always pass `--app` |

CLI flags on `python app.py` (`--host`, `-p`, `-e`, `--debug`) override these for that process only.

---

## Swagger “Authorize” (OpenAPI security scheme)

These configure the **documented** security scheme in Swagger. They do not implement authentication by themselves — see [Customizing the app](extending.md) for JWT.

| Variable | Default | What it does |
|----------|---------|--------------|
| `AUTH_SCHEME` | `bearer` | `bearer` → HTTP Bearer. `apiKey` → API key in a header |
| `AUTH_HEADER` | `Authorization` | Header name when `AUTH_SCHEME=apiKey` |
| `AUTH_BEARER_FORMAT` | `JWT` | Hint shown in Swagger for Bearer tokens |
| `AUTH_SECURITY_NAME` | `httpAuth` | Component name of the security scheme in the OpenAPI document |

---

## Logging

Three loggers: app, request, response. JSON request/response lines go to stream and/or files depending on `LOG_OUTPUT`.

### Shared controls

| Variable | Default | What it does |
|----------|---------|--------------|
| `LOG_LEVEL` | `INFO` | Level for all three loggers. Set `DEBUG` to include base64 request/response **bodies** |
| `LOG_OUTPUT` | `stream,file` | Comma list of sinks: `stream` (console), `file` (log files). Use `stream` alone in Docker |
| `LOG_STREAM` | `stderr` | Console target when `stream` is enabled: `stderr` or `stdout` |
| `LOG_FORMAT` | `%(message)s` | stdlib logging format string (payloads are already JSON in the message) |
| `LOG_DATE_FORMAT` | `%Y-%m-%d %H:%M:%S` | Used if the formatter includes `%(asctime)s` |
| `LOG_PROPAGATE` | `false` | Whether child loggers bubble to the root logger |
| `LOG_REDACT_HEADERS` | `authorization,cookie,set-cookie,x-api-key` | Header names (case-insensitive) replaced with `***` in logs |

### File rotation (when `file` is in `LOG_OUTPUT`)

| Variable | Default | What it does |
|----------|---------|--------------|
| `LOG_ROTATION` | `size` | `size` → rotate by bytes; `time` → rotate by schedule; `none` → single growing file |
| `LOG_MAX_BYTES` | `1048576` | Max size per file when `LOG_ROTATION=size` (1 MiB) |
| `LOG_BACKUP_COUNT` | `5` | How many rotated files to keep |
| `LOG_WHEN` | `midnight` | `TimedRotatingFileHandler` `when` if `LOG_ROTATION=time` |
| `LOG_INTERVAL` | `1` | Interval for timed rotation |

### Per-logger names and paths

| Variable | Default | What it does |
|----------|---------|--------------|
| `LOG_APP_NAME` | `flask.app` | Logger name for application messages |
| `LOG_APP_FILE` | `logs/app.log` | File for app logger (relative to project root unless absolute) |
| `LOG_REQUEST_NAME` | `werkzeug.request` | Logger name for inbound request JSON |
| `LOG_REQUEST_FILE` | `logs/request.log` | File for request logger |
| `LOG_RESPONSE_NAME` | `werkzeug.response` | Logger name for outbound response JSON |
| `LOG_RESPONSE_FILE` | `logs/response.log` | File for response logger |

Request/response JSON includes fields such as `timestamp`, `timezone`, `tz_offset`, `request_id`, `client_ip`, `method`, `path`, optional `trace_id` / `span_id`, and `body` only at `DEBUG`.

To log your own events (app logger, JSON payloads, or a new named logger/file), see [Logging → Log your own data](logging.md#log-your-own-data).

---

## OpenTelemetry

| Variable | Default | What it does |
|----------|---------|--------------|
| `OTEL_ENABLED` | `false` | Enable Flask instrumentation and OTLP span export |
| `OTEL_LOGS_ENABLED` | same as `OTEL_ENABLED` | Attach an OpenTelemetry logging bridge to the three loggers. Console export follows `LOG_OUTPUT` containing `stream`; files still use stdlib handlers |
| `OTEL_SERVICE_NAME` | project name | Resource `service.name` for traces/logs |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` | Collector endpoint |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc` | `grpc`, or `http` / `http/protobuf` for the HTTP exporter |

If OTel packages are missing, the app logs a warning and continues. See [OpenTelemetry](opentelemetry.md).

---

## Static files

| Variable | Default | What it does |
|----------|---------|--------------|
| `STATIC_CACHE_MAX_AGE` | `604800` | `Cache-Control: public, max-age=…` for `{BASE_PATH}/assets/statics/…` (seconds). `0` → `no-cache` |

Swagger UI assets under `{BASE_PATH}/assets/swagger-ui/` are served as normal static files; this TTL applies to **`statics/`** only.

---

## Minimal `.env` examples

Local development:

```env
API_TITLE=myapi
ENV=development
DEBUG=true
HOST=127.0.0.1
PORT=5000
TIMEZONE=UTC
LOG_OUTPUT=stream,file
SECRET_KEY=change-me
```

Behind a reverse proxy under `/api`:

```env
BASE_PATH=/api
DOCS_PATH=/docs
HOST=0.0.0.0
PORT=8080
```

Production-oriented (container still sets `ENV=production` for bjoern):

```env
ENV=production
DEBUG=false
LOG_OUTPUT=stream
OTEL_ENABLED=true
OTEL_SERVICE_NAME=myapi
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
SECRET_KEY=use-a-long-random-value
```

Add your own keys (for example `DATABASE_URL`, `JWT_SECRET_KEY`) when you follow [Customizing the app](extending.md); declare them in `config.py` the same way as the built-ins.
