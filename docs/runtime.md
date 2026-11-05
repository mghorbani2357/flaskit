# Runtime

## Development (Flask)

Default:

```bash
python app.py
# or
python app.py --host 0.0.0.0 -p 8082
```

Uses Werkzeug’s development server with optional `DEBUG`.

Help:

```bash
python app.py -h
```

| Flag | Meaning |
|------|---------|
| `-e` / `--env` | Override `ENV` (`development` / `production`) |
| `--host` | Bind host |
| `-p` / `--port` | Bind port |
| `--debug` / `--no-debug` | Flask debug (dev only) |

You can also use Flask’s CLI:

```bash
flask --app app:create_app run --host 0.0.0.0 --port 8082
```

## Production (bjoern, Docker only)

[bjoern](https://github.com/jonashaag/bjoern) is **not** in `requirements.txt`. The Dockerfile installs it (with `libev`) so local `pip install -r requirements.txt` stays clean on Windows/macOS.

```bash
docker build --build-arg DOCKER_TAG=1.0.0 -t myapi .
docker run --rm -p 8080:80 myapi
```

Inside the image, `ENV=production` makes `app.py` start bjoern. `BJOERN_REUSE_PORT=true` enables Linux `SO_REUSEPORT`.

## Environment selection

| `ENV` value | Server |
|-------------|--------|
| `development`, `dev` (default) | Flask |
| `production`, `prod` | bjoern (available in Docker image) |
