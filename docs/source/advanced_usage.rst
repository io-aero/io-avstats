==============
Advanced Usage
==============

The main tool for operating **IO-AVSTATS** is the **``run_io_avstats``** script.
The script is fully available in the Windows version and in a greatly reduced version for Ubuntu.

Overview
========

The following tasks can be executed with this script:

+--------+-------------------------------------------------------+-------------------------------+
| Code   | Task                                                  | Additional parameter(s)       |
+========+=======================================================+===============================+
| a_o_c  | Load aviation occurrence categories into PostgreSQL   |                               |
+--------+-------------------------------------------------------+-------------------------------+
| c_d_c  | Run Docker Compose tasks - Cloud                      | ``clean``, ``down``, ``logs`` |
|        |                                                       | or ``up``                     |
+--------+-------------------------------------------------------+-------------------------------+
| c_d_i  | Create or update an application Docker image          | ``all`` or single Streamlit   |
|        |                                                       | app                           |
+--------+-------------------------------------------------------+-------------------------------+
| c_d_s  | Create the IO-AVSTATS-DB PostgreSQL database schema   |                               |
+--------+-------------------------------------------------------+-------------------------------+
| c_f_z  | Zip the files for the cloud                           |                               |
+--------+-------------------------------------------------------+-------------------------------+
| c_l_l  | Correct decimal US latitudes and longitudes           |                               |
+--------+-------------------------------------------------------+-------------------------------+
| c_p_d  | Cleansing PostgreSQL data                             |                               |
+--------+-------------------------------------------------------+-------------------------------+
| f_n_a  | Find the nearest airports                             |                               |
+--------+-------------------------------------------------------+-------------------------------+
| l_a_p  | Load airport data into PostgreSQL                     |                               |
+--------+-------------------------------------------------------+-------------------------------+
| l_c_d  | Load data from a correction file into PostgreSQL      | -e / -excel                   |
+--------+-------------------------------------------------------+-------------------------------+
| l_c_s  | Load country and state data into PostgreSQL           |                               |
+--------+-------------------------------------------------------+-------------------------------+
| l_n_a  | Load NTSB MS Access database data into PostgreSQL     | -m / -msaccess                |
+--------+-------------------------------------------------------+-------------------------------+
| l_s_d  | Load simplemaps data into PostgreSQL                  |                               |
+--------+-------------------------------------------------------+-------------------------------+
| l_s_e  | Load sequence of events data into PostgreSQL          |                               |
+--------+-------------------------------------------------------+-------------------------------+
| l_z_d  | Load ZIP Code Database data into PostgreSQL           |                               |
+--------+-------------------------------------------------------+-------------------------------+
| r_d_s  | Refresh the PostgreSQL database schema                |                               |
+--------+-------------------------------------------------------+-------------------------------+
| r_s_a  | Run a Streamlit application                           |                               |
+--------+-------------------------------------------------------+-------------------------------+
| s_d_c  | Set up the IO-AVSTATS-DB PostgreSQL database container|                               |
+--------+-------------------------------------------------------+-------------------------------+
| u_d_s  | Update the IO-AVSTATS-DB PostgreSQL database schema   |                               |
+--------+-------------------------------------------------------+-------------------------------+
| u_p_d  | Complete processing of a modifying MS Access file     | -m / -msaccess                |
+--------+-------------------------------------------------------+-------------------------------+
| version| Show the **IO-AVSTATS** version                       |                               |
+--------+-------------------------------------------------------+-------------------------------+

Detailed task list
==================

``a_o_c`` - Load aviation occurrence categories into PostgreSQL
---------------------------------------------------------------

**Purpose**

Load the definition of the valid CICTT codes.

**Data Source**

The data source can be found on the NTSB website here:

- `AVIATION OCCURRENCE CATEGORIES - DEFINITIONS AND USAGE NOTES <https://www.ntsb.gov/safety/data/Documents/datafiles/OccurrenceCategoryDefinitions.pdf>`_

The NTSB provides the data in a ``pdf`` file which must then be converted to MS Excel format ``xlsx`` before processing.

**Implementation**

.. code-block:: sql

    CREATE TABLE public.io_aviation_occurrence_categories (
        cictt_code varchar(10) NOT NULL,
        identifier varchar(100) NOT NULL,
        definition text NOT NULL,
        first_processed timestamp NOT NULL,
        last_processed timestamp NULL,
        last_seen timestamp NULL,
        CONSTRAINT io_aviation_occurrence_categories_pkey PRIMARY KEY (cictt_code)
    );

...

``c_d_c`` - Run Docker Compose tasks - Cloud
--------------------------------------------

**Purpose**

Manage the Docker containers needed in the cloud:

- **portainer**: container management
- **IO-AVSTATS-DB**: PostgreSQL database
- Application **ae1982**: Aircraft Events since 1982
- Application **pd1982**: Profiling Data since 1982
- Application **slara**: Association Rule Analysis
- **load_balancer**: load balancer NGINX

**Processing Options**

.. code-block:: none

    - clean - Remove all containers and images
    - down  - Stop  Docker Compose
    - logs  - Fetch the logs of a container
    - up    - Start Docker Compose

``c_d_i`` - Create or update an application Docker image
--------------------------------------------------------

**Purpose**

Create the application-specific Docker images and store them on DockerHub.

**Processing Options**

.. code-block:: none

    - all     - All Streamlit applications
    - ae1982  - Aircraft Accidents in the US since 1982
    - pd1982  - Profiling Data for the US since 1982
    - slara   - Association Rule Analysis

``c_d_s`` - Create the IO-AVSTATS-DB PostgreSQL database schema
----------------------------------------------------------------

**Purpose**

Create the database schema including the following steps, among others:

1. creation of a new database user, and
2. creation of a new database, and
3. creation of database objects such as database tables and so on.

The following parameters are used when creating the database schema:

- `postgres_dbname_admin` - administration database name
- `postgres_password_admin` - administration database password
- `postgres_user_admin` - administration database username

Subsequently, the task ``u_d_s`` (Update the PostgreSQL database schema) is also executed.

``c_f_z`` - Zip the files for the cloud
---------------------------------------

**Purpose**

Collect and zip the elements needed for the cloud to run the **IO-AVSTATS** application there.
The result is contained in the file **cloud.zip**.

``c_l_l`` - Correct decimal US latitudes and longitude
------------------------------------------------------

**Purpose**

An attempt is made to calculate missing decimal longitudes and latitudes using the database tables **`io_lat_lng`** and **`io_states`**.

**Implementation**

1. In the database table **`events`** the values in the columns **`io_dec_lat_lng_actions`**, **`io_dec_latitude`**, **`io_dec_longitude`** and **`io_latlong_acq`** are deleted.
2. All rows in the database table **`events`** are processed where at least one of the columns **`dec_latitude`** or **`dec_longitude`** is empty or 0 and the column **`ev_country`** has the content **`USA`**.
    - 2.1 An erroneous swapping of latitude and longitude is corrected.
    - 2.2 An attempt is made to calculate a missing column **`dec_latitude`** from the column **`latitude`** and a missing column **`dec_longitude`** from the column **`longitude`**.
    - 2.3 An attempt is made to calculate a missing column **`dec_latitude`** or **`dec_longitude`** from the column **`ev_site_zipcode`**.
    - 2.4 It tries to calculate a missing column **`dec_latitude`** or **`dec_longitude`** from the column **`ev_city`**.
    - 2.5 An attempt is made to calculate a missing column **`dec_latitude`** or **`dec_longitude`** from the column **`ev_state`**.
    - 2.6 For a missing column **`dec_latitude`** resp. **`dec_longitude`** the center of the USA is assumed.

``c_p_d`` - Cleansing PostgreSQL data
-------------------------------------

**Purpose**

Clean up data the abnormalities in the database.
This includes the following activities:

- remove trailing whitespace in string data types (trimming),
- converting string data types that contain only whitespace to NULL (nullifying).

As a result, a much simplified processing of the data is possible, e.g. for comparisons.

On the one hand, the task can be executed explicitly with the **``run_io_avstats_db``** script (task **``c_p_d``**) and, on the other hand, it always runs after loading NTSB MS Access data into the PostgreSQL database (task **``l_n_a``** and **``u_p_d``**).

``f_n_a`` - Find the nearest airports
-------------------------------------

- TODO

**Purpose**

``l_a_p`` - Load airport data into PostgreSQL
---------------------------------------------

- TODO

**Purpose**

**Data Source**

**Implementation**

``l_c_d`` - Load data from a correction file into PostgreSQL
------------------------------------------------------------

- TODO

**Purpose**

**Data Source**

**Implementation**

This task allows files containing aviation accident data to be downloaded from the NTSB download site.
These files are there as MS Access databases in a compressed format.
The following subtasks are executed:

1. A connection to the NTSB download page is established.
2. The selected file is downloaded to the local system in chunks.
3. The downloaded file is then unpacked.
4. A script with the database schema definition is created with RazorSQL from the downloaded database.
5. The newly created script is then compared with a reference script for matching.

``l_c_s`` - Load country and state data into PostgreSQL
-------------------------------------------------------

- TODO

**Purpose**

**Data Source**

**Implementation**

``l_n_a`` - Load NTSB MS Access database data into PostgreSQL
-------------------------------------------------------------

**Purpose**

This task allows files containing aviation event data to be downloaded from the **NTSB** download site.
These files are there as MS Access databases in a compressed format.
The following subtasks are executed:

1. A connection to the **NTSB** download page is established.
2. The selected file is downloaded to the local system in chunks.
3. The downloaded file is then unpacked.
4. A script with the database schema definition is created with RazorSQL from the downloaded database.
5. The newly created script is then compared with a reference script for matching.

Subsequently, the downloaded data can be loaded into the PostgreSQL database with the task ``l_n_a`` (Load NTSB MS Access database data into PostgreSQL).

**Data Sources**

- **Pre2008.zip**: data set for 1982 through 2007
- **avall.zip**: data set from 2008 to the present
- **upDDMON.zip**: monthly supplements on the 1st, 8th, 15th and 22nd

**Implementation**

The PostgreSQL database **IO-AVSTATS-DB** completely maps the database schema of the **NTSB** MS Access database.

``l_s_d`` - Load simplemaps data into PostgreSQL
------------------------------------------------

- TODO

**Purpose**

**Data Source**

**Implementation**

This task transfers the data from an NTSB MS Access database previously downloaded from the NTSB website to the PostgreSQL database.
The same MS Access database can be processed several times with this task without any problems, since only the changes are newly transferred to the PostgreSQL database.
The initial loading is done with both MS Access databases Pre2008 ubd avall.
After that only the monthly updates are then transferred.

``l_s_e`` - Load sequence of events data into PostgreSQL
--------------------------------------------------------

- TODO

**Purpose**

**Data Source**

**Implementation**

``l_z_d`` - Load ZIP Code Database data into PostgreSQL
-------------------------------------------------------

- TODO

**Purpose**

**Data Source**

**Implementation**

This task transfers the data from an NTSB MS Access database previously downloaded from the NTSB website to the PostgreSQL database.
The same MS Access database can be processed several times with this task without any problems, since only the changes are newly transferred to the PostgreSQL database.
The initial loading is done with both MS Access databases Pre2008 ubd avall.
After that only the monthly updates are then transferred.

``r_d_s`` - Refresh the PostgreSQL database schema
--------------------------------------------------

- TODO

Hereby changes can be made to the database schema.
The task can be executed several times without problems, since before a change is always first checked whether this has already been done.

1. Materialized database view

- **``io_app_ae1982``** - provides the data for processing the task **``c_l_l``** (Correct decimal US latitudes and longitudes).

Example protocol:

    Progress update 2022-...:09.337180 : INFO.00.004 Start Launcher.
    Progress update 2022-...:09.342679 : INFO.00.001 The logger is configured and ready.
    Progress update 2022-...:09.352180 : INFO.00.005 Argument task='r_d_s'.
    Progress update 2022-...:09.352180 : -------------------------------------------------------------------------------.
    Progress update 2022-...:09.352180 : INFO.00.071 Refreshing the database schema.
    Progress update 2022-...:09.352180 : --------------------------------------------------------------------------------
    Progress update 2022-...:19.366370 : INFO.00.069 Materialized database view is refreshed: io_app_ae1982.
    Progress update 2022-...:19.366370 : -------------------------------------------------------------------------------.
    Progress update 2022-...:19.366370 :       10,187,690,800 ns - Total time launcher.
    Progress update 2022-...:19.366370 : INFO.00.006 End   Launcher.
    Progress update 2022-...:19.366370 : ===============================================================================.

``r_s_a`` - Run the IO-AVSTATS application
------------------------------------------

- TODO

``s_d_c`` - Set up the PostgreSQL database container
----------------------------------------------------

- TODO

``u_d_s`` - Update the PostgreSQL database schema
--------------------------------------------------

- TODO

Hereby changes can be made to the database schema.
The task can be executed several times without problems, since before a change is always first checked whether this has already been done.

1. New database tables:

- **``io_countries``**: contains latitude and longitude of selected countries.
- **``io_lat_lng``**: used to store the **simplemaps** and **United States Zip Codes.org** data.
- **``io_states``**: contains the identification, name, latitude and longitude of all US states.

2. Extensions for database tables:

2.1 Database table **``events``**.

- The columns **``io_city``**, **``io_country``**, **``io_latitude``**, **``io_longitude``**, **``io_site_zipcode``** and **``io_state``** to store manual corrections.
- The columns **``io_deviating_dec_latitude``**, **``io_deviating_dec_longitude``**, **``io_invalid_latitude``**, **``io_invalid_longitude``**, **``io_invalid_us_city``**, **``io_invalid_us_state``** and , **``io_invalid_us_zipcode``** for documenting data plausibility (task **``v_n_d``**).
- the columns **``io_dec_lat_lng_actions``**, **``io_dec_latitude``** and **``io_dec_longitude``** to store corrected decimal latitude and longitude values.

3. New database views:

- **``io_lat_lng_issues``** - provides the data for processing the task **``c_l_l``** (Correct decimal US latitudes and longitudes).
- **``io_accidents_us_1982``** - provides event data for aviation accidents in the U.S. since 1982.

``u_p_d`` - Complete processing of a modifying MS Access file
-------------------------------------------------------------

- TODO

``v_n_d`` - Verify selected **NTSB** data
-----------------------------------------

**Purpose**

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
- **`io_invalid_us_city`**: For country `USA` and the given state, is the specified value in the **`ev_city`** column an existing city?
- **`io_invalid_us_city_zipcode`**: For country `USA` and the given state, are the specified values in the **`ev_city`** column and in the **`ev_site_zipcode`** column an existing city?
- **`io_invalid_us_state`**: For country `USA`, is the specified value in the **`ev_state`** column a valid state identifier?
- **`io_invalid_us_zipcode`**: For country `USA`, is the specified value in the **`ev_site_zipcode`** column an existing zip code?

``version`` - Show the **``IO-AVSTATS``** version
-------------------------------------------------

- TODO

First installation
==================

The initial load in a fresh Windows environment requires the execution of the following tasks in the given order:

- **``c_d_s``** - Create the IO-AVSTATS-DB PostgreSQL database schema
- **``l_c_s``** - Load country and state data into PostgreSQL
- **``l_a_p``** - Load airport data into PostgreSQL
- **``a_o_c``** - Load aviation occurrence categories into PostgreSQL
- **``l_s_e``** - Load sequence of events data into PostgreSQL
- **``l_s_d``** - Load simplemaps data into PostgreSQL
- **``l_z_d``** - Load ZIP Code Database data into PostgreSQL
- **``u_p_d``** - Complete processing of a modifying MS Access file: **``Pre2008``**

Regular updates
===============

### Every 1st of the month

1. Stop the Docker container **``IO-AVSTATS-DB``**
2. Restore the current state of Pre2008
3. Start the Docker container **``IO-AVSTATS-DB``**
4. Process the current **``avall``** file with code **``l_n_a``**

### Every 1st, 8th, 15th and 22nd

- Process the current **``upDDMON``** file with code **``u_p_d``**
