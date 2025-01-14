# Copyright (c) 2022-2024 IO-Aero. All rights reserved.
# Use of this source code is governed by the GNU LESSER GENERAL
# PUBLIC LICENSE, that can be found in the LICENSE.md file.
"""Launcher: coverage testing."""
import logging
import os
import platform
import subprocess

import pytest
from iocommon import io_glob
from iocommon.io_settings import settings

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
            shell=False,
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
def _setup_and_teardown() -> None:  # type: ignore
    """Setup and teardown fixture for all tests."""  # noqa: D401
    logging.debug(io_glob.LOGGER_START)

    os.environ["ENV_FOR_DYNACONF"] = "test"

    yield  # This is where the testing happens

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test case: version - Show the IO-AVSTATS version.
# -----------------------------------------------------------------------------
def test_launcher_version() -> None:
    """Test case: Show the IO-AVSTATS version."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "version"],
        "Linux": ["./run_io_avstats_test.sh", "version"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "version"],
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

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "d_d_c"],
        "Linux": ["./run_io_avstats_test.sh", "d_d_c"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "d_d_c"],
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

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "d_d_f"],
        "Linux": ["./run_io_avstats_test.sh", "d_d_f"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "d_d_f"],
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
        "Darwin": ["./run_io_avstats_test.sh", "s_d_c"],
        "Linux": ["./run_io_avstats_test.sh", "s_d_c"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "s_d_c"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: c_d_s   - Create the PostgreSQL database schema.
# -----------------------------------------------------------------------------
def test_launcher_c_d_s() -> None:
    """Test case: Create the PostgreSQL database schema."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "c_d_s"],
        "Linux": ["./run_io_avstats_test.sh", "c_d_s"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "c_d_s"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: u_d_s   - Update the PostgreSQL database schema.
# -----------------------------------------------------------------------------
def test_launcher_u_d_s() -> None:
    """Test case: Update the PostgreSQL database schema."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "u_d_s"],
        "Linux": ["./run_io_avstats_test.sh", "u_d_s"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "u_d_s"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_a_p   - Load airport data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_a_p() -> None:
    """Test case: Load airport data into PostgreSQL."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "l_a_p"],
        "Linux": ["./run_io_avstats_test.sh", "l_a_p"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "l_a_p"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: a_o_c   - Load aviation occurrence categories into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_a_o_c() -> None:
    """Test case: Load aviation occurrence categories into PostgreSQL."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "a_o_c"],
        "Linux": ["./run_io_avstats_test.sh", "a_o_c"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "a_o_c"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_c_s   - Load country and state data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_c_s() -> None:
    """Test case: Load country and state data into PostgreSQL."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "l_c_s"],
        "Linux": ["./run_io_avstats_test.sh", "l_c_s"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "l_c_s"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_c_d   - Load data from a correction file into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_c_d() -> None:
    """Test case: Load data from a correction file into PostgreSQL."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "l_c_d", "test"],
        "Linux": ["./run_io_avstats_test.sh", "l_c_d", "test"],
        "Windows": [
            "cmd.exe",
            "/c",
            "run_io_avstats_test.bat",
            "l_c_d",
            "test",
        ],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_s_e   - Load sequence of events data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_s_e() -> None:
    """Test case: Load sequence of events data into PostgreSQL."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "l_s_e"],
        "Linux": ["./run_io_avstats_test.sh", "l_s_e"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "l_s_e"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_s_d   - Load simplemaps data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_s_d() -> None:
    """Test case: Load simplemaps data into PostgreSQL."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "l_s_d"],
        "Linux": ["./run_io_avstats_test.sh", "l_s_d"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "l_s_d"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_z_d   - Load ZIP Code Database data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_z_d() -> None:
    """Test case: Load ZIP Code Database data into PostgreSQL."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "l_z_d"],
        "Linux": ["./run_io_avstats_test.sh", "l_z_d"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "l_z_d"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: u_p_d   - Complete processing of a modifying MS Access file.
# -----------------------------------------------------------------------------
def test_launcher_u_p_d() -> None:
    """Test case: Complete processing of a modifying MS Access file."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping u_p_d on macOS due to custom handling.")
    if platform.system() == "Linux":
        pytest.skip("Skipping u_p_d on Linux due to custom handling.")

    commands = {
        "Windows": [
            "cmd.exe",
            "/c",
            "run_io_avstats_test.bat",
            "u_p_d",
            "up22APR",
        ],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: l_n_a   - Load NTSB MS Access database data into PostgreSQL.
# -----------------------------------------------------------------------------
def test_launcher_l_n_a() -> None:
    """Test case: Load NTSB MS Access database data into PostgreSQL."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    if platform.system() == "Darwin":
        pytest.skip("Skipping l_n_a on macOS due to custom handling.")
    if platform.system() == "Linux":
        pytest.skip("Skipping l_n_a on Linux due to custom handling.")

    commands = {
        "Windows": [
            "cmd.exe",
            "/c",
            "run_io_avstats_test.bat",
            "l_n_a",
            "up22APR",
        ],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: c_l_l   - Correct decimal US latitudes and longitudes.
# -----------------------------------------------------------------------------
def test_launcher_c_l_l() -> None:
    """Test case: Correct decimal US latitudes and longitudes."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "c_l_l"],
        "Linux": ["./run_io_avstats_test.sh", "c_l_l"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "c_l_l"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: f_n_a   - Find the nearest airport.
# -----------------------------------------------------------------------------
def test_launcher_f_n_a() -> None:
    """Test case: Find the nearest airport."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "f_n_a"],
        "Linux": ["./run_io_avstats_test.sh", "f_n_a"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "f_n_a"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: r_d_s   - Refresh the PostgreSQL database schema.
# -----------------------------------------------------------------------------
def test_launcher_r_d_s() -> None:
    """Test case: Refresh the PostgreSQL database schema."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "r_d_s"],
        "Linux": ["./run_io_avstats_test.sh", "r_d_s"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "r_d_s"],
    }
    command = commands.get(platform.system())
    if not command:
        pytest.fail(io_glob.FATAL_00_908.replace("{os}", platform.system()))

    _run_command(command)


# -----------------------------------------------------------------------------
# Test case: c_p_d   - Cleansing PostgreSQL data.
# -----------------------------------------------------------------------------
def test_launcher_c_p_d() -> None:
    """Test case: Cleansing PostgreSQL data."""
    assert settings.check_value == "test", "Settings check_value is not 'test'"

    commands = {
        "Darwin": ["./run_io_avstats_test.sh", "c_p_d"],
        "Linux": ["./run_io_avstats_test.sh", "c_p_d"],
        "Windows": ["cmd.exe", "/c", "run_io_avstats_test.bat", "c_p_d"],
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
    test_launcher_d_d_c()
    test_launcher_d_d_f()
