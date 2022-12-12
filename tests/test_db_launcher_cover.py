# Copyright (c) 2022 FAA-VAIL-Project. All rights reserved.
# Use of this source code is governed by the GNU LESSER GENERAL
# PUBLIC LICENSE, that can be found in the LICENSE.md file.

"""launcher: coverage testing."""
import os
import platform

from io_avstats_db import io_glob  # pylint: disable=import-error
from io_avstats_db import io_utils  # pylint: disable=import-error

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test case: launcher().
# -----------------------------------------------------------------------------
def test_launcher():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        # d_d_f   - Delete the PostgreSQL database files
        io_glob.logger.debug("next: run_io_avstats_db.bat d_d_f")
        os.system("run_io_avstats_db.bat d_d_f")

        # s_d_c   - Set up the PostgreSQL database container
        io_glob.logger.debug("next: run_io_avstats_db.bat s_d_c")
        os.system("run_io_avstats_db.bat s_d_c")

        # c_d_s   - Create the PostgreSQL database schema
        io_glob.logger.debug("next: pipenv run python src\\launcher.py -t c_d_s")
        os.system("pipenv run python src\\launcher.py -t c_d_s")

        # u_d_s   - Update the PostgreSQL database schema
        io_glob.logger.debug("next: pipenv run python src\\launcher.py -t u_d_s")
        os.system("pipenv run python src\\launcher.py -t u_d_s")

        # d_n_a   - Download a NTSB MS Access database file
        io_glob.logger.debug(
            "next: pipenv run python src\\launcher.py -t d_n_a -m up22OCT"
        )
        os.system("pipenv run python src\\launcher.py -t d_n_a -m up22OCT")

        # l_n_a   - Load NTSB MS Access database data into PostgreSQL
        io_glob.logger.debug(
            "next: pipenv run python src\\launcher.py -t l_n_a -m up22OCT"
        )
        os.system("pipenv run python src\\launcher.py -t l_n_a -m up22OCT")

        # d_d_s   - Drop the PostgreSQL database schema
        io_glob.logger.debug("next: pipenv run python src\\launcher.py -t d_d_s")
        os.system("pipenv run python src\\launcher.py -t d_d_s")

        # version - Show the IO-AVSTATS-DB version
        io_glob.logger.debug("next: pipenv run python src\\launcher.py -t version")
        os.system("pipenv run python src\\launcher.py -t version")
    elif platform.system() == "Linux":
        # d_d_f   - Delete the PostgreSQL database files
        io_glob.logger.debug("next: ./run_io_avstats_db.sh d_d_f")
        os.system("./run_io_avstats_db.sh d_d_f")

        # s_d_c   - Set up the PostgreSQL database container
        io_glob.logger.debug("next: ./run_io_avstats_db.sh s_d_c")
        os.system("./run_io_avstats_db.sh s_d_c")

        # c_d_s   - Create the PostgreSQL database schema
        io_glob.logger.debug("next: pipenv run python src/launcher.py -t c_d_s")
        os.system("pipenv run python src/launcher.py -t c_d_s")

        # u_d_s   - Update the PostgreSQL database schema
        io_glob.logger.debug("next: pipenv run python src/launcher.py -t u_d_s")
        os.system("pipenv run python src/launcher.py -t u_d_s")

        # d_n_a   - Download a NTSB MS Access database file
        io_glob.logger.debug(
            "next: pipenv run python src/launcher.py -t d_n_a -m up22OCT"
        )
        os.system("pipenv run python src/launcher.py -t d_n_a -m up22OCT")

        # l_n_a   - Load NTSB MS Access database data into PostgreSQL
        io_glob.logger.debug(
            "next: pipenv run python src/launcher.py -t l_n_a -m up22OCT"
        )
        os.system("pipenv run python src/launcher.py -t l_n_a -m up22OCT")

        # d_s_f   - Download basic simplemaps files
        io_glob.logger.debug("next: pipenv run python src/launcher.py -t d_s_f")
        os.system("pipenv run python src/launcher.py -t d_s_f")

        # l_s_d   - Load simplemaps data into PostgreSQL
        io_glob.logger.debug("next: pipenv run python src/launcher.py -t l_s_d")
        os.system("pipenv run python src/launcher.py -t l_s_d")

        # c_l_k   - Correct decimal US latitudes and longitudes
        io_glob.logger.debug("next: pipenv run python src/launcher.py -t c_l_l")
        os.system("pipenv run python src/launcher.py -t c_l_l")

        # d_d_s   - Drop the PostgreSQL database schema
        io_glob.logger.debug("next: pipenv run python src/launcher.py -t d_d_s")
        os.system("pipenv run python src/launcher.py -t d_d_s")

        # version - Show the IO-AVSTATS-DB version
        io_glob.logger.debug("next: pipenv run python src/launcher.py -t version")
        os.system("pipenv run python src/launcher.py -t version")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_d_f.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_f():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        # d_d_f   - Delete the PostgreSQL database files
        io_glob.logger.debug("next: run_io_avstats_db.bat d_d_f")
        os.system("run_io_avstats_db.bat d_d_f")
    elif platform.system() == "Linux":
        # d_d_f   - Delete the PostgreSQL database files
        io_glob.logger.debug("next: ./run_io_avstats_db.sh d_d_f")
        os.system("./run_io_avstats_db.sh d_d_f")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - s_d_c.
# -----------------------------------------------------------------------------
def test_launchers_d_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        # s_d_c   - Set up the PostgreSQL database container
        io_glob.logger.debug("next: run_io_avstats_db.bat s_d_c")
        os.system("run_io_avstats_db.bat s_d_c")
    elif platform.system() == "Linux":
        # s_d_c   - Set up the PostgreSQL database container
        io_glob.logger.debug("next: ./run_io_avstats_db.sh s_d_c")
        os.system("./run_io_avstats_db.sh s_d_c")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)
