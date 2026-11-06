# Static files

## Layout

```text
assets/
  swagger-ui/    # Swagger UI (do not put app files here)
  statics/       # your public files
```

Place images, CSS, JS, downloads under `assets/statics/`.

## URLs

Served at `{BASE_PATH}/assets/statics/...`.

| `BASE_PATH` | Example file | URL |
|-------------|--------------|-----|
| `/` | `logo.png` | `/assets/statics/logo.png` |
| `/api` | `logo.png` | `/api/assets/statics/logo.png` |

Flask `static_folder` is `assets` and `static_url_path` is `config.assets_url_path()` so **all** assets (Swagger UI and statics) respect `BASE_PATH`.

## Cache-Control

Responses under `{BASE_PATH}/assets/statics` receive:

```http
Cache-Control: public, max-age=<STATIC_CACHE_MAX_AGE>
```

Default TTL is `604800` (7 days). Set `STATIC_CACHE_MAX_AGE=0` for `no-cache`.

## Documentation for assets

Do not put README files under `assets/`. Project manuals live in the flaskit `docs/` tree (or your own project docs). The scaffold creates empty `statics/` without placeholder text files.
