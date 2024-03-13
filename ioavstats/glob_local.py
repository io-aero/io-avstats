# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Global constants and variables."""

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

ARG_MSACCESS = "msaccess"
ARG_MSACCESS_AVALL = "avall"
ARG_MSACCESS_PRE2008 = "Pre2008"
ARG_MSACCESS_UPDDMON = "upDDMON"
ARG_MSEXCEL = "msexcel"
ARG_TASK = "task"
ARG_TASK_A_O_C = "a_o_c"
ARG_TASK_C_D_S = "c_d_s"
ARG_TASK_C_L_L = "c_l_l"
ARG_TASK_C_P_D = "c_p_d"
ARG_TASK_D_N_A = "d_n_a"
ARG_TASK_F_N_A = "f_n_a"
ARG_TASK_GENERATE = "generate"
ARG_TASK_L_A_P = "l_a_p"
ARG_TASK_L_C_D = "l_c_d"
ARG_TASK_L_C_S = "l_c_s"
ARG_TASK_L_N_A = "l_n_a"
ARG_TASK_L_S_D = "l_s_d"
ARG_TASK_L_S_E = "l_s_e"
ARG_TASK_L_Z_D = "l_z_d"
ARG_TASK_R_D_S = "r_d_s"
ARG_TASK_U_D_S = "u_d_s"
ARG_TASK_VERSION = "version"
ARG_TASK_V_N_D = "v_n_d"

COUNTRY_USA = "USA"

# Error messages.
ERROR_00_901 = (
    "ERROR.00.901 The task '{task}' requires valid argument '-m' or '--msaccess'"
)
ERROR_00_902 = (
    "ERROR.00.902 The task '{task}' does not require an argument '-m' or '--msaccess'"
)
ERROR_00_903 = (
    "ERROR.00.903 '{msaccess}' is not a valid NTSB compliant MS Access database name"
)
ERROR_00_904 = (
    "ERROR.00.904 '{msaccess}': the MS Access database file name must not contain "
    + "a file extension"
)
ERROR_00_905 = "ERROR.00.905 Connection problem with url='{url}'"
ERROR_00_906 = "ERROR.00.906 Unexpected response status code='{status_code}'"
ERROR_00_907 = "ERROR.00.907 File '{filename}' is not a zip file"
ERROR_00_908 = "ERROR.00.908 The operating system '{os}' is not supported"
ERROR_00_909 = "ERROR.00.909 Timeout after '{timeout}' seconds with url='{url}'"
ERROR_00_910 = (
    "ERROR.00.910 The schema definition in file '{filename}' "
    + "does not match the reference definition in file '{reference}'"
)
ERROR_00_911 = (
    "ERROR.00.911 Number of lines differs: file '{filename}' lines {filename_lines}"
    + " versus file '{reference}' lines {reference_lines}"
)
ERROR_00_912 = "ERROR.00.912 The MS Access database file '{filename}' is missing"
ERROR_00_913 = "ERROR.00.913 The US zip code file '{filename}' is missing"
ERROR_00_914 = "ERROR.00.914 The US city file '{filename}' is missing"
ERROR_00_915 = "ERROR.00.915 Unknown US zip code"
ERROR_00_916 = "ERROR.00.916 Unknown US state and city"
ERROR_00_917 = "ERROR.00.917 Unknown US state"
ERROR_00_920 = "ERROR.00.920 Invalid latitude string"
ERROR_00_921 = "ERROR.00.921 Invalid longitude string"
ERROR_00_922 = "ERROR.00.922 Invalid US state id"
ERROR_00_923 = (
    "ERROR.00.923 The task '{task}' requires valid argument '-e' or '--msexcel'"
)
ERROR_00_924 = (
    "ERROR.00.924 The task '{task}' does not allow an argument '-e' or '--msexcel'"
)
ERROR_00_925 = "ERROR.00.925 '{msexcel}' is not a valid Microsoft Excel file"
ERROR_00_926 = "ERROR.00.926 The correction file '{filename}' is missing"
ERROR_00_927 = "ERROR.00.927 Database table not yet supported"
ERROR_00_928 = "ERROR.00.928 Database table column not yet supported"
ERROR_00_929 = "ERROR.00.929 Excel column '{column_name}' must be empty"
ERROR_00_930 = "ERROR.00.930 Excel column '{column_name}' must not be empty"
ERROR_00_931 = "ERROR.00.931 The ev_id is missing in database table events"
ERROR_00_932 = "ERROR.00.932 File '{filename}' is not existing"
ERROR_00_933 = "ERROR.00.933 File directory '{dirname}' is not existing"
ERROR_00_934 = "ERROR.00.934 The country and state data file '{filename}' is missing"
ERROR_00_935 = "ERROR.00.935 The Zip Code Database file '{filename}' is missing"
ERROR_00_936 = "ERROR.00.936 The MS Excel file '{filename}' is missing"
ERROR_00_937 = (
    "ERROR.00.937 The aviation occurrence categories file '{filename}' is missing"
)
ERROR_00_938 = "ERROR.00.938 The sequence of events file '{filename}' is missing"
ERROR_00_939 = (
    "ERROR.00.939 Foreign key value CICTT code='{cictt_code}' "
    + "is missing - soe_no='{soe_no}'"
)
ERROR_00_940 = (
    "ERROR.00.940 The MS Access database {msaccess} is not allowed in this task"
)
ERROR_00_941 = "ERROR.00.941 The Main Phases of Flight file '{filename}' is missing"
ERROR_00_942 = (
    "ERROR.00.942 Event '{ev_id}': issue with the Haversine algorithm: '{error}'"
)
ERROR_00_943 = "ERROR.00.943 The airport file '{filename}' is missing"
ERROR_00_944 = "ERROR.00.944 The runway file '{filename}' is missing"
ERROR_00_945 = "ERROR.00.945 The NPIAS file '{filename}' is missing"
ERROR_00_946 = "ERROR.00.946 The ev_id '{ev_id}' is missing in database table events"
ERROR_00_947 = (
    "ERROR.00.947 The ev_id '{ev_id}' is missing in database table events (suspected)"
)

# Fatal error messages.
FATAL_00_931 = "FATAL.00.931 Fatal Error - The file '{file_name}' was not found"
FATAL_00_932 = "FATAL.00.932 Fatal Error - The file '{file_name}' is empty"
FATAL_00_933 = (
    "FATAL.00.933 Fatal Error - The file '{file_name}' causes the value error '{error}'"
)
FATAL_00_934 = (
    "FATAL.00.934 Fatal Error - The file '{file_name}' causes the error '{error}'"
)

FILE_EXTENSION_MDB = "mdb"
FILE_EXTENSION_SQL = "sql"
FILE_EXTENSION_ZIP = "zip"

# Informational messages.
INFO_00_002 = (
    "INFO.00.002 The configuration parameters (ioavstats) are checked and loaded"
)
INFO_00_003 = (
    "INFO.00.003 Initialize the configuration parameters using the file '{file}'"
)
INFO_00_004 = "INFO.00.004 Start Launcher"
INFO_00_005 = "INFO.00.005 Argument {task}='{value_task}'"
INFO_00_006 = "INFO.00.006 End   Launcher"
INFO_00_007 = "INFO.00.007 Database table   is available: {table}"
INFO_00_008 = (
    "INFO.00.008 Arguments {task}='{value_task}' {msaccess}='{value_msaccess}'"
)
INFO_00_009 = "INFO.00.009 line no.: {line_no}"
INFO_00_010 = "INFO.00.010 {status} '{line}'"
INFO_00_011 = (
    "INFO.00.011 The DDL script for the MS Access database "
    + "'{msaccess}.mdb' was created successfully"
)
INFO_00_012 = (
    "INFO.00.012 The DDL script for the MS Access database "
    + "'{msaccess}.mdb' is identical to the reference script"
)
INFO_00_013 = (
    "INFO.00.013 The connection to the MS Access database file "
    + "'{msaccess}.zip' on the NTSB download page was successfully established"
)
INFO_00_014 = (
    "INFO.00.014 From the file '{msaccess}.zip' {no_chunks} chunks were downloaded"
)
INFO_00_015 = "INFO.00.015 The file '{msaccess}.zip' was successfully unpacked"
INFO_00_016 = "INFO.00.016 Database role    is available: {role}"
INFO_00_017 = "INFO.00.017 Database         is available: {dbname}"
INFO_00_018 = "INFO.00.018 Database role    is dropped:   {role}"
INFO_00_019 = "INFO.00.019 Database         is dropped:   {dbname}"
INFO_00_020 = (
    "INFO.00.020 The DDL script for the MS Access database "
    + "'{msaccess}.mdb' must be checked manually"
)
INFO_00_021 = "INFO.00.021 The following database table is not processed: '{msaccess}'"
INFO_00_022 = (
    "INFO.00.022 The connection to the US zip code file "
    + "'{filename}' on the simplemaps download page was successfully established"
)
INFO_00_023 = (
    "INFO.00.023 From the file '{filename}' {no_chunks} chunks were downloaded"
)
INFO_00_024 = "INFO.00.024 The file '{filename}' was successfully unpacked"
INFO_00_025 = (
    "INFO.00.025 Database table io_lat_lng: Load zipcode data "
    + "from file '{filename}'"
)
INFO_00_027 = (
    "INFO.00.027 Database table io_lat_lng: Load city data " + "from file '{filename}'"
)
INFO_00_028 = "INFO.00.028 Database table io_lat_lng: Load the state data"
INFO_00_029 = "INFO.00.029 Database table io_lat_lng: Load the country data"
INFO_00_030 = (
    "INFO.00.030 The connection to the US city file "
    + "'{filename}' on the simplemaps download page was successfully established"
)
INFO_00_031 = (
    "INFO.00.031 Database column added: table_schema '{schema}' "
    + "table_name '{table}' column_name '{column}'"
)
INFO_00_032 = "INFO.00.032 Database view    is created: {view}"
INFO_00_033 = "INFO.00.033 Correction based on US zip code"
INFO_00_034 = "INFO.00.034 Correction based on US state and city"
INFO_00_035 = "INFO.00.035 Correction based on US state"
INFO_00_036 = "INFO.00.036 Correction based on US country"
INFO_00_037 = "INFO.00.037 Correction based on latitude and longitude"
INFO_00_038 = "INFO.00.038 Correction based on swapped latitude and longitude"
INFO_00_039 = (
    "INFO.00.039 Database table io_lat_lng: Load zipcode data "
    + "from file '{filename}'"
)
INFO_00_040 = "INFO.00.040 Correct decimal US latitudes and longitudes"
INFO_00_041 = "INFO.00.041 Arguments {task}='{value_task}' {msexecel}='{value_msexcel}'"
INFO_00_042 = "INFO.00.042 Load corrections from file '{filename}'"
INFO_00_043 = "INFO.00.043 Verify selected NTSB data"
INFO_00_044 = "INFO.00.044 Creating the database schema"
INFO_00_045 = "INFO.00.045 Updating the database schema"
INFO_00_046 = "INFO.00.046 Dropping the database schema"
INFO_00_047 = "INFO.00.047 Download NTSB MS Access database file '{msaccess}'"
INFO_00_048 = "INFO.00.048 Download basic simplemaps files"
INFO_00_049 = "INFO.00.049 Load NTSB MS Access database data from file '{msaccess}'"
INFO_00_050 = "INFO.00.050 Load simplemaps data"
INFO_00_051 = "INFO.00.051 msaccess_file='{msaccess_file}'"
INFO_00_052 = "INFO.00.052 razorsql_jar_file='{razorsql_jar_file}'"
INFO_00_053 = "INFO.00.053 razorsql_java_path='{razorsql_java_path}'"
INFO_00_054 = "INFO.00.054 ODBC driver='{driver}'"
INFO_00_055 = "INFO.00.055 Download ZIP Code Database file"
INFO_00_056 = "INFO.00.056 Load ZIP Code Database data"
INFO_00_057 = "INFO.00.057 Load country and state data"
INFO_00_058 = (
    "INFO.00.058 The connection to the Zip Code Database file "
    + "'{filename}' on the Zip Codes.org download page was successfully established"
)
INFO_00_059 = "INFO.00.059 Load country data"
INFO_00_060 = "INFO.00.060 Load state data"
INFO_00_061 = "INFO.00.061 Database table io_lat_lng: Load the estimated zip code data"
INFO_00_062 = "INFO.00.062 Database table io_lat_lng: Load the averaged city data"
INFO_00_063 = "INFO.00.063 Processed data source '{data_source}'"
INFO_00_064 = "INFO.00.064 Verification of table '{table}' column(s) '{column}'"
INFO_00_065 = "INFO.00.065 Cleansing PostgreSQL data"
INFO_00_066 = "INFO.00.066 Cleansing table '{table}' column '{column}'"
INFO_00_067 = "INFO.00.067 Database view    is dropped:   {view}"
INFO_00_068 = "INFO.00.068 Materialized database view is created: {view}"
INFO_00_069 = "INFO.00.069 Materialized database view is refreshed: {view}"
INFO_00_070 = "INFO.00.070 Materialized database view is dropped: {view}"
INFO_00_071 = "INFO.00.071 Refreshing the database schema"
INFO_00_072 = ""
INFO_00_073 = "INFO.00.073 Load aviation occurrence categories"
INFO_00_074 = (
    "INFO.00.074 Database table io_aviation_occurrence_categories: "
    + "Load data from file '{filename}'"
)
INFO_00_075 = "INFO.00.075 Load sequence of events data"
INFO_00_076 = (
    "INFO.00.076 Database table io_sequence_of_events: "
    + "Load data from file '{filename}'"
)
INFO_00_077 = "INFO.00.077 Database index  is available: {index}"
INFO_00_078 = "INFO.00.078 Load NTSB MS Access database PKs from file '{msaccess}'"
INFO_00_079 = "INFO.00.079 Process NTSB data deletions in PostgreSQL"
INFO_00_082 = "INFO.00.082 Database role  already existing: {role}"
INFO_00_083 = "INFO.00.083 Database       already existing: {dbname}"
INFO_00_084 = (
    "INFO.00.084 Database table io_md_codes_phase: Load description_main_phase "
    + "from file '{filename}'"
)
INFO_00_085 = "INFO.00.085 Load airports"
INFO_00_086 = "INFO.00.086 Find the nearest airports"
INFO_00_087 = "INFO.00.087 Database table io_airports: Delete the existing data"
INFO_00_088 = "INFO.00.088 Database table io_airports: Load the global identifications"
INFO_00_089 = (
    "INFO.00.089 Database table io_airports: " + "Load data from file '{filename}'"
)
INFO_00_090 = "INFO.00.090 Database table io_runways: Update the runway data"
INFO_00_091 = "INFO.00.091 Database type    is available: {type}"
INFO_00_092 = (
    "INFO.00.092 Database table io_runways: " + "Load data from file '{filename}'"
)

INFORMATION_NOT_YET_AVAILABLE = "n/a"

# Library version number.
IO_AERO_DB_VERSION = "1.8.0"

IO_LAT_LNG_TYPE_CITY = "CITY"
IO_LAT_LNG_TYPE_ZIPCODE = "ZIPCODE"

LOCALE = "en_US.UTF-8"

# MS Access database files.
MSACCESS_AVALL = "avall"
MSACCESS_PRE2008 = "Pre2008"

SOURCE_AVERAGE = "average"
SOURCE_SM_US_CITIES = "simplemaps United States Cities Database"
SOURCE_SM_US_ZIP_CODES = "simplemaps US Zip Codes Database"
SOURCE_ZCO_ZIP_CODES = "Zip Codes.org ZIP Code Database"

# Database table names.
TABLE_NAME_AIRCRAFT = "aircraft"
TABLE_NAME_DT_AIRCRAFT = "dt_aircraft"
TABLE_NAME_DT_EVENTS = "dt_events"
TABLE_NAME_DT_FLIGHT_CREW = "dt_Flight_Crew"
TABLE_NAME_ENGINES = "engines"
TABLE_NAME_EVENTS = "events"
TABLE_NAME_EVENTS_SEQUENCE = "Events_Sequence"
TABLE_NAME_FINDINGS = "Findings"
TABLE_NAME_FLIGHT_CREW = "Flight_Crew"
TABLE_NAME_FLIGHT_TIME = "flight_time"
TABLE_NAME_INJURY = "injury"
TABLE_NAME_NARRATIVES = "narratives"
TABLE_NAME_NTSB_ADMIN = "NTSB_Admin"
TABLE_NAME_OCCURRENCES = "Occurrences"
TABLE_NAME_SEQ_OF_EVENTS = "seq_of_events"

US_STATE_IDS: list[str] = [
    "AK",
    "AL",
    "AR",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
]
