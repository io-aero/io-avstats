.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
	export DELETE_PIPFILE_LOCK=if exist pipfile.lock del /q pipfile.lock
	export PIPENV=python -m pipenv
	export PYTHON=python
	export SQLALCHEMY_WARN_20=1
else
	export DELETE_PIPFILE_LOCK=rm -rf pipfile.lock
	export PIPENV=python3 -m pipenv
	export PYTHON=python3
	export SQLALCHEMY_WARN_20=1
endif

export PYTHONPATH=src

## =============================================================================
## IO-AVSTATS - Aviation Event Statistics - make Documentation.
##                ---------------------------------------------------------------
##                The purpose of this Makefile is to support the whole software
##                development process for io-avstats. It contains also the
##                necessary tools for the CI activities.
##                ---------------------------------------------------------------
##                The available make commands are:
## -----------------------------------------------------------------------------
## help:               Show this help.
## -----------------------------------------------------------------------------
## dev:                Format and lint the code.
dev: format lint
## docs:               Check the API documentation, create and upload the user documentation.
docs: pydocstyle mkdocs
## final:              Format and lint the code and create the documentation.
final: format lint docs
## format:             Format the code with isort, Black and docformatter.
format: isort black docformatter
## lint:               Lint the code with Bandit, Flake8, Pylint and Mypy.
lint: bandit flake8 pylint mypy
## -----------------------------------------------------------------------------

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo Info **********  Start: Bandit ***************************************
	@echo PIPENV    =${PIPENV}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PIPENV} run bandit --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run bandit -c pyproject.toml -r ${PYTHONPATH}
	@echo Info **********  End:   Bandit ***************************************

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:              ## Format the code with Black.
	@echo Info **********  Start: black ****************************************
	@echo PIPENV    =${PIPENV}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PIPENV} run black --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run black ${PYTHONPATH}
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

# Formats docstrings to follow PEP 257
# https://github.com/PyCQA/docformatter
# Configuration file: none
docformatter:       ## Format the docstrings with docformatter.
	@echo Info **********  Start: docformatter *********************************
	@echo PIPENV    =${PIPENV}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PIPENV} run docformatter --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run docformatter --in-place -r ${PYTHONPATH}
	@echo Info **********  End:   docformatter *********************************

# Flake8: Your Tool For Style Guide Enforcement.
# https://github.com/pycqa/flake8
# Configuration file: cfg.cfg
flake8:             ## Enforce the Python Style Guides with Flake8.
	@echo Info **********  Start: Flake8 ***************************************
	@echo PIPENV    =${PIPENV}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PIPENV} run flake8 --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run flake8 ${PYTHONPATH}
	@echo Info **********  End:   Flake8 ***************************************

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort:              ## Edit and sort the imports with isort.
	@echo Info **********  Start: isort ****************************************
	@echo PIPENV    =${PIPENV}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PIPENV} run isort --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run isort ${PYTHONPATH}
	@echo Info **********  End:   isort ****************************************

# Project documentation with Markdown.
# https://github.com/mkdocs/mkdocs/
# Configuration file: none
mkdocs:             ## Create and upload the user documentation with MkDocs.
	@echo Info **********  Start: MkDocs ***************************************
	@echo PIPENV=${PIPENV}
	@echo ----------------------------------------------------------------------
	${PIPENV} run mkdocs --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run mkdocs build
	@echo Info **********  End:   MkDocs ***************************************

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:               ## Find typing issues with Mypy.
	@echo Info **********  Start: Mypy *****************************************
	@echo PIPENV    =${PIPENV}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PIPENV} run mypy --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run mypy ${PYTHONPATH}
	@echo Info **********  End:   Mypy *****************************************

# pip is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
pipenv-dev:         ## Install the package dependencies for development.
	@echo Info **********  Start: Installation of Development Packages *********
	@echo DELETE_PIPFILE_LOCK=${DELETE_PIPFILE_LOCK}
	@echo PIPENV             =${PIPENV}
	@echo PYTHON             =${PYTHON}
	@echo ----------------------------------------------------------------------
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade pipenv
	${PYTHON} -m pip install --upgrade virtualenv
	${DELETE_PIPFILE_LOCK}
	${PIPENV} install --dev
	@echo ----------------------------------------------------------------------
	${PIPENV} run pip freeze
	@echo ----------------------------------------------------------------------
	${PYTHON} --version
	${PYTHON} -m pip --version
	${PYTHON} -m pipenv --version
	${PYTHON} -m virtualenv --version
	@echo Info **********  End:   Installation of Development Packages *********
pipenv-prod:        ## Install the package dependencies for production.
	@echo Info **********  Start: Installation of Production Packages **********
	@echo DELETE_PIPFILE_LOCK=${DELETE_PIPFILE_LOCK}
	@echo PIPENV             =${PIPENV}
	@echo PYTHON             =${PYTHON}
	@echo ----------------------------------------------------------------------
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade pipenv
	${PYTHON} -m pip install --upgrade virtualenv
	${DELETE_PIPFILE_LOCK}
	${PIPENV} install
	@echo ----------------------------------------------------------------------
	${PIPENV} run pip freeze
	@echo ----------------------------------------------------------------------
	${PYTHON} --version
	${PYTHON} -m pip --version
	${PYTHON} -m pipenv --version
	${PYTHON} -m virtualenv --version
	@echo Info **********  End:   Installation of Production Packages **********

# pydocstyle - docstring style checker.
# https://github.com/PyCQA/pydocstyle
# Configuration file: pyproject.toml
pydocstyle:         ## Check the API documentation with pydocstyle.
	@echo Info **********  Start: pydocstyle ***********************************
	@echo PIPENV    =${PIPENV}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PIPENV} run pydocstyle --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run pydocstyle --count --match='(?!PDFLIB\\)*\.py' ${PYTHONPATH}
	@echo Info **********  End:   pydocstyle ***********************************

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: .pylintrc
pylint:             ## Lint the code with Pylint.
	@echo Info **********  Start: Pylint ***************************************
	@echo PIPENV    =${PIPENV}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo ----------------------------------------------------------------------
	${PIPENV} run pylint --version
	@echo ----------------------------------------------------------------------
	${PIPENV} run pylint ${PYTHONPATH}
	@echo Info **********  End:   Pylint ***************************************

version:            ## Show the installed software versions.
	@echo Info **********  Start: version **************************************
	@echo PYTHON=${PYTHON}
	@echo ----------------------------------------------------------------------
	${PYTHON} -m pip --version
	${PYTHON} -m pipenv --version
	@echo Info **********  End:   version **************************************

## =============================================================================
