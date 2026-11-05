"""Ensure Jinja templates are discoverable after packaging."""

from __future__ import annotations

from importlib import resources

import pytest
from jinja2 import Environment, PackageLoader, TemplateNotFound


REQUIRED_TEMPLATES = (
    "project/app.py.j2",
    "project/config.py.j2",
    "project/requirements.txt.j2",
    "project/env.example.j2",
    "module/blueprint.py.j2",
    "module/resource.py.j2",
    "module/schema.py.j2",
)

REQUIRED_STATIC = (
    "templates/project/Dockerfile",
    "templates/project/dockerignore",
    "templates/project/assets/swagger-ui/swagger-ui.css",
    "templates/project/assets/swagger-ui/swagger-ui-bundle.js",
    "templates/project/assets/swagger-ui/swagger-ui-standalone-preset.js",
)


@pytest.fixture(scope="module")
def jinja_env() -> Environment:
    return Environment(
        loader=PackageLoader("flaskit", "templates"),
        keep_trailing_newline=True,
    )


@pytest.mark.parametrize("name", REQUIRED_TEMPLATES)
def test_required_jinja_templates_exist(jinja_env: Environment, name: str) -> None:
    try:
        template = jinja_env.get_template(name)
    except TemplateNotFound as exc:
        pytest.fail(f"Template not found: {name} ({exc})")
    assert template is not None


def test_env_example_template_is_not_dotfile() -> None:
    """Leading-dot templates are dropped by setuptools; use env.example.j2."""
    root = resources.files("flaskit").joinpath("templates/project")
    assert root.joinpath("env.example.j2").is_file()
    assert not root.joinpath(".env.example.j2").is_file()


@pytest.mark.parametrize("relpath", REQUIRED_STATIC)
def test_required_static_package_files_exist(relpath: str) -> None:
    path = resources.files("flaskit").joinpath(relpath)
    assert path.is_file(), f"Missing package file: {relpath}"


def test_env_example_renders_project_name(jinja_env: Environment) -> None:
    text = jinja_env.get_template("project/env.example.j2").render(project_name="demoapi")
    assert "API_TITLE=demoapi" in text
    assert "API_DESCRIPTION=demoapi API" in text
