# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Makefile — single entry point for all dev tasks
#  Usage: make <target>
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.DEFAULT_GOAL := help
.PHONY: help install install-dev lint format typecheck test coverage \
        notebook diagram docker-build docker-up docker-down clean

PYTHON  := python3.11
VENV    := .venv
PIP     := $(VENV)/bin/pip
PYTEST  := $(VENV)/bin/pytest
RUFF    := $(VENV)/bin/ruff
MYPY    := $(VENV)/bin/mypy

# ── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ── Setup ─────────────────────────────────────────────────────────────────────
$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: $(VENV)/bin/activate ## Create venv and install all dependencies
	$(PIP) install -e ".[dev,test,notebooks,docs]"
	$(VENV)/bin/pre-commit install
	@echo "✅  Environment ready. Activate with: source $(VENV)/bin/activate"

install-prod: $(VENV)/bin/activate ## Install production dependencies only
	$(PIP) install -e "."

# ── Code Quality ──────────────────────────────────────────────────────────────
lint: ## Run ruff linter
	$(RUFF) check src/ tests/

format: ## Auto-format code with ruff
	$(RUFF) format src/ tests/
	$(RUFF) check --fix src/ tests/

typecheck: ## Run mypy static type checking
	$(MYPY) src/

check: lint typecheck ## Run all code quality checks (no fixes)

# ── Testing ───────────────────────────────────────────────────────────────────
test: ## Run test suite
	$(PYTEST)

test-unit: ## Run unit tests only
	$(PYTEST) tests/unit/

test-integration: ## Run integration tests only
	$(PYTEST) tests/integration/ -m integration

test-fast: ## Run tests excluding slow ones
	$(PYTEST) -m "not slow"

coverage: ## Run tests with coverage report
	$(PYTEST) --cov=src --cov-report=term-missing --cov-report=html
	@echo "📊  HTML report: htmlcov/index.html"

# ── Notebooks ─────────────────────────────────────────────────────────────────
notebook: ## Launch Jupyter notebook server
	$(VENV)/bin/jupyter notebook notebooks/

# ── Docs & Diagrams ───────────────────────────────────────────────────────────
diagram: ## Regenerate architecture diagrams
	$(PYTHON) docs/architecture/generate_diagram.py
	@echo "📐  Diagrams saved to docs/architecture/"

docs: ## Build documentation site
	$(VENV)/bin/mkdocs build

docs-serve: ## Serve documentation locally
	$(VENV)/bin/mkdocs serve

# ── Docker ────────────────────────────────────────────────────────────────────
docker-build: ## Build Docker image (dev)
	docker compose build

docker-up: ## Start services with Docker Compose
	docker compose up

docker-down: ## Stop Docker services
	docker compose down

docker-prod: ## Build production Docker image
	docker build -f docker/Dockerfile.prod -t project-name:latest .

# ── Utilities ─────────────────────────────────────────────────────────────────
clean: ## Remove build artifacts, caches, and compiled files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete
	rm -rf dist/ build/ .coverage site/
	@echo "🧹  Clean done"

bump-patch: ## Bump patch version (0.0.X)
	$(VENV)/bin/hatch version patch

bump-minor: ## Bump minor version (0.X.0)
	$(VENV)/bin/hatch version minor
