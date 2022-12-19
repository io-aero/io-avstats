# Configuration - **IO-AVSTATS**

For the administration of the configuration parameters of **IO-AVSTATS** the tool [**dynaconf**](https://www.dynaconf.com){:target="_blank"} is used.
The two files `settings.io_avstats.toml` and `.settings.io_avstats.toml` are available as configuration files.
The `.settings.io_avstats.toml` file contains the security related parameters such as passwords and is not made available in the GitHub repository.
The names of **IO-AVSTATS** related environment variables must include the prefix `IO_AVSTATS`.
Layered environments are supported.
The `test` layer is used for the automated tests.

## 1. Available Parameters

| Parameter                               | Default value                                 | Description                                                              |
|-----------------------------------------|-----------------------------------------------|--------------------------------------------------------------------------|
| correction_work_dir                     | data/correction                               | file directory containing the files with the manual corrections          |
| database_commit_size                    | 5000                                          | number of rows processed before a progress message is created            |
| download_chunk_size                     | 524288                                        | chunk size for download from the **NTSB** website                        |
| download_file_countries_states_json     | data/Countries_States/countries_states.json   | name of the file containing data of countries and states                 |
| download_file_simplemaps_us_cities_xlsx | uscities.xlsx                                 | simplemaps: name of the zipped US city file                              |
| download_file_simplemaps_us_cities_zip  | simplemaps_uscities_basicv1.75.zip            | simplemaps: name of the unzipped US city file                            |
| download_file_simplemaps_us_zips_xlsx   | uszips.xlsx                                   | simplemaps: name of the zipped US zip code file                          |
| download_file_simplemaps_us_zips_zip    | simplemaps_uszips_basicv1.81.zip              | simplemaps: name of the unzipped US zip code file                        |
| download_file_zip_codes_org_xls         | zip_code_database.xls                         | ZIP Code Database: name of the unzipped US zip code file                 |
| download_timeout                        | 10                                            | seconds to wait for the server to send data                              |
| download_url_ntsb_prefix                | https://data.ntsb.gov/...                     | prefix of the download link for the **NTSB** data sets                   |
| download_url_simplemaps_us_cities       | https://simplemaps.com/...                    | prefix of the download link for the **simplemaps** US cities data sets   |
| download_url_simplemaps_us_zips         | https://simplemaps.com/...                    | prefix of the download link for the **simplemaps** US zip code data sets |
| download_url_zip_codes_org              | https://www.unitedstateszipcodes.org/...      | prefix of the download link for the **ZIP Code Database** data set       |
| download_work_dir                       | data/download                                 | working directory for the processing of **NTSB** data sets               |
| is_verbose                              | true                                          | display progress messages for processing                                 |
| max_deviation_latitude                  | 0.01                                          | maximum decimal deviation of the latitude in the database table even     |
| max_deviation_longitude                 | 0.01                                          | maximum decimal deviation of the longitude in the database table even    |
| odbc_connection_string                  | Driver={MS Access Driver ...                  | connection string for the MS Access ODBC driver                          |
| pandas_profile_dir                      | a/pandas_profiles                             | directory to store the Pandas profiling results                          |
| postgres_connection_port                | 5432                                          | database port number                                                     |
| postgres_container_name                 | io_avstats_container                          | container name                                                           |
| postgres_container_port                 | 5432                                          | container port number                                                    |
| postgres_database_schema                | public                                        | database schema name                                                     |
| postgres_dbname                         | io_avstats_db                                 | database name                                                            |
| postgres_dbname_admin                   | postgres                                      | administration database name                                             |
| postgres_host                           | db                                            | database server hostname                                                 |
| postgres_password                       | postgresql                                    | database password                                                        |
| postgres_password_admin                 | postgresql                                    | administration database password                                         |
| postgres_pgdata                         | data/postgres                                 | file directory on the host for the database files                        |
| postgres_user                           | io_aero                                       | database username                                                        |
| postgres_user_admin                     | postgres                                      | administration database username                                         |
| postgres_version                        | latest                                        | requested PostgreSQL version from DockerHub                              |
| razorsql_jar_file_windows               | C:\\Program Files\\RazorSQL\\razorsql.jar     | name of the jar file (Windows version)                                   |
| razorsql_java_path_windows              | C:\\Program Files\\RazorSQL\\jre11\\bin\\java | name of the Java file (Windows version)                                  |
| razorsql_profile                        | IO-AVSTATS                                    | name of the RazorSQL connection profile                                  |
| razorsql_reference_dir                  | data/RazorSQL                                 | file directory of the database schema reference file                     |
| razorsql_reference_file                 | 2022.11.01_avall.sql                          | file name of the database schema reference file                          |
| streamlit_server_port                   | 8501                                          | Streamlit port number                                                    |
| streamlit_server_port_faaus2008         | 8501                                          | Streamlit port number for application faaus2008                          |
| streamlit_server_port_pdus2008          | 8502                                          | Streamlit port number for application pdus2008                           |

## 2. Notes

1. The configuration parameters `postgres_password` and `postgres_password_admin` can be found in the configuration file `.settings.io_avstats.toml`.
2. The configuration parameters in the configuration files can be overridden with corresponding environment variables, e.g. the environment variable `IO_AVSTATS_IS_VERBOSE` overrides the configuration parameter `is_verbose`. 
