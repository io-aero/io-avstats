# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""IO-AVSTATS-UI interface."""
from io_avstats_ui import io_config
from io_avstats_ui import io_glob
from io_avstats_ui import io_utils


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> None:
    """Initialise the root logging functionality."""
    io_utils.initialise_logger()


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message
    """
    if io_config.settings.is_verbose:
        io_utils.progress_msg_core(msg)


# ------------------------------------------------------------------
# Streamlit demo.
# ------------------------------------------------------------------
def streamlit_demo() -> None:
    """Streamlit demo."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    print("demo.fatalities()")

    io_glob.logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Terminate the application immediately.
# ------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message
    """

    io_utils.terminate_fatal(error_msg)


# ------------------------------------------------------------------
# Returns the version number of the IO-AVSTATS-DB application.
# ------------------------------------------------------------------
def version() -> str:
    """Returns the version number of the IO-AVSTATS-DB application.

    Returns:
        str:
            The version number of the IO-AVSTATS-DB application
    """
    io_glob.logger.debug(io_glob.LOGGER_START)
    io_glob.logger.debug(io_glob.LOGGER_END)

    return io_glob.IO_AVSTATS_VERSION
