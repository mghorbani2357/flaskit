# Docker

Every `flaskit init` project includes a multi-stage `Dockerfile` and `.dockerignore`.

## Design

1. **Builder** (`python:3.13.1-bookworm`): install `build-essential` + `libev-dev`, pip-install `requirements.txt` **and** `bjoern` (bjoern is Docker-only)
2. **Runtime** (`python:3.13.1-slim-bookworm`): copy site-packages, install `libev4`, non-root `app` user, `ENV=production`

Tunings included:

- `PIP_NO_CACHE_DIR`, `PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED`
- No redundant pip upgrade in the final image
- Stream-only logging for containers
- `ENTRYPOINT ["python3", "app.py"]` → bjoern via `ENV=production`

## Build and run

```bash
docker build --build-arg DOCKER_TAG=1.2.3 -t myapi .
docker run --rm -p 8080:80 myapi
```

`DOCKER_TAG` is copied into `API_VERSION` inside the image.

## Useful overrides

```bash
docker run --rm -p 8080:80 \
  -e API_TITLE="My API" \
  -e BASE_PATH=/api \
  -e LOG_LEVEL=DEBUG \
  myapi
```
