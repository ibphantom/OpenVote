# syntax=docker/dockerfile:1.7

##########
# Builder
##########
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install build deps only in builder stage
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade tooling and build wheels for all dependencies
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip wheel --wheel-dir /wheels -r requirements.txt


##########
# Runtime
##########
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create non-root user/group
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /usr/sbin/nologin appuser

# Copy prebuilt wheels and install without build-time deps
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools && \
    pip install --no-index --find-links=/wheels -r requirements.txt --no-cache-dir && \
    rm -rf /wheels /root/.cache

# Copy application code
COPY . .
RUN chown -R appuser:appgroup /app

EXPOSE 8080

# Healthcheck (make sure /health exists in your Flask app)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8080/health || exit 1

# Switch to non-root user
USER appuser

# Run gunicorn
CMD ["gunicorn", "openvote.app:app", "-b", "0.0.0.0:8080", "--workers", "2", "--timeout", "30"]
