# Logging

Generated apps configure **three** named loggers:

| Purpose | Default name | Default file |
|---------|--------------|--------------|
| App | `flask.app` | `logs/app.log` |
| Request | `werkzeug.request` | `logs/request.log` |
| Response | `werkzeug.response` | `logs/response.log` |

Names and paths are overridable via `LOG_*_NAME` / `LOG_*_FILE`.

## Outputs

`LOG_OUTPUT` is a comma list:

- `stream` — console (default stream: **stderr**, flushed every record)
- `file` — rotating / timed / plain files under `logs/`

Default: `stream,file`.

Docker images typically set `LOG_OUTPUT=stream` so logs go to the container collector.

## Request / response JSON

Each HTTP exchange emits JSON lines with fields such as:

- `timestamp`, `tz_offset`, `api_version`, `api_title`
- `request_id`, `log_id`, `page_number`
- `method`, `path`, `url`, `query_string`
- **`client_ip`** (from `X-Forwarded-For` or `remote_addr`) — request logger
- `headers` (secrets redacted)
- `body` / `body_size`
- response: `status`, `duration`

### Bodies only at DEBUG

`body` is base64-encoded and included **only** when the logger level allows DEBUG (`LOG_LEVEL=DEBUG`). At `INFO`, `body` is an empty string while `body_size` still reflects the raw size.

### Header redaction

`LOG_REDACT_HEADERS` (comma-separated, case-insensitive) defaults to:

`authorization,cookie,set-cookie,x-api-key`

Matched header values are replaced with `***`.

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
