PYTHON_SRC = .

.PHONY: lint
lint:
	@echo "Running Ruff linter..."
	ruff check $(PYTHON_SRC) --fix --preview --unsafe-fixes

.PHONY: format
format:
	@echo "Formatting code with Ruff..."
	ruff format $(PYTHON_SRC)

.PHONY: type-check
type-check:
	@echo "Running MyPy type checker..."
	mypy $(PYTHON_SRC) --extra-checks
	@echo "Running ty..."
	ty check

.PHONY: all
all: lint format type-check

.PHONY: clean
clean:
	@echo "Cleaning up pycache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
