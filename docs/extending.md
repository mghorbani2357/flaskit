# Extending `create_app`

Generated projects intentionally omit databases and other infrastructure. Wire them in the application factory.

## Pattern

Open `app.py` and add setup **after** logging / OTel and **before** `Api(app)` (or immediately after, depending on whether the extension needs the Flask app only):

```python
def create_app():
    app = Flask(
        __name__,
        static_folder="assets",
        static_url_path=config.assets_url_path(),
        template_folder="templates",
    )
    # ... app.config.update(...)

    setup_logging(app)
    setup_request_logging(app)
    setup_static_caching(app)
    setup_otel(app)

    # --- your extensions ---
    init_database(app)
    # init_redis(app)
    # init_migrate(app)
    # -----------------------

    api = Api(app)
    apply_security(api)
    app.extensions["flaskit_api"] = api
    init_app(app)
    return app
```

Keep module discovery in `init_app`. Prefer small `init_*` helpers in separate modules (`db.py`, `cache.py`) imported at the **top** of `app.py`.

## Example: SQLAlchemy + Flask-Migrate

1. Add dependencies to `requirements.txt`:

```text
Flask-SQLAlchemy>=3.1
Flask-Migrate>=4.0
psycopg[binary]>=3.1
```

2. Create `db.py`:

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_database(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get(
        "SQLALCHEMY_DATABASE_URI"
    ) or __import__("os").environ.get(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    db.init_app(app)
    migrate.init_app(app, db)
```

3. Expose `DATABASE_URL` in `config.py` / `.env.example` if you prefer flat constants:

```python
DATABASE_URL = _env("DATABASE_URL", "sqlite:///app.db")
```

Then in `init_database`:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
```

4. Use models from resources:

```python
from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
```

5. Migrate:

```bash
flask --app app:create_app db init
flask --app app:create_app db migrate -m "users"
flask --app app:create_app db upgrade
```

## Example: Redis

```python
# cache.py
import redis
from flask import current_app

_client = None


def init_redis(app):
    global _client
    url = app.config.get("REDIS_URL") or __import__("os").environ.get(
        "REDIS_URL", "redis://localhost:6379/0"
    )
    _client = redis.from_url(url)
    app.extensions["redis"] = _client


def get_redis():
    return current_app.extensions["redis"]
```

## Example: custom auth before handlers

Implement checks in Smorest `@smorest_blp.before_request` or Flask `@flask_bp.before_request`, or a global `@app.before_request` in `create_app`. Keep secrets in env vars (`SECRET_KEY`, JWT keys, …).

## Testing with the factory

```python
def test_health(client):
    # pytest fixture that calls create_app()
    ...
```

```python
# conftest.py
import pytest
from app import create_app

@pytest.fixture
def app():
    application = create_app()
    application.config.update(TESTING=True)
    yield application

@pytest.fixture
def client(app):
    return app.test_client()
```

## Docker and secrets

Pass connection strings as environment variables at runtime — do not bake credentials into the image:

```bash
docker run --rm -p 8080:80 \
  -e DATABASE_URL=postgresql+psycopg://user:pass@db/app \
  -e SECRET_KEY=... \
  myapi
```
