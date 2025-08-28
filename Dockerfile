# Multi-stage build for smaller image
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies without warnings
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip wheel --wheel-dir /wheels -r requirements.txt

# Final stage
FROM python:3.12-slim

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for Unraid compatibility
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser && \
    mkdir -p /app /config /data && \
    chown -R appuser:appuser /app /config /data

# Set working directory
WORKDIR /app

# Copy wheels from builder
COPY --from=builder /wheels /wheels

# Install Python dependencies as non-root user
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*.whl && \
    rm -rf /wheels

# Copy application files
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port (adjust based on your app)
EXPOSE 8080

# Health check for Unraid monitoring
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Environment variables for Unraid
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    CONFIG_PATH=/config \
    DATA_PATH=/data

# Run gunicorn with proper configuration
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--threads", "2", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
