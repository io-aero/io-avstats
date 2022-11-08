# IO-AVSTATS - Aviation Accident Statistics

TODO by lho

## 1. Features

TODO by lho

## 2. Quick Start

TODO by wwe

## 3. Directory and File Structure of this Repository

### 3.1 Directories

| Directory         | Content                                                       |
|-------------------|---------------------------------------------------------------|
| .github/workflows | **[GitHub Action](https://github.com/actions)** workflows.    |
| docs              | Documentation files.                                          |
| resources         | Selected manuals and software.                                |
| scripts           | Supporting Ubuntu and Windows Scripts.                        |
| site              | Documentation as static HTML pages generated with **MkDocs**. |
| src               | Python script files and the **IO-AVSTATS-DB** package.        |
| tests             | Scripts and data for **pytest**.                              |

### 3.2 Files

| File                     | Functionality                                                                                   |
|--------------------------|-------------------------------------------------------------------------------------------------|
| .gitignore               | Configuration of files and folders to be ignored.                                               |
| LICENSE.md               | Text of the licence terms.                                                                      |
| logging_cfg.yaml         | Configuration of the Logger functionality.                                                      |
| Makefile                 | Definition of tasks to be executed with the **`make`** command.                                 |
| mkdocs.yml               | Configuration file for **MkDocs**.                                                              |
| Pipfile                  | Definition of the Python package requirements.                                                  |
| pyproject.toml           | Optional configuration data for the **bandit**, **isort**, **pydocstyle** and **pytest** tools. |
| README.md                | This file.                                                                                      |
| run_io_avstats           | Main script for using the functionality of **IO-AVSTATS**.                                      |
| settings.io_avstats.toml | Configuration data for **IO-AVSTATS**.                                                          |
| setup.cfg                | Optional configuration data for **flake8**.                                                     |
