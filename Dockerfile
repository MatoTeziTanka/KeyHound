# KeyHound Enhanced - Production Docker Container
# Multi-stage build for optimal size and security

# Stage 1: Base image with Python and system dependencies
FROM nvidia/cuda:11.8-runtime-ubuntu20.04 AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN useradd --create-home --shell /bin/bash keyhound

# Stage 2: Python dependencies
FROM base AS dependencies

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM dependencies AS application

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY templates/ ./templates/
COPY static/ ./static/
COPY main.py .
COPY LICENSE .
COPY README.md .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/results /app/results/backups

# Set ownership
RUN chown -R keyhound:keyhound /app

# Switch to non-root user
USER keyhound

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Default command
CMD ["python3", "main.py", "--web", "--config", "config/docker.yaml"]

# Stage 4: GPU-optimized version
FROM application AS gpu

# Install GPU-specific dependencies
USER root
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
USER keyhound

# Override command for GPU usage
CMD ["python3", "main.py", "--web", "--gpu", "--config", "config/docker.yaml"]
