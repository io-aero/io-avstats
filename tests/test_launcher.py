# Copyright (c) 2022-2024 IO-Aero. All rights reserved.
# Use of this source code is governed by the GNU LESSER GENERAL
# PUBLIC LICENSE, that can be found in the LICENSE.md file.

"""Launcher: coverage testing."""
import logging
import os
import platform
import subprocess
import time

import pytest
from iocommon import io_glob
from iocommon.io_config import settings

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Run shell commands safely.
# -----------------------------------------------------------------------------
def _run_command(command: list[str]) -> None:
    """Run shell commands safely."""
    try:
        subprocess.run(
            command,
            check=True,
            shell=False,  # noqa: S603
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(  # noqa: T201
            f"test_launcher - stdout: '{e.stdout}'",
        )  # Print stdout for additional context
        print(  # noqa: T201
            f"test_launcher - stderr: '{e.stderr}'",
        )  # This will print the error output
        pytest.fail(
            f"test_launcher - command failed with exit code: {e.returncode}",
        )


# -----------------------------------------------------------------------------
# Setup and teardown fixture for all tests.
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def _setup_and_teardown() -> None:
    """Setup and teardown fixture for all tests."""  # noqa: D401
    logging.debug(io_glob.LOGGER_START)

    os.environ["ENV_FOR_DYNACONF"] = "test"

    yield  # This is where the testing happens

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: version - Show the IO-AVSTATS version.
# -----------------------------------------------------------------------------
def test_launcher_version() -> None:
    """Test case: launcher() version."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping version on Darwin due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping version on Ubuntu due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "version"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: d_d_c   - Delete the PostgreSQL database container.
# -----------------------------------------------------------------------------
def test_launcher_d_d_c() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping d_d_c on Darwin due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping d_d_c on Ubuntu due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "d_d_c"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: d_d_f   - Delete the PostgreSQL database files.
# -----------------------------------------------------------------------------
def test_launcher_d_d_f() -> None:
    """Test case: Delete the PostgreSQL database files."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping d_d_f on Darwin due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping d_d_f on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "d_d_f"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: s_d_c   - Set up the PostgreSQL database container.
# -----------------------------------------------------------------------------
def test_launcher_s_d_c() -> None:
    """Test case: Set up the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_pytest.zsh", "s_d_c"],
        "Linux": ["./run_io_avstats_pytest.sh", "s_d_c"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "s_d_c"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)

    time.sleep(10)


# -----------------------------------------------------------------------------
# Test case: c_d_s   - Create the PostgreSQL database schema.
# -----------------------------------------------------------------------------
def test_launcher_c_d_s() -> None:
    """Test case: Create or update the PostgreSQL database schema."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping c_d_s on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping c_d_s on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "c_d_s"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: u_d_s   - Update the PostgreSQL database schema.
# -----------------------------------------------------------------------------
def test_launcher_u_d_s() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping u_d_s on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping u_d_s on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "u_d_s"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: a_o_c   - Load aviation occurrence categories
#                                    into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_a_o_c() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping a_o_c on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping a_o_c on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "a_o_c"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_a_p   - Load airport data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_a_p() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping l_a_p on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping l_a_p on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "l_a_p"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_c_s   - Load country and state data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_c_s() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping l_c_s on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping l_c_s on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "l_c_s"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_s_e   - Load sequence of events data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_s_e() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping l_s_e on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping l_s_e on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "l_s_e"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_s_d   - Load simplemaps data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_s_d() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping l_s_d on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping l_s_d on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "l_s_d"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_z_d   - Load ZIP Code Database data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_z_d() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping l_z_d on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping l_z_d on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "l_z_d"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: r_d_s   - Refresh the PostgreSQL database schema.
# -----------------------------------------------------------------------------
def test_launcher_r_d_s() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping r_d_s on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping r_d_s on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "r_d_s"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_c_d   - Load data from a correction file into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_c_d() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping l_c_d on macOS due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping l_c_d on Linux due to custom handling.")

    commands = {
        "Windows": [
            "cmd.exe",
            "/c",
            "run_io_avstats_pytest.bat",
            "l_c_d",
            "test",
        ],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: cleanup - Delete the PostgreSQL database container.
# -----------------------------------------------------------------------------
def test_launcher_clean() -> None:
    """Test case: Delete the PostgreSQL database container."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping clean on Darwin due to custom handling.")

    if platform.system() == "Linux":
        pytest.skip("Skipping clean on Linux due to custom handling.")

    commands = {
        "Windows": ["cmd.exe", "/c", "run_io_avstats_pytest.bat", "d_d_c"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)
