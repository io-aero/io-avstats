# Copyright (c) 2022 FAA-VAIL-Project. All rights reserved.
# Use of this source code is governed by the GNU LESSER GENERAL
# PUBLIC LICENSE, that can be found in the LICENSE.md file.

"""launcher: coverage testing."""
import os
import platform

import pytest

from io_avstats_db import db_utils
from io_avstats_db import io_config
from io_avstats_db import io_glob
from io_avstats_db import io_utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

EV_ID_1 = "20181022X64842"  # not US
EV_ID_2 = "20181212X03941"
EV_ID_3 = "20190401X25202"
EV_ID_4 = "20200908X83855"


# -----------------------------------------------------------------------------
# Test case: launcher() - version - Show the IO-AVSTATS-DB version.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_version():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat version")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh version")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - c_d_s   - Create the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_c_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat c_d_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh c_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_c_s   - Load country and state data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_c_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat l_c_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh l_c_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_c_s   - Load country and state data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_c_s_no_mdb():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(r"pipenv run python src\launcher.py -t l_c_s -m xxx")
    elif platform.system() == "Linux":
        os.system("pipenv run python src/launcher.py -t l_c_s -m xxx")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_n_a   - Download a NTSB MS Access database file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_n_a_no_file():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(r"pipenv run python src\launcher.py -t d_n_a")
    elif platform.system() == "Linux":
        os.system("pipenv run python src/launcher.py -t d_n_a")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_n_a   - Download a NTSB MS Access database file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_n_a_no_file_extension():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(r"pipenv run python src\launcher.py -t d_n_a -m up01JUN.mdb")
    elif platform.system() == "Linux":
        os.system("pipenv run python src/launcher.py -t d_n_a -m up01JUN.mdb")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_n_a   - Download a NTSB MS Access database file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_n_a_ok():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat d_n_a up01JUN")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh d_n_a up01JUN")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_n_a   - Download a NTSB MS Access database file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_n_a_ok_avall():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat d_n_a avall")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh d_n_a avall")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_n_a   - Download a NTSB MS Access database file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_n_a_ok_lower_case():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(r"pipenv run python src\launcher.py -t d_n_a -m up01jun")
    elif platform.system() == "Linux":
        os.system("pipenv run python src/launcher.py -t d_n_a -m up01jun")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_n_a   - Download a NTSB MS Access database file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_n_a_ok_pre2008():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat d_n_a pre2008")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh d_n_a pre2008")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_n_a   - Download a NTSB MS Access database file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_n_a_wrong_month():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat d_n_a up01xxx")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh d_n_a up01xxx")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_n_a   - Load NTSB MS Access database data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_n_a():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("up15JAN", "mdb"),
        ],
        target_path=io_config.settings.download_work_dir,
    )

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat l_n_a up15JAN")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh l_n_a up15JAN")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_s_d   - Load simplemaps data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_s_d():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("uscities", "xlsx"),
            ("uszips", "xlsx"),
        ],
        target_path=io_config.settings.download_work_dir,
    )

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat l_s_d")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh l_s_d")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_c_d   - Load data from a correction file into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_c_d_no_file():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(r"pipenv run python src\launcher.py -t l_c_d")
    elif platform.system() == "Linux":
        os.system("pipenv run python src/launcher.py -t l_c_d")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_c_d   - Load data from a correction file into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_c_d_ok():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("correction_pytest", "xlsx"),
        ],
        target_path=io_config.settings.correction_work_dir,
    )

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat l_c_d correction_pytest")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh l_c_d correction_pytest")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_c_d   - Load data from a correction file into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_c_d_wrong_format():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("correction_wrong_format", "xlsx"),
        ],
        target_path=io_config.settings.correction_work_dir,
    )

    if platform.system() == "Windows":
        os.system(
            r"pipenv run python src\launcher.py -t l_c_d "
            + "-c correction_wrong_format.xlsx"
        )
    elif platform.system() == "Linux":
        os.system(
            "pipenv run python src/launcher.py -t l_c_d "
            + "-c correction_wrong_format.xlsx"
        )
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_s_f   - Download basic simplemaps files.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_s_f():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat d_s_f")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh d_s_f")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_z_d   - Load ZIP Code Database data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_z_d_ok():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("zip_code_database", "xls"),
        ],
        target_path=io_config.settings.download_work_dir,
    )

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat l_z_d")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh l_z_d")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - l_z_d   - Load ZIP Code Database data into PostgreSQL.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_l_z_d_wrong_correction():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(
            r"pipenv run python src\launcher.py -t l_z_d -c correction_pytest.xlsx"
        )
    elif platform.system() == "Linux":
        os.system(
            "pipenv run python src/launcher.py -t l_z_d -c correction_pytest.xlsx"
        )
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_z_f   - Download the ZIP Code Database file.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_z_f():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat d_z_f")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh d_z_f")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - c_l_l   - Correct decimal US latitudes and longitudes.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_c_l_l():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    # Swap latitude and longitude
    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    cur_pg.execute(
        """
    UPDATE events
       SET latitude = substring(longitude,1,7),
           longitude = latitude
     WHERE ev_id = %s
    """,
        (EV_ID_1,),
    )

    cur_pg.execute(
        """
    UPDATE events
       SET latitude = substring(longitude,1,7),
           longitude = latitude
     WHERE ev_id = %s
    """,
        (EV_ID_2,),
    )

    cur_pg.execute(
        """
    UPDATE events
       SET latitude = NULL,
           longitude = NULL
     WHERE ev_id = %s
    """,
        (EV_ID_3,),
    )

    cur_pg.execute(
        """
    UPDATE events
       SET ev_site_zipcode = NULL,
           latitude = NULL,
           longitude = NULL
     WHERE ev_id = %s
    """,
        (EV_ID_4,),
    )

    cur_pg.close()
    conn_pg.commit()
    conn_pg.close()

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat c_l_l")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh c_l_l")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - v_n_d   - Verify selected NTSB data.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_v_n_d():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat v_n_d")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh v_n_d")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - r_d_s   - Refresh the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_r_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat r_d_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh r_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - c_p_d   - Cleansing PostgreSQL data.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_c_p_d():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat c_p_d")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh c_p_d")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - u_d_s   - Update the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_u_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat u_d_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh u_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_d_s   - Drop the PostgreSQL database schema.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_s():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat d_d_s")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh d_d_s")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - d_d_f   - Delete the PostgreSQL database files.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_d_d_f():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system("run_io_avstats.bat d_d_f")
    elif platform.system() == "Linux":
        os.system("./run_io_avstats.sh d_d_f")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - x_x_x   - Unknown task.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_x_x_x():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(r"pipenv run python src\launcher.py -t x_x_x")
    elif platform.system() == "Linux":
        os.system("pipenv run python src/launcher.py -t x_x_x")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: launcher() - generate - Generate SQL Statements.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
def test_launcher_generate():
    """Test case: launcher()."""
    # -------------------------------------------------------------------------
    io_glob.logger.debug(io_glob.LOGGER_START)

    if platform.system() == "Windows":
        os.system(r"scripts\run_generate.bat")
    elif platform.system() == "Linux":
        os.system("./scripts/run_generate.sh")
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            io_glob.ERROR_00_908.replace("{os}", platform.system())
        )

    io_glob.logger.debug(io_glob.LOGGER_END)
