# Publish

The distribution name on PyPI is **`flaskit-cli`** (`pip install flaskit-cli`). The import package and console script remain `flaskit`.

(`flaskit` and `flask-it` are unavailable / blocked by PyPI’s similarity rules.)

Current release line: **0.3.x**. Versions come from **git tags** via `setuptools-scm`.

## Tag and push

```bash
git tag -a v0.3.0 -m "flaskit-cli 0.3.0"
git push origin v0.3.0
```

Tags matching `v*` trigger [`.github/workflows/publish.yml`](https://github.com/mghorbani2357/flaskit/blob/master/.github/workflows/publish.yml). The workflow builds with Python 3.12 and uploads to PyPI automatically.

After a tag push, confirm:

- PyPI: https://pypi.org/project/flaskit-cli/
- Docs: rebuild **latest** from `master` on Read the Docs (Versions → ensure `latest` tracks `master`)

## GitHub configuration

Only one secret is required (repository **Settings → Secrets and variables → Actions**):

| Name | Purpose |
|------|---------|
| `PYPI_API_TOKEN` | PyPI API token (`pypi-...`) |

## Local build check

```bash
pip install -U build
python -m build
```

Confirm the wheel is named `flaskit_cli-0.3.0-…` (or the tag you created) and that `flaskit/templates/project/env.j2` is inside the archive.
