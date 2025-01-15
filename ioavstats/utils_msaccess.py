# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Miscellaneous helper functions."""
from pathlib import Path

import pyodbc  # type: ignore
from iocommon import io_settings, io_utils

from ioavstats import glob_local

# -----------------------------------------------------------------------------

def get_msaccess_cursor(filename: str) -> tuple[pyodbc.Connection, pyodbc.Cursor]:
    """Create an MS Access cursor.

    Args:
        filename (str): MS Access filename.

    Returns:
        tuple[pyodbc.Connection,pyodbc.Cursor]: ODBC database connection and cursor.

    """
    # Corrected line: Use '/' to join paths when working with Path objects from pathlib
    filename_mdb = Path.cwd() / filename

    if not filename_mdb.is_file():
        # ERROR.00.932 File '{filename}' is not existing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_932.replace("{filename}", str(filename_mdb)),
        )

    # Construct the ODBC connection string
    driver = io_settings.settings.odbc_connection_string.replace(
        "{filename}",
        str(filename_mdb),  # Ensure the path is converted to a string
    )

    # INFO.00.054 ODBC driver='{driver}'
    io_utils.progress_msg(glob_local.INFO_00_054.replace("{driver}", driver))

    # Connect using the constructed driver string
    conn_ma = pyodbc.connect(driver)

    return conn_ma, conn_ma.cursor()
