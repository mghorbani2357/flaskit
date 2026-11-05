"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """Empty directory used as flaskit init / generate target."""
    target = tmp_path / "myapi"
    target.mkdir()
    return target
