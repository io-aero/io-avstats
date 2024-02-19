.DEFAULT_GOAL := help

MODULE=ioavstats

ifeq ($(OS),Windows_NT)
	COPY_MYPY_STUBGEN=xcopy /y out\\$(MODULE)\\*.* .\\$(MODULE)\\
	DELETE_BUILD=if exist build rd /s /q build
	DELETE_MYPY_STUBGEN=if exist out rd /s /q out
	DELETE_PIPFILE_LOCK=del /f /q Pipfile.lock
	PIP=pip
	PYTHON=py
	SHELL=cmd
	SPHINX_BUILDDIR=docs\\build
	SPHINX_SOURCEDIR=docs\\source
	DELETE_SPHINX=del /f /q $(SPHINX_BUILDDIR)\\*
else
	COPY_MYPY_STUBGEN=cp -f out/$(MODULE)/* ./$(MODULE)/
	DELETE_BUILD=rm -rf build
	DELETE_MYPY_STUBGEN=rm -rf out
	DELETE_PIPFILE_LOCK=rm -rf Pipfile.lock
	PIP=pip3
	PYTHON=python3
	SHELL=/bin/bash
	SPHINX_BUILDDIR=docs/build
	SPHINX_SOURCEDIR=docs/source
	DELETE_SPHINX=rm -rf $(SPHINX_BUILDDIR)/*
endif

# ToDo: If Conda needed.
CONDA_PACKAGES=gdal pdal python-pdal rasterio
CONDA_ARG=--site-packages
CONDA_ARG=
COVERALLS_REPO_TOKEN=<see coveralls.io>
PYTHONPATH=${MODULE} scripts
#VERSION_PIPENV=v2023.7.23
VERSION_PYTHON=3.10

export ENV_FOR_DYNACONF=test
export LANG=en_US.UTF-8

##                                                                            .
## =============================================================================
## IO-AVSTATS - Aviation Event Statistics - make Documentation.
##              ----------------------------------------------------------------
##              The purpose of this Makefile is to support the whole software
##              development process for io-avstats. It contains also the
##              necessary tools for the CI activities.
##              ----------------------------------------------------------------
##                The available make commands are:
## -----------------------------------------------------------------------------
## help:               Show this help.
## -----------------------------------------------------------------------------
## action:             Run the GitHub Actions locally.
action: action-std
## conda-dev:          Install the package dependencies for development incl.
##                     Conda & pipenv.
conda-dev: conda pipenv-dev-int
## conda-prod:         Install the package dependencies for production incl.
##                     Conda & pipenv.
conda-prod: conda pipenv-prod-int
## dev:                Format, lint and test the code.
dev: format lint tests
## docs:               Check the API documentation, create and upload the user documentation.
docs: pydocstyle sphinx
## everything:         Do everything precheckin
everything: dev docs
## final:              Format, lint and test the code and create the documentation.
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

# Run the GitHub Actions locally.
# https://github.com/nektos/act
# Configuration files: .act_secrets & .act_vars
action-std:         ## Run the GitHub Actions locally: standard.
	@echo Info **********  Start: action ***************************************
	@echo Copy your .aws/creedentials to .aws_secrets
	@echo ----------------------------------------------------------------------
	act --version
	@echo ----------------------------------------------------------------------
	act  --quiet --secret-file .act_secrets --var IO_LOCAL='true' --verbose
	@echo Info **********  End:   action ***************************************

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo Info **********  Start: Bandit ***************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run bandit --version
	@echo ----------------------------------------------------------------------
	pipenv run bandit -c pyproject.toml -r ${PYTHONPATH}
	@echo Info **********  End:   Bandit ***************************************

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:              ## Format the code with Black.
	@echo Info **********  Start: black ****************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run black --version
	@echo ----------------------------------------------------------------------
	pipenv run black ${PYTHONPATH} tests
	@echo Info **********  End:   black ****************************************

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:         ## Byte-compile the Python libraries.
	@echo Info **********  Start: Compile All Python Scripts *******************
	@echo PYTHON=${PYTHON}
	@echo ----------------------------------------------------------------------
	pipenv run python --version
	@echo ----------------------------------------------------------------------
	pipenv run python -m compileall
	@echo Info **********  End:   Compile All Python Scripts *******************

# Miniconda - Minimal installer for conda.
# https://docs.conda.io/en/latest/miniconda.html
# Configuration file: none
conda:              ## Create a new environment.
	@echo Info **********  Start: Miniconda create environment *****************
	conda config --set always_yes true
	conda update conda
	conda --version
	@echo ----------------------------------------------------------------------
	conda install -c conda-forge ${CONDA_PACKAGES}
	@echo ----------------------------------------------------------------------
	conda list
	conda info --envs
	@echo Info **********  End:   Miniconda create environment *****************

# Requires a public repository !!!
# Python interface to coveralls.io API
# https://github.com/TheKevJames/coveralls-python
# Configuration file: none
coveralls:          ## Run all the tests and upload the coverage data to coveralls.
	@echo Info **********  Start: coveralls ***********************************
	pipenv run pytest --cov=${MODULE} --cov-report=xml --random-order tests
	@echo ---------------------------------------------------------------------
	pipenv run coveralls --service=github
	@echo Info **********  End:   coveralls ***********************************

# Formats docstrings to follow PEP 257
# https://github.com/PyCQA/docformatter
# Configuration file: pyproject.toml
docformatter:       ## Format the docstrings with docformatter.
	@echo Info **********  Start: docformatter *********************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run docformatter --version
	@echo ----------------------------------------------------------------------
	pipenv run docformatter --in-place -r ${PYTHONPATH}
	pipenv run docformatter --in-place -r tests
#	pipenv run docformatter -r ${PYTHONPATH}
#	pipenv run docformatter -r tests
	@echo Info **********  End:   docformatter *********************************

# Flake8: Your Tool For Style Guide Enforcement.
# https://github.com/pycqa/flake8
# Configuration file: cfg.cfg
flake8:             ## Enforce the Python Style Guides with Flake8.
	@echo Info **********  Start: Flake8 ***************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run flake8 --version
	@echo ----------------------------------------------------------------------
	pipenv run flake8 ${PYTHONPATH} tests
	@echo Info **********  End:   Flake8 ***************************************

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort:              ## Edit and sort the imports with isort.
	@echo Info **********  Start: isort ****************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run isort --version
	@echo ----------------------------------------------------------------------
	pipenv run isort ${PYTHONPATH} tests
	@echo Info **********  End:   isort ****************************************

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:               ## Find typing issues with Mypy.
	@echo Info **********  Start: Mypy *****************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run mypy --version
	@echo ----------------------------------------------------------------------
	pipenv run mypy ${PYTHONPATH}
	@echo Info **********  End:   Mypy *****************************************

mypy-stubgen:       ## Autogenerate stub files
	@echo Info **********  Start: Mypy *****************************************
	@echo COPY_MYPY_STUBGEN  =${COPY_MYPY_STUBGEN}
	@echo DELETE_MYPY_STUBGEN=${DELETE_MYPY_STUBGEN}
	@echo MODULE             =${MODULE}
	@echo ----------------------------------------------------------------------
	${DELETE_MYPY_STUBGEN}
	pipenv run stubgen --package ${MODULE}
	${COPY_MYPY_STUBGEN}
	${DELETE_MYPY_STUBGEN}
	@echo Info **********  End:   Mypy *****************************************

# $(PIP) is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
# ToDo: If Conda needed.
# pipenv-dev-int:     ## Install the package dependencies for development.
pipenv-dev:         ## Install the package dependencies for development.
	@echo Info **********  Start: Installation of Development Packages *********
	@echo DELETE_PIPFILE_LOCK=${DELETE_PIPFILE_LOCK}
	@echo PIP                =${PIP}
	@echo PYTHON             =${PYTHON}
	@echo ----------------------------------------------------------------------
	$(PIP) install --upgrade pip
#	$(PIP) install --upgrade pipenv==${VERSION_PIPENV}
	$(PIP) install --upgrade pipenv
	$(PIP) install --upgrade virtualenv
	${DELETE_BUILD}
	${DELETE_PIPFILE_LOCK}
	@echo ----------------------------------------------------------------------
	aws codeartifact login --tool pip --repository io-aero-pypi --domain io-aero --domain-owner 444046118275 --region us-east-1
	pipenv install ${CONDA_ARG} --dev
	@echo ----------------------------------------------------------------------
	pipenv run pip freeze
	@echo ----------------------------------------------------------------------
	pipenv run python --version
	$(PIP) --version
	pipenv --version
	pipenv run python -m virtualenv --version
	@echo Info **********  End:   Installation of Development Packages *********
# ToDo: If Conda needed.
# pipenv-prod-int:    ## Install the package dependencies for production.
pipenv-prod:        ## Install the package dependencies for production.
	@echo Info **********  Start: Installation of Production Packages **********
	@echo DELETE_PIPFILE_LOCK=${DELETE_PIPFILE_LOCK}
	@echo PIP                =${PIP}
	@echo PYTHON             =${PYTHON}
	@echo ----------------------------------------------------------------------
	$(PIP) install --upgrade pip
#	$(PIP) install --upgrade pipenv==${VERSION_PIPENV}
	$(PIP) install --upgrade pipenv
	$(PIP) install --upgrade virtualenv
	${DELETE_BUILD}
	${DELETE_PIPFILE_LOCK}
	@echo ----------------------------------------------------------------------
	aws codeartifact login --tool pip --repository io-aero-pypi --domain io-aero --domain-owner 444046118275 --region us-east-1
	pipenv install ${CONDA_ARG}
	@echo ----------------------------------------------------------------------
	pipenv run pip freeze
	@echo ----------------------------------------------------------------------
	pipenv run python --version
	$(PIP) --version
	pipenv --version
	pipenv run python -m virtualenv --version
	@echo Info **********  End:   Installation of Production Packages **********

# pydocstyle - docstring style checker.
# https://github.com/PyCQA/pydocstyle
# Configuration file: pyproject.toml
pydocstyle:         ## Check the API documentation with pydocstyle.
	@echo Info **********  Start: pydocstyle ***********************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run pydocstyle --version
	@echo ----------------------------------------------------------------------
	pipenv run pydocstyle --count ${MODULE} scripts
	@echo Info **********  End:   pydocstyle ***********************************

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: .pylintrc
pylint:             ## Lint the code with Pylint.
	@echo Info **********  Start: Pylint ***************************************
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run pylint --version
	@echo ----------------------------------------------------------------------
	pipenv run pylint ${PYTHONPATH} tests
	@echo Info **********  End:   Pylint ***************************************

# pytest: helps you write better programs.
# https://github.com/pytest-dev/pytest/
# Configuration file: pyproject.toml
pytest:             ## Run all tests with pytest.
	@echo Info **********  Start: pytest ***************************************
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run pytest --version
	@echo ----------------------------------------------------------------------
	aws codeartifact login --tool pip --repository io-aero-pypi --domain io-aero --domain-owner 444046118275 --region us-east-1
	$(PIP) install .
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered --cov-report=lcov -v tests
	@echo Info **********  End:   pytest ***************************************
pytest-ci:          ## Run all tests with pytest after test tool installation.
	@echo Info **********  Start: pytest ***************************************
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv install pytest pytest-cov pytest-deadfixtures pytest-helpers-namespace pytest-random-order
	@echo ----------------------------------------------------------------------
	pipenv run pytest --version
	@echo ----------------------------------------------------------------------
	aws codeartifact login --tool pip --repository io-aero-pypi --domain io-aero --domain-owner 444046118275 --region us-east-1
	$(PIP) install .
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -v tests
	@echo Info **********  End:   pytest ***************************************
pytest-first-issue: ## Run all tests with pytest until the first issue occurs.
	@echo Info **********  Start: pytest ***************************************
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run pytest --version
	@echo ----------------------------------------------------------------------
	aws codeartifact login --tool pip --repository io-aero-pypi --domain io-aero --domain-owner 444046118275 --region us-east-1
	$(PIP) install .
	pipenv run pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -rP -v -x tests
	@echo Info **********  End:   pytest ***************************************
pytest-issue:       ## Run only the tests with pytest which are marked with 'issue'.
	@echo Info **********  Start: pytest ***************************************
	@echo PIP       =${PIP}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	pipenv run pytest --version
	@echo ----------------------------------------------------------------------
	aws codeartifact login --tool pip --repository io-aero-pypi --domain io-aero --domain-owner 444046118275 --region us-east-1
	$(PIP) install .
	pipenv run pytest --cache-clear --capture=no --cov=${MODULE} --cov-report term-missing:skip-covered -m issue -rP -v -x tests
	@echo Info **********  End:   pytest ***************************************
pytest-module:      ## Run test of a specific module with pytest.
	@echo Info **********  Start: pytest ***************************************
	@echo PIP       =${PIP}
	@echo TESTMODULE=tests/$(module)
	@echo ----------------------------------------------------------------------
	aws codeartifact login --tool pip --repository io-aero-pypi --domain io-aero --domain-owner 444046118275 --region us-east-1
	$(PIP) install .
	pipenv run pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -v tests/$(module)
	@echo Info **********  End:   pytest ***************************************

sphinx:            ##  Create the user documentation with Sphinx.
	@echo Info **********  Start: sphinx ***************************************
	@echo DELETE_SPHINX   =${DELETE_SPHINX}
	@echo PIP             =${PIP}
	@echo SPHINX_BUILDDIR =${SPHINX_BUILDDIR}
	@echo SPHINX_SOURCEDIR=${SPHINX_SOURCEDIR}
	@echo ----------------------------------------------------------------------
	${DELETE_SPHINX}
	aws codeartifact login --tool pip --repository io-aero-pypi --domain io-aero --domain-owner 444046118275 --region us-east-1
	$(PIP) install .
	pipenv run sphinx-build -M html ${SPHINX_SOURCEDIR} ${SPHINX_BUILDDIR}
	pipenv run sphinx-build -b rinoh ${SPHINX_SOURCEDIR} ${SPHINX_BUILDDIR}/pdf
	@echo Info **********  End:   sphinx ***************************************

version:            ## Show the installed software versions.
	@echo Info **********  Start: version **************************************
	@echo PIP   =${PIP}
	@echo PYTHON=${PYTHON}
	@echo ----------------------------------------------------------------------
	$(PIP) --version
	pipenv --version
	@echo Info **********  End:   version **************************************

## =============================================================================
