# Quick start

```bash
flaskit init myapi
cd myapi
python -m venv .venv
```

Activate the venv, then:

```bash
pip install -r requirements.txt
flaskit generate module users
python app.py
```

Open http://127.0.0.1:5000/docs.

!!! note "Windows PowerShell activation"
    If scripts are blocked:

    ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1
    ```

!!! tip "Port 5000 blocked on Windows"
    Some Windows setups forbid binding to port 5000. Override:

    ```powershell
    $env:HOST="127.0.0.1"
    $env:PORT="8082"
    python app.py
    ```

## What was generated

```text
myapi/
  app.py              # create_app, init_app, Flask/bjoern entry
  config.py           # flat UPPER_CASE settings from env
  requirements.txt
  Dockerfile
  .dockerignore
  .env.example
  resources/
    users/
      blueprint.py    # Flask Blueprint + URL_PREFIX
      resource.py     # Smorest CRUD stubs
      schema.py       # empty Request / Response schemas
  assets/
    swagger-ui/       # local CSS/JS (no CDN)
    statics/          # your static files (browser-cached)
```

Swagger title defaults to the init folder name (`myapi`). Change it with `API_TITLE`.
