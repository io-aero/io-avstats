# Copyright (c) 2022 FAA-VAIL-Project. All rights reserved.
# Use of this source code is governed by the GNU LESSER GENERAL
# PUBLIC LICENSE, that can be found in the LICENSE.md file.

"""Launcher: coverage testing."""
import os
import platform

from ioavstatsdb import io_glob
from ioavstatsdb.io_config import settings

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test case: launcher() - version - Show the IO-AVSTATS-DB version.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_version():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    try:
        if platform.system() == "Windows":
            os.system("run_io_avstats_pytest.bat version")
        elif platform.system() == "Linux":
            os.system("./run_io_avstats_pytest.sh version")
        else:
            # ERROR.00.908 The operating system '{os}' is not supported
            assert False, io_glob.ERROR_00_908.replace("{os}", platform.system())
    except OSError as error:
        assert False, error

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: d_d_c   - Delete the PostgreSQL database container.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    try:
        if platform.system() == "Windows":
            os.system("run_io_avstats_pytest.bat d_d_c")
        elif platform.system() == "Linux":
            os.system("./run_io_avstats_pytest.sh d_d_c")
        else:
            # ERROR.00.908 The operating system '{os}' is not supported
            assert False, io_glob.ERROR_00_908.replace("{os}", platform.system())
    except OSError as error:
        assert False, error

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: d_d_f   - Delete the PostgreSQL database files.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_f():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    try:
        if platform.system() == "Windows":
            os.system("run_io_avstats_pytest.bat d_d_f")
        elif platform.system() == "Linux":
            os.system("./run_io_avstats_pytest.sh d_d_f")
        else:
            # ERROR.00.908 The operating system '{os}' is not supported
            assert False, io_glob.ERROR_00_908.replace("{os}", platform.system())
    except OSError as error:
        assert False, error

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - s_d_c   - Set up the PostgreSQL database container.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_s_d_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    try:
        if platform.system() == "Windows":
            os.system("run_io_avstats_pytest.bat s_d_c")
        elif platform.system() == "Linux":
            os.system("./run_io_avstats_pytest.sh s_d_c")
        else:
            # ERROR.00.908 The operating system '{os}' is not supported
            assert False, io_glob.ERROR_00_908.replace("{os}", platform.system())
    except OSError as error:
        assert False, error

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - c_d_s   - Create the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_c_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    try:
        if platform.system() == "Windows":
            os.system("run_io_avstats_pytest.bat c_d_s")
        elif platform.system() == "Linux":
            os.system("./run_io_avstats_pytest.sh c_d_s")
        else:
            # ERROR.00.908 The operating system '{os}' is not supported
            assert False, io_glob.ERROR_00_908.replace("{os}", platform.system())
    except OSError as error:
        assert False, error

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - u_d_s   - Update the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_u_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    try:
        if platform.system() == "Windows":
            os.system("run_io_avstats_pytest.bat u_d_s")
        elif platform.system() == "Linux":
            os.system("./run_io_avstats_pytest.sh u_d_s")
        else:
            # ERROR.00.908 The operating system '{os}' is not supported
            assert False, io_glob.ERROR_00_908.replace("{os}", platform.system())
    except OSError as error:
        assert False, error

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - a_o_c   - Load aviation occurrence categories
#                                   into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_a_o_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    try:
        if platform.system() == "Windows":
            os.system("run_io_avstats_pytest.bat a_o_c")
        elif platform.system() == "Linux":
            os.system("./run_io_avstats_pytest.sh a_o_c")
        else:
            # ERROR.00.908 The operating system '{os}' is not supported
            assert False, io_glob.ERROR_00_908.replace("{os}", platform.system())
    except OSError as error:
        assert False, error

    io_glob.logger.debug(io_glob.LOGGER_END)
