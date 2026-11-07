# flaskit

[![PyPI version](https://img.shields.io/pypi/v/flask-it.svg)](https://pypi.org/project/flask-it/)
[![Python versions](https://img.shields.io/pypi/pyversions/flask-it.svg)](https://pypi.org/project/flask-it/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-Read%20the%20Docs-blue)](https://flaskit.readthedocs.io/)
[![CI publish](https://img.shields.io/badge/publish-on%20git%20tag-success)](https://github.com/mghorbani2357/flaskit/actions)

CLI scaffolding for **Flask + Flask-Smorest** APIs: modular resources, auto-discovery, local Swagger UI, JSON logging (optional OpenTelemetry), `BASE_PATH` for every route and asset, and a production Docker image with **bjoern**.

**Documentation:** [flaskit.readthedocs.io](https://flaskit.readthedocs.io/) · source under [`docs/`](docs/)

```bash
pip install -e ".[docs]"
mkdocs serve
```

## Install

```bash
pip install flask-it
# or from source
pip install -e .
```

PyPI name is **`flask-it`** (`flaskit` is taken); the CLI and import stay **`flaskit`**.

Requires Python **3.10+** for the CLI. Generated apps target **3.11–3.13** (3.12 recommended; see `.python-version`).

## Quick start

```bash
flaskit init myapi
cd myapi
python3.12 -m venv .venv
# Windows PowerShell (if scripts are blocked):
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#   .\.venv\Scripts\Activate.ps1
pip install -U pip && pip install -r requirements.txt
flaskit generate module users
python app.py
```

Open [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs).

## CLI

| Command | Description |
|---------|-------------|
| `flaskit init [path]` | Scaffold project (`app.py`, flat `config.py`, `resources/`, `assets/`, `templates/`) |
| `flaskit generate module <name>` | Create `resources/<name>/` with `flask_bp` + `smorest_blp` stubs |

## Layout

```
app.py                 # create_app, init_app
config.py              # flat UPPER_CASE settings from env
templates/
  swagger_ui.html      # Swagger UI page (Jinja)
resources/
  users/
    blueprint.py       # Flask blueprint (flask_bp) + URL_PREFIX
    resource.py        # Smorest blueprint (smorest_blp) + CRUD
    schema.py          # Request / Response schemas
assets/
  swagger-ui/          # local Swagger UI (no CDN)
  statics/             # public files at {BASE_PATH}/assets/statics/...
```

## Highlights

- **`BASE_PATH`** applies to API routes, `/docs`, and `/assets`
- **Timezone** via `TIMEZONE` (IANA); log fields include `timezone` / `tz_offset`
- **Logging** to stream and/or file; optional OTel with the same sinks when enabled
- **Docker** on Python **3.13**; **bjoern** installed in-image only
- **Versioning** of the flaskit package itself from **git tags** (`setuptools-scm`)

## Publish (maintainers)

Push a tag `v*` to trigger [`.github/workflows/publish.yml`](.github/workflows/publish.yml). Set repository secret **`PYPI_API_TOKEN`** only (Python/PyPI URL are fixed in the workflow).

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
