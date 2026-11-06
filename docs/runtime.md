# Runtime

## Development (Flask)

Default when `ENV=development` (or unset):

```bash
python app.py
python app.py --host 0.0.0.0 -p 8082
python app.py -h
```

CLI flags override env for the process:

| Flag | Env |
|------|-----|
| `-e` / `--env` | `ENV` |
| `--host` | `HOST` |
| `-p` / `--port` | `PORT` |
| `--debug` / `--no-debug` | `DEBUG` |

## Production (bjoern)

When `ENV=production` or `prod`, `app.py` runs **bjoern**. bjoern requires **libev** and is installed **only in the Docker image**, not via `requirements.txt`.

Locally:

```bash
# This will exit with a clear error unless bjoern is installed
ENV=production python app.py
```

Use Docker for production-like serving — see [Docker](docker.md).

## Cross-platform notes

| Topic | Guidance |
|-------|----------|
| Paths | Templates use `pathlib.Path`; works on Windows and POSIX |
| Timezone | `zoneinfo` + `tzdata` dependency for IANA zones on Windows |
| Ports | Prefer `PORT=8082` if 5000 is reserved |
| Console encoding | Help text is ASCII-safe; set `PYTHONUTF8=1` if needed |
| Shell env | Use `set` / `$env:` / `export` as appropriate — the app only reads `os.environ` |

## Flask CLI

```bash
flask --app app:create_app run
flask --app app:create_app list-modules
```
