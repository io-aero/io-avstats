# Copyright (c) 2022 FAA-VAIL-Project. All rights reserved.
# Use of this source code is governed by the GNU LESSER GENERAL
# PUBLIC LICENSE, that can be found in the LICENSE.md file.
"""Launcher: coverage testing."""
import logging
import os
import platform
import time

from ioavstatsdb import glob
from iocommon import io_glob
from iocommon.io_config import settings

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Test case: d_d_c   - Delete the PostgreSQL database container.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh d_d_c")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh d_d_c")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat d_d_c")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: d_d_f   - Delete the PostgreSQL database files.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_f():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = 0
    elif platform.system() == "Linux":
        exit_code = 0
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat d_d_f")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - s_d_c   - Set up the PostgreSQL database container.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_s_d_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = 0
    elif platform.system() == "Linux":
        exit_code = 0
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat s_d_c")
        time.sleep(10)
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - c_d_s   - Create the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_c_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = 0
    elif platform.system() == "Linux":
        exit_code = 0
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat c_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - u_d_s   - Update the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_u_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = 0
    elif platform.system() == "Linux":
        exit_code = 0
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat u_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - a_o_c   - Load aviation occurrence categories
#                                   into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_a_o_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = 0
    elif platform.system() == "Linux":
        exit_code = 0
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat a_o_c")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)
