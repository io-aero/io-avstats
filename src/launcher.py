# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Module io_avstats_db: Entry Point Functionality.

This is the entry point to the application IO-AVSTATS.
"""
import argparse
import locale
import sys
import time

from io_avstats_db import avstats
from io_avstats_db import io_glob

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

ARG_MSACCESS = ""
ARG_TASK = ""


# -----------------------------------------------------------------------------
# Check the command line argument: -m / --msaccess.
# -----------------------------------------------------------------------------
def _check_arg_msaccess(args: argparse.Namespace):
    global ARG_MSACCESS  # pylint: disable=global-statement

    if ARG_TASK in [
        io_glob.ARG_TASK_D_M_A,
        io_glob.ARG_TASK_L_M_A,
    ]:
        if not args.msaccess:
            # ERROR.00.901 The task '{task}' requires valid
            # argument '-m' or '--msaccess'
            avstats.terminate_fatal(io_glob.ERROR_00_901.replace("{task}", ARG_TASK))
    else:
        if args.msaccess:
            # ERROR.00.902 The task '{task}' does not require an
            # argument '-m' or '--msaccess'
            avstats.terminate_fatal(io_glob.ERROR_00_902.replace("{task}", ARG_TASK))
        else:
            return

    ARG_MSACCESS = args.msaccess.lower()

    if ARG_MSACCESS == io_glob.ARG_MSACCESS_AVALL:
        return

    if ARG_MSACCESS == io_glob.ARG_MSACCESS_PRE2008.lower():
        ARG_MSACCESS = io_glob.ARG_MSACCESS_PRE2008
        return

    if "." in ARG_MSACCESS:
        # ERROR.00.904 '{msaccess}': the MS Access database file name must not
        # contain a file extension
        avstats.terminate_fatal(
            io_glob.ERROR_00_904.replace("{msaccess}", args.msaccess)
        )

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
        avstats.terminate_fatal(
            io_glob.ERROR_00_903.replace("{msaccess}", args.msaccess)
        )

    ARG_MSACCESS = ARG_MSACCESS[0:4] + ARG_MSACCESS[4:].upper()


# -----------------------------------------------------------------------------
# Check the command line argument: -t / --task.
# -----------------------------------------------------------------------------
def _check_arg_task(args: argparse.Namespace):
    global ARG_TASK  # pylint: disable=global-statement

    ARG_TASK = args.task.lower()

    if not (
        ARG_TASK
        in [
            io_glob.ARG_TASK_C_D_S,
            io_glob.ARG_TASK_D_D_S,
            io_glob.ARG_TASK_D_M_A,
            io_glob.ARG_TASK_GENERATE,
            io_glob.ARG_TASK_L_M_A,
            io_glob.ARG_TASK_VERSION,
        ]
    ):
        avstats.terminate_fatal(
            "The specified task is neither '"
            + io_glob.ARG_TASK_C_D_S
            + "' nor '"
            + io_glob.ARG_TASK_D_D_S
            + "' nor '"
            + io_glob.ARG_TASK_D_M_A
            + "' nor '"
            + io_glob.ARG_TASK_GENERATE
            + "' nor '"
            + io_glob.ARG_TASK_L_M_A
            + "' nor '"
            + io_glob.ARG_TASK_VERSION
            + f"': {args.task}",
        )


# -----------------------------------------------------------------------------
# Load the command line arguments into the memory.
# -----------------------------------------------------------------------------
def _get_args():
    """Load the command line arguments into the memory.

    The only possible command line argument is 'task'.

    'task' is a mandatory input and defines which task should be
    executed:

        - c_d_s : PostgreSQL: Create the database schema
    """
    io_glob.logger.debug(io_glob.LOGGER_START)

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
        "-m",
        "--msaccess",
        help="the microsoft access database file: '"
        + io_glob.ARG_MSACCESS_AVALL
        + "' (Data from January 1, 2008 to today) or '"
        + io_glob.ARG_MSACCESS_PRE2008
        + "' (Data from January 1, 1982 to December 31, 2007) or '"
        + io_glob.ARG_MSACCESS_UPDDMON
        + "' (New additions and updates until DD day in the month MON)",
        metavar="msaccess",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-t",
        "--task",
        help="the task to execute: '"
        + io_glob.ARG_TASK_C_D_S
        + "' (PostgreSQL: Create the database schema) or '"
        + io_glob.ARG_TASK_D_D_S
        + "' (PostgreSQL: Drop the database schema) or '"
        + io_glob.ARG_TASK_D_M_A
        + "' (PostgreSQL: Download Microsoft Access database file) or '"
        + io_glob.ARG_TASK_GENERATE
        + "' (Generate SQL statements) or '"
        + io_glob.ARG_TASK_L_M_A
        + "' (PostgreSQL: Load Microsoft Access database data) or '"
        + io_glob.ARG_TASK_VERSION
        + "' (show the current version of IO-AVSTATS)",
        metavar="task",
        required=True,
        type=str,
    )

    # -------------------------------------------------------------------------
    # Load and check the command line arguments.
    # -------------------------------------------------------------------------
    parsed_args = parser.parse_args()

    _check_arg_task(parsed_args)

    _check_arg_msaccess(parsed_args)

    # --------------------------------------------------------------------------
    # Display the command line arguments.
    # --------------------------------------------------------------------------
    if parsed_args.msaccess:
        # INFO.00.008 Arguments {task}='{value_task}' {msaccess}='{value_msaccess}'
        avstats.progress_msg(
            io_glob.INFO_00_008.replace("{task}", io_glob.ARG_TASK)
            .replace("{value_task}", parsed_args.task)
            .replace("{msaccess}", io_glob.ARG_MSACCESS)
            .replace("{value_msaccess}", parsed_args.msaccess),
        )
    else:
        # INFO.00.005 Arguments {task}='{value_task}'
        avstats.progress_msg(
            io_glob.INFO_00_005.replace("{task}", io_glob.ARG_TASK).replace(
                "{value_task}", parsed_args.task
            ),
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def main(argv: list[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
        argv (list[str]): Command line arguments.
    """
    # Start time measurement.
    start_time = time.time_ns()

    # Provide progress messages.
    avstats.progress_msg("=" * 79)
    # INFO.00.004 Start Launcher.
    avstats.progress_msg(io_glob.INFO_00_004)

    # Initialise the logging functionality.
    avstats.initialise_logger()

    io_glob.logger.debug(io_glob.LOGGER_START)
    io_glob.logger.debug("param argv=%s", argv)

    io_glob.logger.info("Start launcher.py")

    locale.setlocale(locale.LC_ALL, io_glob.LOCALE)

    # Load the command line arguments.
    _get_args()

    avstats.progress_msg("-" * 79)

    # Perform the processing
    if ARG_TASK == io_glob.ARG_TASK_C_D_S:
        avstats.create_db_schema()
    elif ARG_TASK == io_glob.ARG_TASK_D_D_S:
        avstats.drop_db_schema()
    elif ARG_TASK == io_glob.ARG_TASK_D_M_A:
        avstats.download_msaccess_file(ARG_MSACCESS)
    elif ARG_TASK == io_glob.ARG_TASK_GENERATE:
        avstats.generate_sql()
    elif ARG_TASK == io_glob.ARG_TASK_L_M_A:
        avstats.load_msaccess_data(ARG_MSACCESS)
    elif ARG_TASK == io_glob.ARG_TASK_VERSION:
        print(f"The version of IO-AVSTATS is {avstats.version()}")

    avstats.progress_msg("-" * 79)

    # Stop time measurement.
    avstats.progress_msg_time_elapsed(
        time.time_ns() - start_time,
        "launcher",
    )

    # INFO.00.006 End   Launcher
    avstats.progress_msg(io_glob.INFO_00_006)
    avstats.progress_msg("=" * 79)

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
