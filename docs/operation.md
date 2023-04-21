# Operation

The main tool for operating **IO-AVSTATS** is the **`run_io_avstats`** script. 
The script is available in a Windows command line version and in a Linux bash shell version.

## 1. Overview

The following tasks can be executed with this script:

| Code    | Task                                                   | Additional parameter(s)           |
|---------|--------------------------------------------------------|-----------------------------------|
| a_o_c   | Load aviation occurrence categories into PostgreSQL    |                                   |
| c_d_c   | Run Docker Compose tasks - Cloud                       | `clean`, `down`, `logs` or `up`   |
| c_d_i   | Create or update a Docker image                        | `all` or single Streamlit app     |
| c_d_l   | Run Docker Compose tasks - Local                       | `clean`, `down`, `logs` or `up`   |
| c_d_s   | Create the PostgreSQL database schema                  |                                   |
| c_f_z   | Zip the files for the cloud                            |                                   |
| c_l_l   | Correct decimal US latitudes and longitudes            |                                   |
| c_p_d   | Cleansing PostgreSQL data                              |                                   |
| d_d_f   | Delete the PostgreSQL database files                   |                                   |
| d_d_s   | Drop the PostgreSQL database schema                    |                                   |
| d_n_a   | Download a **NTSB** MS Access database file            | -m / -msaccess                    |
| f_n_a   | Find the nearest airports                              |                                   |
| l_a_p   | Load airport data into PostgreSQL                      |                                   |
| l_c_d   | Load data from a correction file into PostgreSQL       | -e / -excel                       |
| l_c_s   | Load country and state data into PostgreSQL            |                                   |
| l_n_a   | Load **NTSB** MS Access database data into PostgreSQL  | -m / -msaccess                    |
| l_n_s   | Load NTSB MS Excel statistic data into PostgreSQL      | -e / -excel                       |
| l_s_d   | Load **simplemaps** data into PostgreSQL               |                                   |
| l_s_e   | Load sequence of events data into PostgreSQL           |                                   |
| l_z_d   | Load ZIP Code Database data into PostgreSQL            |                                   |
| r_d_s   | Refresh the PostgreSQL database schema                 |                                   |
| r_s_a   | Run a Streamlit application                            | single Streamlit app, e.g. ae1982 |
| u_d_s   | Update the PostgreSQL database schema                  |                                   |
| u_p_d   | Complete processing of a modifying MS Access file      | -m / -msaccess                    |
| v_n_d   | Verify selected **NTSB** data                          |                                   |
| version | Show the IO-AVSTATS-DB version                         |                                   | 

## 2. Detailed task list

### **`a_o_c`** - Load aviation occurrence categories into PostgreSQL

- TODO

### **`c_d_c`** - Run Docker Compose tasks - Cloud

- TODO

### **`c_d_i`** - Create or update a Docker image

- TODO

### **`c_d_l`** - Run Docker Compose tasks - Local

- TODO

### **`c_d_s`** - Create the PostgreSQL database schema

- TODO

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

### **`c_f_z`** - Zip the files for the cloud

- TODO

### **`c_l_l`** - Correct decimal US latitudes and longitudes

- TODO

### **`c_p_d`** - Cleansing PostgreSQL data

- TODO

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

### **`d_d_f`** - Delete the PostgreSQL database files

- TODO

This task deletes all PostgreSQL database files.
The execution requires administration rights.
Subsequently, the PostgreSQL database must be completely rebuilt.

**Tip**: The administration password is required to use the administration rights. 
This can be difficult with the Windows operating system, as there seems to be no functionality to set the administration password. 
The use of the Windows Subsystem for Linux can help here. 

### **`d_d_s`** - Drop the PostgreSQL database schema

- TODO

Successful execution of this task requires that no other process uses the database defined with the **`postgres_dbname`** parameter.
After execution, the database with all objects and the database user defined with the **`postgres_user`** parameter are deleted.

### **`d_n_a`** - Download a **NTSB** MS Access database file

- TODO

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

### **`f_n_a`** - Find the nearest airports

- TODO

### **`l_a_p`** - Load airport data into PostgreSQL

- TODO

### **`l_c_d`** - Load data from a correction file into PostgreSQL

- TODO

This task allows files containing aviation accident data to be downloaded from the NTSB download site.
These files are there as MS Access databases in a compressed format.
The following subtasks are executed:

1. A connection to the NTSB download page is established.
2. The selected file is downloaded to the local system in chunks. 
3. The downloaded file is then unpacked. 
4. A script with the database schema definition is created with RazorSQL from the downloaded database.
5. The newly created script is then compared with a reference script for matching.


### **`l_c_s`** - Load country and state data into PostgreSQL

- TODO

### **`l_n_a`** - Load **NTSB** MS Access database data into PostgreSQL

- TODO

This task transfers the data from an **NTSB** MS Access database previously downloaded from the **NTSB** website to the PostgreSQL database.
The same MS Access database can be processed several times with this task without any problems, since only the changes are newly transferred to the PostgreSQL database.
The initial loading is done with both **NTSB** MS Access databases Pre2008 ubd avall.
After that only the monthly updates are then transferred. 

Further details can be found [here](https://github.com/io-aero/io-avstats-db/blob/main/site/db_data_transfer.html){:target="_blank"}.

### **`l_n_s`** - Load **NTSB** MS Excel statistic data into PostgreSQL

- TODO

### **`l_s_d`** - Load **simplemaps** data into PostgreSQL

- TODO

This task transfers the data from an NTSB MS Access database previously downloaded from the NTSB website to the PostgreSQL database.
The same MS Access database can be processed several times with this task without any problems, since only the changes are newly transferred to the PostgreSQL database.
The initial loading is done with both MS Access databases Pre2008 ubd avall.
After that only the monthly updates are then transferred. 

### **`l_s_e`** - Load sequence of events data into PostgreSQL

- TODO

### **`l_z_d`** - Load ZIP Code Database data into PostgreSQL

- TODO

This task transfers the data from an NTSB MS Access database previously downloaded from the NTSB website to the PostgreSQL database.
The same MS Access database can be processed several times with this task without any problems, since only the changes are newly transferred to the PostgreSQL database.
The initial loading is done with both MS Access databases Pre2008 ubd avall.
After that only the monthly updates are then transferred. 

### **`r_d_s`** - Refresh the PostgreSQL database schema

- TODO

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

### **`r_s_a`** - Run a Streamlit application

- TODO

### **`u_d_s`** - Update the PostgreSQL database schema

- TODO

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

### **`u_p_d`** - Complete processing of a modifying MS Access file

- TODO

### **`v_n_d`** - Verify selected **NTSB** data

- TODO

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

### **`version`** - Show the IO-AVSTATS-DB version

- TODO

## 2. First installation

The initial load in a fresh Windows environment requires the execution of the following tasks in the given order:

- **`c_d_l`** - Run Docker Compose tasks - Local                              
- **`c_d_s`** - Create the PostgreSQL database schema 
---
- **`l_c_s`** - Load country and state data into PostgreSQL
- **`l_a_p`** - Load airport data into PostgreSQL
- **`a_o_c`** - Load aviation occurrence categories into PostgreSQL
- **`l_s_e`** - Load sequence of events data into PostgreSQL
- **`l_s_d`** - Load simplemaps data into PostgreSQL
- **`l_z_d`** - Load ZIP Code Database data into PostgreSQL
---
- **`u_p_d`** - Complete processing of a modifying MS Access file
  - file **`Pre2008`**

## 3. Regular updates

### 3.1 Every first of the month

- Restore the current state of Pre2008
- Process the current **`avall`** file with code **`l_n_a`**

### 3.2 Every 1st, 8th, 15th and 22nd of the month 

- Process the current **`upDDMON`** file with code **`u_p_d`**
