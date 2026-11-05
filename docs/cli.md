# CLI reference

Global help (includes examples):

```bash
flaskit -h
flaskit --help
python -m flaskit -h
```

## `flaskit init [path]`

Scaffold a new project in `path` (default: current directory). The project name is the folder name and seeds `API_TITLE` / `API_DESCRIPTION`.

Creates:

| Path | Purpose |
|------|---------|
| `app.py` | Application factory and server entry |
| `config.py` | Flat env-backed settings |
| `requirements.txt` | Flask, Smorest, OTel extras (bjoern only in Docker) |
| `.env.example` | Documented env vars |
| `Dockerfile` / `.dockerignore` | Production image |
| `resources/` | Module root (auto-discovered) |
| `assets/swagger-ui/` | Local Swagger UI assets |

Refuses to overwrite existing scaffold files.

```bash
flaskit init -h
flaskit init myapi
```

## `flaskit generate module <name>`

Create `resources/<name>/{blueprint,resource,schema}.py`.

- Name must be snake_case starting with a letter (`users`, `order_items`)
- `--path` points at the project root (default `.`)

```bash
flaskit generate module users
flaskit generate module order_items --path ./myapi
flaskit generate module -h
```

Restart the app after generating so discovery and Swagger pick up the module.
