# Modules

## Generate

```bash
flaskit generate module users
```

Produces:

```text
resources/users/
  blueprint.py   # Flask blueprint: flask_bp
  resource.py    # Smorest blueprint: smorest_blp
  schema.py
```

## `blueprint.py` (Flask)

```python
URL_PREFIX = "/users"

# Flask application blueprint (URL mounting / registration)
flask_bp = Blueprint("users", __name__)
```

Final routes: `{BASE_PATH}{URL_PREFIX}/...`  
Example with `BASE_PATH=/api` → `/api/users/`.

## `schema.py`

Empty marshmallow schemas:

```python
class UsersRequest(Schema):
    pass

class UsersResponse(Schema):
    pass
```

No database models — add persistence yourself (see [Extending](extending.md)).

## `resource.py` (Smorest)

```python
# Flask-Smorest blueprint (OpenAPI / request-response schemas)
smorest_blp = SmorestBlueprint("users_api", __name__, description="Users")

@smorest_blp.route("/")
class UsersList(MethodView):
    ...

flask_bp.register_blueprint(smorest_blp)
```

| Method | Path | Stub |
|--------|------|------|
| `GET` | `/` | `[]` |
| `POST` | `/` | `{}` (201) |
| `GET` | `/<id>` | `{}` |
| `PATCH` | `/<id>` | `{}` |
| `DELETE` | `/<id>` | `204` |

Operations are tagged with the module name for per-definition Swagger filtering.

## Naming convention

| Variable | Blueprint type |
|----------|----------------|
| `flask_bp` | Flask `Blueprint` |
| `smorest_blp` | Flask-Smorest `Blueprint` |

Use these names so discovery and docs stay consistent.

## Listing modules

```bash
flask --app app:create_app list-modules
```
