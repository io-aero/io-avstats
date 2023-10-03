# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Package ioavstatsdb: Entry Point Functionality.

This is the entry point to the application IO-AVSTATS.
"""
import locale
import sys
import time

from ioavstatsdb import avstatsdb
from ioavstatsdb import glob
from iocommon import io_glob
from iocommon import io_utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
_LOCALE = "en_US.UTF-8"


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def main(argv: list[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
        argv (list[str]): Command line arguments.
    """
    # Start time measurement.
    start_time = time.time_ns()

    # Provide progress messages.
    avstatsdb.progress_msg("=" * 79)
    # INFO.00.004 Start Launcher.
    avstatsdb.progress_msg(glob.INFO_00_004)

    # Initialise the logging functionality.
    avstatsdb.initialise_logger()

    io_glob.logger.debug(io_glob.LOGGER_START)
    io_glob.logger.debug("param argv=%s", argv)

    io_glob.logger.info("Start launcher.py")

    locale.setlocale(locale.LC_ALL, glob.LOCALE)

    # Load the command line arguments.
    avstatsdb.get_args()

    avstatsdb.progress_msg("-" * 79)

    # Perform the processing
    if avstatsdb.ARG_TASK == glob.ARG_TASK_A_O_C:
        avstatsdb.load_aviation_occurrence_categories()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_C_D_S:
        avstatsdb.create_db_schema()
        io_utils.progress_msg("-" * 80)
        avstatsdb.update_db_schema()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_C_L_L:
        avstatsdb.correct_dec_lat_lng()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_C_P_D:
        avstatsdb.cleansing_postgres_data()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_D_N_A:
        avstatsdb.download_ntsb_msaccess_file(avstatsdb.ARG_MSACCESS)
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_F_N_A:
        avstatsdb.find_nearest_airports()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_GENERATE:
        avstatsdb.generate_sql()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_L_A_P:
        avstatsdb.load_airport_data()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_L_C_D:
        avstatsdb.load_correction_data(avstatsdb.ARG_MSEXCEL)
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_L_C_S:
        avstatsdb.load_country_state_data()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_L_N_A:
        avstatsdb.load_ntsb_msaccess_data(avstatsdb.ARG_MSACCESS)
        avstatsdb.cleansing_postgres_data()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_L_S_D:
        avstatsdb.load_simplemaps_data()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_L_S_E:
        avstatsdb.load_sequence_of_events()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_L_Z_D:
        avstatsdb.load_zip_code_db_data()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_R_D_S:
        avstatsdb.refresh_db_schema()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_U_D_S:
        avstatsdb.update_db_schema()
    elif avstatsdb.ARG_TASK == glob.ARG_TASK_V_N_D:
        avstatsdb.verify_ntsb_data()

    avstatsdb.progress_msg("-" * 79)

    # Stop time measurement.
    avstatsdb.progress_msg_time_elapsed(
        time.time_ns() - start_time,
        "launcher",
    )

    # INFO.00.006 End   Launcher
    avstatsdb.progress_msg(glob.INFO_00_006)
    avstatsdb.progress_msg("=" * 79)

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
