# Swagger UI

## Local assets (no CDN)

`flaskit init` copies Swagger UI into `assets/swagger-ui/`. The app serves them at `/assets/swagger-ui/...`. Offline and air-gapped friendly.

## Multi-definition UI

`/docs` (configurable via `DOCS_PATH`) loads Swagger UI with:

- **All modules** → `{DOCS_PATH}/openapi.json`
- One entry per resource → `{DOCS_PATH}/modules/<name>/openapi.json`

Module specs are filtered by OpenAPI tag so each tab shows only that module’s operations.

## Title and description

From config / env:

- `API_TITLE` — page title (defaults to the init project name)
- `API_DESCRIPTION` — OpenAPI `info.description`
- `API_VERSION` — OpenAPI version string

## Servers dropdown

The OpenAPI `servers` array is **omitted** when `BASE_PATH` is unset, empty, or `/`.

When `BASE_PATH` is a real prefix or URL (for example `/api` or `https://api.example.com`), the server entry is added and the Swagger Servers control is shown. Otherwise CSS + DOM cleanup hide Swagger’s default Servers chrome.

## Authorize

Default security is **HTTP Bearer** (`AUTH_SCHEME=bearer`). Switch to API key header with `AUTH_SCHEME=apiKey`.

`persistAuthorization: true` keeps the token when switching definitions in the top dropdown.
