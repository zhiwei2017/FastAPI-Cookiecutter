.PHONY: clean help

help:
	clear;
	@echo "================= Usage =================";
	@echo "clean                  : Remove autogenerated folders and artifacts.";
	@echo "clean-pyc              : Remove python artifacts."
	@echo "clean-build            : Remove build artifacts."
	@echo "test                   : Run tests and generate coverage report.";

# Clean the folder from build/test related folders
clean: clean-build clean-pyc
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -f .coverage

clean-pyc:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

# Install requirements for testing and run tests
test:
	python3 -m pip install -r ./requirements/dev.txt
	python3 -m pytest
