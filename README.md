# flaskit

CLI scaffolding for **Flask + Flask-Smorest** APIs: modular resources, auto-discovery, multi-definition Swagger UI, logging, and optional OpenTelemetry.

**Documentation:** edit Markdown under [`docs/`](docs/), preview with `mkdocs serve`, or publish on [Read the Docs](https://flaskit.readthedocs.io/) (see [`.readthedocs.yaml`](.readthedocs.yaml)).

```bash
pip install -e ".[docs]"
mkdocs serve
```

## Install

```bash
pip install -e .
```

Python 3.10+. If needed, use `python -m flaskit`.

## Quick start

```bash
python -m flaskit init myapi
cd myapi
python -m venv .venv
# Windows PowerShell (if scripts are blocked):
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#   .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m flaskit generate module users
python app.py
```

Open [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs). Swagger title defaults to the init name (`myapi`).

## CLI

| Command | Description |
|---------|-------------|
| `flaskit init [path]` | Scaffold project (`app.py`, flat `config.py`, empty `resources/` + `assets/`) |
| `flaskit generate module <name>` | Create `resources/<name>/{blueprint,resource,schema}.py` |

## Layout

```
app.py              # create_app, init_app
config.py           # flat UPPER_CASE settings from env (includes BASE_PATH)
resources/
  users/
    blueprint.py    # Flask Blueprint + URL_PREFIX
    resource.py     # Smorest CRUD stubs
    schema.py       # empty Request / Response schemas
assets/
  swagger-ui/       # local Swagger UI (no CDN)
  statics/          # public static files (/assets/statics/..., Cache-Control)
```

Modules under `resources/` are discovered automatically — no manual register list. Put images/CSS/JS in `assets/statics/`; browsers cache them via `STATIC_CACHE_MAX_AGE` (default 7 days).

Final module routes are `{BASE_PATH}{URL_PREFIX}/...` — app base from config/env, blueprint path from each `blueprint.py`.

## Config

`config.py` is **flat** (no class). Names match env vars in `UPPER_CASE`:

| Variable | Default |
|----------|---------|
| `API_TITLE` | init project name (Swagger title) |
| `API_DESCRIPTION` | `{name} API` (Swagger description) |
| `BASE_PATH` | `/` (route base when path-like; http(s) URL for Swagger Servers only) |
| `ENV` | `development` (Flask) or `production` (bjoern) |
| `HOST` / `PORT` | `127.0.0.1` / `5000` |
| `BJOERN_REUSE_PORT` | `true` (Linux SO_REUSEPORT) |
| `DOCS_PATH` | `/docs` |
| `AUTH_SCHEME` | `bearer` |
| `LOG_LEVEL` | `INFO` (set `DEBUG` to include request/response bodies) |
| `LOG_OUTPUT` | `stream,file` |
| `LOG_APP_FILE` / `LOG_REQUEST_FILE` / `LOG_RESPONSE_FILE` | separate log files |
| `LOG_REDACT_HEADERS` | secrets stripped from request/response logs |
| `LOG_ROTATION` | `size`, `time`, or `none` |
| `OTEL_ENABLED` | `false` |

Three loggers: `flask.app`, `werkzeug.request`, `werkzeug.response`. Bodies are base64-logged only when level is below INFO (`DEBUG`). Swagger UI assets are served from `assets/swagger-ui/` (no CDN).

Example:

```bash
set HOST=0.0.0.0
set PORT=8080
set API_TITLE=My API
python app.py
```

`python app.py` uses the Flask dev server when `ENV=development` (default). **bjoern** is installed only in Docker (not in `requirements.txt`); the image runs with `ENV=production`.

## Docker

Projects are scaffolded with a multi-stage `Dockerfile` (builder + slim runtime, libev, non-root; installs bjoern in-image only):

```bash
docker build --build-arg DOCKER_TAG=1.2.3 -t myapi .
docker run --rm -p 8080:80 myapi
```

`DOCKER_TAG` is mapped to `API_VERSION` inside the image.

## Swagger

`/docs` header dropdown:

- **All modules**
- one entry per resource module

Authorize uses Bearer by default; `persistAuthorization` keeps the token when switching modules.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
