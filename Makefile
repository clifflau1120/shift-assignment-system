OS = $(shell uname -s)

PACKAGE_NAME=shift-scheduler
MODULE_NAME=shift_scheduler
PYTHON_VERSION=3.12.8


.PHONY: pyenv
pyenv:
ifeq (,  $(shell command -v pyenv))
	curl https://pyenv.run | bash
endif


.PHONY: python
python: pyenv


.PHONY: virtualenv
virtualenv: python
ifeq (,  $(shell command -v pyenv))
	@echo "Please install pyenv and pyenv-virtualenv."
	exit 1;
endif
	pyenv install -s ${PYTHON_VERSION}
	pyenv virtualenv ${PYTHON_VERSION} ${PACKAGE_NAME} || :
	pyenv local ${PACKAGE_NAME}


.PHONY: virtualenv-delete
virtualenv-delete: python
	pyenv virtualenv-delete -f ${PACKAGE_NAME}


requirements.txt: requirements.in
	uv pip compile requirements.in > requirements.txt


.PHONY: install
install: requirements.txt requirements-dev.txt pyproject.toml
	uv pip install -e '.[dev]'


.PHONY: pre-commit
pre-commit:
	pre-commit install


.PHONY: setup
setup: virtualenv install pre-commit


.PHONY: format
format:
	ruff check --select I --fix .
	ruff format


.PHONY: lint
lint:
	ruff format --check
	ruff check
	pyright


.PHONY: test
test:
	pytest


.PHONY: run
run:
	python3 main.py


.PHONY: build
build:
	build


.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf **/__pycache__
	rm -rf **/.mypy_cache
	rm -rf **/.pytest_cache
	rm -rf **/.ruff_cache
	rm -rf **/*.egg-info
	rm -rf **/MANIFEST
	rm -rf coverage coverage.xml .coverage .coverage.*

	find ${MODULE_NAME} -type f -name '*.pyc' -delete
