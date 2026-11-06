# Swagger UI

## Local assets (no CDN)

The UI page is Jinja: `templates/swagger_ui.html`. CSS/JS live under `assets/swagger-ui/` and are served as Flask static files at `{BASE_PATH}/assets/swagger-ui/...`.

Docs URL: `{BASE_PATH}{DOCS_PATH}` (default `/docs`).

## Multi-definition header

The top dropdown includes:

- **All modules** → `{docs}/openapi.json`
- One entry per resource → `{docs}/modules/<name>/openapi.json`

`persistAuthorization` keeps the Bearer (or API key) token when switching definitions.

## Servers dropdown

Shown only when `BASE_PATH` is set to something other than empty or `/`. Otherwise OpenAPI omits `servers` and the UI hides the Servers control.

```bash
export BASE_PATH=/api
python app.py
# UI at http://127.0.0.1:5000/api/docs
```

## Authorize

Default security is HTTP Bearer (`AUTH_*` env vars). Change scheme to `apiKey` for header API keys.

## Customizing the HTML

Edit `templates/swagger_ui.html` in the generated project. Template variables:

| Variable | Meaning |
|----------|---------|
| `title` | Page / API title |
| `css_url`, `bundle_url`, `preset_url` | Asset URLs under `BASE_PATH` |
| `urls` | Swagger UI `urls` array |
| `show_servers` | Whether to show the Servers control |
