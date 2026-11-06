# Quick start

## 1. Scaffold

```bash
flaskit init myapi
cd myapi
```

## 2. Virtual environment (Python 3.12)

=== "Linux / macOS"

    ```bash
    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    ```

=== "Windows PowerShell"

    ```powershell
    py -3.12 -m venv .venv
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1
    python -m pip install -U pip
    pip install -r requirements.txt
    ```

## 3. Add a module and run

```bash
flaskit generate module users
python app.py
```

Open http://127.0.0.1:5000/docs.

!!! tip "Port 5000 blocked (common on Windows)"
    ```powershell
    $env:HOST="127.0.0.1"
    $env:PORT="8082"
    python app.py
    ```

## Generated layout

```text
myapi/
  app.py
  config.py
  requirements.txt
  Dockerfile
  .dockerignore
  .python-version      # 3.12
  .env.example
  templates/
    swagger_ui.html
  resources/
    users/
      blueprint.py     # flask_bp (Flask)
      resource.py      # smorest_blp (Smorest)
      schema.py
  assets/
    swagger-ui/
    statics/
```

Swagger title defaults to the folder name (`myapi`). Override with `API_TITLE`.

## Next steps

- Mount under a prefix: set `BASE_PATH=/api` — routes, docs, and assets all move under `/api`
- Set timezone: `TIMEZONE=Asia/Tehran`
- Add a database or other extensions: [Extending create_app](extending.md)
- Build for production: [Docker](docker.md)
