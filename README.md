# flaskit

[![License](https://img.shields.io/github/license/mghorbani2357/flaskit)](https://raw.githubusercontent.com/mghorbani2357/flaskit/master/LICENSE)
[![Workflow](https://img.shields.io/github/actions/workflow/status/mghorbani2357/flaskit/publish.yml?branch=master&logo=github)](https://github.com/mghorbani2357/flaskit/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/flaskit-cli)](https://pypi.org/project/flaskit-cli/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/flaskit-cli)](https://pypi.org/project/flaskit-cli/)
[![PyPI - Format](https://img.shields.io/pypi/format/flaskit-cli)](https://pypi.org/project/flaskit-cli/)
[![Python versions](https://img.shields.io/pypi/pyversions/flaskit-cli)](https://pypi.org/project/flaskit-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/flaskit-cli)](https://pypistats.org/packages/flaskit-cli)
[![Downloads](https://static.pepy.tech/personalized-badge/flaskit-cli?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/flaskit-cli)
[![Documentation Status](https://readthedocs.org/projects/flaskit/badge/?version=latest)](https://flaskit.readthedocs.io/en/latest/?badge=latest)
[![GitHub last commit](https://img.shields.io/github/last-commit/mghorbani2357/flaskit)](https://github.com/mghorbani2357/flaskit/commits/master)
[![GitHub Release Date](https://img.shields.io/github/release-date/mghorbani2357/flaskit)](https://github.com/mghorbani2357/flaskit/releases)

CLI scaffolding for **Flask + Flask-Smorest** APIs: modular resources, auto-discovery, local Swagger UI, JSON logging (optional OpenTelemetry), `BASE_PATH` for every route and asset, and a production Docker image with **bjoern**.

**Documentation:** [flaskit.readthedocs.io](https://flaskit.readthedocs.io/) · source under [`docs/`](docs/)

```bash
pip install -e ".[docs]"
mkdocs serve
```

## Install

```bash
pip install flaskit-cli
# or from source
pip install -e .
```

PyPI name is **`flaskit-cli`** (`flaskit` / `flask-it` are taken or blocked); the CLI and import stay **`flaskit`**.

Requires Python **3.10+** for the CLI. Generated apps target **Python 3.11+**.

## Quick start

```bash
pip install flaskit-cli
flaskit init myapi
cd myapi
python -m venv .venv
# activate .venv, then:
pip install -U pip && pip install -r requirements.txt
# edit .env as needed
flaskit generate module users
python app.py
```

Open [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs). Full walkthrough: [Quick start](https://flaskit.readthedocs.io/en/latest/quickstart/).

## CLI

| Command | Description |
|---------|-------------|
| `flaskit init [path]` | Scaffold project (`app.py`, `config.py`, `.env`, `resources/`, `assets/`, `templates/`) |
| `flaskit generate module <name>` | Create `resources/<name>/` with `flask_bp` + `smorest_blp` stubs |

## Layout

```text
|- app.py
|- config.py
|- .env
|- templates/
|  > swagger_ui.html
|- resources/
|  > users/
|     |- blueprint.py
|     |- resource.py
|     > schema.py
> assets/
   |- swagger-ui/
   > statics/
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
