"""flaskit — CLI scaffolding for Flask-Smorest applications."""

from __future__ import annotations

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

try:
    __version__ = version("flask-it")
except PackageNotFoundError:  # pragma: no cover - editable / source tree
    __version__ = "0.0.0.dev0"
