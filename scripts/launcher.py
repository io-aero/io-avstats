# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Package ioavstats: Entry Point Functionality.

This is the entry point to the application IO-AVSTATS.
"""
import locale
import logging
import sys
import time
from pathlib import Path

import tomli
from iocommon import io_glob, io_logger, io_utils

from ioavstats import avstats, glob_local

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

io_logger.initialise_logger()

_LOCALE = "en_US.UTF-8"


# -----------------------------------------------------------------------------

def _print_project_version() -> None:
    """Print the version number from pyproject.toml.

    Reads the pyproject.toml file and extracts the version number from it. If the version number is
    found, it is logged at the INFO level. If the version number is not found, the program is
    terminated with a fatal error message.

    """
    # Open the pyproject.toml file in read mode
    with Path("pyproject.toml").open("rb") as toml_file:
        # Use tomli.load() to parse the file and store the data in a dictionary
        pyproject = tomli.load(toml_file)

    # Extract the version information
    # This method safely handles cases where the key might not exist
    version = pyproject.get("project", {}).get("version")

    # Check if the version is found and print it
    if version:
        logging.info("IO-AVSTATS version: %s", version)
    else:
        # If the version isn't found, print an appropriate message
        logging.fatal("IO-AVSTATS version not found in pyproject.toml")


# -----------------------------------------------------------------------------

def main(argv: list[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
        argv : list[str]
            Command line arguments.

    """
    # Start time measurement.
    start_time = time.time_ns()

    # Provide progress messages.
    io_utils.progress_msg("=" * 79)
    # INFO.00.004 Start Launcher
    io_utils.progress_msg(glob_local.INFO_00_004)

    logging.debug(io_glob.LOGGER_START)
    logging.info("param argv=%s", argv)

    logging.info("Start launcher.py")

    try:
        # Set the locale for the application
        locale.setlocale(locale.LC_ALL, glob_local.LOCALE)
    except locale.Error:
        # Fallback to the default locale, if the one specified does not exist
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    logging.info("locale=%s", locale.getlocale())

    # Load the command line arguments.
    avstats.get_args()

    avstats.progress_msg("-" * 79)

    # Perform the processing
    if avstats.ARG_TASK == glob_local.ARG_TASK_A_O_C:
        # Load aviation occurrence categories.
        avstats.load_aviation_occurrence_categories()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_C_D_S:
        # Create database schema.
        avstats.create_db_schema()
        io_utils.progress_msg("-" * 80)
        # Update database schema.
        avstats.update_db_schema()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_C_L_L:
        # Correct dec lat and lng.
        avstats.correct_dec_lat_lng()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_C_P_D:
        # Cleansing PostgreSQL data.
        avstats.cleansing_postgres_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_D_N_A:
        # Download NTSB MS Access file.
        avstats.download_ntsb_msaccess_file(avstats.ARG_MSACCESS)
    elif avstats.ARG_TASK == glob_local.ARG_TASK_F_N_A:
        # Find nearest airports.
        avstats.find_nearest_airports()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_GENERATE:
        # Generate SQL.
        avstats.generate_sql()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_A_P:
        # Load airport data.
        avstats.load_airport_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_C_D:
        # Load correction data.
        avstats.load_correction_data(avstats.ARG_MSEXCEL)
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_C_S:
        # Load country state data.
        avstats.load_country_state_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_N_A:
        # Load NTSB MS Access data.
        avstats.load_ntsb_msaccess_data(avstats.ARG_MSACCESS)
        # Cleansing PostgreSQL data.
        avstats.cleansing_postgres_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_S_D:
        # Load simplemaps data.
        avstats.load_simplemaps_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_S_E:
        # Load sequence of events.
        avstats.load_sequence_of_events()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_Z_D:
        # Load zip code db data.
        avstats.load_zip_code_db_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_R_D_S:
        # Refresh database schema.
        avstats.refresh_db_schema()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_U_D_S:
        # Update database schema.
        avstats.update_db_schema()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_VERSION:
        # Print the version number from pyproject.toml.
        _print_project_version()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_V_N_D:
        # Verify NTSB data.
        avstats.verify_ntsb_data()
    else:
        io_utils.terminate_fatal(
            # FATAL.00.926 The task '{task}' is invalid
            glob_local.FATAL_00_926.replace("{task}", avstats.ARG_TASK),
        )

    io_utils.progress_msg("-" * 79)

    # Stop time measurement.
    io_utils.progress_msg_time_elapsed(
        time.time_ns() - start_time,
        "launcher",
    )

    # INFO.00.006 End   Launcher
    io_utils.progress_msg(glob_local.INFO_00_006)
    io_utils.progress_msg("=" * 79)

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # not testable
    main(sys.argv)
