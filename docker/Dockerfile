# ── Stage 1: base ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ── Stage 2: dependencies ──────────────────────────────────────────────────────
FROM base AS dependencies

# Install system packages needed for common ML/data libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
# Install only runtime deps in this stage
RUN pip install -e ".[dev,test]"

# ── Stage 3: development ───────────────────────────────────────────────────────
FROM dependencies AS development

# Install Jupyter for notebook support
RUN pip install -e ".[notebooks]"

COPY . .

# Expose Jupyter port
EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
