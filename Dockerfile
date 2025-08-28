# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=0

WORKDIR /app

# Install build deps only in builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# Upgrade pip/setuptools/wheel and build wheels for all deps
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip wheel --wheel-dir /wheels -r /app/requirements.txt

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create non-root user
RUN groupadd -g 1000 appgroup || true && \
    useradd -u 1000 -g appgroup -m -s /usr/sbin/nologin appuser || true

# Copy prebuilt wheels and install without build-time deps
COPY --from=builder /wheels /wheels
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools && \
    pip install --no-index --find-links=/wheels -r /app/requirements.txt --no-cache-dir && \
    rm -rf /wheels /root/.cache

# Copy application code
COPY . /app
RUN chown -R appuser:appgroup /app

EXPOSE 8080

# Healthcheck route should exist in the app
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8080/health || exit 1

# Switch to non-root user
USER appuser

# Run gunicorn as non-root
ENV APP_MODULE=openvote.app:app \
    PORT=8080 \
    WORKERS=2
CMD ["gunicorn", "openvote.app:app", "-b", "0.0.0.0:8080", "--workers", "2", "--timeout", "30"]
