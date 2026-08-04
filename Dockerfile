FROM python:3.12.13-alpine3.22 AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.11.28 /uv /uvx /bin/

FROM python-base AS development
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY tests ./tests
RUN uv sync --frozen --all-groups --no-editable
CMD ["uv", "run", "--no-sync", "pytest", "-q"]

FROM python-base AS builder
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable

FROM python:3.12.13-alpine3.22 AS production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"
RUN addgroup -S -g 10001 bot \
    && adduser -S -D -H -u 10001 -G bot bot
WORKDIR /app
COPY --from=builder --chown=bot:bot /app/.venv /app/.venv
USER bot
STOPSIGNAL SIGTERM
CMD ["market-bot"]
