# Customizing the app

flaskit generates a **blank Flask-Smorest shell**. Persistence, JWT, caches, and other capabilities are added by you inside `create_app`. This page shows the recommended pattern and complete recipes for PostgreSQL, database initialization, and JWT.

## Where to plug in

| Hook | Use for |
|------|---------|
| **`create_app()`** | Extensions: DB, JWT, Redis, mail, … |
| **`init_app(app)`** | Module discovery (leave alone unless you know why) |
| **`resources/<name>/`** | Business handlers, schemas, per-module auth |

Keep helpers in their own modules (`db.py`, `auth.py`, …) and **import them at the top** of `app.py`.

```python
# app.py (top)
from db import init_database
from auth import init_jwt

def create_app():
    app = Flask(
        __name__,
        static_folder="assets",
        static_url_path=config.assets_url_path(),
        template_folder="templates",
    )
    app.config.update(
        SECRET_KEY=config.SECRET_KEY,
        # … existing OPENAPI_* settings …
    )

    setup_logging(app)
    setup_request_logging(app)
    setup_static_caching(app)
    setup_otel(app)

    init_database(app)   # your code
    init_jwt(app)        # your code

    api = Api(app)
    apply_security(api)  # documents Bearer in Swagger
    app.extensions["flaskit_api"] = api
    init_app(app)
    return app
```

Add matching keys to **`.env`** and **`config.py`** so settings stay flat and env-driven.

```env
# .env
DATABASE_URL=postgresql+psycopg://app:secret@localhost:5432/app
JWT_SECRET_KEY=change-me-too
JWT_ACCESS_TOKEN_EXPIRES=3600
```

```python
# config.py
DATABASE_URL = _env("DATABASE_URL", "sqlite:///app.db")
JWT_SECRET_KEY = _env("JWT_SECRET_KEY", SECRET_KEY)
JWT_ACCESS_TOKEN_EXPIRES = int(_env("JWT_ACCESS_TOKEN_EXPIRES", "3600") or "3600")
```

---

## PostgreSQL with SQLAlchemy

### 1. Dependencies

Add to `requirements.txt`:

```text
Flask-SQLAlchemy>=3.1
Flask-Migrate>=4.0
psycopg[binary]>=3.1
```

### 2. `db.py`

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import config

db = SQLAlchemy()
migrate = Migrate()


def init_database(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)
```

Call `init_database(app)` from `create_app` as shown above.

### 3. Model (example)

```python
# models/user.py
from db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
```

Use the model from a resource:

```python
# resources/users/resource.py
from models.user import User
from db import db

@smorest_blp.route("/")
class UsersList(MethodView):
    @smorest_blp.response(200, UsersResponse(many=True))
    def get(self):
        return User.query.order_by(User.id).all()
```

Fill `UsersResponse` fields in `schema.py` to match the model.

### 4. Migrations (recommended)

```bash
flask --app app:create_app db init
flask --app app:create_app db migrate -m "create users"
flask --app app:create_app db upgrade
```

Repeat `migrate` / `upgrade` when models change.

### 5. Simple DB init without Migrate

For prototypes only:

```python
def init_database(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        import models.user  # noqa: F401 — register models
        db.create_all()
```

Prefer Flask-Migrate for anything beyond a toy app.

### 6. Docker Compose sketch

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app
    ports:
      - "5432:5432"
  api:
    build: .
    environment:
      DATABASE_URL: postgresql+psycopg://app:secret@db:5432/app
      SECRET_KEY: change-me
      ENV: production
    ports:
      - "8080:80"
    depends_on:
      - db
```

Do **not** copy `.env` into the image (`.dockerignore` already excludes it). Pass secrets at runtime.

---

## JWT authentication

Swagger already documents Bearer auth via `AUTH_*` settings. Wire real verification with **Flask-JWT-Extended** (or raw PyJWT).

### 1. Dependencies

```text
Flask-JWT-Extended>=4.6
```

### 2. `auth.py`

```python
from datetime import timedelta

from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

import config

jwt = JWTManager()


def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        seconds=config.JWT_ACCESS_TOKEN_EXPIRES
    )
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def missing_token(reason):
        return jsonify(message="Missing or invalid token", detail=reason), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify(message="Invalid token", detail=reason), 401
```

### 3. Login route (new module or existing)

```bash
flaskit generate module auth
```

Example `resources/auth/resource.py`:

```python
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint as SmorestBlueprint
from marshmallow import Schema, fields

from resources.auth.blueprint import flask_bp
# from models.user import User
# from werkzeug.security import check_password_hash

smorest_blp = SmorestBlueprint("auth_api", __name__, description="Auth")


class LoginRequest(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class TokenResponse(Schema):
    access_token = fields.String()


@smorest_blp.route("/login")
class Login(MethodView):
    @smorest_blp.arguments(LoginRequest)
    @smorest_blp.response(200, TokenResponse)
    def post(self, body):
        # user = User.query.filter_by(email=body["email"]).first()
        # if not user or not check_password_hash(user.password_hash, body["password"]):
        #     abort(401, message="Bad credentials")
        token = create_access_token(identity=body["email"])
        return {"access_token": token}


flask_bp.register_blueprint(smorest_blp)
```

Set `URL_PREFIX = "/auth"` in `blueprint.py`. With `BASE_PATH=/api`, login is `POST /api/auth/login`.

### 4. Protect a resource

```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@smorest_blp.route("/me")
class Me(MethodView):
    @jwt_required()
    @smorest_blp.response(200, UsersResponse)
    def get(self):
        email = get_jwt_identity()
        return {"email": email}
```

In Swagger UI: **Authorize** → paste `Bearer <access_token>` (or the raw token if the UI prepends `Bearer`).

Align OpenAPI with JWT by keeping:

```env
AUTH_SCHEME=bearer
AUTH_BEARER_FORMAT=JWT
```

---

## Other common extensions

### Redis

```python
# cache.py
import redis
import config

def init_redis(app):
    client = redis.from_url(config.REDIS_URL)
    app.extensions["redis"] = client
```

```env
REDIS_URL=redis://localhost:6379/0
```

### Global before-request guard

```python
from flask import request, abort
from flask_jwt_extended import verify_jwt_in_request

def init_http_guards(app):
    @app.before_request
    def require_auth_for_api():
        path = request.path
        # skip docs, openapi, login, statics
        if path.startswith(config.docs_url_prefix()):
            return
        if path.endswith("/auth/login"):
            return
        if "/assets/" in path:
            return
        verify_jwt_in_request()
```

Register after `init_jwt(app)`.

### Seed data on first boot

```python
def seed_admin():
    if User.query.filter_by(email="admin@example.com").first():
        return
    user = User(email="admin@example.com", password_hash=generate_password_hash("admin"))
    db.session.add(user)
    db.session.commit()

def init_database(app):
    # … db.init_app …
    with app.app_context():
        db.create_all()  # or rely on migrations only
        seed_admin()
```

---

## Testing with the factory

```python
# conftest.py
import pytest
from app import create_app
from db import db


@pytest.fixture
def app():
    application = create_app()
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
```

---

## Checklist

1. Add packages to `requirements.txt`
2. Add settings to `.env` and `config.py`
3. Create `init_*` module; import at top of `app.py`
4. Call `init_*` from `create_app` after logging, before or after `Api(app)` as needed
5. Use models / JWT helpers inside `resources/*/resource.py`
6. Pass secrets via env in Docker; never bake `.env` into the image

See also: [Configuration](configuration.md), [Modules](modules.md), [Docker](docker.md).
