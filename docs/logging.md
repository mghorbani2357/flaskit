# Logging

Generated apps configure **three** named loggers:

| Purpose | Default name | Default file |
|---------|--------------|--------------|
| App | `flask.app` | `logs/app.log` |
| Request | `werkzeug.request` | `logs/request.log` |
| Response | `werkzeug.response` | `logs/response.log` |

Override with `LOG_*_NAME` / `LOG_*_FILE`.

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

## Shared knobs

| Variable | Default |
|----------|---------|
| `LOG_LEVEL` | `INFO` |
| `LOG_STREAM` | `stderr` |
| `LOG_FORMAT` | `%(message)s` |
| `LOG_DATE_FORMAT` | `%Y-%m-%d %H:%M:%S` |
| `LOG_PROPAGATE` | `false` |

### Example

```bash
export LOG_LEVEL=DEBUG
export LOG_OUTPUT=stream,file
export LOG_STREAM=stderr
export TIMEZONE=UTC
python app.py
```
