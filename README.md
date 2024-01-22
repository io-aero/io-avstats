# IO-AVSTATS - Aviation Event Statistics Application

## Key Functionalities of IO-AVSTATS

Currently, **`IO-AVSTATS`** includes the following applications:

- **`ae1982`** - Aviation Event Analysis
- **`pd1982`** - IO-AVSTATS-DB Database Profiling
- **`slara`**&nbsp;&nbsp; - Association Rule Analysis

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

- [IO-COMMON - Common Globals, Functions, and Processes for the IO-Aero Libraries](https://io-aero.github.io/io-common/)
- [IO-LIDAR - Lidar Processing Libraries](https://io-aero.github.io/io-lidar/)
- [IO-LIDAR-BATCH - Maintenance of the directory of LAZ and metadata from Rockyweb](https://io-aero.github.io/io-lidar-batch/)
- [IO-RASTER - TODO](https://io-aero.github.io/io-raster/)
- [IO-VECTOR - Vector Map Repository](https://io-aero.github.io/io-vector/)
- [IO-XPA-DATA - IO-XPA related data acquisition and data analysis](https://io-aero.github.io/io-xpa-data/)
<!-- - [IO-AVSTATS - Aviation Event Statistics](https://io-aero.github.io/io-avstats/) -->

## Directory and File Structure of this Repository

### 1. Directories

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
| tests             | Scripts and data for **pytest**.                           |
| upload            | Cloud related upload directory.                            |

### 2. Files

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
