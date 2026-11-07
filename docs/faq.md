# FAQ

## `No matching distribution found for marshmallow...`

The venv is likely **Python 3.14**. Use **3.12**:

```bash
# macOS (Homebrew)
brew install python@3.12
cd your-project
rm -rf .venv
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Generated projects include `.python-version` = `3.12`. Supported app range: **3.11–3.13**.

## `TemplateNotFound` for env templates

Old installs looked for a leading-dot Jinja name. Current packages ship `templates/project/env.j2` and write project **`.env`**.

```bash
pip uninstall flaskit-cli flask-it flaskit -y
pip install -U flaskit-cli
flaskit --version
flaskit init tpm
```

## Is flaskit a Flask extension?

No. It is a **CLI scaffold**. Generated projects run without importing `flaskit`.

## Why is there no database or JWT layer?

By design. Add PostgreSQL, migrations, JWT, and other extensions in `create_app` — see [Customizing the app](extending.md).

## Why don’t I see a Servers dropdown?

With default `BASE_PATH=/` the OpenAPI `servers` list is omitted. Set `BASE_PATH=/api` (or similar).

## Why don’t request bodies appear in logs?

Bodies are logged (base64) only when `LOG_LEVEL=DEBUG`.

## Where did `page_number` go?

Removed. Logs use `request_id`, `log_id`, timezone fields, and optional `trace_id` / `span_id`.

## Console empty but log files have lines?

Keep `stream` in `LOG_OUTPUT` and `LOG_STREAM=stderr`. Handlers flush after every record. Restart after config changes.

## Does `BASE_PATH` affect static files?

Yes — API routes, docs, and `/assets/...` all sit under `BASE_PATH`.

## bjoern / production server

Installed **only in Docker**. Locally use `ENV=development`. For production-like serving, build and run the image.

## `ZoneInfoNotFoundError` on Windows

Install project deps (`tzdata` is in `requirements.txt`) or set `TIMEZONE=UTC`.

## `python app.py -h` Unicode error on Windows

Help text uses ASCII (`->`). If you customize descriptions, avoid characters your console code page cannot encode, or set `PYTHONUTF8=1`.

## How do I publish docs on Read the Docs?

1. Push the repo (`docs/`, `mkdocs.yml`, `.readthedocs.yaml`)
2. Import on [readthedocs.io](https://readthedocs.io/)
3. RTD builds with MkDocs via `.readthedocs.yaml`

```bash
pip install -e ".[docs]"
mkdocs serve
```
