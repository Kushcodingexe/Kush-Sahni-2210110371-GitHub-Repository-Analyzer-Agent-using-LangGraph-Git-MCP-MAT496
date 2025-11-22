# Multi-stage Dockerfile for GitHub Repository Analyzer Agent
# Optimized for production use

# ============================================================================
# Stage 1: Builder - Install dependencies
# ============================================================================
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================================================
# Stage 2: Runtime - Create minimal production image
# ============================================================================
FROM python:3.10-slim

# Set metadata
LABEL maintainer="github-agent"
LABEL description="AI agent for analyzing GitHub repositories using LangGraph"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY README.md LICENSE ./
COPY setup.py pyproject.toml ./

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Install the package
RUN pip install --no-cache-dir -e .

# Create non-root user for security
RUN useradd -m -u 1000 agentuser && \
    chown -R agentuser:agentuser /app

# Switch to non-root user
USER agentuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port (if running as server in future)
# EXPOSE 8000

# Health check (optional - for future server mode)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "from src.config import Config; Config.validate()"

# Default command - interactive mode
CMD ["github-agent", "interactive"]

# Alternative commands:
# CMD ["github-agent", "config"]  # Show config
# CMD ["github-agent", "--help"]  # Show help
