# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""IO-AVSTATS interface."""
from __future__ import annotations

import argparse
import logging
import zipfile
from pathlib import Path

from iocommon import io_glob, io_settings, io_utils
from openpyxl.reader.excel import load_workbook
from openpyxl.utils.exceptions import InvalidFileException  # type: ignore

from ioavstats import (
    code_generator,
    db_ddl_base,
    db_dml_base,
    db_dml_corr,
    db_dml_msaccess,
    glob_local,
)

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

ARG_MSACCESS = ""
ARG_MSEXCEL = ""
ARG_TASK = ""


# -----------------------------------------------------------------------------

def check_arg_msaccess(args: argparse.Namespace) -> None:
    """Check the command line argument: -m / --msaccess.

    Args:
        args (argparse.Namespace): Command line arguments.

    The MS Access database name must be in the format 'upDDmmm' where:
        - 'up' is a fixed prefix
        - 'DD' is the day of the month as a two digit number (01-31)
        - 'mmm' is the month as a three letter abbreviation (jan-dec)

    If the task is 'd_n_a' or 'l_n_a', the argument '-m' or '--msaccess' is
    required. Otherwise, it is not allowed.

    """
    global ARG_MSACCESS

    if ARG_TASK in [
        glob_local.ARG_TASK_D_N_A,
        glob_local.ARG_TASK_L_N_A,
    ]:
        if not args.msaccess:
            # ERROR.00.901 The task '{task}' requires valid
            # argument '-m' or '--msaccess'
            terminate_fatal(glob_local.ERROR_00_901.replace("{task}", ARG_TASK))
    elif args.msaccess:
        # ERROR.00.902 The task '{task}' does not require an
        # argument '-m' or '--msaccess'
        terminate_fatal(glob_local.ERROR_00_902.replace("{task}", ARG_TASK))
    else:
        return

    ARG_MSACCESS = args.msaccess.lower()

    if ARG_MSACCESS == glob_local.ARG_MSACCESS_AVALL:
        return

    if glob_local.ARG_MSACCESS_PRE2008.lower() == ARG_MSACCESS:
        ARG_MSACCESS = glob_local.ARG_MSACCESS_PRE2008
        return

    if "." in ARG_MSACCESS:
        # ERROR.00.904 '{msaccess}': the MS Access database file name must not
        # contain a file extension
        terminate_fatal(glob_local.ERROR_00_904.replace("{msaccess}", args.msaccess))

    if not (
        ARG_MSACCESS[0:2] == "up"
        and "00" < ARG_MSACCESS[2:4] <= "31"
        and ARG_MSACCESS[4:]
        in [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]
    ):
        # ERROR.00.903 '{msaccess}' is not a valid NTSB compliant
        # MS Access database name
        terminate_fatal(glob_local.ERROR_00_903.replace("{msaccess}", args.msaccess))

    ARG_MSACCESS = ARG_MSACCESS[0:4] + ARG_MSACCESS[4:].upper()


# -----------------------------------------------------------------------------

def check_arg_msexcel(args: argparse.Namespace) -> None:
    """Check the command line argument: -e / --msexcel.

    This function checks whether the command line argument -e / --msexcel
    is valid. If the argument is required but not provided, or if the file
    does not exist or is not a valid Microsoft Excel file, a fatal error
    is raised.

    Args:
        args (argparse.Namespace): Command line arguments.

    """
    global ARG_MSEXCEL

    # Check if the argument is required but not provided
    if ARG_TASK in [glob_local.ARG_TASK_L_C_D]:
        if not args.msexcel:
            # ERROR.00.923 The task '{task}' requires valid
            # argument '-e' or '--msexcel'
            terminate_fatal(glob_local.ERROR_00_923.replace("{task}", ARG_TASK))
    # Check if the argument is provided but not required
    elif args.msexcel:
        # ERROR.00.924 The task '{task}' does not require an
        # argument '-e' or '--msexcel'
        terminate_fatal(glob_local.ERROR_00_924.replace("{task}", ARG_TASK))
    else:
        return

    # Get the directory name and file name
    directory_name = ""
    if ARG_TASK == glob_local.ARG_TASK_L_C_D:
        directory_name = io_settings.settings.correction_work_dir

    ARG_MSEXCEL = args.msexcel

    if ARG_TASK in [glob_local.ARG_TASK_L_C_D, glob_local.ARG_TASK_L_C_D]:
        file_name = Path(directory_name) / ARG_MSEXCEL
    else:
        file_name = Path(directory_name) / ARG_MSEXCEL / ".xlsx"

    # Check if the file exists and is a valid Microsoft Excel file
    try:
        load_workbook(
            filename=file_name,
            read_only=True,
            data_only=True,
        )
    except FileNotFoundError:
        # ERROR.00.932 File '{filename}' is not existing
        terminate_fatal(glob_local.ERROR_00_932.replace("{filename}", file_name))
    except (InvalidFileException, zipfile.BadZipFile):
        # ERROR.00.925 '{msexcel}' is not a valid Microsoft Excel file
        terminate_fatal(glob_local.ERROR_00_925.replace("{msexcel}", file_name))


# -----------------------------------------------------------------------------

def check_arg_task(args: argparse.Namespace) -> None:
    """Check the command line argument: -t / --task.

    Check if the specified task is a valid task name. If not, terminate the program
    with a fatal error message.

    Args:
        args (argparse.Namespace): Command line arguments.

    """
    global ARG_TASK

    ARG_TASK = args.task.lower()

    # Check if the specified task is a valid task name
    if ARG_TASK not in [
        glob_local.ARG_TASK_A_O_C,
        glob_local.ARG_TASK_C_D_S,
        glob_local.ARG_TASK_C_L_L,
        glob_local.ARG_TASK_C_P_D,
        glob_local.ARG_TASK_D_N_A,
        glob_local.ARG_TASK_F_N_A,
        glob_local.ARG_TASK_GENERATE,
        glob_local.ARG_TASK_L_A_P,
        glob_local.ARG_TASK_L_C_D,
        glob_local.ARG_TASK_L_C_S,
        glob_local.ARG_TASK_L_N_A,
        glob_local.ARG_TASK_L_S_D,
        glob_local.ARG_TASK_L_S_E,
        glob_local.ARG_TASK_L_Z_D,
        glob_local.ARG_TASK_R_D_S,
        glob_local.ARG_TASK_U_D_S,
        glob_local.ARG_TASK_VERSION,
        glob_local.ARG_TASK_V_N_D,
    ]:
        # Terminate the program with a fatal error message
        terminate_fatal(
            "The specified task is neither '"
            + glob_local.ARG_TASK_A_O_C
            + "' nor '"
            + glob_local.ARG_TASK_C_D_S
            + "' nor '"
            + glob_local.ARG_TASK_C_L_L
            + "' nor '"
            + glob_local.ARG_TASK_C_P_D
            + "' nor '"
            + glob_local.ARG_TASK_D_N_A
            + "' nor '"
            + glob_local.ARG_TASK_F_N_A
            + "' nor '"
            + glob_local.ARG_TASK_GENERATE
            + "' nor '"
            + glob_local.ARG_TASK_L_A_P
            + "' nor '"
            + glob_local.ARG_TASK_L_C_D
            + "' nor '"
            + glob_local.ARG_TASK_L_C_S
            + "' nor '"
            + glob_local.ARG_TASK_L_N_A
            + "' nor '"
            + glob_local.ARG_TASK_L_S_D
            + "' nor '"
            + glob_local.ARG_TASK_L_S_E
            + "' nor '"
            + glob_local.ARG_TASK_L_Z_D
            + "' nor '"
            + glob_local.ARG_TASK_R_D_S
            + "' nor '"
            + glob_local.ARG_TASK_U_D_S
            + "' nor '"
            + glob_local.ARG_TASK_VERSION
            + "' nor '"
            + glob_local.ARG_TASK_V_N_D
            + f"': {args.task}",
        )


# -----------------------------------------------------------------------------

def cleansing_postgres_data() -> None:
    """c_p_d: Cleansing PostgreSQL data.

    This function cleanses the PostgreSQL database.
    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.065 Cleansing PostgreSQL data
    io_utils.progress_msg(glob_local.INFO_00_065)
    io_utils.progress_msg("-" * 80)

    db_dml_corr.cleansing_postgres_data()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def correct_dec_lat_lng() -> None:
    """c_l_l: Correct US decimal latitudes and longitudes.

    This function corrects the decimal latitude and longitude values in the
    PostgreSQL database.
    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.040 Correct decimal US latitudes and longitudes
    io_utils.progress_msg(glob_local.INFO_00_040)
    io_utils.progress_msg("-" * 80)

    db_dml_corr.correct_dec_lat_lng()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def create_db_schema() -> None:
    """c_d_s: Create the PostgreSQL database schema.

    This function creates the PostgreSQL database schema.
    """
    logging.debug(io_glob.LOGGER_START)

    # Create the PostgreSQL database schema
    db_ddl_base.create_db_schema()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def download_ntsb_msaccess_file(msaccess: str) -> None:
    """d_n_a: Download a NTSB MS Access database file.

    This function downloads a NTSB MS Access database file.

    Args:
        msaccess (str):
            The NTSB MS Access database file without file extension.

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.047 Download NTSB MS Access database file '{msaccess}'
    io_utils.progress_msg(glob_local.INFO_00_047.replace("{msaccess}", msaccess))
    io_utils.progress_msg("-" * 80)

    # Download the specified NTSB MS Access database file
    db_dml_msaccess.download_ntsb_msaccess_file(msaccess)

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def find_nearest_airports() -> None:
    """f_n_a: Find the nearest airports.

    This function determines the nearest airports to the event sites.
    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.086 Find the nearest airports
    io_utils.progress_msg(glob_local.INFO_00_086)
    io_utils.progress_msg("-" * 80)

    # Find the nearest airports
    db_dml_corr.find_nearest_airports()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def generate_sql() -> None:
    """Generate SQL statements: INSERT & UPDATE.

    This function generates SQL statements: INSERT & UPDATE.

    It calls the function :func:`code_generator.generate_sql` to generate the
    SQL statements.

    .. :noindex:
    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.044 Generate SQL statements
    io_utils.progress_msg(glob_local.INFO_00_044)
    io_utils.progress_msg("-" * 80)

    code_generator.generate_sql()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def get_args() -> None:
    """Load the command line arguments into the memory.

    This function loads the command line arguments using the `argparse` module
    and checks the arguments for validity.

    The available command line arguments are:

    - **-e**, **--msexcel**: The MS Excel file.
    - **-m**, **--msaccess**: The Microsoft Access database file:
        - **avall**: Data from January 1, 2008 to today.
        - **pre2008**: Data from January 1, 1982 to December 31, 2007.
        - **upDDMON**: New additions and updates until DD day in the month MON.
    - **-t**, **--task**: The task to execute:
        - **a_o_c**: Load aviation occurrence categories into PostgreSQL.
        - **c_d_s**: Create the PostgreSQL database schema.
        - **c_l_l**: Correct decimal US latitudes and longitudes.
        - **c_p_d**: Cleansing PostgreSQL data.
        - **d_n_a**: Download a NTSB MS Access database file.
        - **f_n_a**: Find the nearest airports.
        - **generate**: Generate SQL statements.
        - **l_a_p**: Load airport data into PostgreSQL.
        - **l_c_d**: Load data from a correction file into PostgreSQL.
        - **l_c_s**: Load country and state data into PostgreSQL.
        - **l_n_a**: Load NTSB MS Access database data into PostgreSQL.
        - **l_s_d**: Load simplemaps data into PostgreSQL.
        - **l_s_e**: Load sequence of events data into PostgreSQL.
        - **l_z_d**: Load ZIP Code Database data into PostgreSQL.
        - **r_d_s**: Update the PostgreSQL database schema.
        - **u_d_s**: Refresh the PostgreSQL database schema.
        - **version**: Show the current version of IO-AVSTATS.
        - **v_n_d**: Verify selected NTSB data.

    """
    logging.debug(io_glob.LOGGER_START)

    parser = argparse.ArgumentParser(
        description="Perform a IO-AVSTATS task",
        prog="launcher",
        prefix_chars="--",
        usage="%(prog)s options",
    )

    # -------------------------------------------------------------------------
    # Definition of the command line arguments.
    # ------------------------------------------------------------------------
    parser.add_argument(
        "-e",
        "--msexcel",
        help="the MS Excel file",
        metavar="msexcel",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-m",
        "--msaccess",
        help="the Microsoft Access database file: '"
        + glob_local.ARG_MSACCESS_AVALL
        + "' (Data from January 1, 2008 to today) or '"
        + glob_local.ARG_MSACCESS_PRE2008
        + "' (Data from January 1, 1982 to December 31, 2007) or '"
        + glob_local.ARG_MSACCESS_UPDDMON
        + "' (New additions and updates until DD day in the month MON)",
        metavar="msaccess",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-t",
        "--task",
        help="the task to execute: '"
        + glob_local.ARG_TASK_A_O_C
        + "' (Load aviation occurrence categories into PostgreSQL) or '"
        + glob_local.ARG_TASK_C_D_S
        + "' (Create the PostgreSQL database schema) or '"
        + glob_local.ARG_TASK_C_L_L
        + "' (Correct decimal US latitudes and longitudes) or '"
        + glob_local.ARG_TASK_C_P_D
        + "' (Cleansing PostgreSQL data) or '"
        + glob_local.ARG_TASK_D_N_A
        + "' (Download a NTSB MS Access database file) or '"
        + glob_local.ARG_TASK_F_N_A
        + "' (Find the nearest airports) or '"
        + glob_local.ARG_TASK_GENERATE
        + "' (Generate SQL statements) or '"
        + glob_local.ARG_TASK_L_A_P
        + "' (Load airport data into PostgreSQL) or '"
        + glob_local.ARG_TASK_L_C_D
        + "' (Load data from a correction file into PostgreSQL) or '"
        + glob_local.ARG_TASK_L_C_S
        + "' (Load country and state data into PostgreSQL) or '"
        + glob_local.ARG_TASK_L_N_A
        + "' (Load NTSB MS Access database data into PostgreSQL) or '"
        + glob_local.ARG_TASK_L_S_D
        + "' (Load simplemaps data into PostgreSQL) or '"
        + glob_local.ARG_TASK_L_S_E
        + "' (Load sequence of events data into PostgreSQL) or '"
        + glob_local.ARG_TASK_L_Z_D
        + "' (Load ZIP Code Database data into PostgreSQL) or '"
        + glob_local.ARG_TASK_R_D_S
        + "' (Update the PostgreSQL database schema) or '"
        + glob_local.ARG_TASK_U_D_S
        + "' (Refresh the PostgreSQL database schema) or '"
        + glob_local.ARG_TASK_VERSION
        + "' (Show the current version of IO-AVSTATS)"
        + glob_local.ARG_TASK_V_N_D
        + "' (Verify selected NTSB data)",
        metavar="task",
        required=True,
        type=str,
    )

    # -------------------------------------------------------------------------
    # Load and check the command line arguments.
    # -------------------------------------------------------------------------
    parsed_args = parser.parse_args()

    check_arg_task(parsed_args)

    check_arg_msaccess(parsed_args)

    check_arg_msexcel(parsed_args)

    # --------------------------------------------------------------------------
    # Display the command line arguments.
    # --------------------------------------------------------------------------
    if parsed_args.msexcel:
        # INFO.00.041 Arguments {task}='{value_task}' {msexcel}='{value_msexcel}'
        progress_msg(
            glob_local.INFO_00_041.replace("{task}", glob_local.ARG_TASK)
            .replace("{value_task}", parsed_args.task)
            .replace("{msexcel}", glob_local.ARG_MSEXCEL)
            .replace("{value_msexcel}", parsed_args.msexcel),
        )
    elif parsed_args.msaccess:
        # INFO.00.008 Arguments {task}='{value_task}' {msaccess}='{value_msaccess}'
        progress_msg(
            glob_local.INFO_00_008.replace("{task}", glob_local.ARG_TASK)
            .replace("{value_task}", parsed_args.task)
            .replace("{msaccess}", glob_local.ARG_MSACCESS)
            .replace("{value_msaccess}", parsed_args.msaccess),
        )
    else:
        # INFO.00.005 Arguments {task}='{value_task}'
        progress_msg(
            glob_local.INFO_00_005.replace("{task}", glob_local.ARG_TASK).replace(
                "{value_task}",
                parsed_args.task,
            ),
        )

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def load_aviation_occurrence_categories() -> None:
    """a_o_c: Load aviation occurrence categories into PostgreSQL.

    This function loads the aviation occurrence categories into the PostgreSQL
    database.
    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.073 Load aviation occurrence categories
    io_utils.progress_msg(glob_local.INFO_00_073)
    io_utils.progress_msg("-" * 80)

    # Load the aviation occurrence categories.
    db_dml_base.load_aviation_occurrence_categories()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def load_airport_data() -> None:
    """l_a_p: Load airport data into PostgreSQL.

    This function loads the airport data into the PostgreSQL database.
    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.085 Load airports
    io_utils.progress_msg(glob_local.INFO_00_085)
    io_utils.progress_msg("-" * 80)

    # Load the airport data.
    db_dml_base.load_airport_data()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def load_correction_data(filename: str) -> None:
    """l_c_d: Load data from a correction file into PostgreSQL.

    Load data from a correction file into the PostgreSQL database.

    Args:
        filename (str):
            The filename of the correction file.

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.042 Load corrections from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_042.replace("{filename}", filename),
    )
    io_utils.progress_msg("-" * 80)

    # Load the correction data.
    db_dml_corr.load_correction_data(filename)

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def load_country_state_data() -> None:
    """l_c_s: Load country and state data into PostgreSQL.

    This function loads the country and state data from a CSV file into the
    PostgreSQL database.

    Notes:
        - The country and state data is loaded from a CSV file.
        - The CSV file is assumed to be in the same directory as the script.
        - The CSV file is assumed to have the following columns:
            - country
            - country_name
            - state
            - state_name
        - The data is loaded into the PostgreSQL tables:
            - io_countries
            - io_states

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.057 Load country and state data
    io_utils.progress_msg(glob_local.INFO_00_057)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_country_state_data()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def load_ntsb_msaccess_data(msaccess: str) -> None:
    """l_n_a: Load NTSB MS Access database data into PostgreSQL.

    Load the NTSB MS Access database data into the PostgreSQL database.

    Args:
        msaccess (str):
            The NTSB MS Access database file without file extension.

    Notes:
        - The NTSB MS Access database file is assumed to be in the same directory as the script.
        - The NTSB MS Access database file is assumed to have the following tables:
            - aircraft
            - dt_aircraft
            - dt_events
            - dt_flight_crew
            - engines
            - events
            - events_sequence
            - findings
            - flight_crew
            - flight_time
            - injury
            - narratives
            - ntsb_admin
            - occurrences
            - seq_of_events
        - The data is loaded into the PostgreSQL tables:
            - aircraft
            - dt_aircraft
            - dt_events
            - dt_flight_crew
            - engines
            - events
            - events_sequence
            - findings
            - flight_crew
            - flight_time
            - injury
            - narratives
            - ntsb_admin
            - occurrences
            - seq_of_events

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.049 Load NTSB MS Access database data from file '{msaccess}'
    io_utils.progress_msg(glob_local.INFO_00_049.replace("{msaccess}", msaccess))
    io_utils.progress_msg("-" * 80)

    # Load the NTSB MS Access database data.
    db_dml_msaccess.load_ntsb_msaccess_data(msaccess)

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def load_sequence_of_events() -> None:
    """l_s_e: Load sequence of events data into PostgreSQL.

    Loads the sequence of events data from a CSV file into the PostgreSQL
    database.

    Notes:
        - The sequence of events data is loaded from a CSV file.
        - The CSV file is assumed to be in the same directory as the script.
        - The CSV file is assumed to have the following columns:
            - eventsoe_no
            - meaning
            - cictt_code
        - The data is loaded into the PostgreSQL table:
            - seq_of_events

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.075 Load sequence of events data
    io_utils.progress_msg(glob_local.INFO_00_075)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_sequence_of_events()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def load_simplemaps_data() -> None:
    """l_s_d: Load simplemaps data into PostgreSQL.

    Notes:
        - The simplemaps data is loaded from two CSV files.
        - The CSV files are assumed to be in the same directory as the script.
        - The CSV files are assumed to have the following columns:
            - us_cities.csv:
                - city
                - lat
                - lng
                - state
                - state_id
                - zips
            - us_zips.csv:
                - zip
                - lat
                - lng
                - city
                - state
                - state_id
                - county
                - county_fips
        - The data is loaded into the PostgreSQL tables:
            - io_lat_lng

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.050 Load simplemaps data
    io_utils.progress_msg(glob_local.INFO_00_050)
    io_utils.progress_msg("-" * 80)

    # Load the simplemaps data.
    db_dml_base.load_simplemaps_data()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def load_zip_code_db_data() -> None:
    """l_z_d: Load ZIP Code Database data into PostgreSQL.

    Notes:
        - The ZIP Code Database data is loaded from an Excel file.
        - The Excel file is assumed to be in the same directory as the script.
        - The Excel file is assumed to have the following columns:
            - zip_code
            - lat
            - lng
            - city
            - state
            - state_id
            - county
            - county_fips
        - The data is loaded into the PostgreSQL table:
            - io_lat_lng

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.056 Load ZIP Code Database data
    io_utils.progress_msg(glob_local.INFO_00_056)
    io_utils.progress_msg("-" * 80)

    db_dml_base.load_zip_codes_org_data()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message to be displayed.

    Notes:
        - The progress message is only displayed if the verbose mode is on.

    """
    if io_settings.settings.is_verbose:
        io_utils.progress_msg_core(msg)


# -----------------------------------------------------------------------------

def progress_msg_time_elapsed(duration: int, event: str) -> None:
    """Create a time elapsed message.

    The time elapsed is displayed in seconds and milliseconds.

    Args:
        duration (int): Time elapsed in ns.
        event (str): Event description.

    Notes:
        - The time elapsed message is only displayed if the verbose mode is on.

    """
    io_utils.progress_msg_time_elapsed(duration, event)


# -----------------------------------------------------------------------------

def refresh_db_schema() -> None:
    """Refresh the PostgreSQL database schema.

    Notes:
        - This function uses the following functions:
            - db_ddl_base.refresh_db_schema()

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.071 Refreshing the database schema
    io_utils.progress_msg(glob_local.INFO_00_071)
    io_utils.progress_msg("-" * 80)

    db_ddl_base.refresh_db_schema()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message to be displayed.

    Notes:
        - This function is used to terminate the application immediately with
          an error message.

    """
    io_utils.terminate_fatal(error_msg)


# -----------------------------------------------------------------------------

def update_db_schema() -> None:
    """Update the PostgreSQL database schema.

    Notes:
        - This function calls db_ddl_base.update_db_schema() to update the
          database schema.

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.045 Updating the database schema
    io_utils.progress_msg(glob_local.INFO_00_045)
    io_utils.progress_msg("-" * 80)

    # Update the database schema.
    db_ddl_base.update_db_schema()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def verify_ntsb_data() -> None:
    """v_n_d: Verify selected NTSB data.

    This function verifies selected NTSB data.

    Notes:
        - This function is used to verify selected NTSB data.
        - This function is called by the main entry point of the application.

    """
    logging.debug(io_glob.LOGGER_START)

    # INFO.00.043 Verify selected NTSB data
    io_utils.progress_msg(glob_local.INFO_00_043)
    io_utils.progress_msg("-" * 80)

    # Call the function to verify selected NTSB data.
    db_dml_corr.verify_ntsb_data()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def version() -> str:
    """Return the version number of the IO-AVSTATS application.

    Notes:
        - This function returns the version number of the IO-AVSTATS application.

    Returns:
        str:
            The version number of the IO-AVSTATS application

    """
    logging.debug(io_glob.LOGGER_START)
    logging.debug(io_glob.LOGGER_END)

    # Return the version number of the IO-AVSTATS application
    return glob_local.IO_AERO_DB_VERSION
