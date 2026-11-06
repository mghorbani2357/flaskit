# Docker

Scaffolded projects include a multi-stage `Dockerfile` based on **Python 3.13** (current stable baseline with broad wheel support).

## Build and run

```bash
docker build --build-arg DOCKER_TAG=1.2.3 -t myapi .
docker run --rm -p 8080:80 \
  -e TIMEZONE=UTC \
  -e BASE_PATH=/api \
  myapi
```

| Build arg / env | Effect |
|-----------------|--------|
| `DOCKER_TAG` | Mapped to `API_VERSION` in the image |
| Image defaults | `ENV=production`, `HOST=0.0.0.0`, `PORT=80`, `LOG_OUTPUT=stream` |

bjoern is installed in the builder stage (`pip install bjoern`) and copied into the slim runtime with `libev4`. The process runs as a non-root `app` user.

## Why not bjoern in requirements.txt?

bjoern needs native **libev** and is aimed at Linux containers. Local development uses the Flask server; production uses the image.

## Health check tip

Expose a simple route in a module, or probe `/docs` / OpenAPI JSON behind your load balancer. Remember to include `BASE_PATH` in the probe path when set.
