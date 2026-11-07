# Logging

Generated apps configure **three** named loggers:

| Purpose | Default name | Default file |
|---------|--------------|--------------|
| App | `flask.app` | `logs/app.log` |
| Request | `werkzeug.request` | `logs/request.log` |
| Response | `werkzeug.response` | `logs/response.log` |

Override with `LOG_*_NAME` / `LOG_*_FILE`.

## Log your own data

### Use the app logger (simplest)

Anywhere you have the Flask app (factory, extensions, resources via `current_app`):

```python
from flask import current_app

current_app.logger.info("order created id=%s", order_id)
current_app.logger.warning("payment retry user=%s", user_id)
current_app.logger.exception("failed to sync inventory")  # includes traceback
```

Inside `create_app` / `init_*` helpers you already have `app`:

```python
def init_database(app):
    app.logger.info("database uri configured")
```

These lines go to the **app** logger sinks (`LOG_APP_FILE` / stream) with the same level and format as the rest of the app logger.

### Structured JSON (recommended for custom events)

Match the request/response style by logging a JSON object:

```python
import json
import time
import uuid
from flask import current_app, g, request

def log_business_event(event, **fields):
    payload = {
        "timestamp": time.time(),
        "event": event,
        "request_id": getattr(g, "request_id", None),
        "path": request.path if request else None,
        **fields,
    }
    current_app.logger.info(json.dumps(payload, ensure_ascii=False))
```

Call it from a resource:

```python
log_business_event("user.created", user_id=42, email=body["email"])
```

### Create a dedicated logger

Use a separate name/file when you want billing, audit, or jobs isolated from `logs/app.log`.

1. Add settings to `.env` / `config.py`:

```env
LOG_AUDIT_NAME=myapi.audit
LOG_AUDIT_FILE=logs/audit.log
```

```python
# config.py
LOG_AUDIT_NAME = _env("LOG_AUDIT_NAME", "myapi.audit") or "myapi.audit"
LOG_AUDIT_FILE = _env("LOG_AUDIT_FILE", "logs/audit.log") or "logs/audit.log"
```

2. Wire it in `setup_logging` (same helpers the scaffold already uses):

```python
# near the top of app.py, with the other loggers
audit_logger = logging.getLogger(config.LOG_AUDIT_NAME)

def setup_logging(app):
    # … existing app / request / response setup …
    _configure_logger(audit_logger, config.LOG_AUDIT_FILE)

    if config.OTEL_LOGS_ENABLED and LoggingHandler is not None:
        # if you already build otel_handler above, also:
        audit_logger.addHandler(otel_handler)
```

3. Log from anywhere:

```python
from app import audit_logger
import json

audit_logger.info(json.dumps({
    "action": "role.changed",
    "actor": actor_id,
    "target": user_id,
    "role": "admin",
}))
```

`_configure_logger` applies `LOG_LEVEL`, `LOG_OUTPUT`, `LOG_STREAM`, and rotation from your existing env — no extra handler code required.

### Child logger under the app name

If you only need a different logger **name** in the message (same files as the app logger), set `LOG_PROPAGATE=true` or attach handlers yourself. Prefer a dedicated logger + `_configure_logger` when you need a separate file.

## Outputs

`LOG_OUTPUT` is a comma-separated list:

| Value | Behavior |
|-------|----------|
| `stream` | Console (`LOG_STREAM`, default **stderr**), flushed every record |
| `file` | Rotating / timed / plain files under `logs/` |

Default: `stream,file`. Docker images typically use `LOG_OUTPUT=stream`.

When OpenTelemetry logs are enabled (`OTEL_LOGS_ENABLED`), an OTel `LoggingHandler` is attached to the same loggers. Console export follows `stream` in `LOG_OUTPUT`; file output continues through the stdlib file handlers.

## Request / response JSON fields

| Field | Notes |
|-------|-------|
| `timestamp` | Unix time |
| `tz_offset` | Seconds east of UTC for `TIMEZONE` |
| `timezone` | IANA name from `TIMEZONE` |
| `api_version` / `api_title` | From config |
| `request_id` / `log_id` | Correlation ids |
| `trace_id` / `span_id` | Filled when OTel span is active |
| `method`, `path`, `url`, `query_string` | Request |
| `client_ip` | `X-Forwarded-For` or `remote_addr` |
| `headers` | Secrets redacted |
| `body` / `body_size` | Body base64 only at DEBUG |
| `status`, `duration` | Response |

There is **no** `page_number` / `g.page` field.

### Bodies only at DEBUG

`body` is base64-encoded only when the logger level allows DEBUG (`LOG_LEVEL=DEBUG`). At `INFO`, `body` is `""` while `body_size` still reflects raw size.

### Header redaction

`LOG_REDACT_HEADERS` (comma-separated, case-insensitive) defaults to:

`authorization,cookie,set-cookie,x-api-key`

## Rotation

| `LOG_ROTATION` | Behavior |
|----------------|----------|
| `size` (default) | `RotatingFileHandler` (`LOG_MAX_BYTES`, `LOG_BACKUP_COUNT`) |
| `time` | `TimedRotatingFileHandler` (`LOG_WHEN`, `LOG_INTERVAL`) |
| `none` | plain `FileHandler` |

Full variable reference (names, defaults, behavior): [Configuration → Logging](configuration.md#logging).

### Example `.env`

```env
LOG_LEVEL=DEBUG
LOG_OUTPUT=stream,file
LOG_STREAM=stderr
TIMEZONE=UTC
```
