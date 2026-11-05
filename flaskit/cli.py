"""flaskit command-line interface."""

from __future__ import annotations

import re
import shutil
from importlib import resources
from pathlib import Path

import click
from jinja2 import Environment, PackageLoader, StrictUndefined, select_autoescape

MODULE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def _env() -> Environment:
    return Environment(
        loader=PackageLoader("flaskit", "templates"),
        undefined=StrictUndefined,
        autoescape=select_autoescape(enabled_extensions=()),
        keep_trailing_newline=True,
    )


def _render(template_name: str, **context: object) -> str:
    return _env().get_template(template_name).render(**context)


def _write(path: Path, content: str, *, force: bool = False) -> None:
    if path.exists() and not force:
        raise click.ClickException(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    if not any(path.iterdir()) and not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(package_name="flaskit")
def main() -> None:
    """Scaffold Flask-Smorest projects and resource modules.

    \b
    Examples:
      flaskit init myapi
      flaskit generate module users
      flaskit generate module order_items --path ./myapi
      python -m flaskit -h

    \b
    After init:
      cd myapi && python -m venv .venv
      pip install -r requirements.txt
      flaskit generate module users
      python app.py
    """


@main.command("init")
@click.argument(
    "path",
    required=False,
    default=".",
    type=click.Path(file_okay=False, path_type=Path),
)
def init_project(path: Path) -> None:
    """Create a new flaskit project (app.py, config.py, resources/, assets/).

    The folder name becomes the default API_TITLE / project name.

    \b
    Examples:
      flaskit init
      flaskit init myapi
      flaskit init ./services/payments
      python -m flaskit init myapi
    """
    target = path.resolve()
    target.mkdir(parents=True, exist_ok=True)
    project_name = target.name

    project_files = {
        "app.py": "project/app.py.j2",
        "config.py": "project/config.py.j2",
        "requirements.txt": "project/requirements.txt.j2",
        # Template is env.example.j2 (no leading dot) so setuptools packages it
        ".env.example": "project/env.example.j2",
    }

    for dest_name, template_name in project_files.items():
        dest = target / dest_name
        if dest.exists():
            raise click.ClickException(f"Project already initialized (found {dest_name})")
        _write(dest, _render(template_name, project_name=project_name))

    # Static Docker assets (not Jinja)
    package_root = resources.files("flaskit").joinpath("templates/project")
    for dest_name, src_name in (
        ("Dockerfile", "Dockerfile"),
        (".dockerignore", "dockerignore"),
    ):
        dest = target / dest_name
        if dest.exists():
            raise click.ClickException(f"Project already initialized (found {dest_name})")
        src = package_root.joinpath(src_name)
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    _ensure_dir(target / "resources")
    _ensure_dir(target / "assets")
    _ensure_dir(target / "assets" / "statics")

    # Local Swagger UI assets (no CDN)
    swagger_src = resources.files("flaskit").joinpath("templates/project/assets/swagger-ui")
    swagger_dst = target / "assets" / "swagger-ui"
    if swagger_dst.exists():
        shutil.rmtree(swagger_dst)
    shutil.copytree(swagger_src, swagger_dst)

    # Cached static files directory (browser Cache-Control)
    statics_src = resources.files("flaskit").joinpath("templates/project/assets/statics")
    statics_dst = target / "assets" / "statics"
    if statics_src.is_dir():
        for item in statics_src.iterdir():
            dest = statics_dst / item.name
            if not dest.exists():
                if item.is_file():
                    dest.write_bytes(item.read_bytes())
                elif item.is_dir():
                    shutil.copytree(item, dest)

    click.echo(f"Initialized flaskit project '{project_name}' in {target}")
    click.echo("Next steps:")
    cwd = Path.cwd().resolve()
    if target == cwd:
        click.echo("  1. (already in the project directory)")
    else:
        try:
            cd_arg = str(target.relative_to(cwd))
        except ValueError:
            cd_arg = str(target)
        click.echo(f"  1. cd {cd_arg}")
    click.echo("  2. python -m venv .venv && activate it")
    click.echo("  3. pip install -r requirements.txt")
    click.echo("  4. flaskit generate module <name>")
    click.echo("  5. python app.py   # ENV=development (Flask)")
    click.echo(
        f"     # production (bjoern, Docker only): "
        f"docker build --build-arg DOCKER_TAG=1.0.0 -t {project_name} ."
    )



@main.group("generate")
def generate() -> None:
    """Generate project artifacts.

    \b
    Examples:
      flaskit generate module users
      flaskit generate module order_items --path ./myapi
    """


@generate.command("module")
@click.argument("name")
@click.option(
    "--path",
    "project_path",
    default=".",
    type=click.Path(file_okay=False, exists=True, path_type=Path),
    help="Project root containing resources/ (default: current directory).",
)
def generate_module(name: str, project_path: Path) -> None:
    """Generate a resource module under resources/<name>/.

    NAME must be snake_case (e.g. users, order_items).
    Creates blueprint.py, resource.py, and schema.py.

    \b
    Examples:
      flaskit generate module users
      flaskit generate module order_items
      flaskit generate module invoices --path ./myapi
      python -m flaskit generate module users
    """
    if not MODULE_NAME_RE.match(name):
        raise click.ClickException(
            "Module name must be snake_case starting with a letter "
            "(e.g. users, order_items)."
        )

    root = project_path.resolve()
    resources_dir = root / "resources"
    if not resources_dir.is_dir():
        raise click.ClickException(
            f"No resources/ directory in {root}. Run 'flaskit init' first."
        )

    module_dir = resources_dir / name
    if module_dir.exists():
        raise click.ClickException(f"Module already exists: {module_dir}")

    class_prefix = "".join(part.capitalize() for part in name.split("_"))
    context = {
        "name": name,
        "class_prefix": class_prefix,
        "title": name.replace("_", " ").title(),
    }

    module_dir.mkdir(parents=True, exist_ok=False)
    try:
        for filename, template_name in (
            ("blueprint.py", "module/blueprint.py.j2"),
            ("resource.py", "module/resource.py.j2"),
            ("schema.py", "module/schema.py.j2"),
        ):
            _write(module_dir / filename, _render(template_name, **context))
    except Exception:
        shutil.rmtree(module_dir, ignore_errors=True)
        raise

    click.echo(f"Generated module resources/{name}/")
    click.echo("  blueprint.py  resource.py  schema.py")
    click.echo("Restart the app to pick up the module in Swagger.")


if __name__ == "__main__":
    main()
