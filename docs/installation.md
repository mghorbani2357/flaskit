# Installation

## Requirements

- Python **3.10+** (3.11–3.13 recommended; 3.14 needs marshmallow 4.x — handled in generated `requirements.txt`)
- `pip`

## Install flaskit (the CLI)

From the repository root:

```bash
pip install -e .
```

Or with docs tooling:

```bash
pip install -e ".[docs]"
```

Verify:

```bash
flaskit -h
# or
python -m flaskit -h
```

`-h` and `--help` both work.

## What gets installed

flaskit itself only depends on **Click** and **Jinja2**. Runtime stacks (Flask, Smorest, OpenTelemetry, …) are written into each generated project’s `requirements.txt` when you run `flaskit init`. **bjoern** is installed only inside the Docker image (not via `pip install -r requirements.txt`).
