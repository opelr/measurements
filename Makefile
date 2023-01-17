.PHONY: all
all: lint test

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install:  ## Install project dependencies
	@poetry install

.PHONY: lint
lint: ## Run linters
	@poetry run black .
	@poetry run isort .
	@poetry run flake8 --extend-ignore=E501 .

.PHONY: test
test: ## Run tests
	@poetry run pytest .
