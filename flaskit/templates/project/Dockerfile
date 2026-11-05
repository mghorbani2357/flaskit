# syntax=docker/dockerfile:1

# --- Builder: compile bjoern against libev ---
FROM python:3.13.1-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libev-dev \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip

COPY requirements.txt .
# App deps + bjoern (production WSGI; not in requirements.txt for local/Windows installs)
RUN pip install --prefix=/install -r requirements.txt \
    && pip install --prefix=/install "bjoern>=3.2.2"

# --- Runtime: slim image, non-root, bjoern via app.py ---
FROM python:3.13.1-slim-bookworm AS base

ARG DOCKER_TAG=0.0.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ENV=production \
    HOST=0.0.0.0 \
    PORT=80 \
    API_VERSION=${DOCKER_TAG} \
    BJOERN_REUSE_PORT=true \
    LOG_OUTPUT=stream \
    LOG_STREAM=stderr

EXPOSE 80

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libev4 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 1000 app \
    && useradd --system --uid 1000 --gid app --home-dir /app --shell /usr/sbin/nologin app \
    && mkdir -p /app/logs \
    && chown -R app:app /app

COPY --from=builder /install /usr/local
COPY --chown=app:app . .

USER app

# app.py selects bjoern when ENV=production
ENTRYPOINT ["python3", "app.py"]
