# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Miscellaneous helper functions."""
import os
from pathlib import Path

import pyodbc  # type: ignore
from iocommon import io_config
from iocommon import io_utils

from ioavstats import glob


# ------------------------------------------------------------------
# Create an ODBC database connection and cursor.
# ------------------------------------------------------------------
def get_msaccess_cursor(filename: str) -> tuple[pyodbc.Connection, pyodbc.Cursor]:
    """Create an MS Access cursor.

    Args:
        filename (str): MS Access filename.

    Returns:
        tuple[pyodbc.Connection,pyodbc.Cursor]: ODBC database connection and cursor.

    """
    filename_mdb = os.getcwd() + os.path.sep + filename

    if not Path(filename_mdb).is_file():
        # ERROR.00.932 File '{filename}' is not existing
        io_utils.terminate_fatal(glob.ERROR_00_932.replace("{filename}", filename_mdb))

    # Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ={filename}}
    driver = io_config.settings.odbc_connection_string.replace(
        "{filename}", filename_mdb
    )

    # INFO.00.054 ODBC driver='{driver}'
    io_utils.progress_msg(glob.INFO_00_054.replace("{driver}", driver))

    conn_ma = pyodbc.connect(driver)  # pylint: disable=c-extension-no-member

    return conn_ma, conn_ma.cursor()
