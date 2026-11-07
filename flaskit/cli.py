"""flaskit command-line interface."""

from __future__ import annotations

import os
import re
import shutil
import sys
from importlib import resources
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound
from jinja2 import select_autoescape

MODULE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")

TEMPLATE_ALIASES = {
    "project/.env.example.j2": "project/env.example.j2",
}


def _templates_root() -> Path:
    """Return filesystem path to packaged Jinja templates."""
    traversable = resources.files("flaskit").joinpath("templates")
    try:
        path = Path(os.fspath(traversable))  # type: ignore[arg-type]
    except TypeError:
        path = Path(str(traversable))
    if not path.is_dir():
        raise click.ClickException(
            "flaskit templates are missing from the installation. "
            "Reinstall with: pip install -U git+https://github.com/mghorbani2357/flaskit.git"
        )
    return path


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(_templates_root()),
        undefined=StrictUndefined,
        autoescape=select_autoescape(enabled_extensions=()),
        keep_trailing_newline=True,
    )


def _render(template_name: str, **context: object) -> str:
    name = TEMPLATE_ALIASES.get(template_name, template_name)
    env = _env()
    try:
        return env.get_template(name).render(**context)
    except TemplateNotFound as exc:
        available = sorted(env.list_templates(extensions=("j2",)))
        raise click.ClickException(
            f"Template not found: {template_name} (resolved: {name}). "
            f"Available: {', '.join(available) or '(none)'}. "
            "Reinstall flaskit from the latest git tag/master."
        ) from exc


def _write(path: Path, content: str, *, force: bool = False) -> None:
    if path.exists() and not force:
        raise click.ClickException(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _ensure_dir(path: Path) -> None:
    """Create an empty directory (no .gitkeep)."""
    path.mkdir(parents=True, exist_ok=True)


def _copy_tree(src: Path, dst: Path) -> None:
    """Copy a directory tree; works cross-platform."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(package_name="flaskit-cli")
def main() -> None:
    """Scaffold Flask-Smorest projects and resource modules.

    \b
    Examples:
      flaskit init myapi
      flaskit generate module users
      flaskit generate module order_items --path ./myapi
      python -m flaskit -h

    \b
    After init (use Python 3.12):
      cd myapi
      python3.12 -m venv .venv
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

    if sys.version_info >= (3, 14):
        click.echo(
            "WARNING: Python "
            f"{sys.version_info.major}.{sys.version_info.minor} detected. "
            "Generated apps expect Python 3.11-3.13 (3.12 recommended). "
            "Create the venv with Python 3.12, e.g.:\n"
            "  brew install python@3.12\n"
            "  /opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv",
            err=True,
        )

    project_files = {
        "app.py": "project/app.py.j2",
        "config.py": "project/config.py.j2",
        "requirements.txt": "project/requirements.txt.j2",
        ".env.example": "project/env.example.j2",
    }

    for dest_name, template_name in project_files.items():
        dest = target / dest_name
        if dest.exists():
            raise click.ClickException(f"Project already initialized (found {dest_name})")
        _write(dest, _render(template_name, project_name=project_name))

    package_root = _templates_root() / "project"
    for dest_name, src_name in (
        ("Dockerfile", "Dockerfile"),
        (".dockerignore", "dockerignore"),
        (".python-version", "python-version"),
    ):
        dest = target / dest_name
        if dest.exists():
            raise click.ClickException(f"Project already initialized (found {dest_name})")
        src = package_root / src_name
        if not src.is_file():
            raise click.ClickException(
                f"Missing packaged file templates/project/{src_name}. Reinstall flaskit."
            )
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    _ensure_dir(target / "resources")
    _ensure_dir(target / "assets")
    _ensure_dir(target / "assets" / "statics")
    _ensure_dir(target / "templates")

    swagger_src = package_root / "assets" / "swagger-ui"
    if not swagger_src.is_dir():
        raise click.ClickException(
            "Missing packaged swagger-ui assets. Reinstall flaskit from latest git tag."
        )
    _copy_tree(swagger_src, target / "assets" / "swagger-ui")

    swagger_html = package_root / "templates" / "swagger_ui.html"
    if not swagger_html.is_file():
        raise click.ClickException("Missing templates/swagger_ui.html in package.")
    _write(
        target / "templates" / "swagger_ui.html",
        swagger_html.read_text(encoding="utf-8"),
        force=True,
    )

    statics_src = package_root / "assets" / "statics"
    statics_dst = target / "assets" / "statics"
    if statics_src.is_dir():
        for item in statics_src.iterdir():
            if item.name.lower().startswith("readme"):
                continue
            dest = statics_dst / item.name
            if not dest.exists():
                if item.is_file():
                    shutil.copy2(item, dest)
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
    click.echo("  2. python3.12 -m venv .venv && activate it  # 3.11-3.13 required")
    click.echo("  3. pip install -U pip && pip install -r requirements.txt")
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

    Creates Flask blueprint (flask_bp) + Smorest blueprint (smorest_blp) stubs.

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
    click.echo("  blueprint.py (flask_bp)  resource.py (smorest_blp)  schema.py")
    click.echo("Restart the app to pick up the module in Swagger.")


if __name__ == "__main__":
    main()
