# Operation


Please see [here](https://github.com/io-aero/io-avstats/blob/main/docs/operation.md){:target="_blank"}



The main tool for operating **IO-AVSTATS** is the **`run_io_avstats`** script. 
The script is available in a Windows command line version and in a Linux bash shell version.

The following tasks can be executed with this script:

| Code    | Task                                                  | Additional parameter(s) |
|---------|-------------------------------------------------------|-------------------------|
| `c_d_s` | Create the PostgreSQL database schema                 |                         |
| `c_l_l` | Correct decimal US latitudes and longitudes           |                         |
| `c_p_d` | Cleansing PostgreSQL data                             |                         |
| `d_d_f` | Delete the PostgreSQL database files                  |                         |
| `d_d_s` | Drop the PostgreSQL database schema                   |                         |
| `d_n_a` | Download a **NTSB** MS Access database file           | -m / -msaccess          |
| `d_s_f` | Download basic **simplemaps** files                   |                         |
| `d_z_f` | Download the ZIP Code Database file                   |                         |
| `l_c_d` | Load data from a correction file into PostgreSQL      | -c / -correction        |
| `l_c_s` | Load country and state data into PostgreSQL           |                         |
| `l_n_a` | Load **NTSB** MS Access database data into PostgreSQL | -m / -msaccess          |
| `l_s_d` | Load **simplemaps** data into PostgreSQL              |                         |
| `l_z_d` | Load ZIP Code Database data into PostgreSQL           |                         |
| `r_d_s` | Refresh the PostgreSQL database schema              |                         |
| `s_d_c` | Set up the PostgreSQL database container              |                         |
| `u_d_s` | Update the PostgreSQL database schema                 |                         |
| `v_n_d` | Verify selected **NTSB** data                         |                         |

## 1. Detailed task list

### 1.1 **`c_d_s`** - Create the PostgreSQL database schema

The creation of the database schema includes the following steps, among others:

1. creation of a new database user, and
2. creation of a new database, and
3. creation of database objects such as database tables and so on.

The following parameters are used when creating the database schema:

- `postgres_dbname_admin` - administration database name
- `postgres_password_admin` - administration database password
- `postgres_user_admin` - administration database username

Subsequently, the task **`u_d_s`** (Update the PostgreSQL database schema) is also executed.

Successful creation of a new database schema requires that neither the user to be created nor the database to be created exists in the PostgreSQL DBMS.
This is achieved by the previous execution of the following task:

- **`d_d_s`** - Drop the PostgreSQL database schema

Example protocol:

    Progress update 2022-11-26 02:25:26.802413 : ===============================================================================.
    Progress update 2022-11-26 02:25:26.802413 : INFO.00.004 Start Launcher.
    Progress update 2022-11-26 02:25:26.804413 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-26 02:25:26.812413 : INFO.00.005 Argument task='c_d_s'.
    Progress update 2022-11-26 02:25:26.812413 : -------------------------------------------------------------------------------.
    Progress update 2022-11-26 02:25:26.812413 : INFO.00.044 Creating the database schema.
    Progress update 2022-11-26 02:25:26.812913 : --------------------------------------------------------------------------------
    Progress update 2022-11-26 02:25:26.899052 : INFO.00.016 Database user is available: io_aero.
    Progress update 2022-11-26 02:25:27.874113 : INFO.00.017 Database is available: io_avstats_dev_db.
    Progress update 2022-11-26 02:25:28.024496 : INFO.00.007 Database table is available: events.
    Progress update 2022-11-26 02:25:28.132516 : INFO.00.007 Database table is available: aircraft.
    Progress update 2022-11-26 02:25:28.191012 : INFO.00.007 Database table is available: dt_events.
    Progress update 2022-11-26 02:25:28.241033 : INFO.00.007 Database table is available: ntsb_admin.
    Progress update 2022-11-26 02:25:28.298867 : INFO.00.007 Database table is available: dt_aircraft.
    Progress update 2022-11-26 02:25:28.357619 : INFO.00.007 Database table is available: engines.
    Progress update 2022-11-26 02:25:28.415529 : INFO.00.007 Database table is available: events_sequence.
    Progress update 2022-11-26 02:25:28.465931 : INFO.00.007 Database table is available: findings.
    Progress update 2022-11-26 02:25:28.666134 : INFO.00.007 Database table is available: flight_crew.
    Progress update 2022-11-26 02:25:28.757239 : INFO.00.007 Database table is available: injury.
    Progress update 2022-11-26 02:25:28.840655 : INFO.00.007 Database table is available: narratives.
    Progress update 2022-11-26 02:25:28.890426 : INFO.00.007 Database table is available: occurrences.
    Progress update 2022-11-26 02:25:28.940723 : INFO.00.007 Database table is available: dt_flight_crew.
    Progress update 2022-11-26 02:25:28.990598 : INFO.00.007 Database table is available: flight_time.
    Progress update 2022-11-26 02:25:29.057116 : INFO.00.007 Database table is available: seq_of_events.
    Progress update 2022-11-26 02:25:29.107615 : INFO.00.007 Database table is available: io_countries.
    Progress update 2022-11-26 02:25:29.157116 : INFO.00.007 Database table is available: io_states.
    Progress update 2022-11-26 02:25:29.224119 : INFO.00.007 Database table is available: io_lat_lng.
    Progress update 2022-11-26 02:25:29.290617 : INFO.00.007 Database table is available: io_processed_files.
    Progress update 2022-11-26 02:25:29.290617 : --------------------------------------------------------------------------------
    Progress update 2022-11-26 02:25:29.290617 : INFO.00.045 Updating the database schema.
    Progress update 2022-11-26 02:25:29.291115 : --------------------------------------------------------------------------------
    Progress update 2022-11-26 02:25:29.407115 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_city'.
    Progress update 2022-11-26 02:25:29.432118 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_country'.
    Progress update 2022-11-26 02:25:29.457114 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_dec_lat_lng_actions'.
    Progress update 2022-11-26 02:25:29.482114 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_dec_latitude'.
    Progress update 2022-11-26 02:25:29.507115 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_dec_longitude'.
    Progress update 2022-11-26 02:25:29.532116 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_deviating_latitude'.
    Progress update 2022-11-26 02:25:29.557114 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_deviating_longitude'.
    Progress update 2022-11-26 02:25:29.582115 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_latitude'.
    Progress update 2022-11-26 02:25:29.607614 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_longitude'.
    Progress update 2022-11-26 02:25:29.632114 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_us_city'.
    Progress update 2022-11-26 02:25:29.657614 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_us_state'.
    Progress update 2022-11-26 02:25:29.682117 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_us_zipcode'.
    Progress update 2022-11-26 02:25:29.707116 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_latitude'.
    Progress update 2022-11-26 02:25:29.731616 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_longitude'.
    Progress update 2022-11-26 02:25:29.756848 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_site_zipcode'.
    Progress update 2022-11-26 02:25:29.781847 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_state'.
    Progress update 2022-11-26 02:25:29.806863 : INFO.00.032 Database view is available: io_accidents_us_1982.
    Progress update 2022-11-26 02:25:29.831848 : INFO.00.032 Database view is available: io_lat_lng_issues.
    Progress update 2022-11-26 02:25:29.831848 : -------------------------------------------------------------------------------.
    Progress update 2022-11-26 02:25:29.832351 :        3,172,935,000 ns - Total time launcher.
    Progress update 2022-11-26 02:25:29.832351 : INFO.00.006 End   Launcher.
    Progress update 2022-11-26 02:25:29.832351 : ===============================================================================.

### 1.2 **`c_l_l`** - Correct decimal US latitudes and longitudes

TODO

Example protocol:

    Progress update 2022-11-29 14:26:53.195199 : ===============================================================================.
    Progress update 2022-11-29 14:26:53.195199 : INFO.00.004 Start Launcher.
    Progress update 2022-11-29 14:26:53.197199 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-29 14:26:53.205699 : INFO.00.005 Argument task='c_l_l'.
    Progress update 2022-11-29 14:26:53.205699 : -------------------------------------------------------------------------------.
    Progress update 2022-11-29 14:26:53.205699 : INFO.00.040 Correct decimal US latitudes and longitudes.
    Progress update 2022-11-29 14:26:53.205699 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:26:56.179717 : Number of rows so far read :   5000.
    Progress update 2022-11-29 14:26:56.217217 : Number of rows so far read :  10000.
    Progress update 2022-11-29 14:26:56.255218 : Number of rows so far read :  15000.
    Progress update 2022-11-29 14:26:56.350217 : Number of rows so far read :  20000.
    Progress update 2022-11-29 14:26:56.418218 : Number of rows so far read :  25000.
    Progress update 2022-11-29 14:26:56.506301 : Number of rows so far read :  30000.
    Progress update 2022-11-29 14:26:56.544302 : Number of rows so far read :  35000.
    Progress update 2022-11-29 14:26:56.582301 : Number of rows so far read :  40000.
    Progress update 2022-11-29 14:26:58.644218 : Number of rows so far read :  45000.
    Progress update 2022-11-29 14:27:04.165484 : Number of rows so far read :  50000.
    Progress update 2022-11-29 14:27:04.202984 : Number of rows so far read :  55000.
    Progress update 2022-11-29 14:27:04.264984 : Number of rows so far read :  60000.
    Progress update 2022-11-29 14:27:04.302484 : Number of rows so far read :  65000.
    Progress update 2022-11-29 14:27:04.340484 : Number of rows so far read :  70000.
    Progress update 2022-11-29 14:27:04.378484 : Number of rows so far read :  75000.
    Progress update 2022-11-29 14:27:04.416985 : Number of rows so far read :  80000.
    Progress update 2022-11-29 14:27:04.454984 : Number of rows so far read :  85000.
    Progress update 2022-11-29 14:27:04.494488 : Number of rows so far read :  90000.
    Progress update 2022-11-29 14:27:04.533484 : Number of rows so far read :  95000.
    Progress update 2022-11-29 14:27:26.444050 : Number of rows so far read : 100000.
    Progress update 2022-11-29 14:28:59.310881 : Number of rows so far read : 105000.
    Progress update 2022-11-29 14:29:13.783233 : Number of rows so far read : 110000.
    Progress update 2022-11-29 14:30:30.710774 : Number of rows so far read : 115000.
    Progress update 2022-11-29 14:32:47.465443 : Number of rows so far read : 120000.
    Progress update 2022-11-29 14:35:07.660574 : Number of rows so far read : 125000.
    Progress update 2022-11-29 14:37:26.256310 : Number of rows so far read : 130000.
    Progress update 2022-11-29 14:39:43.194030 : Number of rows so far read : 135000.
    Progress update 2022-11-29 14:39:43.332530 : Number rows selected : 135081.
    Progress update 2022-11-29 14:39:43.332530 : Number rows updated  :  26989.
    Progress update 2022-11-29 14:39:43.333028 : -------------------------------------------------------------------------------.
    Progress update 2022-11-29 14:39:43.333028 :      770,285,829,500 ns - Total time launcher.
    Progress update 2022-11-29 14:39:43.333028 : INFO.00.006 End   Launcher.
    Progress update 2022-11-29 14:39:43.333028 : ===============================================================================.


### 1.3 **`c_p_d`** - Cleansing PostgreSQL data

The task cleans up data abnormalities in the database. 
This includes the following activities:

- remove trailing whitespace in string data types (trimming),
- converting string data types that contain only whitespace to NULL (nullifying).

As a result, a much simplified simplification of data is possible, e.g. for comparisons.

The functionality is limited to the following database columns:

| DB table | DB columns                                    |
|----------|-----------------------------------------------|
| events   | ev_city, ev_site_zipcode, latitude, longitude |

On the one hand, the task can be executed explicitly with the **`run_io_avstats_db`** script (task **`c_p_d`**) and, on the other hand, it always runs after loading NTSB MS Access data into the PostgreSQL database (task **`l_n_a`**).

Example protocol:

    Progress update 2022-11-29 13:03:13.182527 : ===============================================================================.
    Progress update 2022-11-29 13:03:13.182527 : INFO.00.004 Start Launcher.
    Progress update 2022-11-29 13:03:13.184528 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-29 13:03:13.192529 : INFO.00.005 Argument task='c_p_d'.
    Progress update 2022-11-29 13:03:13.193028 : -------------------------------------------------------------------------------.
    Progress update 2022-11-29 13:03:13.193028 : INFO.00.065 Cleansing PostgreSQL data.
    Progress update 2022-11-29 13:03:13.193028 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 13:03:13.264027 : INFO.00.066 Cleansing table 'events' column 'ev_city'.
    Progress update 2022-11-29 13:03:14.812228 : Number cols trimmed  :  47967.
    Progress update 2022-11-29 13:03:14.853583 : Number cols nullified:      4.
    Progress update 2022-11-29 13:03:14.854085 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 13:03:14.854085 : INFO.00.066 Cleansing table 'events' column 'ev_site_zipcode'.
    Progress update 2022-11-29 13:03:15.795002 : Number cols trimmed  :  48691.
    Progress update 2022-11-29 13:03:15.870127 : Number cols nullified:   2299.
    Progress update 2022-11-29 13:03:15.870127 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 13:03:15.870632 : INFO.00.066 Cleansing table 'events' column 'latitude'.
    Progress update 2022-11-29 13:03:16.720436 : Number cols trimmed  :  42292.
    Progress update 2022-11-29 13:03:17.979937 : Number cols nullified:  42292.
    Progress update 2022-11-29 13:03:17.980436 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 13:03:17.980436 : INFO.00.066 Cleansing table 'events' column 'longitude'.
    Progress update 2022-11-29 13:03:19.136341 : Number cols trimmed  :  42292.
    Progress update 2022-11-29 13:03:21.218871 : Number cols nullified:  42292.
    Progress update 2022-11-29 13:03:21.218871 : -------------------------------------------------------------------------------.
    Progress update 2022-11-29 13:03:21.218871 :        8,180,840,400 ns - Total time launcher.
    Progress update 2022-11-29 13:03:21.219372 : INFO.00.006 End   Launcher.
    Progress update 2022-11-29 13:03:21.219372 : ===============================================================================.

### 1.4 **`d_d_f`** - Delete the PostgreSQL database files

This task deletes all PostgreSQL database files.
The execution requires administration rights.
Subsequently, the PostgreSQL database must be completely rebuilt.

**Tip**: The administration password is required to use the administration rights. 
This can be difficult with the Windows operating system, as there seems to be no functionality to set the administration password. 
The use of the Windows Subsystem for Linux can help here. 

### 1.5 **`d_d_s`** - Drop the PostgreSQL database schema

Successful execution of this task requires that no other process uses the database defined with the **`postgres_dbname`** parameter.
After execution, the database with all objects and the database user defined with the **`postgres_user`** parameter are deleted.

Example protocol:

    Progress update 2022-11-22 19:40:05.757556 : ===============================================================================.
    Progress update 2022-11-22 19:40:05.757556 : INFO.00.004 Start Launcher.
    Progress update 2022-11-22 19:40:05.762558 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-22 19:40:05.771056 : INFO.00.005 Argument task='d_d_s'.
    Progress update 2022-11-22 19:40:05.771558 : -------------------------------------------------------------------------------.
    Progress update 2022-11-22 19:40:05.771558 : INFO.00.046 Dropping the database schema.
    Progress update 2022-11-22 19:40:05.771558 : -------------------------------------------------------------------------------.
    Progress update 2022-11-22 19:40:06.742328 : INFO.00.019 Database is dropped: io_avstats_db.
    Progress update 2022-11-22 19:40:06.775829 : INFO.00.018 Database user is dropped: io_aero.
    Progress update 2022-11-22 19:40:06.775829 : -------------------------------------------------------------------------------.
    Progress update 2022-11-22 19:40:06.775829 :        1,186,272,600 ns - Total time launcher.
    Progress update 2022-11-22 19:40:06.775829 : INFO.00.006 End   Launcher.
    Progress update 2022-11-22 19:40:06.776329 : ===============================================================================.

### 1.6 **`d_n_a`** - Download a **NTSB** MS Access database file

This task allows files containing aviation accident data to be downloaded from the **NTSB** download site.
These files are there as MS Access databases in a compressed format.
The following subtasks are executed:

1. A connection to the **NTSB** download page is established.
2. The selected file is downloaded to the local system in chunks. 
3. The downloaded file is then unpacked. 
4. A script with the database schema definition is created with RazorSQL from the downloaded database.
5. The newly created script is then compared with a reference script for matching.

Subsequently, the downloaded data can be loaded into the PostgreSQL database with the task **`l_n_a`** (Load **NTSB** MS Access database data into PostgreSQL).

Further details can be found [here](https://github.com/io-aero/io-avstats-db/blob/main/site/db_data_transfer.html){:target="_blank"}.

Example protocol:

    Progress update 2022-11-23 12:20:05.623207 : ===============================================================================.
    Progress update 2022-11-23 12:20:05.623207 : INFO.00.004 Start Launcher.
    Progress update 2022-11-23 12:20:05.625207 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-23 12:20:05.633207 : INFO.00.008 Arguments task='d_n_a' msaccess='up22oct'.
    Progress update 2022-11-23 12:20:05.633707 : -------------------------------------------------------------------------------.
    Progress update 2022-11-23 12:20:05.633707 : INFO.00.047 Downloading NTSB MS Access database file 'up22OCT'.
    Progress update 2022-11-23 12:20:05.633707 : --------------------------------------------------------------------------------
    Progress update 2022-11-23 12:20:06.163453 : INFO.00.013 The connection to the MS Access database file 'up22OCT.zip' on the NTSB download page was successfully established.
    Progress update 2022-11-23 12:20:07.188487 : INFO.00.014 From the file 'up22OCT.zip' 2 chunks were downloaded.
    Progress update 2022-11-23 12:20:07.206986 : INFO.00.015 The file 'up22OCT.zip' was successfully unpacked.
    Progress update 2022-11-23 12:20:07.218987 : INFO.00.051 msaccess_file     ='D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\data\download\IO-AVSTATS.mdb'.
    Progress update 2022-11-23 12:20:07.219487 : INFO.00.051 msaccess_file     ='D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\data\download\up22OCT.sql'.
    Progress update 2022-11-23 12:20:07.219487 : INFO.00.052 razorsql_jar_file ='C:\Program Files\RazorSQL\razorsql.jar'.
    Progress update 2022-11-23 12:20:07.219487 : INFO.00.053 razorsql_java_path='C:\Program Files\RazorSQL\jre11\bin\java'.
    1669202407306: launching RazorSQL . . .
    1669202407307: args . . .
    -backup
    IO-AVSTATS
    null
    null
    ;
    null
    D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\data\download\up22OCT.sql
    NO
    tables
    YES
    null
    NO
    NO
    1669202407342: userName: walte
    1669202407342: libraryPath: C:\Program Files\RazorSQL\jre11\bin;C:\WINDOWS\Sun\Java\bin;C:\WINDOWS\system32;C:\WINDOWS;C:\Users\walte\.virtualenvs\io-avstats-db-NXLRYNgF\Scripts;C:\Program Files (x86)\VMware\VMware Player\bin\;C:\Program Files (x86)\infogridpacific\AZARDI;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\Calibre2\;C:\Program Files\dotnet\;C:\Program Files\Git LFS;C:\Program Files\Microsoft SQL Server\110\Tools\Binn\;C:\Program Files\NVIDIA Corporation\NVIDIA NvDLISR;C:\Program Files\Pandoc\;C:\Program Files\TortoiseGit\bin;C:\Software\GnuWin32\bin;C:\WINDOWS;C:\WINDOWS\system32;C:\WINDOWS\System32\OpenSSH\;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\Users\walte\.nimble\bin;C:\Windows;C:\Windows\system32;C:\Windows\System32\OpenSSH\;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Software\.cargo\bin;%GRADLE_HOME%\bin;%HOME_ELIXIR%\bin;%HOME_ERLANG%\bin;%HOME_GO%\bin;%HOME_JULIA%\bin;%HOME_NIM%\bin;C:\Software\PostgreSQL\15\bin;C:\Software\poppler-0.68.0\bin;C:\Software\Python\Python310;C:\Software\Python\Python310\Scripts;C:\Software\rebar3;%HOME_RUST%\bin;C:\Software\Tesseract-OCR;C:\Software\jdk-18.0.2\bin;%KOTLIN_HOME%\bin;C:\Software\oracle\instantclient_21_6;C:\Software\Gpg4win\..\GnuPG\bin;C:\Program Files\Git\cmd;C:\Program Files\LLVM\bin;C:\Program Files\nodejs\;C:\Program Files\Docker\Docker\resources\bin;C:\Users\walte\.cargo\bin;C:\Users\walte\AppData\Local\Microsoft\WindowsApps;C:\Software\Microsoft VS Code\bin;C:\Users\walte\go\bin;C:\Software\texlive\2021\bin\win32;c:\users\walte\.local\bin;C:\Users\walte\AppData\Local\JetBrains\Toolbox\scripts;C:\Users\walte\AppData\Roaming\npm;.
    1669202407343: javaVersion: 11.0.13
    1669202407343:
    1669202407343: Verifying RazorSQL resources location.
    1669202407343:
    1669202407343: testing base url: / = file:/C:/Program%20Files/RazorSQL/
    1669202407343:
    1669202407344: testString1: file:/C:/Program%20Files/RazorSQL/razorsql.jar
    1669202407344: testString2: file:/C:/Program%20Files/RazorSQL/data/base.ssql
    1669202407344: testFile1: C:\Program Files\RazorSQL\razorsql.jar
    1669202407344: testFile2: C:\Program Files\RazorSQL\data\base.ssql
    1669202407344: both test file exists.  Base URL found.
    1669202407344: resource directory: file:/C:/Program%20Files/RazorSQL/
    1669202407344: user home: C:\Users\walte
    1669202407346: user profile: C:\Users\walte
    1669202407346: app data: C:\Users\walte\AppData\Roaming
    1669202407346: checking write access to: C:\Users\walte\AppData\Roaming
    1669202407346: write dir: C:\Users\walte\AppData\Roaming\RichardsonSoftware
    1669202407346: can write to C:\Users\walte\AppData\Roaming
    1669202407346: user.home: C:\Users\walte\AppData\Roaming
    1669202407346: RazorSQL Scratch Directory: C:\Users\walte\AppData\Roaming\RazorSQL
    1669202407347: RazorSQL Scratch Directory exists
    1669202407347: checking for sub directories
    1669202407347: razorsql launch log: C:\Users\walte\AppData\Roaming\RazorSQL\razorsql_launch_log.txt
    1669202407347: launch log file = C:\Users\walte\AppData\Roaming\RazorSQL\razorsql_launch_log.txt
    1669202407347: Checking for graphics properties
    1669202407348: graphics properties file: C:\Users\walte\AppData\Roaming\RazorSQL\data\graphics_properties.txt
    1669202407348: gOverride: null
    1669202407348: not disabling advanced graphics
    1669202407348: path0: file:/C:/Program%20Files/RazorSQL/data/run.ssql
    1669202407348: path1: file:/C:/Program%20Files/RazorSQL/razorsql.jar
    1669202407348: runArgs: true
    1669202407348: showScreen: false
    1669202407349: args[0]: -backup
    1669202407349: args[1]: IO-AVSTATS
    1669202407349: args[2]: null
    1669202407349: args[3]: null
    1669202407349: args[4]: ;
    1669202407349: args[5]: null
    1669202407349: args[6]: D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\data\download\up22OCT.sql
    1669202407349: args[7]: NO
    1669202407349: args[8]: tables
    1669202407349: args[9]: YES
    1669202407349: args[10]: null
    1669202407349: args[11]: NO
    1669202407349: args[12]: NO
    1669202407349: Command: -backup
    1669202407350: Running -backup
    h: name = C:\Program Files\RazorSQL\data\run.ssql
    h: name = C:\Program Files\RazorSQL\razorsql.jar
    1669202407356: Attempting to load . . .
    command found
    uOne: file:/C:/Program%20Files/RazorSQL/
    h: name = C:\Program Files\RazorSQL\data\run.ssql
    1669202407367reading file . . .C:\Program Files\RazorSQL\data\base.ssql
    1669202407392done reading . . .
    1669202407401done converting
    1669202407401starting lib load.
    1669202407413lib load complete.
    In command line processor
    Max Memory: 30688.0
    Current Total Memory: 2048.0
    Free Memory: 1957.998046875
    1669202407486: r init
    1669202407486: d init
    1669202407487: get default file encoding
    1669202407487: end d init
    custom home directory: null
    Checking for user data from old versions
    1669202407488: user home: C:\Users\walte
    1669202407489: user profile: C:\Users\walte
    1669202407489: app data: C:\Users\walte\AppData\Roaming
    1669202407489: checking write access to: C:\Users\walte\AppData\Roaming
    1669202407489: write dir: C:\Users\walte\AppData\Roaming\RichardsonSoftware
    1669202407489: can write to C:\Users\walte\AppData\Roaming
    newHome: C:\Users\walte\AppData\Roaming\RazorSQL
    dataHome: C:\Users\walte\AppData\Roaming/RazorSQL/data/
    preferences file: C:\Users\walte\AppData\Roaming\RazorSQL\data\preferences.txt
    Profiles Exist
    1669202407499: loading icons
    1669202407663: done r init
    Getting connection data from: IO-AVSTATS
    1669202407665: r init
    1669202407665: d init
    1669202407665: get default file encoding
    1669202407665: end d init
    custom home directory: null
    Checking for user data from old versions
    newHome: C:\Users\walte\AppData\Roaming\RazorSQL
    dataHome: C:\Users\walte\AppData\Roaming/RazorSQL/data/
    preferences file: C:\Users\walte\AppData\Roaming\RazorSQL\data\preferences.txt
    Profiles Exist
    1669202407666: loading icons
    1669202407675: done r init
    getting connection . . .
    Not using SSH Tunnel
    driver: sun.jdbc.odbc.JdbcOdbcDriver
    classLocation: C:\Program Files\RazorSQL\drivers\common\odbc.jar
    loadedCommonJars: false
    commonURL: file:/C:/Program%20Files/RazorSQL/drivers/common/
    commonDir: C:\Program Files\RazorSQL\drivers\common
    commonFiles[0]: file:/C:/Program%20Files/RazorSQL/drivers/common/activation.jar
    commonFiles[1]: file:/C:/Program%20Files/RazorSQL/drivers/common/common.jar
    commonFiles[2]: file:/C:/Program%20Files/RazorSQL/drivers/common/jaxb-api.jar
    commonFiles[3]: file:/C:/Program%20Files/RazorSQL/drivers/common/jaxb-core.jar
    commonFiles[4]: file:/C:/Program%20Files/RazorSQL/drivers/common/jaxb-impl.jar
    commonFiles[6]: file:/C:/Program%20Files/RazorSQL/drivers/common/odbc.jar
    connection type: ODBC
    final classLocation: C:\Program Files\RazorSQL\drivers\common\odbc.jar
    classLocation file: C:\Program Files\RazorSQL\drivers\common\odbc.jar
    building sql manager
    Loading driver
    Done loading driver
    Getting connection with no login info
    JdbcOdbcDriver: in initialize
    OdbcApi == null
    Creating new OdbcApi, nativePrefix:
    JdbcOdbc constructor
    Attempting to load JdbcOdbc library
    Got OdbcApi: sun.jdbc.odbc.JdbcOdbc@2d127a61
    Getting charset
    JdbcOdbcDriver.OdbcApi.charSet: Cp1252
    Connection obtained
    obtained connection
    database major version = 2
    database product name: ACCESS
    multiValueInsert: false
    includeIdentifyColumns: false
    Calling backup . . .
    Retrieving Tables . . .
    Generating Table DDL . . .
    1 of 20
    number of columns 93
    column map size: 93
    foundNull: false
    2 of 20
    number of columns 2
    column map size: 2
    foundNull: false
    3 of 20
    number of columns 11
    column map size: 11
    foundNull: false
    4 of 20
    number of columns 2
    column map size: 2
    foundNull: false
    5 of 20
    number of columns 6
    column map size: 6
    foundNull: false
    6 of 20
    number of columns 5
    column map size: 5
    foundNull: false
    7 of 20
    number of columns 7
    column map size: 7
    foundNull: false
    8 of 20
    number of columns 13
    column map size: 13
    foundNull: false
    9 of 20
    number of columns 17
    column map size: 17
    foundNull: false
    10 of 20
    number of columns 73
    column map size: 73
    foundNull: false
    11 of 20
    number of columns 10
    column map size: 10
    foundNull: false
    12 of 20
    number of columns 13
    column map size: 13
    foundNull: false
    13 of 20
    number of columns 33
    column map size: 33
    foundNull: false
    14 of 20
    number of columns 8
    column map size: 8
    foundNull: false
    15 of 20
    number of columns 7
    column map size: 7
    foundNull: false
    16 of 20
    number of columns 8
    column map size: 8
    foundNull: false
    17 of 20
    number of columns 5
    column map size: 5
    foundNull: false
    18 of 20
    number of columns 8
    column map size: 8
    foundNull: false
    19 of 20
    number of columns 11
    column map size: 11
    foundNull: false
    20 of 20
    number of columns 3
    column map size: 3
    foundNull: false
    Generating Alter Table DDL . . .
    1 of 20
    2 of 20
    3 of 20
    4 of 20
    5 of 20
    6 of 20
    7 of 20
    8 of 20
    9 of 20
    10 of 20
    11 of 20
    12 of 20
    13 of 20
    14 of 20
    15 of 20
    16 of 20
    17 of 20
    18 of 20
    19 of 20
    20 of 20
    backup finished
    closing connection . . .
    connection closed.
    Shutting down logging streams
    Done shutting down logging streams
    Exiting . . .
    Progress update 2022-11-23 12:20:08.292807 : INFO.00.011 The DDL script for the MS Access database 'up22OCT.mdb' was created successfully.
    Progress update 2022-11-23 12:20:08.297807 : INFO.00.012 The DDL script for the MS Access database 'up22OCT.mdb' is identical to the reference script.
    Progress update 2022-11-23 12:20:08.297807 : -------------------------------------------------------------------------------.
    Progress update 2022-11-23 12:20:08.297807 :        2,816,100,200 ns - Total time launcher.
    Progress update 2022-11-23 12:20:08.297807 : INFO.00.006 End   Launcher.
    Progress update 2022-11-23 12:20:08.298305 : ===============================================================================.

### 1.7 **`d_s_f`** - Download basic **simplemaps** files

This task downloads the basic versions of the two databases **`United States Cities`** and **`US Zip Codes`** from the **simplemaps** website to the file directory defined in **`download_work_dir`**.

Subsequently, the downloaded data can be loaded into the PostgreSQL database with the task **`l_s_d`** (Load **simplemaps** data into PostgreSQL).

Further details can be found [here](https://github.com/io-aero/io-avstats-db/blob/main/site/db_data_transfer.html){:target="_blank"}.

Example protocol:

    Progress update 2023-01-16 08:52:42.402122 : ===============================================================================.
    Progress update 2023-01-16 08:52:42.402622 : INFO.00.004 Start Launcher.
    Progress update 2023-01-16 08:52:42.407122 : INFO.00.001 The logger is configured and ready.
    Progress update 2023-01-16 08:52:42.416122 : INFO.00.005 Argument task='d_s_f'.
    Progress update 2023-01-16 08:52:42.416122 : -------------------------------------------------------------------------------.
    Progress update 2023-01-16 08:52:42.416122 : INFO.00.048 Downloading basic simplemaps files.
    Progress update 2023-01-16 08:52:42.416122 : --------------------------------------------------------------------------------
    Progress update 2023-01-16 08:52:42.614735 : INFO.00.030 The connection to the US city file 'simplemaps_uscities_basicv1.75.zip' on the simplemaps download page was successfully established.
    Progress update 2023-01-16 08:52:42.707338 : INFO.00.023 From the file 'simplemaps_uscities_basicv1.75.zip' 8 chunks were downloaded.
    Progress update 2023-01-16 08:52:42.740839 : INFO.00.024 The file 'simplemaps_uscities_basicv1.75.zip' was successfully unpacked.
    Progress update 2023-01-16 08:52:42.907725 : INFO.00.022 The connection to the US zip code file 'simplemaps_uszips_basicv1.81.zip' on the simplemaps download page was successfully established.
    Progress update 2023-01-16 08:52:43.003439 : INFO.00.023 From the file 'simplemaps_uszips_basicv1.81.zip' 8 chunks were downloaded.
    Progress update 2023-01-16 08:52:43.037441 : INFO.00.024 The file 'simplemaps_uszips_basicv1.81.zip' was successfully unpacked.
    Progress update 2023-01-16 08:52:43.037441 : -------------------------------------------------------------------------------.
    Progress update 2023-01-16 08:52:43.037441 :          787,318,600 ns - Total time launcher.
    Progress update 2023-01-16 08:52:43.037441 : INFO.00.006 End   Launcher.
    Progress update 2023-01-16 08:52:43.037939 : ===============================================================================.

### 1.8 **`d_z_f`** - Download the ZIP Code Database file

With this task, the free version of the file [ZIP Code Database](https://www.unitedstateszipcodes.org/zip-code-database/){:target="_blank"} can be downloaded from the website [**United States Zip Codes.org**](https://www.unitedstateszipcodes.org/).
However, since a license window appears first before the actual download, it is better to download the file manually.
Therefore, this task is currently not offered in the **`run_io_avstats_db`** shell script menu.

<kbd>![](img/Zip Codes.org Verify License Terms.png)</kbd>

Example protocol:

    Progress update 2022-11-26 07:12:23.326957 : ===============================================================================.
    Progress update 2022-11-26 07:12:23.326957 : INFO.00.004 Start Launcher.
    Progress update 2022-11-26 07:12:23.328958 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-26 07:12:23.336956 : INFO.00.005 Argument task='d_z_f'.
    Progress update 2022-11-26 07:12:23.337457 : -------------------------------------------------------------------------------.
    Progress update 2022-11-26 07:12:23.337457 : INFO.00.055 Downloading ZIP Code Database file.
    Progress update 2022-11-26 07:12:23.337457 : --------------------------------------------------------------------------------
    
      File "D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\src\launcher.py", line 416, in <module>
        main(sys.argv)
      File "D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\src\launcher.py", line 376, in main
        avstats.download_zip_code_db_file()
      File "D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\src\io_avstats_db\avstats.py", line 98, in download_zip_code_db_file
        db_dml_base.download_zip_code_db_file()
      File "D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\src\io_avstats_db\db_dml_base.py", line 4052, in download_zip_code_db_file
        io_utils.terminate_fatal(
      File "D:\SoftDevelopment\Projects\IO-Aero\io-avstats-db\src\io_avstats_db\io_utils.py", line 99, in terminate_fatal
        traceback.print_stack()
    
    FATAL ERROR: program abort =====>
    FATAL ERROR: program abort =====> ERROR.00.906 Unexpected response status code='403' <===== FATAL ERROR
    FATAL ERROR: program abort =====>
    Processing of the script run_io_avstats was aborted, error code=0

### 1.9 **`l_c_d`** - Load data from a correction file into PostgreSQL

TODO

This task allows files containing aviation accident data to be downloaded from the NTSB download site.
These files are there as MS Access databases in a compressed format.
The following subtasks are executed:

1. A connection to the NTSB download page is established.
2. The selected file is downloaded to the local system in chunks. 
3. The downloaded file is then unpacked. 
4. A script with the database schema definition is created with RazorSQL from the downloaded database.
5. The newly created script is then compared with a reference script for matching.


### 1.10 **`l_c_s`** - Load country and state data into PostgreSQL

TODO

Example protocol:

    Progress update 2022-11-27 14:15:55.817859 : ===============================================================================.
    Progress update 2022-11-27 14:15:55.817859 : INFO.00.004 Start Launcher.
    Progress update 2022-11-27 14:15:55.819858 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-27 14:15:55.827859 : INFO.00.005 Argument task='l_c_s'.
    Progress update 2022-11-27 14:15:55.827859 : -------------------------------------------------------------------------------.
    Progress update 2022-11-27 14:15:55.827859 : INFO.00.057 Loading country and state data.
    Progress update 2022-11-27 14:15:55.828359 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 14:15:55.894605 : INFO.00.059 Loading country data.
    Progress update 2022-11-27 14:15:55.894605 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 14:15:55.954085 : Number rows selected :     52.
    Progress update 2022-11-27 14:15:55.954597 : Number rows inserted :      1.
    Progress update 2022-11-27 14:15:55.954597 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 14:15:55.954597 : INFO.00.060 Loading state data.
    Progress update 2022-11-27 14:15:55.954597 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 14:15:57.545443 : Number rows selected :     52.
    Progress update 2022-11-27 14:15:57.545443 : Number rows inserted :     51.
    Progress update 2022-11-27 14:15:57.570593 : -------------------------------------------------------------------------------.
    Progress update 2022-11-27 14:15:57.570593 :        1,896,734,300 ns - Total time launcher.
    Progress update 2022-11-27 14:15:57.570593 : INFO.00.006 End   Launcher.
    Progress update 2022-11-27 14:15:57.571096 : ===============================================================================.

### 1.11 **`l_n_a`** - Load **NTSB** MS Access database data into PostgreSQL

This task transfers the data from an **NTSB** MS Access database previously downloaded from the **NTSB** website to the PostgreSQL database.
The same MS Access database can be processed several times with this task without any problems, since only the changes are newly transferred to the PostgreSQL database.
The initial loading is done with both **NTSB** MS Access databases Pre2008 ubd avall.
After that only the monthly updates are then transferred. 

Further details can be found [here](https://github.com/io-aero/io-avstats-db/blob/main/site/db_data_transfer.html){:target="_blank"}.

Example protocol:

    Progress update 2022-11-27 14:15:55.817859 : ===============================================================================.
    Progress update 2022-11-27 14:15:55.817859 : INFO.00.004 Start Launcher.
    Progress update 2022-11-27 14:15:55.819858 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-27 14:15:55.827859 : INFO.00.005 Argument task='l_c_s'.
    Progress update 2022-11-27 14:15:55.827859 : -------------------------------------------------------------------------------.
    Progress update 2022-11-27 14:15:55.827859 : INFO.00.057 Loading country and state data.
    Progress update 2022-11-27 14:15:55.828359 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 14:15:55.894605 : INFO.00.059 Loading country data.
    Progress update 2022-11-27 14:15:55.894605 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 14:15:55.954085 : Number rows selected :     52.
    Progress update 2022-11-27 14:15:55.954597 : Number rows inserted :      1.
    Progress update 2022-11-27 14:15:55.954597 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 14:15:55.954597 : INFO.00.060 Loading state data.
    Progress update 2022-11-27 14:15:55.954597 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 14:15:57.545443 : Number rows selected :     52.
    Progress update 2022-11-27 14:15:57.545443 : Number rows inserted :     51.
    Progress update 2022-11-27 14:15:57.570593 : -------------------------------------------------------------------------------.
    Progress update 2022-11-27 14:15:57.570593 :        1,896,734,300 ns - Total time launcher.
    Progress update 2022-11-27 14:15:57.570593 : INFO.00.006 End   Launcher.
    Progress update 2022-11-27 14:15:57.571096 : ===============================================================================.

### 1.12 **`l_n_s`** - Load **NTSB** MS Excel statistic data into PostgreSQL

TODO

Example protocol:

    Progress update 2023-01-15 12:46:10.973510 : ===============================================================================.
    Progress update 2023-01-15 12:46:10.973510 : INFO.00.004 Start Launcher.
    Progress update 2023-01-15 12:46:10.979008 : INFO.00.001 The logger is configured and ready.
    Progress update 2023-01-15 12:46:18.297008 : INFO.00.041 Arguments task='l_n_s' {msexecel}='AviationAccidentStatistics_2002-2021_20221208'.
    Progress update 2023-01-15 12:46:18.297008 : -------------------------------------------------------------------------------.
    Progress update 2023-01-15 12:46:18.297008 : INFO.00.072 Loading NTSB MS Ecel statistic data from file 'AviationAccidentStatistics_2002-2021_20221208'.
    Progress update 2023-01-15 12:46:18.297508 : --------------------------------------------------------------------------------
    Unprocessed row #     1: Table 29. Accident Aircraft, 2002 through 2021, US Civil Aviation | None | None | ...
    Unprocessed row #     2: None | None | None | ...
    Unprocessed row #     3: NTSB Number | Accident Report | Event Date | ...
    Progress update 2023-01-15 12:48:30.355445 : Number of rows so far read :   5000.
    Progress update 2023-01-15 12:50:35.554697 : Number of rows so far read :  10000.
    Progress update 2023-01-15 12:52:39.895361 : Number of rows so far read :  15000.
    Progress update 2023-01-15 12:54:44.828003 : Number of rows so far read :  20000.
    Progress update 2023-01-15 12:56:47.277567 : Number of rows so far read :  25000.
    Progress update 2023-01-15 12:58:50.693799 : Number of rows so far read :  30000.
    Unprocessed row # 30245: None | None | None | ...
    ...
    Unprocessed row # 30729: None | None | None | ...
    Progress update 2023-01-15 12:58:59.416221 : Number rows selected :  30729.
    Progress update 2023-01-15 12:58:59.416723 : Number rows inserted :  30241.
    Progress update 2023-01-15 12:58:59.416723 : Number rows updated  :  90723.
    Progress update 2023-01-15 12:58:59.416723 : -------------------------------------------------------------------------------.
    Progress update 2023-01-15 12:58:59.417222 :      768,612,714,000 ns - Total time launcher.
    Progress update 2023-01-15 12:58:59.417222 : INFO.00.006 End   Launcher.
    Progress update 2023-01-15 12:58:59.417222 : ===============================================================================.

### 1.13 **`l_s_d`** - Load **simplemaps** data into PostgreSQL

TODO

This task transfers the data from an NTSB MS Access database previously downloaded from the NTSB website to the PostgreSQL database.
The same MS Access database can be processed several times with this task without any problems, since only the changes are newly transferred to the PostgreSQL database.
The initial loading is done with both MS Access databases Pre2008 ubd avall.
After that only the monthly updates are then transferred. 

Example protocol:

        Progress update 2022-11-21 18:52:41.629692 : ===============================================================================.
        Progress update 2022-11-21 18:52:41.629692 : INFO.00.004 Start Launcher.
        Progress update 2022-11-21 18:52:41.631692 : INFO.00.001 The logger is configured and ready.
        Progress update 2022-11-21 18:52:41.640190 : INFO.00.005 Argument task='l_s_d'.
        Progress update 2022-11-21 18:52:41.640190 : -------------------------------------------------------------------------------.
        Progress update 2022-11-21 18:52:41.685192 : INFO.00.039 Database table io_lat_lng: Loading the zipcode data from file uscities.xlsx.
        Progress update 2022-11-21 18:55:11.254186 : Number of rows so far read :   5000.
        Progress update 2022-11-21 18:57:31.973745 : Number of rows so far read :  10000.
        Progress update 2022-11-21 18:59:47.094776 : Number of rows so far read :  15000.
        Progress update 2022-11-21 19:02:08.097587 : Number of rows so far read :  20000.
        Progress update 2022-11-21 19:04:27.858850 : Number of rows so far read :  25000.
        Progress update 2022-11-21 19:06:49.294785 : Number of rows so far read :  30000.
        Progress update 2022-11-21 19:09:07.306370 : Number of rows so far read :  35000.
        Progress update 2022-11-21 19:11:28.117981 : Number of rows so far read :  40000.
        Progress update 2022-11-21 19:12:10.470503 : Number rows selected :  41620.
        Progress update 2022-11-21 19:12:10.470503 : Number rows inserted :  41620.
        Progress update 2022-11-21 19:12:10.530003 : INFO.00.025 Database table io_lat_lng: Loading the zipcode data from file uszips.xlsx.
        Progress update 2022-11-21 19:14:41.797284 : Number of rows so far read :   5000.
        Progress update 2022-11-21 19:17:10.506606 : Number of rows so far read :  10000.
        Progress update 2022-11-21 19:19:38.757474 : Number of rows so far read :  15000.
        Progress update 2022-11-21 19:22:08.373896 : Number of rows so far read :  20000.
        Progress update 2022-11-21 19:24:29.851643 : Number of rows so far read :  25000.
        Progress update 2022-11-21 19:26:58.685870 : Number of rows so far read :  30000.
        Progress update 2022-11-21 19:28:47.784316 : Number rows selected :  33788.
        Progress update 2022-11-21 19:28:47.784316 : Number rows inserted :   9651.
        Progress update 2022-11-21 19:28:47.784316 : Number rows updated  :  24133.
        Progress update 2022-11-21 19:28:47.784815 : INFO.00.026 Database table io_us_stats: Loading data.
        Progress update 2022-11-21 19:28:49.122315 : Number rows selected :     56.
        Progress update 2022-11-21 19:28:49.122315 : Number rows inserted :     51.
        Progress update 2022-11-21 19:28:49.122315 : INFO.00.027 Database table io_lat_lng: Loading the city data.
        Progress update 2022-11-21 19:31:05.759170 : Number of rows so far read :   5000.
        Progress update 2022-11-21 19:33:29.969709 : Number of rows so far read :  10000.
        Progress update 2022-11-21 19:35:42.591083 : Number of rows so far read :  15000.
        Progress update 2022-11-21 19:38:00.961652 : Number of rows so far read :  20000.
        Progress update 2022-11-21 19:40:21.097913 : Number of rows so far read :  25000.
        Progress update 2022-11-21 19:42:39.434729 : Number of rows so far read :  30000.
        Progress update 2022-11-21 19:45:05.010766 : Number of rows so far read :  35000.
        Progress update 2022-11-21 19:46:26.359902 : Number rows selected :  37982.
        Progress update 2022-11-21 19:46:26.360403 : Number rows inserted :  37982.
        Progress update 2022-11-21 19:46:26.360403 : INFO.00.028 Database table io_lat_lng: Loading the state data.
        Progress update 2022-11-21 19:46:28.312902 : Number rows selected :     56.
        Progress update 2022-11-21 19:46:28.312902 : Number rows inserted :     56.
        Progress update 2022-11-21 19:46:28.313404 : INFO.00.029 Database table io_lat_lng: Loading the country data.
        Progress update 2022-11-21 19:46:28.346407 : Number rows inserted :      1.
        Progress update 2022-11-21 19:46:28.391904 : INFO.00.027 Database table io_lat_lng: Loading the city data.
        Progress update 2022-11-21 19:48:23.972756 : Number of rows so far read :   5000.
        Progress update 2022-11-21 19:50:01.546746 : Number of rows so far read :  10000.
        Progress update 2022-11-21 19:51:44.317761 : Number of rows so far read :  15000.
        Progress update 2022-11-21 19:53:32.879336 : Number of rows so far read :  20000.
        Progress update 2022-11-21 19:55:18.566257 : Number of rows so far read :  25000.
        Progress update 2022-11-21 19:56:46.677403 : Number of rows so far read :  30000.
        Progress update 2022-11-21 19:56:52.002902 : Number rows selected :  30409.
        Progress update 2022-11-21 19:56:52.003409 : Number rows updated  :  20621.
        Progress update 2022-11-21 19:56:52.003409 : -------------------------------------------------------------------------------.
        Progress update 2022-11-21 19:56:52.003409 :    3,850,528,217,800 ns - Total time launcher.
        Progress update 2022-11-21 19:56:52.003903 : INFO.00.006 End   Launcher.
        Progress update 2022-11-21 19:56:52.003903 : ===============================================================================.

### 1.14 **`l_z_d`** - Load ZIP Code Database data into PostgreSQL

TODO

This task transfers the data from an NTSB MS Access database previously downloaded from the NTSB website to the PostgreSQL database.
The same MS Access database can be processed several times with this task without any problems, since only the changes are newly transferred to the PostgreSQL database.
The initial loading is done with both MS Access databases Pre2008 ubd avall.
After that only the monthly updates are then transferred. 

Example protocol:

    Progress update 2022-11-29 14:12:25.117005 : ===============================================================================.
    Progress update 2022-11-29 14:12:25.117502 : INFO.00.004 Start Launcher.
    Progress update 2022-11-29 14:12:25.119503 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-29 14:12:25.128005 : INFO.00.005 Argument task='l_z_d'.
    Progress update 2022-11-29 14:12:25.128005 : -------------------------------------------------------------------------------.
    Progress update 2022-11-29 14:12:25.128005 : INFO.00.056 Loading ZIP Code Database data.
    Progress update 2022-11-29 14:12:25.128005 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:12:25.179505 : INFO.00.061 Database table io_lat_lng: Loading the estimated zip code data.
    Progress update 2022-11-29 14:12:25.179505 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:13:21.866512 : Number of rows so far read :   5000.
    Progress update 2022-11-29 14:14:16.970167 : Number of rows so far read :  10000.
    Progress update 2022-11-29 14:15:10.266064 : Number of rows so far read :  15000.
    Progress update 2022-11-29 14:16:08.694846 : Number of rows so far read :  20000.
    Progress update 2022-11-29 14:16:47.652646 : Number of rows so far read :  25000.
    Progress update 2022-11-29 14:17:32.877233 : Number of rows so far read :  30000.
    Progress update 2022-11-29 14:18:06.643788 : Number of rows so far read :  35000.
    Progress update 2022-11-29 14:18:55.944095 : Number of rows so far read :  40000.
    Progress update 2022-11-29 14:19:13.847623 : Number rows selected :  42735.
    Progress update 2022-11-29 14:19:13.848123 : Number rows inserted :  10115.
    Progress update 2022-11-29 14:19:13.848123 : Number rows duplicate:  32660.
    Progress update 2022-11-29 14:19:13.848123 : Number rows updated  :   3252.
    Progress update 2022-11-29 14:19:13.848123 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:19:13.919921 : INFO.00.063 Processed data source 'average'.
    Progress update 2022-11-29 14:19:13.919921 : Number rows deleted  :   7631.
    Progress update 2022-11-29 14:19:13.919921 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:19:13.919921 : INFO.00.062 Database table io_lat_lng: Loading the averaged city data.
    Progress update 2022-11-29 14:19:13.919921 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:20:03.226487 : Number of rows so far read :   5000.
    Progress update 2022-11-29 14:20:49.819656 : Number of rows so far read :  10000.
    Progress update 2022-11-29 14:21:36.281703 : Number of rows so far read :  15000.
    Progress update 2022-11-29 14:22:22.562620 : Number of rows so far read :  20000.
    Progress update 2022-11-29 14:23:04.766437 : Number of rows so far read :  25000.
    Progress update 2022-11-29 14:23:48.995380 : Number of rows so far read :  30000.
    Progress update 2022-11-29 14:24:37.784042 : Number of rows so far read :  35000.
    Progress update 2022-11-29 14:25:21.929065 : Number of rows so far read :  40000.
    Progress update 2022-11-29 14:26:07.064444 : Number rows selected :  44743.
    Progress update 2022-11-29 14:26:07.064444 : Number rows inserted :  14392.
    Progress update 2022-11-29 14:26:07.064444 : Number rows duplicate:  30351.
    Progress update 2022-11-29 14:26:07.090743 : -------------------------------------------------------------------------------.
    Progress update 2022-11-29 14:26:07.090743 :      822,117,242,100 ns - Total time launcher.
    Progress update 2022-11-29 14:26:07.090743 : INFO.00.006 End   Launcher.
    Progress update 2022-11-29 14:26:07.090743 : ===============================================================================.

### 1.15 **`r_d_s`** - Refresh the PostgreSQL database schema

Hereby changes can be made to the database schema.
The task can be executed several times without problems, since before a change is always first checked whether this has already been done.

1. Materialized database view

- **`io_app_ae1982`** - provides the data for processing the task **`c_l_l`** (Correct decimal US latitudes and longitudes).

Example protocol:

    Progress update 2022-12-19 08:37:09.337180 : INFO.00.004 Start Launcher.
    Progress update 2022-12-19 08:37:09.342679 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-12-19 08:37:09.352180 : INFO.00.005 Argument task='r_d_s'.
    Progress update 2022-12-19 08:37:09.352180 : -------------------------------------------------------------------------------.
    Progress update 2022-12-19 08:37:09.352180 : INFO.00.071 Refreshing the database schema.
    Progress update 2022-12-19 08:37:09.352180 : --------------------------------------------------------------------------------
    Progress update 2022-12-19 08:37:19.366370 : INFO.00.069 Materialized database view is refreshed: io_app_ae1982.
    Progress update 2022-12-19 08:37:19.366370 : -------------------------------------------------------------------------------.
    Progress update 2022-12-19 08:37:19.366370 :       10,187,690,800 ns - Total time launcher.
    Progress update 2022-12-19 08:37:19.366370 : INFO.00.006 End   Launcher.
    Progress update 2022-12-19 08:37:19.366370 : ===============================================================================.

### 1.16 **`s_d_c`** - Set up the PostgreSQL database container

The default installation of the PostgreSQL database is done using the official Docker images from Dockerhub - see [here](https://hub.docker.com/_/postgres){:target="_blank"}.

This task consists of the following steps:

1. any running Docker container is stopped.
2. any existing Docker container is deleted.
3. if not already present, the file directory for the PostgreSQL database files is created.
4. the Docker network for the PostgreSQL database is created if it does not already exist.
5. the PostgreSQL Docker image is either created or updated based on DockerHub.
6. a new PostgreSQL Docker container is started.

Example protocol:

    Docker stop/rm io_avstats_db_dev_container .................... before:
    CONTAINER ID   IMAGE                    COMMAND                  CREATED       STATUS        PORTS                                                      NAMES
    66c741493677   postgres:latest          "docker-entrypoint.s…"   8 hours ago   Up 8 hours    0.0.0.0:5433->5432/tcp                                     io_avstats_db_dev_container
    a4469ea39fdd   postgres:latest          "docker-entrypoint.s…"   2 weeks ago   Up 10 hours   0.0.0.0:5432->5432/tcp                                     io_avstats_container
    f67eb28b8888   portainer/portainer-ce   "/portainer"             4 weeks ago   Up 10 hours   0.0.0.0:8000->8000/tcp, 0.0.0.0:9000->9000/tcp, 9443/tcp   portainer
    66c741493677   postgres:latest          "docker-entrypoint.sÔÇª"   8 hours ago   Up 8 hours    0.0.0.0:5433->5432/tcp                                     io_avstats_db_dev_container
    io_avstats_db_dev_container
    66c741493677   postgres:latest          "docker-entrypoint.sÔÇª"   8 hours ago   Exited (0) Less than a second ago                                                              io_avstats_db_dev_container
    io_avstats_db_dev_container
    ............................................................. after:
    CONTAINER ID   IMAGE                    COMMAND                  CREATED       STATUS        PORTS                                                      NAMES
    a4469ea39fdd   postgres:latest          "docker-entrypoint.s…"   2 weeks ago   Up 10 hours   0.0.0.0:5432->5432/tcp                                     io_avstats_container
    f67eb28b8888   portainer/portainer-ce   "/portainer"             4 weeks ago   Up 10 hours   0.0.0.0:8000->8000/tcp, 0.0.0.0:9000->9000/tcp, 9443/tcp   portainer
    Timer 4.0 - Command Line Timer - www.Gammadyne.com
    Copyright (C) 2007-2017 by Greg Wittmeyer - All Rights Reserved
    Timer started: 22.11.2022 19:35:22
    PostgreSQL
    --------------------------------------------------------------------------------
    Docker create io_avstats_db_dev_container (PostgreSQL latest)
    Docker network io_avstats_db_dev_net already existing
    93a1342e70d367bee07fa9b021293324d7ce04a8113563a3d995d63f9d5b6172
    Docker start io_avstats_db_dev_container (PostgreSQL ) ...
    io_avstats_db_dev_container
    NETWORK ID     NAME                    DRIVER    SCOPE
    6c9fa25a23dc   AVSTATS_POSTGRES_NET    bridge    local
    ad56537ead3f   bridge                  bridge    local
    da3331b29cb2   host                    host      local
    d6ad44ee9141   io_avstats_db_dev_net   bridge    local
    e33d9f5149d3   io_avstats_net          bridge    local
    3df9e6ac5dfa   none                    null      local
    [
        {
            "Name": "io_avstats_db_dev_net",
            "Id": "d6ad44ee9141424aec5d8e5643d4f4349e13482935a594f2553f4a7fd4648446",
            "Created": "2022-11-06T12:04:36.9326894Z",
            "Scope": "local",
            "Driver": "bridge",
            "EnableIPv6": false,
            "IPAM": {
                "Driver": "default",
                "Options": {},
                "Config": [
                    {
                        "Subnet": "172.20.0.0/16",
                        "Gateway": "172.20.0.1"
                    }
                ]
            },
            "Internal": false,
            "Attachable": false,
            "Ingress": false,
            "ConfigFrom": {
                "Network": ""
            },
            "ConfigOnly": false,
            "Containers": {},
            "Options": {},
            "Labels": {}
        }
    ]
    DOCKER PostgreSQL was ready in 30.2 seconds
    CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                                                      NAMES
    93a1342e70d3   postgres:latest          "docker-entrypoint.s…"   30 seconds ago   Up 29 seconds   0.0.0.0:5433->5432/tcp                                     io_avstats_db_dev_container
    a4469ea39fdd   postgres:latest          "docker-entrypoint.s…"   2 weeks ago      Up 10 hours     0.0.0.0:5432->5432/tcp                                     io_avstats_container
    f67eb28b8888   portainer/portainer-ce   "/portainer"             4 weeks ago      Up 10 hours     0.0.0.0:8000->8000/tcp, 0.0.0.0:9000->9000/tcp, 9443/tcp   portainer

### 1.17 **`u_d_s`** - Update the PostgreSQL database schema

Hereby changes can be made to the database schema.
The task can be executed several times without problems, since before a change is always first checked whether this has already been done.

1. New database tables:

- **`io_countries`**: contains latitude and longitude of selected countries.
- **`io_lat_lng`**: used to store the **simplemaps** and **United States Zip Codes.org** data.
- **`io_states`**: contains the identification, name, latitude and longitude of all US states.

2. Extensions for database tables:

2.1 Database table **`events`**.

- The columns **`io_city`**, **`io_country`**, **`io_latitude`**, **`io_longitude`**, **`io_site_zipcode`** and **`io_state`** to store manual corrections.
- The columns **`io_deviating_dec_latitude`**, **`io_deviating_dec_longitude`**, **`io_invalid_latitude`**, **`io_invalid_longitude`**, **`io_invalid_us_city`**, **`io_invalid_us_state`** and , **`io_invalid_us_zipcode`** for documenting data plausibility (task **`v_n_d`**).
- the columns **`io_dec_lat_lng_actions`**, **`io_dec_latitude`** and **`io_dec_longitude`** to store corrected decimal latitude and longitude values.

3. New database views:

- **`io_lat_lng_issues`** - provides the data for processing the task **`c_l_l`** (Correct decimal US latitudes and longitudes).
- **`io_accidents_us_1982`** - provides event data for aviation accidents in the U.S. since 1982.

Example protocol:

    Progress update 2022-11-27 13:37:13.316694 : ===============================================================================.
    Progress update 2022-11-27 13:37:13.316694 : INFO.00.004 Start Launcher.
    Progress update 2022-11-27 13:37:13.318694 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-27 13:37:13.327195 : INFO.00.005 Argument task='u_d_s'.
    Progress update 2022-11-27 13:37:13.327195 : -------------------------------------------------------------------------------.
    Progress update 2022-11-27 13:37:13.327195 : INFO.00.045 Updating the database schema.
    Progress update 2022-11-27 13:37:13.327195 : --------------------------------------------------------------------------------
    Progress update 2022-11-27 13:37:13.436194 : INFO.00.007 Database table is available: io_msaccess_file.
    Progress update 2022-11-27 13:37:13.520032 : INFO.00.007 Database table is available: io_countries.
    Progress update 2022-11-27 13:37:13.595030 : INFO.00.007 Database table is available: io_states.
    Progress update 2022-11-27 13:37:13.770060 : INFO.00.007 Database table is available: io_lat_lng.
    Progress update 2022-11-27 13:37:13.810990 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_city'.
    Progress update 2022-11-27 13:37:13.844989 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_country'.
    Progress update 2022-11-27 13:37:13.878039 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_dec_lat_lng_actions'.
    Progress update 2022-11-27 13:37:13.911450 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_dec_latitude'.
    Progress update 2022-11-27 13:37:13.944473 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_dec_longitude'.
    Progress update 2022-11-27 13:37:13.977929 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_deviating_dec_latitude'.
    Progress update 2022-11-27 13:37:14.010969 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_deviating_dec_longitude'.
    Progress update 2022-11-27 13:37:14.044449 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_latitude'.
    Progress update 2022-11-27 13:37:14.077702 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_longitude'.
    Progress update 2022-11-27 13:37:14.111268 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_us_city'.
    Progress update 2022-11-27 13:37:14.144267 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_us_state'.
    Progress update 2022-11-27 13:37:14.178253 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_invalid_us_zipcode'.
    Progress update 2022-11-27 13:37:14.211254 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_latitude'.
    Progress update 2022-11-27 13:37:14.244753 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_longitude'.
    Progress update 2022-11-27 13:37:14.277753 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_site_zipcode'.
    Progress update 2022-11-27 13:37:14.311253 : INFO.00.031 Database column added: table_schema 'public' table_name 'events' column_name 'io_state'.
    Progress update 2022-11-27 13:37:14.378313 : INFO.00.032 Database view is available: io_accidents_us_1982.
    Progress update 2022-11-27 13:37:14.402813 : INFO.00.032 Database view is available: io_lat_lng_issues.
    Progress update 2022-11-27 13:37:14.402813 : -------------------------------------------------------------------------------.
    Progress update 2022-11-27 13:37:14.402813 :        1,230,619,900 ns - Total time launcher.
    Progress update 2022-11-27 13:37:14.403313 : INFO.00.006 End   Launcher.
    Progress update 2022-11-27 13:37:14.403313 : ===============================================================================.

### 1.18 **`v_n_d`** - Verify selected **NTSB** data

This task can be used to perform a plausibility check for the following columns in the database table **`events`**:

- **`dec_latitude`**,
- **`dec_longitude`**,
- **`ev_state`**,
- **`ev_site_zipcode`**,
- **`latitude`**,
- **`longitude`**,

and the combination of:

- **`ev_state`** and **`ev_city`**,
- **`ev_state`**, **`ev_city`** and **`ev_site_zipcode`**.

The results of the check are stored in the following columns:

- **`io_deviating_dec_latitude`** (absolute difference),
- **`io_deviating_dec_longitude`** (absolute difference),
- **`io_invalid_latitude`** (true),
- **`io_invalid_longitude`** (true),
- **`io_invalid_us_city`** (true),
- **`io_invalid_us_city_zipcode`** (true),
- **`io_invalid_us_state`** (true),
- **`io_invalid_us_zipcode`** (true).

The tests are performed according to the following logic:

- **`io_deviating_dec_latitude`**: Absolute difference between **`dec_latitude`** and **`latitude`** exceeding a given limit in **`max_deviation_latitude`**.
- **`io_deviating_dec_longitude`**: Absolute difference between **`dec_longitude`** and **`longitude`** exceeding a given limit **`max_deviation_longitude`**.
- **`io_invalid_latitude`**: Can the latitude in the **`latitude`** column be converted to its decimal equivalent?
- **`io_invalid_longitude`**: Can the longitude in the **`longitude`** column be converted to its decimal equivalent?
- **`io_invalid_us_city`**: For country `USA` and the given state, is the specified value in the **`ev_city`** column a existing city?
- **`io_invalid_us_city_zipcode`**: For country `USA` and the given state, are the specified values in the **`ev_city`** column and in the **`ev_site_zipcode`** column a existing city?
- **`io_invalid_us_state`**: For country `USA`, is the specified value in the **`ev_state`** column a valid state identifier?
- **`io_invalid_us_z ipcode`**: For country `USA`, is the specified value in the **`ev_site_zipcode`** column a existing zip code?

Example protocol:

    Progress update 2022-11-29 14:52:27.221649 : ===============================================================================.
    Progress update 2022-11-29 14:52:27.221649 : INFO.00.004 Start Launcher.
    Progress update 2022-11-29 14:52:27.223649 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-11-29 14:52:27.232150 : INFO.00.005 Argument task='v_n_d'.
    Progress update 2022-11-29 14:52:27.232150 : -------------------------------------------------------------------------------.
    Progress update 2022-11-29 14:52:27.232150 : INFO.00.043 Verify selected NTSB data.
    Progress update 2022-11-29 14:52:27.232150 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:52:27.449649 : INFO.00.064 Verification of table 'events' column(s) 'latitude & longitude'.
    Progress update 2022-11-29 14:52:27.449649 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:52:28.124099 : Number of rows so far read :   5000.
    Progress update 2022-11-29 14:52:33.701741 : Number of rows so far read :  10000.
    Progress update 2022-11-29 14:53:21.979567 : Number of rows so far read :  15000.
    Progress update 2022-11-29 14:54:41.899911 : Number of rows so far read :  20000.
    Progress update 2022-11-29 14:55:56.229700 : Number of rows so far read :  25000.
    Progress update 2022-11-29 14:57:09.659083 : Number of rows so far read :  30000.
    Progress update 2022-11-29 14:58:10.139422 : Number rows errors   :  12322.
    Progress update 2022-11-29 14:58:10.139422 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:58:10.139422 : INFO.00.064 Verification of table 'events' column(s) 'ev_city'.
    Progress update 2022-11-29 14:58:10.968104 : Number rows errors   :   6039.
    Progress update 2022-11-29 14:58:10.968104 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:58:10.968104 : INFO.00.064 Verification of table 'events' column(s) 'ev_city & ev_site_zipcode'.
    Progress update 2022-11-29 14:58:11.934347 : Number rows errors   :  16491.
    Progress update 2022-11-29 14:58:11.934347 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:58:11.934846 : INFO.00.064 Verification of table 'events' column(s) 'ev_state'.
    Progress update 2022-11-29 14:58:12.175729 : Number rows errors   :    292.
    Progress update 2022-11-29 14:58:12.176230 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:58:12.176230 : INFO.00.064 Verification of table 'events' column(s) 'ev_site_zipcode'.
    Progress update 2022-11-29 14:58:12.400731 : Number rows errors   :   6029.
    Progress update 2022-11-29 14:58:12.401230 : --------------------------------------------------------------------------------
    Progress update 2022-11-29 14:58:12.402230 : Number rows selected :  34221.
    Progress update 2022-11-29 14:58:12.402230 : Number rows updated  :  41173.
    Progress update 2022-11-29 14:58:12.402730 : Number rows errors   :  41173.
    Progress update 2022-11-29 14:58:12.402730 : -------------------------------------------------------------------------------.
    Progress update 2022-11-29 14:58:12.402730 :      345,321,580,900 ns - Total time launcher.
    Progress update 2022-11-29 14:58:12.402730 : INFO.00.006 End   Launcher.
    Progress update 2022-11-29 14:58:12.402730 : ===============================================================================.

## 2. First installation

The initial load in a fresh Windows environment requires the execution of the following tasks in the given order:

- **`s_d_c`** - Set up the PostgreSQL database container                              
- **`c_d_s`** - Create the PostgreSQL database schema 
- **`d_n_a`** - Download the **NTSB** MS Access files Pre2008 and avall                      
- **`l_n_a`** - Load the **NTSB** MS Access database from Pre2008 and avall

## 3. Regular updates

[see](how_to_add_ntsb_accident_files.md){:target="_blank"}
