"""Tests for flaskit generate module."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from flaskit.cli import main


def _init(runner: CliRunner, project_dir: Path) -> None:
    result = runner.invoke(main, ["init", str(project_dir)])
    assert result.exit_code == 0, result.output


def test_generate_module_creates_files(runner: CliRunner, project_dir: Path) -> None:
    _init(runner, project_dir)
    result = runner.invoke(
        main, ["generate", "module", "users", "--path", str(project_dir)]
    )
    assert result.exit_code == 0, result.output
    module = project_dir / "resources" / "users"
    assert (module / "blueprint.py").is_file()
    assert (module / "resource.py").is_file()
    assert (module / "schema.py").is_file()

    blueprint = (module / "blueprint.py").read_text(encoding="utf-8")
    resource = (module / "resource.py").read_text(encoding="utf-8")
    schema = (module / "schema.py").read_text(encoding="utf-8")
    assert 'URL_PREFIX = "/users"' in blueprint
    assert "flask_bp = Blueprint" in blueprint
    assert "Flask application blueprint" in blueprint or "flask_bp" in blueprint
    assert "smorest_blp = SmorestBlueprint" in resource
    assert "Flask-Smorest blueprint" in resource
    assert "class UsersList" in resource
    assert "class UsersRequest" in schema
    assert "class UsersResponse" in schema
    assert "flask_bp" in result.output
    assert "smorest_blp" in result.output


def test_generate_module_snake_case(runner: CliRunner, project_dir: Path) -> None:
    _init(runner, project_dir)
    result = runner.invoke(
        main, ["generate", "module", "order_items", "--path", str(project_dir)]
    )
    assert result.exit_code == 0, result.output
    resource = (
        project_dir / "resources" / "order_items" / "resource.py"
    ).read_text(encoding="utf-8")
    assert "class OrderItemsList" in resource
    assert "OrderItemsRequest" in resource


def test_generate_rejects_invalid_name(runner: CliRunner, project_dir: Path) -> None:
    _init(runner, project_dir)
    result = runner.invoke(
        main, ["generate", "module", "Users", "--path", str(project_dir)]
    )
    assert result.exit_code != 0
    assert "snake_case" in result.output


def test_generate_requires_init(runner: CliRunner, tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    result = runner.invoke(main, ["generate", "module", "users", "--path", str(empty)])
    assert result.exit_code != 0
    assert "flaskit init" in result.output


def test_generate_refuses_duplicate(runner: CliRunner, project_dir: Path) -> None:
    _init(runner, project_dir)
    first = runner.invoke(
        main, ["generate", "module", "users", "--path", str(project_dir)]
    )
    assert first.exit_code == 0, first.output
    second = runner.invoke(
        main, ["generate", "module", "users", "--path", str(project_dir)]
    )
    assert second.exit_code != 0
    assert "already exists" in second.output.lower()


def test_generate_help_includes_examples(runner: CliRunner) -> None:
    result = runner.invoke(main, ["generate", "module", "-h"])
    assert result.exit_code == 0
    assert "Examples:" in result.output
    assert "flaskit generate module users" in result.output
