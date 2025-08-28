# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=0

WORKDIR /app

# Build deps minimal set for common Python libs and gosu for PUID/PGID runtime user switch
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl ca-certificates gosu && \
    rm -rf /var/lib/apt/lists/*

# Pre-copy only requirements for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy the rest of the application
COPY . /app

# Add entrypoint script
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Non-root default; IDs will be remapped at runtime by entrypoint using gosu
RUN useradd -u 1000 -m appuser && \
    groupadd -g 1000 appgroup && \
    usermod -a -G appgroup appuser

EXPOSE 8080

# Simple HTTP healthcheck; adjust if your app exposes a different path
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://127.0.0.1:8080/health || exit 1

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
