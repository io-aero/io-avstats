# IO-AVSTATS - Aviation Event Statistics Application

## 1. Features

- Applications based on the library ioavstatsdb:
  - Association Rule Analysis
  - Aviation Event Analysis
  - Database Profiling

## 2. Documentation

The full documentation can be found [here](https://io-aero.github.io/io-avstats/).

## 3. Quick Start

Please follow the instructions given here:

- [Requirements](https://io-aero.github.io/io-avstats/setup_requirements.html)
- [Installation](https://io-aero.github.io/io-avstats/setup_installation.html)

All processing tasks can be performed using the **`run_io_avstats`** shell script.

## 4. Directory and File Structure of this Repository

### 4.1 Directories

| Directory         | Content                                                    |
|-------------------|------------------------------------------------------------|
| .github/workflows | **[GitHub Action](https://github.com/actions)** workflows. |
| .streamlit        | Streamlit configuration files.                             |
| config            | Configuration files.                                       |
| data              | Application data related files.                            |
| dist              | Contains an executable of this application.                |
| docs              | Documentation files.                                       |
| ioavstats         | Python script files.                                       |
| libs              | Third party libraries.                                     |
| resources         | Selected manuals and software.                             |
| scripts           | Supporting macOS, Ubuntu and Windows Scripts.              |
| site              | Documentation as static HTML pages.                        |
| tests             | Scripts and data for **pytest**.                           |
| upload            | Cloud related upload directory.                            |

### 4.2 Files

| File                      | Functionality                                                   |
|---------------------------|-----------------------------------------------------------------|
| .gitignore                | Configuration of files and folders to be ignored.               |
| .pylintrc                 | **pylint** configuration file.                                  |
| docker-compose_cloud.yaml | Cloud related Docker Compose configuration file.                |
| docker-compose_local.yaml | Local Docker Compose configuration file.                        |
| dockerfile                | Build instructions for the Streamlit application images.        |
| LICENSE.md                | Text of the licence terms.                                      |
| logging_cfg.yaml          | Configuration of the Logger functionality.                      |
| Makefile                  | Tasks to be executed with the **`make`** command.               |
| mkdocs.yml                | Configuration file for **MkDocs**.                              |
| nginx.conf                | Configuration file for **Nginx**.                               |
| Pipfile                   | Definition of the Python package requirements.                  |
| pyproject.toml            | Optional configuration data for the software quality tools.     |
| README.md                 | This file.                                                      |
| run_io_avstats            | Main script for using the functionality of **IO-AVSTATS**.      |
| run_io_avstats_pytest     | Main script for using the test functionality of **IO-AVSTATS**. |
| settings.io_aero.toml     | Configuration data.                                             |
| setup.cfg                 | Optional configuration data for **flake8**.                     |
