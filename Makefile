.PHONY: test clean dev docs

# Test the package
test:
	python -m pytest tests/ -v

# Install package in development mode
dev:
	pip install -e .

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/ src/*.egg-info/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Build documentation
docs:
	@echo "Documentation build not configured yet"

# Default target
.DEFAULT_GOAL := test
