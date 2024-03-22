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

import tomli
from iocommon import file, io_glob, io_utils

from ioavstats import avstats, glob_local

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
_LOCALE = "en_US.UTF-8"

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Print the version number from pyproject.toml.
# -----------------------------------------------------------------------------
def _print_project_version() -> None:
    """Print the version number from pyproject.toml."""
    # Open the pyproject.toml file in read mode
    with open("pyproject.toml", "rb") as toml_file:
        # Use toml.load() to parse the file and store the data in a dictionary
        pyproject = tomli.load(toml_file)

    # Extract the version information
    # This method safely handles cases where the key might not exist
    version = pyproject.get("project", {}).get("version")

    # Check if the version is found and print it
    if version:
        logger.info("IO-AVSTATS version: %s", version)
    else:
        # If the version isn't found, print an appropriate message
        logger.fatal("IO-AVSTATS version not found in pyproject.toml")


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def main(argv: list[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
    ----
        argv (list[str]): Command line arguments.

    """
    # Start time measurement.
    start_time = time.time_ns()

    # Provide progress messages.
    avstats.progress_msg("=" * 79)
    # INFO.00.004 Start Launcher.
    avstats.progress_msg(glob_local.INFO_00_004)

    # Initialise the logging functionality.
    avstats.initialise_logger()

    logger.debug(io_glob.LOGGER_START)
    logger.info("param argv=%s", argv)

    logger.info("Start launcher.py")

    try:
        locale.setlocale(locale.LC_ALL, glob_local.LOCALE)
    except locale.Error:
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    logger.info("locale=%s", locale.getlocale())

    # Load the command line arguments.
    avstats.get_args()

    avstats.progress_msg("-" * 79)

    # Perform the processing
    if avstats.ARG_TASK == glob_local.ARG_TASK_A_O_C:
        avstats.load_aviation_occurrence_categories()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_C_D_S:
        avstats.create_db_schema()
        io_utils.progress_msg("-" * 80)
        avstats.update_db_schema()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_C_L_L:
        avstats.correct_dec_lat_lng()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_C_P_D:
        avstats.cleansing_postgres_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_D_N_A:
        avstats.download_ntsb_msaccess_file(avstats.ARG_MSACCESS)
    elif avstats.ARG_TASK == glob_local.ARG_TASK_F_N_A:
        avstats.find_nearest_airports()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_GENERATE:
        avstats.generate_sql()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_A_P:
        avstats.load_airport_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_C_D:
        avstats.load_correction_data(avstats.ARG_MSEXCEL)
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_C_S:
        avstats.load_country_state_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_N_A:
        avstats.load_ntsb_msaccess_data(avstats.ARG_MSACCESS)
        avstats.cleansing_postgres_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_S_D:
        avstats.load_simplemaps_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_S_E:
        avstats.load_sequence_of_events()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_L_Z_D:
        avstats.load_zip_code_db_data()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_R_D_S:
        avstats.refresh_db_schema()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_U_D_S:
        avstats.update_db_schema()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_VERSION:
        file.print_pkg_structs(["iocommon"])
        _print_project_version()
    elif avstats.ARG_TASK == glob_local.ARG_TASK_V_N_D:
        avstats.verify_ntsb_data()
    else:
        io_utils.terminate_fatal(
            # FATAL.00.926 The task '{task}' is invalid
            glob_local.FATAL_00_926.replace("{task}", avstats.ARG_TASK),
        )

    avstats.progress_msg("-" * 79)

    # Stop time measurement.
    avstats.progress_msg_time_elapsed(
        time.time_ns() - start_time,
        "launcher",
    )

    # INFO.00.006 End   Launcher
    avstats.progress_msg(glob_local.INFO_00_006)
    avstats.progress_msg("=" * 79)

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
