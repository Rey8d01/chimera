# An example using multi-stage image builds to create a final image without uv.

# First, build the application in the `/app` directory.
# See `Dockerfile` for details.
FROM ghcr.io/astral-sh/uv:0.7.17-python3.13-alpine AS builder
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Disable Python downloads, because we want to use the system interpreter
# across both images. If using a managed Python version, it needs to be
# copied from the build image into the final image; see `standalone.Dockerfile`
# for an example.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev
COPY . /app

# Then, use a final image without uv
FROM python:3.13.5-alpine3.22
# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.11-slim-bookworm`
# will fail.

RUN addgroup -S app && adduser -S -G app app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy the application from the builder
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
RUN chmod +x /app/docker-entrypoint.sh

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

USER app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --quiet --spider http://127.0.0.1:80/health || exit 1

# Run the FastAPI application by default
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["web"]
