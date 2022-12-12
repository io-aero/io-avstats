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
# Test case: launcher() - -t n/a.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_task_d_d_f_c_d_s():
    """Test case: launcher() - Task."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats d_d_f")
        os.system("pipenv run python src\\launcher.py -t c_d_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats_db.sh d_d_f")
        os.system("pipenv run python src/launcher.py -t c_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - -t n/a.
# -----------------------------------------------------------------------------
def test_launcher_task_n_a():
    """Test case: launcher() - Task."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(
            "pipenv run python src\\launcher.py -t "
            + io_glob.INFORMATION_NOT_YET_AVAILABLE
        )
    elif platform.system() == "Linux":
        os.system(
            "pipenv run python src/launcher.py -t "
            + io_glob.INFORMATION_NOT_YET_AVAILABLE
        )
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)
