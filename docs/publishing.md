# Publishing flaskit to PyPI

Package versions are derived from **git tags** using `setuptools-scm` (configured in `pyproject.toml`).

## Tag and push

```bash
git tag -a v0.2.0 -m "flaskit 0.2.0"
git push origin v0.2.0
```

Tags matching `v*` trigger [`.github/workflows/publish.yml`](https://github.com/mghorbani2357/flaskit/blob/master/.github/workflows/publish.yml).

## GitHub configuration

### Secret

| Name | Purpose |
|------|---------|
| `PYPI_API_TOKEN` | PyPI API token (`pypi-...`) used as the publish password |

### Variables (optional)

| Name | Default | Purpose |
|------|---------|---------|
| `PYTHON_VERSION` | `3.12` | Builder Python |
| `PYPI_REPOSITORY_URL` | `https://upload.pypi.org/legacy/` | Use TestPyPI URL for dry runs |
| `PYPI_ENVIRONMENT` | `pypi` | GitHub Environment name |

Create them under **Settings → Secrets and variables → Actions**.

### Environment

The workflow references a GitHub Environment (`vars.PYPI_ENVIRONMENT` or `pypi`). Create that environment and attach the secret if you use environment-scoped secrets.

## Local build check

```bash
pip install -U build
python -m build
```

Confirm the wheel version matches the tag and that `flaskit/templates/project/env.example.j2` is inside the archive.
