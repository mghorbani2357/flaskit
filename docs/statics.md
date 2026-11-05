# Static files (`assets/statics`)

Put public files (images, CSS, JS, fonts, downloads) in:

```text
assets/statics/
```

They are served by Flask’s static folder at:

```text
/assets/statics/<filename>
```

Example: `assets/statics/logo.png` → `http://127.0.0.1:5000/assets/statics/logo.png`

## Browser caching

Responses under `/assets/statics/` get:

```http
Cache-Control: public, max-age=604800
```

Default TTL is **7 days** (`604800` seconds). Override with:

```bash
STATIC_CACHE_MAX_AGE=31536000   # 1 year
```

Set `STATIC_CACHE_MAX_AGE=0` to send `Cache-Control: no-cache`.

Flask still emits `ETag` / `Last-Modified` for conditional requests (`304`).

## Notes

- `swagger-ui/` stays separate under `assets/swagger-ui/` (docs UI assets).
- `flaskit init` creates an empty `assets/statics/` directory for you.
