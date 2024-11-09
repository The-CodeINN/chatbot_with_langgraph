# Use Python 3.13 Alpine image as base
FROM python:3.13-alpine3.20

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Install uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install build dependencies including C++ compiler and numpy requirements
RUN apk add --no-cache --virtual .build-deps \
    g++ \
    gcc \
    gfortran \
    linux-headers \
    musl-dev \
    openblas-dev \
    python3-dev \
    && apk add --no-cache \
    openblas

# Create non-root user and set up directories with correct permissions
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    mkdir -p /app /home/appuser/.cache/uv && \
    chown -R appuser:appgroup /app /home/appuser/.cache

# Set working directory
WORKDIR /app

# Copy dependency files
COPY --chown=appuser:appgroup pyproject.toml .
COPY --chown=appuser:appgroup uv.lock* .

# Switch to non-root user for installation
USER appuser

# Install dependencies without installing the project
RUN uv sync --frozen --no-install-project

# Copy the application code
COPY --chown=appuser:appgroup . .

# Install the project itself
RUN uv sync --frozen

# Switch back to root to remove build dependencies
USER root
RUN apk del .build-deps

# Switch back to non-root user
USER appuser

# Copy the entrypoint script with executable permissions set on the host
COPY entrypoint.sh /entrypoint.sh

# Use "sh" to run the entrypoint script
ENTRYPOINT ["sh", "/entrypoint.sh"]
