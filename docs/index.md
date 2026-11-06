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

## Not included (by design)

- No ORM or database layer — add your own in `create_app` (see [Extending](extending.md))
- No CDN for Swagger — assets ship with the project
- No `.gitkeep` placeholders — empty directories are created as directories

## Preview these docs

```bash
pip install -e ".[docs]"
mkdocs serve
```

Open http://127.0.0.1:8000.

## License

GPL-3.0-or-later — see the repository `LICENSE` file.
