# CLI reference

```bash
flaskit -h
flaskit --help
python -m flaskit -h
flaskit --version
```

## `flaskit init [path]`

Scaffold a project in `path` (default: `.`). The **folder name** seeds `API_TITLE` / `API_DESCRIPTION`.

Creates (among others):

| Path | Purpose |
|------|---------|
| `app.py` | Factory, logging, discovery, Flask/bjoern entry |
| `config.py` | Flat env-backed settings |
| `requirements.txt` | App dependencies (no bjoern) |
| `.env.example` | Documented environment variables |
| `.python-version` | `3.12` |
| `Dockerfile` / `.dockerignore` | Production image |
| `templates/swagger_ui.html` | Swagger UI page |
| `resources/` | Empty module root |
| `assets/swagger-ui/` | Local Swagger UI assets |
| `assets/statics/` | Empty public static directory |

Empty directories are created **without** `.gitkeep` files. Refuses to overwrite existing scaffold files.

```bash
flaskit init
flaskit init myapi
flaskit init ./services/payments
flaskit init -h
```

## `flaskit generate module <name>`

Create `resources/<name>/{blueprint,resource,schema}.py`.

| Symbol | File | Kind |
|--------|------|------|
| `flask_bp` | `blueprint.py` | Flask `Blueprint` |
| `smorest_blp` | `resource.py` | Flask-Smorest `Blueprint` |

- Name must be snake_case starting with a letter (`users`, `order_items`)
- `--path` selects the project root (default `.`)

```bash
flaskit generate module users
flaskit generate module order_items --path ./myapi
flaskit generate module -h
```

Restart the app after generating so discovery and Swagger pick up the module.
