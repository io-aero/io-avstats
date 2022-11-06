# IO-AVSTATS - Operation

The main tool for operating **IO-AVSTATS** is the `run_io_avstats` script. 
The script is available in a Windows command line version and in a Linux bash shell version.

The following tasks can be executed with this script:

| Code    | Task                                       | Additional parameter(s) |
|---------|--------------------------------------------|-------------------------|
| `c_d_s` | PostgreSQL: Create the database schema     |                         |
| `d_d_f` | PostgreSQL: Delete the database files      |                         |
| `d_d_s` | PostgreSQL: Drop the database schema       |                         |
| `d_m_a` | PostgreSQL: Download Microsoft Access file | msaccess                |
| `l_m_a` | PostgreSQL: Load Microsoft Access data     | msaccess                |
| `s_d_c` | PostgreSQL: Set up the database container  |                         |

## 1. Detailed task list

### 1.1 `c_d_s` - PostgreSQL: Create the database schema

The creation of the database schema includes the following steps, among others:

1. creation of a new database user, and
2. creation of a new database, and
3. creation of database objects such as database tables and so on.

The following parameters are used when creating the database schema:

- `postgres_dbname_admin` - administration database name
- `postgres_password_admin` - administration database password
- `postgres_user_admin` - administration database username

Successful creation of a new database schema requires that neither the user to be created nor the database to be created exists in the PostgreSQL DBMS.
This is achieved by the previous execution of the following task:

- `d_d_s` - PostgreSQL: Drop the database schema

Example protocol:

    ===============================================================================.
    INFO.00.004 Start Launcher.
    INFO.00.001 The logger is configured and ready.
    INFO.00.005 Argument task='c_d_s'.
    -------------------------------------------------------------------------------.
    INFO.00.016 Database user is available: io_aero.
    INFO.00.017 Database is available: io_avstats_db.
    INFO.00.007 Database table is available: events.
    INFO.00.007 Database table is available: aircraft.
    INFO.00.007 Database table is available: dt_events.
    INFO.00.007 Database table is available: ntsb_admin.
    INFO.00.007 Database table is available: dt_aircraft.
    INFO.00.007 Database table is available: engines.
    INFO.00.007 Database table is available: events_sequence.
    INFO.00.007 Database table is available: findings.
    INFO.00.007 Database table is available: flight_crew.
    INFO.00.007 Database table is available: injury.
    INFO.00.007 Database table is available: narratives.
    INFO.00.007 Database table is available: occurrences.
    INFO.00.007 Database table is available: dt_flight_crew.
    INFO.00.007 Database table is available: flight_time.
    INFO.00.007 Database table is available: seq_of_events.
    -------------------------------------------------------------------------------.
           2,918,000,200 ns - Total time launcher.
    INFO.00.006 End   Launcher.
    ===============================================================================.

### 1.2 `d_d_f` - PostgreSQL: Delete the database files

This task deletes all PostgreSQL database files.
The execution requires administration rights.
Subsequently, the PostgreSQL database must be completely rebuilt.

**Tip**: The administration password is required to use the administration rights. 
This can be difficult with the Windows operating system, as there seems to be no functionality to set the administration password. 
The use of the Windows Subsystem for Linux can help here. 

### 1.3 `d_d_s` - PostgreSQL: Delete the database schema

Successful execution of this task requires that the existing database files are empty.
This is achieved by the previous execution of the following two tasks:

1. `d_d_f` - PostgreSQL: Delete the database files
2. `s_d_c` - PostgreSQL: Set up the database container

Example protocol:

    ===============================================================================.
    INFO.00.004 Start Launcher.
    INFO.00.001 The logger is configured and ready.
    INFO.00.005 Argument task='d_d_s'.
    -------------------------------------------------------------------------------.
    INFO.00.019 Database is dropped: io_avstats_db.
    INFO.00.018 Database user is dropped: io_aero.
    -------------------------------------------------------------------------------.
           1,083,501,100 ns - Total time launcher.
    INFO.00.006 End   Launcher.
    ===============================================================================.

### 1.4 `d_m_a` - PostgreSQL: Download Microsoft Access file

This task allows files containing aviation accident data to be downloaded from the NTSB download site.
These files are there as Microsoft Access databases in a compressed format.
The following subtasks are executed:

1. A connection to the NTSB download page is established.
2. The selected file is downloaded to the local system in chunks. 
3. The downloaded file is then unpacked. 
4. A script with the database schema definition is created with RazorSQL from the downloaded database.
5. The newly created script is then compared with a reference script for matching.

Example protocol:

    ===============================================================================.
    INFO.00.004 Start Launcher.
    INFO.00.001 The logger is configured and ready.
    INFO.00.008 Arguments task='d_m_a' msaccess='up22OCT'.
    -------------------------------------------------------------------------------.
    INFO.00.013 The connection to the MS Access database file 'up22OCT.zip' on the NTSB download page was successfully established.
    INFO.00.014 From the file 'up22OCT.zip' 2 chunks were downloaded.
    INFO.00.015 The file 'up22OCT.zip'  was successfully unpacked.
    INFO.00.011 The DDL script for the MS Access database 'up22OCT.mdb' was created successfully.
    INFO.00.012 The DDL script for the MS Access database 'up22OCT.mdb' is identical to the reference script.
    -------------------------------------------------------------------------------.
          2,479,000,200 ns - Total time launcher.
    INFO.00.006 End   Launcher.
    ===============================================================================.

### 1.5 `l_m_a` - PostgreSQL: Load Microsoft Access data


### 1.6 `s_d_c` - PostgreSQL: Set up the database container

The default installation of the PostgreSQL database is done using the official Docker images from Dockerhub - see [here](https://hub.docker.com/_/postgres){:target="_blank"}.

This task consists of the following steps:

1. any running Docker container is stopped.
2. any existing Docker container is deleted.
3. if not already present, the file directory for the PostgreSQL database files is created.
4. the Docker network for the PostgreSQL database is created if it does not already exist.
5. the PostgreSQL Docker image is either created or updated based on DockerHub.
6. a new PostgreSQL Docker container is started.

## 2. First installation

## 3. Regular updates