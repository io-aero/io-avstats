# Copyright (c) 2022 FAA-VAIL-Project. All rights reserved.
# Use of this source code is governed by the GNU LESSER GENERAL
# PUBLIC LICENSE, that can be found in the LICENSE.md file.

"""Launcher: coverage testing."""
import logging
import os
import platform
import time

from iocommon import io_glob
from iocommon.io_config import settings

from ioavstats import glob

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Test case: version - Show the ioavstats version.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_version():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh version")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh version")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat version")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


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
        exit_code = os.system("./run_io_avstats_pytest.zsh d_d_f")
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
# Test case:s_d_c   - Set up the PostgreSQL database container.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_s_d_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh s_d_c")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh s_d_c")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat s_d_c")
        time.sleep(10)
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:c_d_s   - Create the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_c_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh c_d_s")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh c_d_s")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat c_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:u_d_s   - Update the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_u_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh u_d_s")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh u_d_s")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat u_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:a_o_c   - Load aviation occurrence categories
#                                   into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_a_o_c():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh a_o_c")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh a_o_c")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat a_o_c")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:l_a_p   - Load airport data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_a_p():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh l_a_p")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh l_a_p")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat l_a_p")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:l_c_s   - Load country and state data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_c_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh l_c_s")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh l_c_s")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat l_c_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:l_s_e   - Load sequence of events data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_s_e():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh l_s_e")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh l_s_e")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat l_s_e")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:l_s_d   - Load simplemaps data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_s_d():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh l_s_d")
    elif platform.system() == "Linux":
        exit_code = 0
    elif platform.system() == "Windows":
        exit_code = 0
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:l_z_d   - Load ZIP Code Database data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_z_d():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh l_z_d")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh l_z_d")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat l_z_d")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case:r_d_s   - Refresh the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def _test_launcher_r_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    logger.debug(io_glob.LOGGER_START)

    assert settings.check_value == "test"

    if platform.system() == "Darwin":
        exit_code = os.system("./run_io_avstats_pytest.zsh r_d_s")
    elif platform.system() == "Linux":
        exit_code = os.system("./run_io_avstats_pytest.sh r_d_s")
    elif platform.system() == "Windows":
        exit_code = os.system("run_io_avstats_pytest.bat r_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        assert False, glob.ERROR_00_908.replace("{os}", platform.system())

    assert exit_code == 0, f"Command failed with exit code {exit_code}"

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: cleanup - Delete the PostgreSQL database container.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_clean():
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
