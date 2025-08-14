# Sendora OCR Docker Configuration
# Multi-stage build for production deployment

# Stage 1: Base environment with system dependencies
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    curl \
    wget \
    # Fonts for better PDF rendering
    fonts-liberation \
    fonts-dejavu-core \
    fontconfig \
    # Image processing
    libjpeg-dev \
    libpng-dev \
    # X11 for wkhtmltopdf
    xvfb \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install wkhtmltopdf manually from official repository
RUN wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6.1-3.jammy_amd64.deb || true \
    && apt-get update && apt-get install -f -y \
    && rm wkhtmltox_0.12.6.1-3.jammy_amd64.deb

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 app

# Stage 2: Python dependencies
FROM base as dependencies

# Set working directory
WORKDIR /app

# Copy requirements file first (for Docker layer caching)
COPY requirements_v2.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements_v2.txt

# Stage 3: Application assembly
FROM dependencies as application

# Set working directory first
WORKDIR /app

# Copy application code with proper ownership
COPY --chown=app:app backend/ backend/
COPY --chown=app:app frontend/ frontend/
COPY --chown=app:app config/ config/
COPY --chown=app:app debug_extraction.py .
COPY --chown=app:app test_size_extraction.py .

# Create required directories as root, then change ownership
RUN mkdir -p uploads job_orders job_orders/pdf temp logs && \
    chown -R app:app uploads job_orders temp logs

# Switch to app user
USER app

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=backend.app_v2:app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Production startup with Gunicorn
CMD ["python", "-m", "gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--threads", "2", \
     "--timeout", "120", \
     "--keep-alive", "2", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "backend.app_v2:app"]