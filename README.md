# IO-AVSTATS - Aviation Event Statistics Application

## Key Functionalities of IO-AVSTATS

Currently, **`IO-AVSTATS`** includes the following applications:

- **`ae1982`** - Aviation Event Analysis
- **`pd1982`** - IO-AVSTATS-DB Database Profiling
- **`slara`** - Association Rule Analysis

## Quickstart

This is a quick start guide.
Detailed instructions can be found in the [documentation](https://io-aero.github.io/io-avstats/) under Requirements, Installation and First Steps.

1. Install Python 3.11
2. Install Conda or Miniconda
3. Install Docker Desktop
4. Install the MS Access Database Engine - only necessary for database updates
5. Install RazorSQL - only necessary for database updates
6. Clone this repository:

    `git clone https://github.com/io-aero/io-avstats`

7. Create the virtual environment:

    `make conda-dev`

8. Switch to the created virtual environment:

    `conda activate ioavstats`

9. Create a file named `.settings.io_aero.toml` which contains the database access data

10. Test the whole functionality:

    `make final`

10. All Makefile commands can be found by running:

    `make` or `make help`

```
=============================================================================
make Script       The purpose of this Makefile is to support the whole
                  software development process for an application. It
                  contains also the necessary tools for the CI activities.
                  -----------------------------------------------------------
                  The available make commands are:
-----------------------------------------------------------------------------
help:               Show this help.
-----------------------------------------------------------------------------
action:             Run the GitHub Actions locally.
dev:                Format, lint and test the code.
docs:               Check the API documentation, create and upload the user documentation.
everything:         Do everything precheckin
final:              Format, lint and test the code and create the documentation.
format:             Format the code with Black and docformatter.
lint:               Lint the code with ruff, Bandit, vulture, Pylint and Mypy.
pre-push:           Preparatory work for the pushing process.
tests:              Run all tests with pytest.
-----------------------------------------------------------------------------
action-std:         Run the GitHub Actions locally: standard.
bandit:             Find common security issues with Bandit.
black:              Format the code with Black.
compileall:         Byte-compile the Python libraries.
conda-dev:          Create a new environment for development.
conda-prod:         Create a new environment for production.
coveralls:          Run all the tests and upload the coverage data to coveralls.
docformatter:       Format the docstrings with docformatter.
docker:             Create a docker image.
mypy:               Find typing issues with Mypy.
mypy-stubgen:       Autogenerate stub files.
next-version:       Increment the version number.
pylint:             Lint the code with Pylint.
pytest:             Run all tests with pytest.
pytest-ci:          Run all tests with pytest after test tool installation.
pytest-first-issue: Run all tests with pytest until the first issue occurs.
pytest-issue:       Run only the tests with pytest which are marked with 'issue'.
pytest-module:      Run test of a specific module with pytest.
ruff:               An extremely fast Python linter and code formatter.
sphinx:             Create the user documentation with Sphinx.
version:            Show the installed software versions.
vulture:            Find dead Python code.
=============================================================================
```

## Operation

The whole functionality of **IO-AVSTATS** can be used with the script `run_io_avstats`.
The script is available in versions for macOS, Ubuntu and Windows 10/11 and provides the following functionality:

    r_s_a   - Run the IO-AVSTATS application
    ---------------------------------------------------------
    u_p_d   - Complete processing of a modifying MS Access file
    l_n_a   - Load NTSB MS Access database data into PostgreSQL
    ---------------------------------------------------------
    c_p_d   - Cleansing PostgreSQL data
    c_l_l   - Correct decimal US latitudes and longitudes
    f_n_a   - Find the nearest airports
    v_n_d   - Verify selected NTSB data
    ---------------------------------------------------------
    l_a_p   - Load airport data into PostgreSQL
    a_o_c   - Load aviation occurrence categories into PostgreSQL
    l_c_s   - Load country and state data into PostgreSQL
    l_c_d   - Load data from a correction file into PostgreSQL
    l_s_e   - Load sequence of events data into PostgreSQL
    l_s_d   - Load simplemaps data into PostgreSQL
    l_z_d   - Load ZIP Code Database data into PostgreSQL
    ---------------------------------------------------------
    s_d_c   - Set up the PostgreSQL database container
    c_d_s   - Create the PostgreSQL database schema
    u_d_s   - Update the PostgreSQL database schema
    r_d_s   - Refresh the PostgreSQL database schema
    ---------------------------------------------------------
    c_f_z   - Zip the files for the cloud
    c_d_i   - Create or update an application Docker image
    c_d_c   - Run Docker Compose tasks - Cloud
    c_d_l   - Run Docker Compose tasks - Local
    ---------------------------------------------------------
    version - Show the IO-AVSTATS version

## Documentation

The complete documentation for this repository is contained in the github pages [here](https://io-aero.github.io/io-avstats/).
See that documentation for installation instructions

Further IO-Aero software documentation can be found under the following links.

- [IO-AIRPLANE-SIM - Airplane Simulator](https://io-aero.github.io/io-airplane-sim/)
- [IO-COMMON - Common Elements](https://io-aero.github.io/io-common/) 
- [IO-DATA-SOURCES - Data Source Documentation](https://io-aero.github.io/io-data-sources/) 
- [IO-EVAA-MAP-CREATOR - A tool to create EVAA elevation maps](https://io-aero.github.io/io-evaa-map-creator/) 
- [IO-LANDINGSPOT - Landing spot identification](https://io-aero.github.io/io-landingspot/) 
- [IO-LIDAR - Lidar Map Processing](https://io-aero.github.io/io-lidar/) 
- [IO-LIDAR-DATA - Lidar Data Management](https://io-aero.github.io/io-lidar-data/)
- [IO-MAP-APPS - IO Map Applications](https://io-aero.github.io/io-map-apps/) 
- [IO-RASTER - Raster Map Processing](https://io-aero.github.io/io-raster/) 
- [IO-TEMPLATE-APP - Template for Application Repositories](https://io-aero.github.io/io-template-app/)
- [IO-TEMPLATE-LIB - Template for Library Repositories](https://io-aero.github.io/io-template-lib/)
- [IO-VECTOR - Vector Map Processing](https://io-aero.github.io/io-vector/) 
- [IO-XPA-CORE - IO-XPA Data Processing](https://io-aero.github.io/io-xpa-core/)
<!-- - [IO-AVSTATS - Aviation Event Statistics](https://io-aero.github.io/io-avstats/) -->

## Directory and File Structure of this Repository

### 1. Directories

| Directory         | Content                                       |
|-------------------|-----------------------------------------------|
| .github/workflows | **GitHub Action** workflow.                   |
| .streamlit        | Streamlit configuration files.                |
| .vscode           | Visual Studio Code configuration files.       |
| cloud_old         | Legacy cloud related files.                   |
| config            | Configuration files.                          |
| data              | Application data related files.               |
| dist              | **docker2ex** application files.              |
| docs              | Documentation files.                          |
| ioavstats         | Python script files.                          |
| libs              | Contains libraries that are not used via pip. |
| resources         | Selected manuals and software.                |
| scripts           | Supporting macOS, Ubuntu and Windows Scripts. |
| tests             | Scripts and data for **pytest**.              |

### 2. Files

| File                            | Functionality                                                         |
|---------------------------------|-----------------------------------------------------------------------|
| .act_secrets_template           | Template file for the configuration of ``make action``.               |
| .dockerignore                   | Configuration of files and folders to be ignored with Docker.         |
| .gitattributes                  | Handling of the os-specific file properties.                          |
| .gitignore                      | Configuration of files and folders to be ignored with Git.            |
| .pylintrc                       | Pylint configuration file.                                            |
| .settings.io_aero_template.toml | Template file for the secret configuration data.                      |
| Dockerfile                      | Build instructions for the docker2exe application images.             |
| environment.yml                 | Conda environment parameter file - production version.                |
| environment_dev.yml             | Conda environment parameter file - development version.               |
| LICENSE.md                      | Text of the licence terms.                                            |
| logging_cfg.yaml                | Configuration of the Logger functionality.                            |
| Makefile                        | Tasks to be executed with the **`make`** command.                     |
| mypy.ini                        | Mypy configuration file.                                              |
| pyproject.toml                  | Optional configuration data for the software quality tools.           |
| README.md                       | This file.                                                            |
| run_io_avstats                  | Main script for using the functionality in a productive environment.  |
| run_io_avstats_dev              | Main script for using the functionality in a development environment. |
| run_io_avstats_pytest           | Main script for using the functionality in a test environment.        |
| run_ioavstats                   | Main script for using the functionality based on a Docker executable. |
| settings.io_aero.toml           | Configuration data.                                                   |
| setup.cfg                       | Optional configuration data.                                          |

## Converting the application into an executable file with docker2exe

**Target Platforms**

The tools support creating executables specifically for macOS, Ubuntu, or Windows. This allows for precise targeting based on deployment needs.

**Platform-Specific Build**

The process of creating an executable is required to be conducted on the operating system for which the executable is intended. This means building a Windows executable on a Windows machine, a macOS executable on a macOS machine, and so on.

**Use of Makefile**

Both `docker2exe` utilizes the Makefile of `io-avstats` to facilitate the construction of executables. 

**Prerequisites**
- Go Programming Language: `docker2exe` is developed in Go, so Go must be installed on the system to either compile from source or run the pre-compiled binaries.
- Docker: Docker is required as `docker2exe` converts Docker images into executable files.

The executable files for `docker2exe` are downloaded from the [GitHub Releases page](https://github.com/rzane/docker2exe). Note that the executable for Windows has been renamed to `docker2exe-windows-amd64.exe` and is located in the `dist` directory of the application. Visit the [docker2exe tool page](https://github.com/rzane/docker2exe) for more details and to access the source code.

**Creating the Executable File**

- Run `make docker`

- The Docker image named `ioavstats` is first created.
 
- `docker2exe` is then used to convert the Docker image into an executable file.

- A directory is finally created containing all the files necessary for running the application. The name of this directory varies depending on the operating system and architecture:
    - **macOS**: `app-darwin-amd64` or `app-darwin-arm64`
    - **Ubuntu**: `app-linux-amd64`
    - **Windows**: `app-windows-amd64`

- The directory, in addition to the executable file (`ioavstats` or `ioavstats.exe`), includes the following components:
    - **data**: A directory for the application data.
    - **logging_cfg.yaml**: A configuration file for logging.
    - **run_ioavstats.[bat|sh|zsh]**: A shell script to run the application.
    - **settings.io-aero.toml**: Configuration data for the `io-avstats` application.

- The converted application requires Docker to be installed in order to run, ensuring that the application's environment is appropriately replicated.
