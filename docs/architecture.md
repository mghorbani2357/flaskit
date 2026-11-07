# Architecture

flaskit is a **generator**. The CLI writes a self-contained Flask project that does not depend on the `flaskit` package at runtime.

## `create_app` vs `init_app`

| Function | Role |
|----------|------|
| **`create_app()`** | Application **factory**. Builds `Flask` (with `static_url_path` under `BASE_PATH`), logging, OpenTelemetry, Flask-Smorest `Api`, security schemes, then calls `init_app`. |
| **`init_app(app)`** | **Registration**. Discovers modules, mounts Flask blueprints, registers Smorest views in the OpenAPI spec, mounts docs. Idempotent (`flaskit_ready`). |

```text
create_app()
  -> Flask(static_url_path=assets under BASE_PATH, template_folder=templates)
  -> setup_logging / request logging / static caching / otel
  -> Api(app) + security
  -> init_app(app)
       -> discover_modules()  # flask_bp + smorest_blp
       -> register blueprints + /docs
  -> return app
```

Hook databases, caches, and auth in `create_app` — see [Customizing the app](extending.md).

## Blueprint nesting

Each module exposes:

1. **`flask_bp`** — Flask blueprint + `URL_PREFIX` (`blueprint.py`)
2. **`smorest_blp`** — Smorest blueprint with `MethodView`s (`resource.py`)

`resource.py` registers the Smorest blueprint **on** the Flask blueprint. The app registers `flask_bp` at `{BASE_PATH}{URL_PREFIX}`.

Legacy names `bp` / `blp` are still accepted by discovery for older scaffolds.

## Auto-discovery

`discover_modules()` scans `resources/*/`:

- Directory name → module id / Swagger tag
- Requires `blueprint.py` and `resource.py`
- Skips names starting with `.` or `_`
- No `__init__.py` required

## Entry points

| How you start | What runs |
|---------------|-----------|
| `python app.py` (`ENV=development`) | Flask / Werkzeug |
| `python app.py` (`ENV=production`) | bjoern (Docker/Linux) |
| `flask --app app:create_app run` | Flask CLI |
| Docker `ENTRYPOINT` | `python3 app.py` with `ENV=production` |
