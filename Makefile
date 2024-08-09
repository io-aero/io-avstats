.DEFAULT_GOAL := help

MODULE=ioavstats

ifeq (${OS},Windows_NT)
    COPY_MYPY_STUBGEN=xcopy /y out\\${MODULE}\\*.* .\\${MODULE}\\
    DELETE_MYPY_STUBGEN=if exist out rd /s /q out
    DOCKER2EXE_CHMOD=echo no operation with
    DOCKER2EXE_COPY=copy
    DOCKER2EXE_CURR=%%CD%%
    DOCKER2EXE_DIR=windows-amd64
    DOCKER2EXE_EXEC=dist\docker2exe-${DOCKER2EXE_DIR}.exe
    DOCKER2EXE_EXT=.exe
    DOCKER2EXE_MOVE=move
    DOCKER2EXE_RMDIR=if exist app-${DOCKER2EXE_DIR} rmdir /s /q app-${DOCKER2EXE_DIR}
    DOCKER2EXE_SCRIPT=bat
    DOCKER2EXE_TARGET=windows/amd64
    NUITKA_OPTION=--msvc=latest
    NUITKA_OS=windows
    PATH_SEP=\\
    PIP=pip
    PYTHON=python
    DELETE_SPHINX=del /f /q ${SPHINX_BUILDDIR}\\*
    REMOVE_DOCKER_CONTAINER=@docker ps -a | findstr /r /c:"${MODULE}" && docker rm --force ${MODULE}         || echo "No existing container to remove."
    REMOVE_DOCKER_IMAGE=@docker image ls  | findstr /r /c:"${MODULE}" && docker rmi --force ${MODULE}:latest || echo "No existing image to remove."
else
	ARCH:=$(shell uname -m)
	OS:=$(shell uname -s)
    COPY_MYPY_STUBGEN=cp -f out/${MODULE}/* ./${MODULE}/
    DELETE_MYPY_STUBGEN=rm -rf out
    ifeq (${OS},Linux)
        DOCKER2EXE_DIR=linux-amd64
	    DOCKER2EXE_SCRIPT=sh
        DOCKER2EXE_TARGET=linux/amd64
    else ifeq (${OS},Darwin)
        DOCKER2EXE_SCRIPT=zsh
        ifeq (${ARCH},arm64)
	        DOCKER2EXE_DIR=darwin-arm64
	        DOCKER2EXE_TARGET=darwin/arm64
    	else ifeq (${ARCH},x86_64)
	        DOCKER2EXE_DIR=darwin-amd64
	        DOCKER2EXE_TARGET=darwin/amd64
    	endif
    endif
    DOCKER2EXE_CHMOD=chmod +x
    DOCKER2EXE_COPY=cp
    DOCKER2EXE_CURR=$$PWD
    DOCKER2EXE_EXEC=./dist/docker2exe-${DOCKER2EXE_DIR}
    DOCKER2EXE_EXT=
    DOCKER2EXE_MOVE=mv
    DOCKER2EXE_RMDIR=rm -rf app-${DOCKER2EXE_DIR}
    NUITKA_OPTION=--disable-ccache
    ifeq (${OS},Linux)
        NUITKA_OS=linux
    else
        NUITKA_OS=macos
    endif
    PATH_SEP=/
    PIP=pip3
    PYTHON=python3
    DELETE_SPHINX=rm -rf ${SPHINX_BUILDDIR}/*
    REMOVE_DOCKER_CONTAINER=@sh -c 'docker ps -a | grep -q "${MODULE}" && docker rm --force ${MODULE} || echo "No existing container to remove."'
    REMOVE_DOCKER_IMAGE=@sh -c 'docker image ls | grep -q "${MODULE}" && docker rmi --force ${MODULE}:latest || echo "No existing image to remove."'
endif

COVERALLS_REPO_TOKEN=<see coveralls.io>
DOCKER2EXE_CURR=.
PYTHONPATH=${MODULE} docs scripts tests
SPHINX_BUILDDIR=docs${PATH_SEP}build
SPHINX_SOURCEDIR=docs${PATH_SEP}source

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
everything: dev docs nuitka
## final:              Format, lint and test the code and create the documentation.
final: format lint docs tests
## format:             Format the code with Black and docformatter.
format: isort black docformatter
## lint:               Lint the code with ruff, Bandit, vulture, Pylint and Mypy.
lint: ruff bandit vulture pylint mypy
## pre-push:           Preparatory work for the pushing process.
pre-push: format lint tests next-version docs
## tests:              Run all tests with pytest.
tests: pytest
## -----------------------------------------------------------------------------

help:
	@sed -ne '/@sed/!s/## //p' ${MAKEFILE_LIST}

# Run the GitHub Actions locally.
# https://github.com/nektos/act
# Configuration files: .act_secrets & .act_vars
action-std:         ## Run the GitHub Actions locally: standard.
	@echo "Info **********  Start: action ***************************************"
	@echo "Copy your .aws/credentials to .aws_secrets"
	@echo "----------------------------------------------------------------------"
	act --version
	@echo "----------------------------------------------------------------------"
	act --quiet \
        --secret-file .act_secrets \
        --var IO_LOCAL='true' \
        --verbose \
        -P ubuntu-latest=catthehacker/ubuntu:act-latest \
        -W .github/workflows/github_pages.yml
	act --quiet \
        --secret-file .act_secrets \
        --var IO_LOCAL='true' \
        --verbose \
        -P ubuntu-latest=catthehacker/ubuntu:act-latest \
        -W .github/workflows/standard.yml
	@echo "Info **********  End:   action ***************************************"

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo "Info **********  Start: Bandit ***************************************"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	bandit --version
	@echo "----------------------------------------------------------------------"
	bandit -c pyproject.toml -r ${PYTHONPATH}
	@echo "Info **********  End:   Bandit ***************************************"

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:              ## Format the code with Black.
	@echo "Info **********  Start: black ****************************************"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	black --version
	@echo "----------------------------------------------------------------------"
	black ${PYTHONPATH}
	@echo "Info **********  End:   black ****************************************"

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:         ## Byte-compile the Python libraries.
	@echo "Info **********  Start: Compile All Python Scripts *******************"
	@echo "PYTHON=${PYTHON}"
	@echo "----------------------------------------------------------------------"
	${PYTHON} --version
	@echo "----------------------------------------------------------------------"
	${PYTHON} -m compileall
	@echo "Info **********  End:   Compile All Python Scripts *******************"

# Miniconda - Minimal installer for conda.
# https://docs.conda.io/en/latest/miniconda.html
# Configuration file: none
conda-dev:          ## Create a new environment for development.
	@echo "Info **********  Start: Miniconda create development environment *****"
	conda config --set always_yes true
	conda --version
	echo "PYPI_PAT=${PYPI_PAT}"
	@echo "----------------------------------------------------------------------"
	conda env remove -n ${MODULE}
	conda env create -f environment_dev.yml
	@echo "----------------------------------------------------------------------"
	conda info --envs
	conda list
	@echo "Info **********  End:   Miniconda create development environment *****"
conda-prod:         ## Create a new environment for production.
	@echo "Info **********  Start: Miniconda create production environment ******"
	conda config --set always_yes true
	conda --version
	@echo "----------------------------------------------------------------------"
	conda env remove -n ${MODULE}
	conda env create -f environment.yml
	@echo "----------------------------------------------------------------------"
	conda info --envs
	conda list
	@echo "Info **********  End:   Miniconda create production environment ******"

# Requires a public repository !!!
# Python interface to coveralls.io API
# https://github.com/TheKevJames/coveralls-python
# Configuration file: none
coveralls:          ## Run all the tests and upload the coverage data to coveralls.
	@echo "Info **********  Start: coveralls ************************************"
	pytest --cov=${MODULE} --cov-report=xml --random-order tests
	@echo "----------------------------------------------------------------------"
	coveralls --service=github
	@echo "Info **********  End:   coveralls ************************************"

# Formats docstrings to follow PEP 257
# https://github.com/PyCQA/docformatter
# Configuration file: pyproject.toml
docformatter:       ## Format the docstrings with docformatter.
	@echo "Info **********  Start: docformatter *********************************"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	docformatter --version
	@echo "----------------------------------------------------------------------"
	docformatter --in-place -r ${PYTHONPATH}
#	docformatter -r ${PYTHONPATH}
	@echo "Info **********  End:   docformatter *********************************"

# Creates Docker executables
# https://github.com/rzane/docker2exe
# Configuration files: .dockerignore & Dockerfile
docker:             ## Create a docker image.
	@echo "Info **********  Start: Docker ***************************************"
	@echo "OS               =${OS}"
	@echo "ARCH             =${ARCH}"
	@echo "----------------------------------------------------------------------"
	@echo "DOCKER2EXE_CHMOD =${DOCKER2EXE_CHMOD}"
	@echo "DOCKER2EXE_COPY  =${DOCKER2EXE_COPY}"
	@echo "DOCKER2EXE_CURR  =${DOCKER2EXE_CURR}"
	@echo "DOCKER2EXE_DIR   =${DOCKER2EXE_DIR}"
	@echo "DOCKER2EXE_EXEC  =${DOCKER2EXE_EXEC}"
	@echo "DOCKER2EXE_MOVE  =${DOCKER2EXE_MOVE}"
	@echo "DOCKER2EXE_RMDIR =${DOCKER2EXE_RMDIR}"
	@echo "DOCKER2EXE_SCRIPT=${DOCKER2EXE_SCRIPT}"
	@echo "DOCKER2EXE_TARGET=${DOCKER2EXE_TARGET}"
	@echo "----------------------------------------------------------------------"
	docker ps -a
	@echo "----------------------------------------------------------------------"
	${REMOVE_DOCKER_CONTAINER}
	${REMOVE_DOCKER_IMAGE}
	docker system prune -a -f
	docker build --build-arg PYPI_PAT=${PYPI_PAT} -t ${MODULE} .
	@echo "----------------------------------------------------------------------"
	${DOCKER2EXE_RMDIR}
	mkdir app-${DOCKER2EXE_DIR}
	${DOCKER2EXE_CHMOD} dist${PATH_SEP}docker2exe-${DOCKER2EXE_DIR}
	${DOCKER2EXE_EXEC} --name ${MODULE} \
					   --image ${MODULE}:latest \
					   --embed \
					   -t ${DOCKER2EXE_TARGET} \
					   -v ${DOCKER2EXE_CURR}${PATH_SEP}data:/app/data \
					   -v ${DOCKER2EXE_CURR}${PATH_SEP}logging_cfg.yaml:/app/logging_cfg.yaml \
					   -v ${DOCKER2EXE_CURR}${PATH_SEP}settings.io_aero.toml:/app/settings.io_aero.toml
	mkdir app-${DOCKER2EXE_DIR}${PATH_SEP}data
	${DOCKER2EXE_MOVE} dist${PATH_SEP}${MODULE}-${DOCKER2EXE_DIR} app-${DOCKER2EXE_DIR}${PATH_SEP}${MODULE}${DOCKER2EXE_EXT}
	${DOCKER2EXE_CHMOD}  app-${DOCKER2EXE_DIR}${PATH_SEP}${MODULE}
	${DOCKER2EXE_COPY} logging_cfg.yaml                           app-${DOCKER2EXE_DIR}${PATH_SEP}
	${DOCKER2EXE_COPY} run_ioavstats.${DOCKER2EXE_SCRIPT}         app-${DOCKER2EXE_DIR}${PATH_SEP}
	${DOCKER2EXE_CHMOD} app-${DOCKER2EXE_DIR}${PATH_SEP}*.${DOCKER2EXE_SCRIPT}
	${DOCKER2EXE_COPY} settings.io_aero.toml                      app-${DOCKER2EXE_DIR}${PATH_SEP}
	@echo "Info **********  End:   Docker ***************************************"

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort:              ## Edit and sort the imports with isort.
	@echo "Info **********  Start: isort ****************************************"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	isort --version
	@echo "----------------------------------------------------------------------"
	isort ${PYTHONPATH}
	@echo "Info **********  End:   isort ****************************************"

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:               ## Find typing issues with Mypy.
	@echo "Info **********  Start: Mypy *****************************************"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	mypy --version
	@echo "----------------------------------------------------------------------"
	mypy ${PYTHONPATH}
	@echo "Info **********  End:   Mypy *****************************************"

mypy-stubgen:       ## Autogenerate stub files.
	@echo "Info **********  Start: Mypy *****************************************"
	@echo "COPY_MYPY_STUBGEN  =${COPY_MYPY_STUBGEN}"
	@echo "DELETE_MYPY_STUBGEN=${DELETE_MYPY_STUBGEN}"
	@echo "MODULE             =${MODULE}"
	@echo "----------------------------------------------------------------------"
	${DELETE_MYPY_STUBGEN}
	stubgen --package ${MODULE}
	${COPY_MYPY_STUBGEN}
	${DELETE_MYPY_STUBGEN}
	@echo "Info **********  End:   Mypy *****************************************"

next-version:       ## Increment the version number.
	@echo "Info **********  Start: next_version *********************************"
	@echo "PYTHON    =${PYTHON}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	${PYTHON} scripts/next_version.py
	@echo "Info **********  End:   next version *********************************"

# Nuitka: Python compiler written in Python
# https://github.com/Nuitka/Nuitka
nuitka:             ## Create a dynamic link library.
	@echo "Info **********  Start: nuitka ***************************************"
	@echo "MODULE       =${MODULE}"
	@echo "NUITKA_OPTION=${NUITKA_OPTION}"
	@echo "PIP          =${PIP}"
	@echo "PYTHON       =${PYTHON}"
	@echo "----------------------------------------------------------------------"
	${PYTHON} -m nuitka ${NUITKA_OPTION} \
			  --main=scripts/launcher.py \
			  --onefile \
			  --onefile-tempdir-spec=.temp \
			  --output-dir=dist/${NUITKA_OS} \
			  --output-filename=${MODULE} \
			  --show-modules \
			  --standalone \
			  --static-libpython=no
	@echo "Info **********  End:   nuitka ***************************************"

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: .pylintrc
pylint:             ## Lint the code with Pylint.
	@echo "Info **********  Start: Pylint ***************************************"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	pylint --version
	@echo "----------------------------------------------------------------------"
	pylint ${PYTHONPATH}
	@echo "Info **********  End:   Pylint ***************************************"

# pytest: helps you write better programs.
# https://github.com/pytest-dev/pytest/
# Configuration file: pyproject.toml
pytest:             ## Run all tests with pytest.
	@echo "Info **********  Start: pytest ***************************************"
	@echo "CONDA     =${CONDA_PREFIX}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --dead-fixtures tests
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered --cov-report=lcov -v tests
	@echo "Info **********  End:   pytest ***************************************"
pytest-ci:          ## Run all tests with pytest after test tool installation.
	@echo "Info **********  Start: pytest ***************************************"
	@echo "CONDA     =${CONDA_PREFIX}"
	@echo "PIP       =${PIP}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	${PIP} install pytest pytest-cov pytest-deadfixtures pytest-helpers-namespace pytest-random-order
	@echo "----------------------------------------------------------------------"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --dead-fixtures tests
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -v tests
	@echo "Info **********  End:   pytest ***************************************"
pytest-first-issue: ## Run all tests with pytest until the first issue occurs.
	@echo "Info **********  Start: pytest ***************************************"
	@echo "CONDA     =${CONDA_PREFIX}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -rP -v -x tests
	@echo "Info **********  End:   pytest ***************************************"
pytest-ignore-mark: ## Run all tests without marker with pytest."
	@echo "Info **********  Start: pytest ***************************************"
	@echo "CONDA     =${CONDA_PREFIX}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --dead-fixtures -m "not no_ci" tests
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered --cov-report=lcov -m "not no_ci" -v tests
	@echo Info **********  End:   pytest ***************************************
pytest-issue:       ## Run only the tests with pytest which are marked with 'issue'.
	@echo Info **********  Start: pytest ***************************************
	@echo CONDA     =${CONDA_PREFIX}
	@echo PYTHONPATH=${PYTHONPATH}
	@echo "----------------------------------------------------------------------"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --dead-fixtures tests
	pytest --cache-clear --capture=no --cov=${MODULE} --cov-report term-missing:skip-covered -m issue -rP -v -x tests
	@echo "Info **********  End:   pytest ***************************************"
pytest-module:      ## Run test of a specific module with pytest.
	@echo "Info **********  Start: pytest ***************************************"
	@echo "CONDA     =${CONDA_PREFIX}"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "TESTMODULE=tests/${TEST-MODULE}.py"
	@echo "----------------------------------------------------------------------"
	pytest --version
	@echo "----------------------------------------------------------------------"
	pytest --cache-clear --cov=${MODULE} --cov-report term-missing:skip-covered -v tests/${TEST-MODULE}.py
	@echo "Info **********  End:   pytest ***************************************"

# https://github.com/astral-sh/ruff
# Configuration file: pyproject.toml
ruff:               ## An extremely fast Python linter and code formatter.
	@echo "Info **********  Start: ruff *****************************************"
	ruff --version
	@echo "----------------------------------------------------------------------"
	ruff check --fix
	@echo "Info **********  End:   ruff *****************************************"

sphinx:             ## Create the user documentation with Sphinx.
	@echo "Info **********  Start: sphinx ***************************************"
	@echo "DELETE_SPHINX   =${DELETE_SPHINX}"
	@echo "PIP             =${PIP}"
	@echo "SPHINX_BUILDDIR =${SPHINX_BUILDDIR}"
	@echo "SPHINX_SOURCEDIR=${SPHINX_SOURCEDIR}"
	@echo "----------------------------------------------------------------------"
	${PIP} install --no-deps -e .
	@echo "----------------------------------------------------------------------"
	${DELETE_SPHINX}
	sphinx-apidoc -o ${SPHINX_SOURCEDIR} ${MODULE}
	sphinx-build -M html ${SPHINX_SOURCEDIR} ${SPHINX_BUILDDIR}
	sphinx-build -b rinoh ${SPHINX_SOURCEDIR} ${SPHINX_BUILDDIR}/pdf
	@echo "Info **********  End:   sphinx ***************************************"

version:            ## Show the installed software versions.
	@echo "Info **********  Start: version **************************************"
	@echo "PIP   =${PIP}"
	@echo "PYTHON=${PYTHON}"
	@echo "----------------------------------------------------------------------"
	${PIP} --version
	@echo "Info **********  End:   version **************************************"

# Find dead Python code
# https://github.com/jendrikseipp/vulture
# Configuration file: pyproject.toml
vulture:            ## Find dead Python code.
	@echo "Info **********  Start: vulture **************************************"
	@echo "PYTHONPATH=${PYTHONPATH}"
	@echo "----------------------------------------------------------------------"
	vulture --version
	@echo "----------------------------------------------------------------------"
	vulture ${PYTHONPATH}
	@echo "Info **********  End:   vulture **************************************"

## =============================================================================
