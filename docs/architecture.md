# Architecture

flaskit is a **generator**. The CLI writes a self-contained Flask project; that project does not depend on the `flaskit` package at runtime.

## `create_app` vs `init_app`

| Function | Role |
|----------|------|
| **`create_app()`** | Application **factory**. Builds `Flask()`, loads config, logging, OpenTelemetry, Flask-Smorest `Api`, security schemes, then calls `init_app`. Used by `flask --app app:create_app`, tests, Docker/`python app.py`, and bjoern. |
| **`init_app(app)`** | **Registration** step. Discovers modules under `resources/`, mounts blueprints, registers OpenAPI tags/views, sets up `/docs`. Idempotent (`flaskit_ready` guard). |

Typical flow:

```text
create_app()
  -> setup_logging / request logging / otel
  -> Api(app) + security
  -> init_app(app)
       -> discover_modules()
       -> register blueprints + docs
  -> return app
```

Customize cross-cutting concerns in `create_app`. Keep module wiring in `init_app` (or regenerate modules with the CLI).

## Blueprint nesting

Each module has:

1. A **Flask** `Blueprint` (`blueprint.py`) with `URL_PREFIX`
2. A **Smorest** `Blueprint` (`resource.py`) with CRUD `MethodView`s

The Smorest blueprint is registered **on** the Flask blueprint (`bp.register_blueprint(blp)`). The app registers the Flask blueprint at `{BASE_PATH}{URL_PREFIX}`.

## Auto-discovery

`discover_modules()` scans `resources/*/`:

- Directory name is the module id / Swagger tag
- Requires `blueprint.py` and `resource.py`
- Skips names starting with `.` or `_`
- No `__init__.py` required

## Entry points

| How you start | What runs |
|---------------|-----------|
| `python app.py` (`ENV=development`) | Werkzeug / Flask dev server |
| `python app.py` (`ENV=production`) | bjoern |
| `flask --app app:create_app run` | Flask CLI (dev) |
| Docker `ENTRYPOINT` | `python3 app.py` with `ENV=production` |
