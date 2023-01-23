# IO-AVSTATS - Aviation Event Statistics

TODO by lho

## 1. Features

- Demo showing the aviation fatalities in the U.S. per year since 1982.

## 2. Quick Start

All processing tasks can be performed using the **`run_io_avstats`** shell script.

## 3. Warning about the Database

This Repository contains the latest version of the **IO-AVSTATS** database files in the `data/postgres` file directory. 
The underlying database management system is [PostgreSQL](https://www.postgresql.org).

Unfortunately, the database files cannot be made available via GitHub due to restrictions on GitHub:

    remote: warning: File data/postgres/base/26303/26490 is 65.88 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
    remote: warning: File data/postgres/base/26303/26343 is 62.95 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
    remote: warning: File data/postgres/base/26303/26435 is 91.64 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
    remote: error: Trace: 686e558f33fcfe8570217bc82f91eadd38abdae6588066bad7e8e82559ca1f33        
    remote: error: See http://git.io/iEPt8g for more information.        
    remote: error: File data/postgres/base/26303/26487 is 109.09 MB; this exceeds GitHub's file size limit of 100.00 MB        
    remote: error: File data/postgres/base/26303/26438 is 105.01 MB; this exceeds GitHub's file size limit of 100.00 MB        
    remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.        
    error: failed to push some refs to 'https://github.com/io-aero/io-avstats-db'
    To https://github.com/io-aero/io-avstats-db
    !	refs/heads/main:refs/heads/main	[remote rejected] (pre-receive hook declined)
    Done

For the transition period until a suitable cloud solution is implemented, the database files will be made available in the corresponding Google Drive via the Google Account ioavstats.ioaero@gmail.com.  

The latest version of the **IO-AVSTATS** database can be found here: 

[Google Drive](https://drive.google.com/drive/folders/1VvIHxnsTbaoQnkLnr-jiszwOO1HD5bTc?usp=share_link)

## 4. Directory and File Structure of this Repository

### 4.1 Directories

| Directory         | Content                                                       |
|-------------------|---------------------------------------------------------------|
| .github/workflows | **[GitHub Action](https://github.com/actions)** workflows.    |
| .streamlit        | Streamlit configuration files.                                |
| data              | Application data related files.                               |
| docs              | Documentation files.                                          |
| resources         | Selected manuals and software.                                |
| scripts           | Supporting Ubuntu and Windows Scripts.                        |
| site              | Documentation as static HTML pages generated with **MkDocs**. |
| src               | Python script files and the **IO-AVSTATS-DB** package.        |
| tests             | Scripts and data for **pytest**.                              |

### 4.2 Files

| File                                  | Functionality                                                                                   |
|---------------------------------------|-------------------------------------------------------------------------------------------------|
| .gitignore                            | Configuration of files and folders to be ignored.                                               |
| docker-compose.yaml                   | Docker Compose configuration file.                                                              |
| dockerfile                            | Build instructions for the Streamlit application images.                                        |
| LICENSE.md                            | Text of the licence terms.                                                                      |
| logging_cfg.yaml                      | Configuration of the Logger functionality.                                                      |
| Makefile                              | Definition of tasks to be executed with the **`make`** command.                                 |
| mkdocs.yml                            | Configuration file for **MkDocs**.                                                              |
| Pipfile                               | Definition of the Python package requirements.                                                  |
| pyproject.toml                        | Optional configuration data for the **bandit**, **isort**, **pydocstyle** and **pytest** tools. |
| README.md                             | This file.                                                                                      |
| run_create_image                      | Script to create the Streamlit application images.                                              |
| run_docker_compose                    | Script to start the Docker orchestration.                                                       |
| run_io_avstats                        | Main script for using the functionality of **IO-AVSTATS**.                                      |
| settings.io_avstats.toml              | Configuration data for **IO-AVSTATS**.                                                          |
| settings.io_avstats_4_dockerfile.toml | Configuration data for **IO-AVSTATS** - variant for the Streamlit application images.           |
| setup.cfg                             | Optional configuration data for **flake8**.                                                     |
