# Quick start

This page walks through one full journey: install flaskit → create a project → configure `.env` → add a module → run the API → open Swagger.

## 1. Install flaskit

```bash
pip install flaskit-cli
flaskit --version
```

The PyPI name is `flaskit-cli`. The command and import stay `flaskit`.

## 2. Create a project

```bash
flaskit init myapi
cd myapi
```

`init` writes the application files and a **`.env`** next to `app.py`. Layout:

```text
myapi/
|- app.py
|- config.py
|- requirements.txt
|- Dockerfile
|- .dockerignore
|- .python-version
|- .env
|- templates/
|  > swagger_ui.html
|- resources/
|- assets/
|  |- swagger-ui/
|  > statics/
> …
```

## 3. Create a virtual environment and install app deps

Generated apps need **Python 3.11+**.

```bash
python -m venv .venv
```

Activate `.venv` for your shell, then:

```bash
pip install -U pip
pip install -r requirements.txt
```

## 4. Configure `.env`

`config.py` loads `.env` automatically (`python-dotenv`). Edit values before the first run:

```env
API_TITLE=myapi
API_DESCRIPTION=myapi API
ENV=development
DEBUG=true
HOST=127.0.0.1
PORT=5000
BASE_PATH=/
DOCS_PATH=/docs
TIMEZONE=UTC
LOG_OUTPUT=stream,file
SECRET_KEY=change-me
```

Useful tweaks:

```env
BASE_PATH=/api
PORT=8080
TIMEZONE=Asia/Tehran
```

With `BASE_PATH=/api`, routes and docs move under `/api` (for example `/api/docs`, `/api/users/`).

Full variable list: [Configuration](configuration.md).

## 5. Generate an API module

```bash
flaskit generate module users
```

Creates:

```text
resources/
> users/
   |- blueprint.py    # flask_bp (Flask) + URL_PREFIX=/users
   |- resource.py     # smorest_blp (Smorest) CRUD stubs
   > schema.py        # Request / Response schemas
```

Restart is not required yet if the app is not running; discovery runs on startup.

## 6. Run the app

```bash
python app.py
```

Default mode is `ENV=development` (Flask). You should see the process bind to `HOST:PORT` from `.env`.

## 7. Open Swagger and try a call

Open:

- Docs: http://127.0.0.1:5000/docs  
  (or http://127.0.0.1:8080/api/docs if you set `PORT=8080` and `BASE_PATH=/api`)

In the UI:

1. Select **users** (or **All modules**)
2. Try `GET /users/` — stub returns `[]`
3. Try `POST /users/` — stub returns `{}` with status 201

Example with curl (defaults):

```bash
curl -s http://127.0.0.1:5000/users/
curl -s -X POST http://127.0.0.1:5000/users/ \
  -H "Content-Type: application/json" \
  -d "{}"
```

OpenAPI JSON: http://127.0.0.1:5000/docs/openapi.json

## 8. What to do next

| Goal | Where |
|------|--------|
| Change env settings | Edit `.env` → [Configuration](configuration.md) |
| Add fields / real handlers | Edit `resources/users/schema.py` and `resource.py` → [Modules](modules.md) |
| PostgreSQL, JWT, Redis | [Customizing the app](extending.md) |
| Production image | [Docker](docker.md) |
| Custom application logs | [Logging](logging.md) |

You now have a running Flask-Smorest API with local Swagger, logging, and one generated module.
