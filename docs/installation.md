# Installation

## Requirements

| Component | Python |
|-----------|--------|
| flaskit CLI | **3.10+** |
| Generated applications | **3.11–3.13** (**3.12** recommended) |

!!! warning "Avoid Python 3.14 for generated apps"
    Marshmallow / flask-smorest often fail to install on 3.14 from PyPI. Use 3.12 and the generated `.python-version` file.

## Install the CLI

=== "PyPI"

    ```bash
    pip install flask-it
    ```

    The PyPI project is **`flask-it`** (the name `flaskit` is taken). After install, the CLI and import package are still **`flaskit`**.

=== "Editable (development)"

    ```bash
    git clone https://github.com/mghorbani2357/flaskit.git
    cd flaskit
    pip install -e .
    ```

=== "With docs tooling"

    ```bash
    pip install -e ".[docs]"
    ```

=== "With test extras"

    ```bash
    pip install -e ".[test]"
    ```

Verify:

```bash
flaskit -h
flaskit --version
python -m flaskit -h
```

## What the CLI depends on

flaskit itself only needs **Click** and **Jinja2**. Flask, Smorest, OpenTelemetry, and related packages are written into each project’s `requirements.txt` by `flaskit init`.

**bjoern** is installed only inside the Docker image (not via `pip install -r requirements.txt`).

## Versioning

The published package version comes from **git tags** via `setuptools-scm` (for example `v0.2.0`). See [Publishing](publishing.md).
