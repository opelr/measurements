.PHONY: install
install:
	@poetry install

.PHONY: lint
lint:
	@poetry run black .
	@poetry run isort .
	@poetry run flake8 --extend-ignore=E501 .
