# flaskit

**flaskit** is a scaffolding CLI for **Flask + Flask-Smorest** APIs. It generates a standalone project; it is **not** a runtime library you import into an existing app.

Generated projects include:

- Modular resources under `resources/` with **automatic discovery**
- Flat `UPPER_CASE` config driven by environment variables
- Local Swagger UI (no CDN) with per-module OpenAPI definitions
- JSON request/response logging to console and/or files
- Optional OpenTelemetry
- Docker image with **Flask** in development and **bjoern** in production

## Feature checklist

| Feature | Status |
|---------|--------|
| `flaskit init` scaffolds a full project | Yes |
| `flaskit generate module` creates blueprint / resource / schema | Yes |
| Smorest + marshmallow only (no ORM / DB layer) | Yes |
| Flat env-based config (`API_TITLE`, `BASE_PATH`, …) | Yes |
| Swagger title/description from config (title defaults to init name) | Yes |
| `BASE_PATH` combines with each module `URL_PREFIX` | Yes |
| Servers dropdown only when `BASE_PATH` is set (not empty / `/`) | Yes |
| Multi-definition Swagger (“All modules” + one tab per module) | Yes |
| Bearer auth in Swagger by default; `persistAuthorization` | Yes |
| Local `assets/swagger-ui/` (no CDN) | Yes |
| `assets/statics/` with browser `Cache-Control` | Yes |
| Nested Smorest blueprint under Flask blueprint | Yes |
| No `__init__.py` packages required (namespace / flat imports) | Yes |
| Three loggers: app, request, response | Yes |
| Bodies base64-logged only at `LOG_LEVEL=DEBUG` | Yes |
| `client_ip` on request logs | Yes |
| Console streaming (stderr by default, flushed) + optional files | Yes |
| Header redaction (`authorization`, cookies, …) | Yes |
| `create_app` factory + `init_app` registration | Yes |
| `python app.py -h` and `flaskit -h` | Yes |
| Dev = Flask; production = bjoern (installed only in Docker) | Yes |
| Multi-stage Dockerfile; `DOCKER_TAG` → `API_VERSION` | Yes |
| Optional OpenTelemetry (OTLP) | Yes |

## Docs in this folder

These pages are plain Markdown. Edit them in any text editor, preview locally with MkDocs, or publish on [Read the Docs](https://readthedocs.io/).

```bash
pip install -e ".[docs]"
mkdocs serve
```

Then open http://127.0.0.1:8000.

## License

GPL-3.0-or-later. See the repository `LICENSE` file.
