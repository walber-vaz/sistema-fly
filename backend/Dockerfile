FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /build

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /build
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.12-slim-bookworm

WORKDIR /build

RUN addgroup --gid 1001 --system sfuser \
    && adduser --gid 1001 --shell /bin/false --disabled-password --uid 1001 sfuser

COPY --from=builder --chown=sfuser:sfuser /build /build

ENV PATH="/build/.venv/bin:$PATH"

RUN chmod +x ./scripts/entrypoint.sh \
    && chown -R sfuser:sfuser /build
EXPOSE 8000

ENTRYPOINT []

CMD ["sh", "./scripts/entrypoint.sh"]
