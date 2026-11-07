"""Build a real wheel and prove templates (incl. env.j2) are installed."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def built_wheel(tmp_path_factory: pytest.TempPathFactory) -> Path:
    dist = tmp_path_factory.mktemp("dist")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "build", "-q"],
        check=True,
        cwd=REPO_ROOT,
    )
    subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist)],
        check=True,
        cwd=REPO_ROOT,
    )
    wheels = list(dist.glob("flaskit_cli-*.whl")) + list(dist.glob("flaskit-cli-*.whl"))
    assert wheels, f"No wheel produced in {dist}"
    return wheels[0]


def test_wheel_contains_env_example_template(built_wheel: Path) -> None:
    with zipfile.ZipFile(built_wheel) as zf:
        names = zf.namelist()
    assert "flaskit/templates/project/env.j2" in names
    assert "flaskit/templates/project/.env.j2" not in names
    assert "flaskit/templates/project/.env.example.j2" not in names

    assert "flaskit/templates/project/app.py.j2" in names
    assert "flaskit/templates/project/Dockerfile" in names
    assert "flaskit/templates/project/dockerignore" in names
    assert "flaskit/templates/project/python-version" in names
    assert "flaskit/templates/project/templates/swagger_ui.html" in names
    assert any(n.endswith("swagger-ui/swagger-ui.css") for n in names)
    assert not any(n.endswith(".gitkeep") for n in names)


def test_wheel_install_init_succeeds(built_wheel: Path, tmp_path: Path) -> None:
    """Clean venv + wheel install must run `flaskit init` without TemplateNotFound."""
    venv = tmp_path / "venv"
    project = tmp_path / "tpm"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    if sys.platform == "win32":
        python = venv / "Scripts" / "python.exe"
        flaskit = venv / "Scripts" / "flaskit.exe"
    else:
        python = venv / "bin" / "python"
        flaskit = venv / "bin" / "flaskit"

    subprocess.run(
        [str(python), "-m", "pip", "install", "-q", str(built_wheel)],
        check=True,
    )
    cli_src = subprocess.check_output(
        [
            str(python),
            "-c",
            "import flaskit.cli,inspect; print(inspect.getsource(flaskit.cli))",
        ],
        text=True,
    )
    assert '".env": "project/env.j2"' in cli_src

    result = subprocess.run(
        [str(flaskit), "init", str(project)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert (project / ".env").is_file()
    assert not (project / ".env.example").exists()
    assert (project / "app.py").is_file()
    assert (project / "Dockerfile").is_file()
    assert "TemplateNotFound" not in result.stderr
    assert "Initialized flaskit project 'tpm'" in result.stdout
