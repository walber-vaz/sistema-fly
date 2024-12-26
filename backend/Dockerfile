FROM python:3.12.8-alpine3.21 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /build

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust

RUN pip install --no-cache-dir -U pip setuptools wheel \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.in-project true \
    && poetry config installer.max-workers 10

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-dev

FROM python:3.12.8-alpine3.21

WORKDIR /build

RUN apk add --no-cache libffi libstdc++ su-exec && \
    addgroup -S sfuser -g 1001 && \
    adduser -S sfuser -G sfuser -u 1001 -s /bin/false

COPY --from=builder --chown=sfuser:sfuser /build/.venv .venv

COPY --chown=sfuser:sfuser . .

RUN chmod +x ./scripts/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/build/scripts/entrypoint.sh"]
