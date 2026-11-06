# FAQ

## `No matching distribution found for marshmallow...`

**Cause:** the venv is almost certainly **Python 3.14**. Marshmallow / flask-smorest are not reliably installable on 3.14 from PyPI (and many mirrors) yet.

**Fix: use Python 3.12**

```bash
brew install python@3.12
cd your-project
rm -rf .venv
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv
source .venv/bin/activate
python -V          # should show 3.12.x
pip install -U pip
pip install -r requirements.txt
```

Generated projects include `.python-version` set to `3.12`. Supported range for app deps: **3.11–3.13**.

## `TemplateNotFound: project/.env.example.j2`

You are on an **old install** (pre-0.1.1). Setuptools omits templates whose names start with `.`; the file is now `project/env.example.j2`.

Upgrade and reinstall (Homebrew / user site included):

```bash
pip uninstall flaskit -y
pip install -U "git+https://github.com/mghorbani2357/flaskit.git@master"
flaskit --version   # expect 0.1.1+
flaskit init tpm
```

If `flaskit` still points at `/opt/homebrew/...`, uninstall that copy too (`pip3 uninstall flaskit` / `brew` unlink) until `which flaskit` matches the upgraded environment.

## Is flaskit a Flask extension?

No. It is a **CLI scaffold**. Generated projects run without importing `flaskit`.

## Why is there no database layer?

By design: Smorest + marshmallow stubs only. Add your own persistence inside the generated resource methods.

## Why don’t I see a Servers dropdown?

With default `BASE_PATH=/` the OpenAPI `servers` list is omitted and the UI control is hidden. Set `BASE_PATH` to something like `/api` to show it.

## Why don’t request bodies appear in logs?

Bodies are logged (base64) only when `LOG_LEVEL=DEBUG`.

## Console is empty but log files have lines?

Prefer `LOG_STREAM=stderr` (default) and keep `stream` in `LOG_OUTPUT`. Handlers flush after every record. Restart the process after config changes.

## bjoern / production server

bjoern is installed **only in Docker**, not via `requirements.txt`. Locally use `ENV=development` (Flask). For production-like serving, build and run the image.

## `python app.py -h` Unicode error on Windows

Help text uses ASCII (`->`). If you customize the description, avoid characters that your console code page cannot encode.

## How do I publish these docs on Read the Docs?

1. Push the repo (includes `docs/`, `mkdocs.yml`, `.readthedocs.yaml`)
2. Import the project on [readthedocs.io](https://readthedocs.io/)
3. RTD builds with MkDocs using `.readthedocs.yaml`

Local preview:

```bash
pip install -e ".[docs]"
mkdocs serve
```
