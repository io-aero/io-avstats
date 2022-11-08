# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Module io_avstats_db: Entry Point Functionality.

This is the entry point to the application IO-AVSTATS.
"""
import argparse
import locale
import sys

from io_avstats_ui import avstats
from io_avstats_ui import io_glob

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

ARG_MSACCESS = ""
ARG_TASK = ""


# -----------------------------------------------------------------------------
# Check the command line argument: -t / --task.
# -----------------------------------------------------------------------------
def _check_arg_task(args: argparse.Namespace):
    global ARG_TASK  # pylint: disable=global-statement

    ARG_TASK = args.task.lower()

    if not (
        ARG_TASK
        in [
            io_glob.ARG_TASK_DEMO,
            io_glob.ARG_TASK_VERSION,
        ]
    ):
        avstats.terminate_fatal(
            "The specified task is neither '"
            + io_glob.ARG_TASK_DEMO
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
        "-t",
        "--task",
        help="the task to execute: '"
        + io_glob.ARG_TASK_DEMO
        + "' (Demo) or '"
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

    # --------------------------------------------------------------------------
    # Display the command line arguments.
    # --------------------------------------------------------------------------

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
    if ARG_TASK == io_glob.ARG_TASK_DEMO:
        avstats.streamlit_demo()
    elif ARG_TASK == io_glob.ARG_TASK_VERSION:
        print(f"The version of IO-AVSTATS is {avstats.version()}")

    avstats.progress_msg("-" * 79)

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
