# flaskit

**flaskit** is a scaffolding CLI for **Flask + Flask-Smorest** APIs. It generates a self-contained project; generated apps do **not** import `flaskit` at runtime.

## What you get

| Capability | Detail |
|------------|--------|
| Modular resources | `flaskit generate module` → `flask_bp` + `smorest_blp` + schemas |
| Auto-discovery | Folders under `resources/` registered on startup |
| Flat configuration | `UPPER_CASE` env vars in `config.py` |
| `BASE_PATH` | Prefixes API routes, docs, and static assets |
| Local Swagger UI | Served from Jinja `templates/swagger_ui.html` + `assets/swagger-ui/` (no CDN) |
| Multi-definition OpenAPI | “All modules” plus one definition per resource |
| JSON logging | App / request / response loggers → stream and/or file |
| Timezone | `TIMEZONE` (IANA) on log payloads |
| OpenTelemetry | Optional traces + log bridge respecting `LOG_OUTPUT` |
| Docker | Python 3.13 multi-stage image; **bjoern** only in Docker |
| Cross-platform | Windows / macOS / Linux; `tzdata` for IANA zones |

## Customize

Generated apps are a shell. Add PostgreSQL, migrations, JWT, Redis, and other capabilities in `create_app` — see **[Customizing the app](extending.md)** for full recipes.

## Not included (by design)

- No ORM or auth layer out of the box (documented hooks instead)
- No CDN for Swagger — assets ship with the project

## Preview these docs

```bash
pip install -e ".[docs]"
mkdocs serve
```

Open http://127.0.0.1:8000.

## License

GPL-3.0-or-later — see the repository `LICENSE` file.
