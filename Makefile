.DEFAULT_GOAL := help

MODULE=ioavstats

ifeq ($(OS),Windows_NT)
	COPY_MYPY_STUBGEN=xcopy /y out\\$(MODULE)\\*.* .\\$(MODULE)\\
	DELETE_MYPY_STUBGEN=if exist out rd /s /q out
	PIP=pip
	PYTHON=py
	SPHINX_BUILDDIR=docs\\build
	SPHINX_SOURCEDIR=docs\\source
	DELETE_SPHINX=del /f /q $(SPHINX_BUILDDIR)\\*
else
	COPY_MYPY_STUBGEN=cp -f out/$(MODULE)/* ./$(MODULE)/
	DELETE_MYPY_STUBGEN=rm -rf out
	PIP=pip3
	PYTHON=python3
	SPHINX_BUILDDIR=docs/build
	SPHINX_SOURCEDIR=docs/source
	DELETE_SPHINX=rm -rf $(SPHINX_BUILDDIR)/*
endif

COVERALLS_REPO_TOKEN=<see coveralls.io>
PYTHONPATH=${MODULE} docs scripts tests
VERSION_PYTHON=3.11

export ENV_FOR_DYNACONF=test
export LANG=en_US.UTF-8

##                                                                            .
## =============================================================================
## make Script       The purpose of this Makefile is to support the whole
##                   software development process for an application. It
##                   contains also the necessary tools for the CI activities.
##                   -----------------------------------------------------------
##                   The available make commands are:
## -----------------------------------------------------------------------------
## help:               Show this help.
## -----------------------------------------------------------------------------
## action:             Run the GitHub Actions locally.
action: action-std
## dev:                Format, lint and test the code.
dev: format lint tests
## docs:               Check the API documentation, create and upload the user documentation.
docs: sphinx
## everything:         Do everything precheckin
everything: dev docs
## final:              Format, lint and test the code and create the documentation.
final: format lint docs tests
## format:             Format the code with Black and docformatter.
format: black docformatter
## lint:               Lint the code with ruff, Bandit, vulture, Pylint and Mypy.
lint: ruff bandit vulture pylint mypy
## tests:              Run all tests with pytest.
tests: pytest
## -----------------------------------------------------------------------------

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

# Run the GitHub Actions locally.
# https://github.com/nektos/act
# Configuration files: .act_secrets & .act_vars
action-std:         ## Run the GitHub Actions locally: standard.
	@echo Info **********  Start: action ***************************************
	@echo Copy your .aws/creedentials to .aws_secrets
	@echo ----------------------------------------------------------------------
	act --version
	@echo ----------------------------------------------------------------------
	act --quiet --secret-file .act_secrets --var IO_LOCAL='true' --verbose -P ubuntu-latest=catthehacker/ubuntu:act-latest -W .github/workflows/standard.yml
	@echo Info **********  End:   action ***************************************

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo Info **********  Start: Bandit ***************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	bandit --version
	@echo ----------------------------------------------------------------------
	bandit -c pyproject.toml -r ${PYTHONPATH}
	@echo Info **********  End:   Bandit ***************************************

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:              ## Format the code with Black.
	@echo Info **********  Start: black ****************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	black --version
	@echo ----------------------------------------------------------------------
	black ${PYTHONPATH}
	@echo Info **********  End:   black ****************************************

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:         ## Byte-compile the Python libraries.
	@echo Info **********  Start: Compile All Python Scripts *******************
	@echo PYTHON=${PYTHON}
	@echo ----------------------------------------------------------------------
	${PYTHON} --version
	@echo ----------------------------------------------------------------------
	${PYTHON} -m compileall
	@echo Info **********  End:   Compile All Python Scripts *******************

# Miniconda - Minimal installer for conda.
# https://docs.conda.io/en/latest/miniconda.html
# Configuration file: none
conda-dev:          ## Create a new environment for development.
	@echo Info **********  Start: Miniconda create development environment *****
	conda config --set always_yes true
	conda --version
	echo PYPI_PAT=${PYPI_PAT}
	@echo ----------------------------------------------------------------------
	conda env remove -n ${MODULE}
	conda env create -f environment_dev.yml
	@echo ----------------------------------------------------------------------
	conda info --envs
	conda list
	@echo Info **********  End:   Miniconda create development environment *****
conda-prod:         ## Create a new environment for production.
	@echo Info **********  Start: Miniconda create production environment ******
	conda config --set always_yes true
	conda --version
	@echo ----------------------------------------------------------------------
	conda env remove -n ${MODULE}
	conda env create -f environment.yml
	@echo ----------------------------------------------------------------------
	conda info --envs
	conda list
	@echo Info **********  End:   Miniconda create production environment ******

# Requires a public repository !!!
# Python interface to coveralls.io API
# https://github.com/TheKevJames/coveralls-python
# Configuration file: none
coveralls:          ## Run all the tests and upload the coverage data to coveralls.
	@echo Info **********  Start: coveralls ***********************************
	pytest --cov=${MODULE} --cov-report=xml --random-order tests
	@echo ---------------------------------------------------------------------
	coveralls --service=github
	@echo Info **********  End:   coveralls ***********************************

# Formats docstrings to follow PEP 257
# https://github.com/PyCQA/docformatter
# Configuration file: pyproject.toml
docformatter:       ## Format the docstrings with docformatter.
	@echo Info **********  Start: docformatter *********************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	docformatter --version
	@echo ----------------------------------------------------------------------
	docformatter --in-place -r ${PYTHONPATH}
	docformatter --in-place -r tests
#	docformatter -r ${PYTHONPATH}
#	docformatter -r tests
	@echo Info **********  End:   docformatter *********************************

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:               ## Find typing issues with Mypy.
	@echo Info **********  Start: Mypy *****************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	mypy --version
	@echo ----------------------------------------------------------------------
	mypy ${PYTHONPATH}
	@echo Info **********  End:   Mypy *****************************************

mypy-stubgen:       ## Autogenerate stub files.
	@echo Info **********  Start: Mypy *****************************************
	@echo COPY_MYPY_STUBGEN  =${COPY_MYPY_STUBGEN}
	@echo DELETE_MYPY_STUBGEN=${DELETE_MYPY_STUBGEN}
	@echo MODULE             =${MODULE}
	@echo ----------------------------------------------------------------------
	${DELETE_MYPY_STUBGEN}
	stubgen --package ${MODULE}
	${COPY_MYPY_STUBGEN}
	${DELETE_MYPY_STUBGEN}
	@echo Info **********  End:   Mypy *****************************************

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: .pylintrc
pylint:             ## Lint the code with Pylint.
	@echo Info **********  Start: Pylint ***************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pylint --version
	@echo ----------------------------------------------------------------------
	pylint ${PYTHONPATH}
	@echo Info **********  End:   Pylint ***************************************

# pytest: helps you write better programs.
# https://github.com/pytest-dev/pytest/
# Configuration file: pyproject.toml
pytest:             ## Run all tests with pytest.
	@echo Info **********  Start: pytest ***************************************
	@echo CONDA     =$(CONDA_PREFIX)
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pytest --version
	@echo ----------------------------------------------------------------------
	pytest --dead-fixtures tests
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered --cov-report=lcov -v tests
	@echo Info **********  End:   pytest ***************************************
pytest-ci:          ## Run all tests with pytest after test tool installation.
	@echo Info **********  Start: pytest ***************************************
	@echo CONDA     =$(CONDA_PREFIX)
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pip install pytest pytest-cov pytest-deadfixtures pytest-helpers-namespace pytest-random-order
	@echo ----------------------------------------------------------------------
	pytest --version
	@echo ----------------------------------------------------------------------
	pytest --dead-fixtures tests
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -v tests
	@echo Info **********  End:   pytest ***************************************
pytest-first-issue: ## Run all tests with pytest until the first issue occurs.
	@echo Info **********  Start: pytest ***************************************
	@echo CONDA     =$(CONDA_PREFIX)
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pytest --version
	@echo ----------------------------------------------------------------------
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -rP -v -x tests
	@echo Info **********  End:   pytest ***************************************
pytest-issue:       ## Run only the tests with pytest which are marked with 'issue'.
	@echo Info **********  Start: pytest ***************************************
	@echo CONDA     =$(CONDA_PREFIX)
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pytest --version
	@echo ----------------------------------------------------------------------
	pytest --dead-fixtures tests
	pytest --cache-clear --capture=no --cov=${MODULE} --cov-report term-missing:skip-covered -m issue -rP -v -x tests
	@echo Info **********  End:   pytest ***************************************
pytest-module:      ## Run test of a specific module with pytest.
	@echo Info **********  Start: pytest ***************************************
	@echo CONDA     =$(CONDA_PREFIX)
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo TESTMODULE=tests/$(TEST-MODULE).py
	@echo ----------------------------------------------------------------------
	pytest --version
	@echo ----------------------------------------------------------------------
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -v tests/$(TEST-MODULE).py
	@echo Info **********  End:   pytest ***************************************

# https://github.com/astral-sh/ruff
# Configuration file: pyproject.toml
ruff:               ## An extremely fast Python linter and code formatter.
	@echo Info **********  Start: ruff *****************************************
	ruff --version
	@echo ----------------------------------------------------------------------
	ruff check --fix
	@echo Info **********  End:   ruff *****************************************

sphinx:             ##  Create the user documentation with Sphinx.
	@echo Info **********  Start: sphinx ***************************************
	@echo DELETE_SPHINX   =${DELETE_SPHINX}
	@echo PIP             =${PIP}
	@echo SPHINX_BUILDDIR =${SPHINX_BUILDDIR}
	@echo SPHINX_SOURCEDIR=${SPHINX_SOURCEDIR}
	@echo ----------------------------------------------------------------------
	pip install --no-deps -e .
	@echo ----------------------------------------------------------------------
	${DELETE_SPHINX}
	sphinx-apidoc -o ${SPHINX_SOURCEDIR} ${MODULE}
	sphinx-build -M html ${SPHINX_SOURCEDIR} ${SPHINX_BUILDDIR}
	sphinx-build -b rinoh ${SPHINX_SOURCEDIR} ${SPHINX_BUILDDIR}/pdf
	@echo Info **********  End:   sphinx ***************************************

version:            ## Show the installed software versions.
	@echo Info **********  Start: version **************************************
	@echo PIP   =${PIP}
	@echo PYTHON=${PYTHON}
	@echo ----------------------------------------------------------------------
	$(PIP) --version
	@echo Info **********  End:   version **************************************

# Find dead Python code
# https://github.com/jendrikseipp/vulture
# Configuration file: pyproject.toml
vulture:            ##  Find dead Python code.
	@echo Info **********  Start: vulture **************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	vulture --version
	@echo ----------------------------------------------------------------------
	vulture ${PYTHONPATH}
	@echo Info **********  End:   vulture **************************************

## =============================================================================
