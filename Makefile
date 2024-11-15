# =============================================================================
# make Script       The purpose of this Makefile is to support the whole
#                   software development process for an application. It
#                   contains also the necessary tools for the CI activities.
# =============================================================================

.DEFAULT_GOAL := help

.PHONY: action \
        conda-dev \
        conda-prod \
        dev \
        docs \
        everything \
        final \
        format \
        lint \
        mypy-stubgen \
        pre-push \
        pytest-ci \
        pytest-first-issue \
        pytest-ignore-mark \
        pytest-issue \
        pytest-module \
        tests \
        version

MODULE=ioavstats

SPHINX_BUILDDIR=docs${PATH_SEP}build
SPHINX_SOURCEDIR=docs${PATH_SEP}source

ifeq (${OS},Windows_NT)
    COPY_MYPY_STUBGEN=xcopy /y out\\${MODULE}\\*.* .\\${MODULE}\\
    DELETE_MYPY_STUBGEN=if exist out rd /s /q out
    PATH_SEP=\\
    PIP=pip
    PYTHON=python
    DELETE_SPHINX=del /f /q ${SPHINX_BUILDDIR}\\*
    REMOVE_DOCKER_CONTAINER=@docker ps -a | findstr /r /c:"${MODULE}" && docker rm --force ${MODULE}         || echo "No existing container to remove."
    REMOVE_DOCKER_IMAGE=@docker image ls  | findstr /r /c:"${MODULE}" && docker rmi --force ${MODULE}:latest || echo "No existing image to remove."
else
	OS:=$(shell uname -s)
    COPY_MYPY_STUBGEN=cp -f out/${MODULE}/* ./${MODULE}/
    DELETE_MYPY_STUBGEN=rm -rf out
    PATH_SEP=/
    PIP=pip3
    PYTHON=python3
    DELETE_SPHINX=rm -rf ${SPHINX_BUILDDIR}/*
    REMOVE_DOCKER_CONTAINER=@sh -c 'docker ps -a | grep -q "${MODULE}" && docker rm --force ${MODULE} || echo "No existing container to remove."'
    REMOVE_DOCKER_IMAGE=@sh -c 'docker image ls | grep -q "${MODULE}" && docker rmi --force ${MODULE}:latest || echo "No existing image to remove."'
endif

PYTHONPATH=${MODULE} docs scripts tests

export ENV_FOR_DYNACONF=test
export LANG=en_US.UTF-8

# =============================================================================
# Helper Functions
# =============================================================================

define CHECK_TOOL
	@command -v $(1) >/dev/null 2>&1 || { echo >&2 "$(1) is required but not installed. Aborting."; exit 1; }
endef

# =============================================================================
# Makefile Targets
# =============================================================================

## Show this help.
help:
	@echo "========================================================================"
	@echo "Recommended Makefile Targets:"
	@echo "------------------------------------------------------------------------"
	@awk 'BEGIN { ESC = sprintf("%c", 27); } /^[a-zA-Z0-9_-]+:.*?## .*$$/ { \
		target = $$1; \
		gsub(/:/, "", target); \
		desc = substr($$0, index($$0, "## ") + 3); \
		# Assign color based on target, default to cyan \
		if (target == "dev" || target == "docs" || target == "everything" || target == "final" || target == "format" || target == "lint" || target == "pre-push" || target == "tests") { \
			color = ESC "[31m"; # Red \
		} else { \
			color = ESC "[36m"; # Cyan \
		} \
		printf "  %s%-25s%s %s\n", color, target, ESC "[0m", desc; \
	}' $(MAKEFILE_LIST)

## Ensure all required tools are installed.
#check-tools:
#	$(call CHECK_TOOL,bandit)
#	$(call CHECK_TOOL,coveralls)
#	$(call CHECK_TOOL,docformatter)
#	$(call CHECK_TOOL,mypy)
#	$(call CHECK_TOOL,pylint)
#	$(call CHECK_TOOL,pytest)
#	$(call CHECK_TOOL,ruff)
#	$(call CHECK_TOOL,sphinx-apidoc)
#	$(call CHECK_TOOL,sphinx-build)
#	$(call CHECK_TOOL,stubgen)
#	$(call CHECK_TOOL,vulture)

## Clean build artifacts and temporary files.
clean:
	@echo "Info **********  Start: Clean ***************************************"
	rm -rf docs/build
	rm -rf *.pyc __pycache__
	rm -rf dist
	rm -rf app-*
	@echo "Info **********  End:   Clean ***************************************"

# =============================================================================
# Tool Targets
# =============================================================================

action: ## action: Run the GitHub Actions locally.
action: action-std

## Run the GitHub Actions locally: standard.
action-std:
	@echo "Info **********  Start: action ***************************************"
	@echo "Copy your .aws/credentials to .aws_secrets"
	@echo "----------------------------------------------------------------------"
	bin/act.exe --version
	@echo "----------------------------------------------------------------------"
	bin/act --quiet \
			--secret-file config/.act_secrets \
			--var IO_LOCAL='true' \
			-P ubuntu-latest=catthehacker/ubuntu:act-latest \
			-W .github/workflows/github_pages.yml
	bin/act --quiet \
			--secret-file config/.act_secrets \
			--var IO_LOCAL='true' \
			-P ubuntu-latest=catthehacker/ubuntu:act-latest \
			-W .github/workflows/standard.yml
	@echo "Info **********  End:   action ***************************************"

## Find common security issues with Bandit.
bandit:
	@echo "Info **********  Start: Bandit ***************************************"
	bandit --version
	@echo "----------------------------------------------------------------------"
	bandit -c pyproject.toml -r ${PYTHONPATH} --severity-level high --severity-level medium
	@echo "Info **********  End:   Bandit ***************************************"

## Byte-compile the Python libraries.
compileall:
	@echo "Info **********  Start: Compile All Python Scripts *******************"
	${PYTHON} --version
	@echo "----------------------------------------------------------------------"
	${PYTHON} -m compileall ${PYTHONPATH}
	@echo "Info **********  End:   Compile All Python Scripts *******************"

conda-dev: ## Create a new environment for development.
	@echo "Info **********  Start: Miniconda create development environment *****"
	conda --version
	@echo "----------------------------------------------------------------------"
	conda config --set always_yes true
	conda config --set channel_priority flexible
	conda env create -f config/environment_dev.yml || conda env update --prune -f config/environment_dev.yml
	@echo "----------------------------------------------------------------------"
	conda info --envs
	conda list
	@echo "Info **********  End:   Miniconda create development environment *****"

conda-prod: ## Create a new environment for production.
	@echo "Info **********  Start: Miniconda create production environment ******"
	conda --version
	@echo "----------------------------------------------------------------------"
	conda config --set always_yes true
	conda config --set channel_priority flexible
	conda env create -f config/environment.yml || conda env update --prune -f config/environment.yml
	@echo "----------------------------------------------------------------------"
	conda info --envs
	conda list
	@echo "Info **********  End:   Miniconda create production environment ******"

## Run all the tests and upload the coverage data to coveralls.
coveralls:
	@echo "Info **********  Start: coveralls ************************************"
	pytest --cov=${MODULE} --cov-report=xml --random-order tests
	@echo "----------------------------------------------------------------------"
	coveralls --service=github
	@echo "Info **********  End:   coveralls ************************************"

dev: ## dev: Format, lint and test the code.
#dev: check-tools format lint tests
dev: format lint tests

## Format the docstrings with docformatter.
docformatter:
	@echo "Info **********  Start: docformatter *********************************"
	docformatter --version
	@echo "----------------------------------------------------------------------"
	docformatter --in-place --recursive ${PYTHONPATH}
#	docformatter -r ${PYTHONPATH}
	@echo "Info **********  End:   docformatter *********************************"

# Creates Docker executables
# https://github.com/rzane/docker2exe
# Configuration files: .dockerignore & Dockerfile
docker:             ## Create a docker image.
	@echo "Info **********  Start: Docker ***************************************"
	docker --version
	@echo "----------------------------------------------------------------------"
	docker ps -a
	@echo "----------------------------------------------------------------------"
	${REMOVE_DOCKER_CONTAINER}
	${REMOVE_DOCKER_IMAGE}
	docker system prune -a -f
	docker build --build-arg PYPI_PAT=${PYPI_PAT} -t ${MODULE} .
	@echo "Info **********  End:   Docker ***************************************"

docs: ## docs: Create the user documentation.
docs: sphinx

everything: ## everything: Do everything pre-checkin
#everything: check-tools dev docs
everything: dev docs

final: ## final: Format, lint and test the code and create the documentation.
#final: check-tools format lint docs tests
final: format lint docs tests

format: ## format: Format the code with docformatter.
format: docformatter

lint: ## lint: Lint the code with ruff, Bandit, Vulture, Pylint and Mypy.
lint: ruff bandit vulture pylint mypy

## Find typing issues with Mypy.
mypy:
	@echo "Info **********  Start: Mypy *****************************************"
	mypy --version
	@echo "----------------------------------------------------------------------"
	mypy --ignore-missing-imports ${PYTHONPATH}
	@echo "Info **********  End:   Mypy *****************************************"

mypy-stubgen: ## Autogenerate stub files.
	@echo "Info **********  Start: Mypy Stubgen **********************************"
	${DELETE_MYPY_STUBGEN}
	stubgen --package ${MODULE}
	${COPY_MYPY_STUBGEN}
	${DELETE_MYPY_STUBGEN}
	@echo "Info **********  End:   Mypy Stubgen **********************************"

## Increment the version number.
next-version:
	@echo "Info **********  Start: next_version *********************************"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	${PYTHON} --version
	@echo "----------------------------------------------------------------------"
	${PYTHON} scripts/next_version.py
	@echo "Info **********  End:   next version *********************************"

pre-push: ## pre-push: Preparatory work for the pushing process.
#pre-push: check-tools format lint tests next-version docs
pre-push: format lint tests next-version docs

## Lint the code with Pylint.
pylint:
	@echo "Info **********  Start: Pylint ***************************************"
	pylint --version
	@echo "----------------------------------------------------------------------"
	pylint --rcfile=config/.pylintrc ${PYTHONPATH}
	@echo "Info **********  End:   Pylint ***************************************"

## Run all tests with pytest.
pytest:
	@echo "Info **********  Start: pytest ***************************************"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --dead-fixtures tests
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered --cov-report=lcov -v tests
	@echo "Info **********  End:   pytest ***************************************"

pytest-ci: ## Run all tests after test tool installation.
	@echo "Info **********  Start: pytest-ci *************************************"
	pip3 install openpyxl
	pip3 install pytest pytest-benchmark pytest-cov pytest-deadfixtures pytest-helpers-namespace pytest-random-order
	pip3 install requests
	@echo "----------------------------------------------------------------------"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --dead-fixtures tests
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -v tests
	@echo "Info **********  End:   pytest-ci *************************************"

pytest-first-issue: ## Run all tests until the first issue occurs.
	@echo "Info **********  Start: pytest-first-issue ****************************"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -rP -v -x tests
	@echo "Info **********  End:   pytest-first-issue ****************************"

pytest-ignore-mark: ## Run all tests without marker.
	@echo "Info **********  Start: pytest-ignore-mark ***************************"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --dead-fixtures -m "not no_ci" tests
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered --cov-report=lcov -m "not no_ci" -v tests
	@echo "Info **********  End:   pytest-ignore-mark ***************************"

pytest-issue: ## Run only the tests which are marked with 'issue'.
	@echo "Info **********  Start: pytest-issue *********************************"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --dead-fixtures tests
	pytest --cache-clear --capture=no --cov=${MODULE} --cov-report term-missing:skip-covered -m issue -rP -v -x tests
	@echo "Info **********  End:   pytest-issue *********************************"

pytest-module: ## Run the tests of a specific module.
	@echo "Info **********  Start: pytest-module ********************************"
	@echo "TESTMODULE=tests/${TEST-MODULE}.py"
	@echo "----------------------------------------------------------------------"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -v tests/${TEST-MODULE}.py
	@echo "Info **********  End:   pytest-module ********************************"

## An extremely fast Python linter and code formatter.
ruff:
	@echo "Info **********  Start: ruff *****************************************"
	ruff --version
	@echo "----------------------------------------------------------------------"
	ruff check --fix ${PYTHONPATH}
	@echo "Info **********  End:   ruff *****************************************"

## Create the user documentation with Sphinx.
sphinx:
	@echo "Info **********  Start: sphinx ***************************************"
	sphinx-apidoc --version
	sphinx-build --version
	@echo "----------------------------------------------------------------------"
	${DELETE_SPHINX}
	sphinx-apidoc -o ${SPHINX_SOURCEDIR} ${MODULE}
	sphinx-build -M html ${SPHINX_SOURCEDIR} ${SPHINX_BUILDDIR}
	sphinx-build -b rinoh ${SPHINX_SOURCEDIR} ${SPHINX_BUILDDIR}/pdf
	@echo "Info **********  End:   sphinx ***************************************"

tests: ## tests: Run all tests.
tests: pytest

version: ## Show the installed software versions.
	@echo "Info **********  Start: version **************************************"
	@echo "PIP   =${PIP}"
	@echo "PYTHON=${PYTHON}"
	@echo "----------------------------------------------------------------------"
	${PIP} --version
	@echo "Info **********  End:   version **************************************"

## Find dead Python code.
vulture:
	@echo "Info **********  Start: vulture **************************************"
	vulture --version
	@echo "----------------------------------------------------------------------"
	vulture ${PYTHONPATH}
	@echo "Info **********  End:   vulture **************************************"

## =============================================================================
