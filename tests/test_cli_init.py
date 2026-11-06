"""Tests for flaskit init."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from flaskit.cli import main


EXPECTED_ROOT_FILES = (
    "app.py",
    "config.py",
    "requirements.txt",
    ".env.example",
    "Dockerfile",
    ".dockerignore",
    ".python-version",
)


def test_init_creates_project_layout(runner: CliRunner, project_dir: Path) -> None:
    result = runner.invoke(main, ["init", str(project_dir)])
    assert result.exit_code == 0, result.output
    assert "Initialized flaskit project 'myapi'" in result.output
    assert project_dir.name in result.output
    assert ("cd " in result.output) or ("already in the project" in result.output)

    for name in EXPECTED_ROOT_FILES:
        assert (project_dir / name).is_file(), f"missing {name}"

    assert (project_dir / "resources").is_dir()
    assert (project_dir / "assets" / "statics").is_dir()
    assert (project_dir / "assets" / "swagger-ui" / "swagger-ui.css").is_file()
    assert (project_dir / "assets" / "swagger-ui" / "swagger-ui-bundle.js").is_file()
    assert (
        project_dir / "assets" / "swagger-ui" / "swagger-ui-standalone-preset.js"
    ).is_file()


def test_init_seeds_title_from_folder_name(runner: CliRunner, tmp_path: Path) -> None:
    target = tmp_path / "payments"
    result = runner.invoke(main, ["init", str(target)])
    assert result.exit_code == 0, result.output

    env_example = (target / ".env.example").read_text(encoding="utf-8")
    config = (target / "config.py").read_text(encoding="utf-8")
    assert "API_TITLE=payments" in env_example
    assert 'API_TITLE = _env("API_TITLE", "payments")' in config


def test_init_refuses_overwrite(runner: CliRunner, project_dir: Path) -> None:
    first = runner.invoke(main, ["init", str(project_dir)])
    assert first.exit_code == 0, first.output
    second = runner.invoke(main, ["init", str(project_dir)])
    assert second.exit_code != 0
    assert "already initialized" in second.output.lower()


def test_init_requirements_exclude_bjoern(runner: CliRunner, project_dir: Path) -> None:
    result = runner.invoke(main, ["init", str(project_dir)])
    assert result.exit_code == 0, result.output
    reqs = (project_dir / "requirements.txt").read_text(encoding="utf-8")
    install_lines = [
        line.strip()
        for line in reqs.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert not any("bjoern" in line for line in install_lines)
    dockerfile = (project_dir / "Dockerfile").read_text(encoding="utf-8")
    assert "bjoern" in dockerfile


def test_init_writes_python_version_and_marshmallow_pin(
    runner: CliRunner, project_dir: Path
) -> None:
    result = runner.invoke(main, ["init", str(project_dir)])
    assert result.exit_code == 0, result.output
    assert (project_dir / ".python-version").read_text(encoding="utf-8").strip() == "3.12"
    reqs = (project_dir / "requirements.txt").read_text(encoding="utf-8")
    assert "marshmallow>=3.24.1,<5" in reqs
    assert "3.11–3.13" in reqs or "3.11-3.13" in reqs or "3.14" in reqs


def test_init_app_has_core_hooks(runner: CliRunner, project_dir: Path) -> None:
    result = runner.invoke(main, ["init", str(project_dir)])
    assert result.exit_code == 0, result.output
    app_src = (project_dir / "app.py").read_text(encoding="utf-8")
    for needle in (
        "def create_app(",
        "def init_app(",
        "def setup_static_caching(",
        "def _run_bjoern(",
        "/assets/statics",
        "client_ip",
        "show_servers",
    ):
        assert needle in app_src, f"missing {needle}"


def test_init_help_includes_examples(runner: CliRunner) -> None:
    result = runner.invoke(main, ["init", "-h"])
    assert result.exit_code == 0
    assert "Examples:" in result.output
    assert "flaskit init myapi" in result.output


def test_root_help_includes_examples(runner: CliRunner) -> None:
    result = runner.invoke(main, ["-h"])
    assert result.exit_code == 0
    assert "Examples:" in result.output
    assert "flaskit generate module users" in result.output
