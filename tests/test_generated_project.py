"""Smoke-test a generated project without starting a server."""

from __future__ import annotations

import ast
import importlib.util
import os
import sys
from pathlib import Path

from click.testing import CliRunner

from flaskit.cli import main


def _scaffold(runner: CliRunner, project_dir: Path) -> None:
    assert runner.invoke(main, ["init", str(project_dir)]).exit_code == 0
    assert (
        runner.invoke(
            main, ["generate", "module", "users", "--path", str(project_dir)]
        ).exit_code
        == 0
    )


def _clear_generated_modules() -> None:
    for mod in list(sys.modules):
        if mod == "config" or mod == "app" or mod.startswith("resources"):
            del sys.modules[mod]


def test_generated_python_parses(runner: CliRunner, project_dir: Path) -> None:
    _scaffold(runner, project_dir)
    for rel in (
        "app.py",
        "config.py",
        "resources/users/blueprint.py",
        "resources/users/resource.py",
        "resources/users/schema.py",
    ):
        src = (project_dir / rel).read_text(encoding="utf-8")
        ast.parse(src)


def test_create_app_factory_loads(runner: CliRunner, project_dir: Path) -> None:
    """Import create_app from a generated tree if Flask deps are installed."""
    _scaffold(runner, project_dir)

    if importlib.util.find_spec("flask") is None:
        import pytest

        pytest.skip("Flask not installed (pip install -e '.[test]')")

    env = {
        "ENV": "development",
        "HOST": "127.0.0.1",
        "PORT": "8765",
        "LOG_OUTPUT": "stream",
        "OTEL_ENABLED": "false",
        "OTEL_LOGS_ENABLED": "false",
        "TIMEZONE": "UTC",
        "BASE_PATH": "/",
    }
    old = {key: os.environ.get(key) for key in env}
    os.environ.update(env)
    sys.path.insert(0, str(project_dir))
    try:
        _clear_generated_modules()
        import app as generated_app  # type: ignore

        application = generated_app.create_app()
        assert application.name
        client = application.test_client()
        docs = client.get("/docs")
        assert docs.status_code == 200
        assert b"swagger-ui" in docs.data
        assert b"scheme-container" in docs.data
        openapi = client.get("/docs/openapi.json")
        assert openapi.status_code == 200
        payload = openapi.get_json()
        assert "servers" not in payload
        statics_dir = project_dir / "assets" / "statics"
        sample = statics_dir / "hello.txt"
        sample.write_text("hi", encoding="utf-8")
        static_resp = client.get("/assets/statics/hello.txt")
        assert static_resp.status_code == 200
        assert "max-age" in static_resp.headers.get("Cache-Control", "")
        users = client.get("/users/")
        assert users.status_code == 200
    finally:
        sys.path[:] = [p for p in sys.path if p != str(project_dir)]
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        _clear_generated_modules()


def test_base_path_applies_to_routes_docs_and_assets(
    runner: CliRunner, project_dir: Path
) -> None:
    _scaffold(runner, project_dir)

    if importlib.util.find_spec("flask") is None:
        import pytest

        pytest.skip("Flask not installed (pip install -e '.[test]')")

    env = {
        "ENV": "development",
        "LOG_OUTPUT": "stream",
        "OTEL_ENABLED": "false",
        "BASE_PATH": "/api",
        "TIMEZONE": "UTC",
    }
    old = {key: os.environ.get(key) for key in env}
    os.environ.update(env)
    sys.path.insert(0, str(project_dir))
    try:
        _clear_generated_modules()
        import app as generated_app  # type: ignore

        application = generated_app.create_app()
        client = application.test_client()

        assert client.get("/docs").status_code == 404
        docs = client.get("/api/docs")
        assert docs.status_code == 200
        assert b"/api/assets/swagger-ui/" in docs.data

        openapi = client.get("/api/docs/openapi.json")
        assert openapi.status_code == 200
        assert openapi.get_json()["servers"][0]["url"] == "/api"

        (project_dir / "assets" / "statics" / "x.txt").write_text("x", encoding="utf-8")
        assert client.get("/assets/statics/x.txt").status_code == 404
        static_resp = client.get("/api/assets/statics/x.txt")
        assert static_resp.status_code == 200

        assert client.get("/users/").status_code == 404
        assert client.get("/api/users/").status_code == 200
    finally:
        sys.path[:] = [p for p in sys.path if p != str(project_dir)]
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        _clear_generated_modules()
