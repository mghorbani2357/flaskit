# Publish

The distribution name on PyPI is **`flaskit-cli`** (`pip install flaskit-cli`). The import package and console script remain `flaskit`.

(`flaskit` and `flask-it` are unavailable / blocked by PyPI’s similarity rules.)

Package versions are derived from **git tags** using `setuptools-scm` (configured in `pyproject.toml`).

## Tag and push

```bash
git tag -a v0.2.1 -m "flaskit-cli 0.2.1"
git push origin v0.2.1
```

Tags matching `v*` trigger [`.github/workflows/publish.yml`](https://github.com/mghorbani2357/flaskit/blob/master/.github/workflows/publish.yml). The workflow builds with Python 3.12 and uploads to PyPI automatically.

## GitHub configuration

Only one secret is required (repository **Settings → Secrets and variables → Actions**):

| Name | Purpose |
|------|---------|
| `PYPI_API_TOKEN` | PyPI API token (`pypi-...`) |

No Actions variables are needed. Python version and the PyPI upload URL are fixed in the workflow file.

## Local build check

```bash
pip install -U build
python -m build
```

Confirm the wheel is named `flaskit_cli-…` and that `flaskit/templates/project/env.j2` is inside the archive.
