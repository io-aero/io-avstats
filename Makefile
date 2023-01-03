.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
	export ENV_FOR_DYNACONF=test
	export PIPENV=python -m pipenv
	export PYTHON=python
	export PYTHONPATH=src\\streamlit_apps
	export PYTHONPATH_DEV=src\\streamlit_apps
	export PYTHONPATH_MYPY=src\\streamlit_apps
	export PYTHONPATH_PYTEST=src
else
	export ENV_FOR_DYNACONF=test
	export PIPENV=python3 -m pipenv
	export PYTHON=python3
	export PYTHONPATH=src/streamlit_apps
	export PYTHONPATH_DEV=src/streamlit_apps
	export PYTHONPATH_MYPY=src/streamlit_apps
	export PYTHONPATH_PYTEST=src
endif

##                                                                            .
## =============================================================================
## IO-AVSTATS - Aviation Accident Statistics - make Documentation.
##                -------------------------------------------------------------
##                The purpose of this Makefile is to support the whole software
##                development process for io-avstats. It contains also the
##                necessary tools for the CI activities.
##                -------------------------------------------------------------
##                The available make commands are:
## ------------------------------------------------------------------------------
## help:               Show this help.
## -----------------------------------------------------------------------------
## dev:                Format, lint and test the code.
dev: format lint tests
## docs:               Check the API documentation, create and upload the user documentation.
docs: pydocstyle mkdocs
## final:              Format, lint and test the code and the documentation.
final: format lint docs tests
## format:             Format the code with isort, Black and docformatter.
format: isort black docformatter
## lint:               Lint the code with Bandit, Flake8, Pylint and Mypy.
lint: bandit flake8 pylint mypy
## tests:              Run all tests with pytest.
tests: pytest
## -----------------------------------------------------------------------------

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo Info **********  Start: Bandit ***************************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH_DEV}
	${PIPENV} run bandit --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run bandit -c pyproject.toml -r ${PYTHONPATH_DEV}
	@echo Info **********  End:   Bandit ***************************************

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:              ## Format the code with Black.
	@echo Info **********  Start: black ****************************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH_DEV}
	${PIPENV} run black --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run black ${PYTHONPATH_DEV} tests
	@echo Info **********  End:   black ****************************************

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:         ## Byte-compile the Python libraries.
	@echo Info **********  Start: Compile All Python Scripts ******************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PYTHON} --version
	@echo ---------------------------------------------------------------------
	${PYTHON} -m compileall
	@echo Info **********  End:   Compile All Python Scripts ******************

# Python interface to coveralls.io API
# https://github.com/TheKevJames/coveralls-python
# Configuration file: none
coveralls:          ## Run all the tests and upload the coverage data to coveralls.
	@echo Info **********  Start: coveralls ***********************************
	${PIPENV} run pytest --cov=${PYTHONPATH_PYTEST} --cov-report=xml tests
	@echo ----------------------------------------------------------------------
	${PIPENV} run coveralls --service=github
	@echo Info **********  End:   coveralls ***********************************

# Formats docstrings to follow PEP 257
# https://github.com/PyCQA/docformatter
# Configuration file: none
docformatter:       ## Format the docstrings with docformatter.
	@echo Info **********  Start: docformatter ********************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PIPENV} run docformatter --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run docformatter --in-place -r ${PYTHONPATH} tests
	@echo Info **********  End:   docformatter ********************************

# Flake8: Your Tool For Style Guide Enforcement.
# https://github.com/pycqa/flake8
# Configuration file: cfg.cfg
flake8:             ## Enforce the Python Style Guides with Flake8.
	@echo Info **********  Start: Flake8 **************************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PIPENV} run flake8 --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run flake8 ${PYTHONPATH} tests
	@echo Info **********  End:   Flake8 **************************************

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort:              ## Edit and sort the imports with isort.
	@echo Info **********  Start: isort ***************************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH_DEV}
	${PIPENV} run isort --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run isort ${PYTHONPATH_DEV} tests
	@echo Info **********  End:   isort ***************************************

# Project documentation with Markdown.
# https://github.com/mkdocs/mkdocs/
# Configuration file: none
mkdocs:             ## Create and upload the user documentation with MkDocs.
	@echo Info **********  Start: MkDocs **************************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PIPENV} run mkdocs --version
	@echo ---------------------------------------------------------------------
	${PIPENV} run mkdocs build
	@echo Info **********  End:   MkDocs **************************************

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:               ## Find typing issues with Mypy.
	@echo Info **********  Start: Mypy ****************************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH_MYPY}
	${PIPENV} run mypy --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run mypy ${PYTHONPATH_MYPY}
	@echo Info **********  End:   Mypy ****************************************

# pip is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
pipenv-dev:         ## Install the package dependencies for development.
	@echo Info **********  Start: Installation of Development Packages ********
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade pipenv
	${PYTHON} -m pip uninstall -y virtualenv
	${PYTHON} -m pip install virtualenv
	${PIPENV} install
	${PIPENV} --rm
	${PIPENV} install --dev
	${PIPENV} update --dev
	@echo ----------------------------------------------------------------------
	${PIPENV} run pip freeze
	@echo ----------------------------------------------------------------------
	${PYTHON} --version
	${PYTHON} -m pip --version
	${PYTHON} -m pipenv --version
	@echo Info **********  End:   Installation of Development Packages ********
pipenv-prod:        ## Install the package dependencies for production.
	@echo Info **********  Start: Installation of Production Packages *********
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade pipenv
	${PYTHON} -m pip uninstall -y virtualenv
	${PYTHON} -m pip install virtualenv
	${PIPENV} install
	${PIPENV} --rm
	${PIPENV} install
	${PIPENV} update
	@echo ----------------------------------------------------------------------
	${PIPENV} run pip freeze
	@echo ----------------------------------------------------------------------
	${PYTHON} --version
	${PYTHON} -m pip --version
	${PYTHON} -m pipenv --version
	@echo Info **********  End:   Installation of Production Packages *********

# pydocstyle - docstring style checker.
# https://github.com/PyCQA/pydocstyle
# Configuration file: pyproject.toml
pydocstyle:         ## Check the API documentation with pydocstyle.
	@echo Info **********  Start: pydocstyle **********************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PIPENV} run pydocstyle --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run pydocstyle --count --match='(?!PDFLIB\\)*\.py' ${PYTHONPATH} tests
	@echo Info **********  End:   pydocstyle **********************************

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: .pylintrc
pylint:             ## Lint the code with Pylint.
	@echo Info **********  Start: Pylint **************************************
	@echo PYTHON    =${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PIPENV} run pylint --version
	@echo ----------------------------------------------------------------------
#   ${PIPENV} run pylint ${PYTHONPATH} tests
	${PIPENV} run pylint ${PYTHONPATH}
	@echo Info **********  End:   Pylint **************************************

# pytest: helps you write better programs.
# https://github.com/pytest-dev/pytest/
# Configuration file: pyproject.toml
pytest:             ## Run all tests with pytest.
	@echo Info **********  Start: pytest **************************************
	${PIPENV} run pytest --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run pytest --dead-fixtures tests
	${PIPENV} run pytest --cache-clear --cov=${PYTHONPATH_PYTEST} --cov-report term-missing:skip-covered -v tests
	@echo Info **********  End:   pytest **************************************
pytest-ci:          ## Run all tests with pytest after test tool installation.
	@echo Info **********  Start: pytest **************************************
	${PIPENV} install pytest
	${PIPENV} install pytest-cov
	${PIPENV} install pytest-deadfixtures
	${PIPENV} install pytest-helpers-namespace
	${PIPENV} install pytest-random-order
	@echo ----------------------------------------------------------------------
	${PIPENV} run pytest --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run pytest --dead-fixtures tests
	${PIPENV} run pytest --cache-clear --cov=${PYTHONPATH_PYTEST} --cov-report term-missing:skip-covered -v tests
	@echo Info **********  End:   pytest **************************************
pytest-first-issue: ## Run all tests with pytest until the first issue occurs.
	@echo Info **********  Start: pytest **************************************
	${PIPENV} run pytest --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run pytest --cache-clear --cov=${PYTHONPATH_PYTEST} --cov-report term-missing:skip-covered -rP -v -x tests
	@echo Info **********  End:   pytest **************************************
pytest-issue:       ## Run only the tests with pytest which are marked with 'issue'.
	@echo Info **********  Start: pytest **************************************
	${PIPENV} run pytest --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run pytest --cache-clear --capture=no --cov=${PYTHONPATH_PYTEST} --cov-report term-missing:skip-covered -m issue -rP -v -x tests
	@echo Info **********  End:   pytest **************************************
pytest-module:      ## Run tests of specific module(s) with pytest - test_all & test_cfg_cls_setup & test_db_cls.
	@echo Info **********  Start: pytest **************************************
	${PIPENV} run pytest --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run pytest --cache-clear --cov=${PYTHONPATH_PYTEST} --cov-report term-missing:skip-covered -v tests/test_db_cls_action.py
	@echo Info **********  End:   pytest **************************************

version:            ## Show the installed software versions.
	@echo Info **********  Start: version *************************************
	@echo PYTHON=${PYTHON}
	@echo PYTHONPATH=${PYTHONPATH}
	${PYTHON} -m pip --version
	${PYTHON} -m pipenv --version
	@echo Info **********  End:   version *************************************

## ============================================================================
