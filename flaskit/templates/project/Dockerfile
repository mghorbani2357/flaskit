# syntax=docker/dockerfile:1
# Python 3.13 — current stable with broad wheel support (LTS-quality baseline)

FROM python:3.13-bookworm AS builder

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
RUN pip install --prefix=/install -r requirements.txt \
    && pip install --prefix=/install "bjoern>=3.2.2"

FROM python:3.13-slim-bookworm AS base

ARG DOCKER_TAG=0.0.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ENV=production \
    HOST=0.0.0.0 \
    PORT=80 \
    API_VERSION=${DOCKER_TAG} \
    TIMEZONE=UTC \
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

ENTRYPOINT ["python3", "app.py"]
