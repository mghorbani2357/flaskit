# Modules

## Generate

```bash
flaskit generate module users
```

Produces:

```text
resources/users/
  blueprint.py
  resource.py
  schema.py
```

## `blueprint.py`

Flask blueprint plus mount path:

```python
URL_PREFIX = "/users"
bp = Blueprint("users", __name__)
```

Final routes: `{BASE_PATH}{URL_PREFIX}/...`  
Example with `BASE_PATH=/api` → `/api/users/`.

## `schema.py`

Empty marshmallow schemas ready to fill:

```python
class UsersRequest(Schema):
    pass

class UsersResponse(Schema):
    pass
```

No database models — Smorest + marshmallow only.

## `resource.py`

CRUD stubs with Smorest annotations:

| Method | Path | Stub behavior |
|--------|------|----------------|
| `GET` | `/` | `[]` |
| `POST` | `/` | `{}` (201) |
| `GET` | `/<id>` | `{}` |
| `PATCH` | `/<id>` | `{}` |
| `DELETE` | `/<id>` | `204` |

Each operation is tagged for the module name so Swagger can filter per definition.

## Listing modules

Generated apps register a Flask CLI command:

```bash
flask --app app:create_app list-modules
```
