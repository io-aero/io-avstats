# IO-AVSTATS - Configuration

For the administration of the configuration parameters of **IO-AVSTATS** the tool [**dynaconf**](https://www.dynaconf.com){:target="_blank"} is used.
The two files `settings.io_avstats.toml` and `.settings.io_avstats.toml` are available as configuration files.
The names of **IO-AVSTATS** related environment variables must include the prefix `IO_AVSTATS`.
Layered environments are supported.
The `test` layer is used for the automated tests.

### Available Parameters:

| Parameter                  | Default value                                 | Description                                                   |
|----------------------------|-----------------------------------------------|---------------------------------------------------------------|
| is_verbose                 | true                                          | output of progress messages                                   |
| msaccess_chunk_size        | 10000                                         | number of rows processed before a progress message is created |
| ntsb_chunk_size            | 524288                                        | chunk size for download from NTSB website                     |
| ntsb_timeout               | 10                                            | seconds to wait for the server to send data                   |
| ntsb_url_prefix            | https://data.ntsb.gov/...                     | prefix of the download link for the NTSB data sets            |
| ntsb_work_dir              | data/NTSB                                     | working directory for the processing of NTSB data sets        |
| odbc_connection_string     | Driver={Microsoft Access Driver ...           | connection string for the Microsoft Access ODBC driver        |
| postgres_connection_port   | 5432                                          | databasse IP address                                          |
| postgres_container_name    | io_avstats_container                          | container name                                                |
| postgres_container_port    | 5432                                          | container IP address                                          |
| postgres_dbname            | io_avstats_db                                 | database name                                                 |
| postgres_dbname_admin      | postgres                                      | administration database name                                  |
| postgres_host              | localhost                                     | database server hostname                                      |
| postgres_net               | io_avstats_net                                | Docker network name                                           |
| postgres_password          | postgresql                                    | database password                                             |
| postgres_password_admin    | postgresql                                    | administration database password                              |
| postgres_pgdata            | data/postgres                                 | file directory on the host for the database files             |
| postgres_user              | io_aero                                       | database username                                             |
| postgres_user_admin        | postgres                                      | administration database username                              |
| postgres_version           | latest                                        | requested PostgreSQL version from DockerHub                   |
| razorsql_jar_file_windows  | C:\\Program Files\\RazorSQL\\razorsql.jar     | name of the jar file (Windows version)                        |
| razorsql_java_path_windows | C:\\Program Files\\RazorSQL\\jre11\\bin\\java | name of the Java file (Windows version)                       |
| razorsql_profile           | IO-AVSTATS                                    | name of the RazorSQL connection profile                       |
| razorsql_reference_dir     | data/RazorSQL                                 | file directory of the database schema reference file          |
| razorsql_reference_file    | 2022.11.01_avall.sql                          | file name of the database schema reference file               |

### Notes:

1. The configuration parameters `postgres_password` and `postgres_password_admin` can be found in the configuration file `.settings.io_avstats.toml` which is not a part of the repository.
2. The configuration parameters in the configuration files can be overridden with corresponding environment variables, e.g. the environment variable `IO_AVSTATS_IS_VERBOSE` overrides the configuration parameter `is_verbose`. 
