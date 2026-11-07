# flaskit

**flaskit** scaffolds **Flask + Flask-Smorest** APIs. It is a CLI generator: the created project does not import `flaskit` at runtime.

```bash
pip install flaskit-cli
flaskit init myapi
```

Then follow the [Quick start](quickstart.md) from virtualenv through Swagger.

## Highlights

- Modular `resources/` with auto-discovery (`flask_bp` + `smorest_blp`)
- Flat `.env` / `UPPER_CASE` config (`BASE_PATH` applies to routes, docs, and assets)
- Local Swagger UI (no CDN), multi-definition OpenAPI
- JSON logging (stream and/or file) and optional OpenTelemetry
- Docker image with bjoern for production

## Customize

Add PostgreSQL, JWT, Redis, and other capabilities in `create_app` — see [Customizing the app](extending.md).

## Publish

Package releases and PyPI: [Publish](publishing.md).

## License

GPL-3.0-or-later — see the repository `LICENSE` file.
