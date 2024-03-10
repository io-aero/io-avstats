========================
Configuration IO-AVSTATS
========================

For the administration of the configuration parameters of **IO-AVSTATS** the tool `dynaconf <https://www.dynaconf.com>`_ is used.
The file ``settings.io_aero.toml`` is available as the configuration file.
The names of **IO-AVSTATS** related environment variables must include the prefix ``IO_AERO``.
Layered environments are supported.
The ``test`` layer is used for the automated tests.

Available Parameters
---------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Parameter
     - Description
   * - correction_work_dir
     - file directory containing the files with the manual corrections
   * - database_commit_size
     - number of rows processed before a progress message is created
   * - download_chunk_size
     - chunk size for download from the **NTSB** website
   * - download_file_aviation_occurrence_categories
     - name of the file containing data of aviation occurrence categories
   * - download_file_countries_states_json
     - name of the file containing data of countries and states
   * - download_file_faa_airports_xlsx
     - name of the file containing data of airports
   * - download_file_faa_npias
     - name of the file containing National Plan of Integrated Airport Systems
   * - download_file_faa_runways_xlsx
     - name of the file containing data of runways
   * - download_file_main_phases_of_flight_xlsx
     - name of the file containing data of main phases of a flight
   * - download_file_sequence_of_events
     - name of the file containing data of sequence of events
   * - download_file_simplemaps_us_cities_xlsx
     - simplemaps: name of the zipped US city file
   * - download_file_simplemaps_us_zips_xlsx
     - simplemaps: name of the zipped US zip code file
   * - download_file_zip_codes_org_xls
     - ZIP Code Database: name of the unzipped US zip code file
   * - download_timeout
     - seconds to wait for the server to send data
   * - download_url_ntsb_prefix
     - prefix of the download link for the **NTSB** data sets
   * - download_work_dir
     - working directory for the processing of **NTSB** data sets
   * - is_runtime_environment_local
     - local execution environment - unlike Docker
   * - is_verbose
     - display progress messages for processing
   * - max_deviation_latitude
     - maximum decimal deviation of the latitude in the database table even
   * - max_deviation_longitude
     - maximum decimal deviation of the longitude in the database table even
   * - odbc_connection_string
     - connection string for the MS Access ODBC driver
   * - postgres_connection_port
     - database port number
   * - postgres_container_name
     - container name
   * - postgres_database_schema
     - database schema name
   * - postgres_dbname
     - database name
   * - postgres_dbname_admin
     - administration database name
   * - postgres_host
     - database server hostname
   * - postgres_password
     - database password
   * - postgres_password_admin
     - administration database password
   * - postgres_password_guest
     - guest database password
   * - postgres_pgdata
     - file directory on the host for the database files
   * - postgres_user
     - database username
   * - postgres_user_admin
     - administration database username
   * - postgres_user_guest
     - guest database username
   * - postgres_version
     - requested PostgreSQL version from DockerHub
   * - razorsql_jar_file_windows
     - name of the jar file (Windows version)
   * - razorsql_java_path_windows
     - name of the Java file (Windows version)
   * - razorsql_profile
     - name of the RazorSQL connection profile
   * - razorsql_reference_dir
     - file directory of the database schema reference file
   * - razorsql_reference_file
     - file name of the database schema reference file

Example
-------

.. code-block::

    [default]
    check_value = "default"
    correction_work_dir = "data/correction"
    database_commit_size = 10000
    download_chunk_size = 524288
    ...

    [test]
    check_value = "test"
    correction_work_dir = "data/correction_test"
    download_work_dir = "data/download_test"
    postgres_connection_port = 5433
    postgres_container_name = "io_avstats_db_test"
    postgres_password = "postgres_password"
    postgres_password_admin = "postgres_password_admin"
    postgres_pgdata ="data/postgres_test"

Notes
-----

The configuration parameters in the configuration files can be overridden with corresponding environment variables, e.g. the environment variable ``IO_AERO_IS_VERBOSE`` overrides the configuration parameter ``is_verbose``.
