# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test configuration and store fixtures.

Returns:
    [type]: None.

"""
import configparser
import logging
import os
import pathlib
import shutil

import pytest
from iocommon import io_glob

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------

CONFIG_PARSER: configparser.ConfigParser = configparser.ConfigParser()

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_4_pytest(
    file_list: list[
        tuple[tuple[str, str | None], tuple[pathlib.Path, list[str], str | None]]
    ]
) -> None:
    """Copy files from the sample test file directory.

    Args:
        file_list (list[
            tuple[
                tuple[str, str | None],
                tuple[pathlib.Path, list[str], str | None]
            ]
        ]): list of files to be copied.

    """
    logger.debug(io_glob.LOGGER_START)

    assert os.path.isdir(
        get_os_independent_name(get_test_files_source_directory_name())
    ), ("source directory '" + get_test_files_source_directory_name() + "' missing")

    for (
        (source_stem, source_ext),
        (target_dir, target_file_comp, target_ext),
    ) in file_list:
        source_filename = (
            source_stem if source_ext is None else source_stem + "." + source_ext
        )
        source_file = get_full_name_from_components(
            get_test_files_source_directory_name(), source_filename
        )
        assert os.path.isfile(source_file), (
            "source file '" + str(source_file) + "' missing"
        )

        assert os.path.isdir(get_os_independent_name(target_dir)), (
            "target directory '" + target_dir + "' missing"
        )
        target_filename = (
            "_".join(target_file_comp)
            if target_ext is None
            else "_".join(target_file_comp) + "." + target_ext
        )
        target_file = get_full_name_from_components(target_dir, target_filename)
        assert os.path.isfile(target_file) is False, (
            "target file '" + str(target_file) + "' already existing"
        )

        shutil.copy(source_file, target_file)
        assert os.path.isfile(target_file), (
            "target file '" + str(target_file) + "' is missing"
        )

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_4_pytest_2_dir(
    source_files: list[tuple[str, str | None]],
    target_path: pathlib.Path,
) -> None:
    """Copy files from the sample test file directory.

    Args:
        source_files: list[tuple[str, str | None]]: Source file names.
        target_path: Path: Target directory.

    """
    logger.debug(io_glob.LOGGER_START)

    for source_file in source_files:
        (source_stem, source_ext) = source_file
        copy_files_4_pytest([(source_file, (target_path, [source_stem], source_ext))])

    logger.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Fixture - Before any test.
# -----------------------------------------------------------------------------
# pylint: disable=protected-access
@pytest.fixture(scope="session", autouse=True)
def fxtr_before_any_test():
    """Fixture Factory: Before any test."""
    logger.debug(io_glob.LOGGER_START)

    os.environ["ENV_FOR_DYNACONF"] = "test"

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Get the full name of a file from its components.
# ------------------------------------------------------------------
@pytest.helpers.register
def get_full_name_from_components(
    directory_name: pathlib.Path | str,
    stem_name: str = "",
    file_extension: str = "",
) -> str:
    """Get the full name of a file from its components.

    The possible components are directory name, stem name and file extension.

    Args:
        directory_name (pathlib.Path or str): Directory name or directory path.
        stem_name (str, optional): Stem name or file name including file extension.
            Defaults to "".
        file_extension (str, optional): File extension.
            Defaults to "".

    Returns:
        str: Full file name.

    """
    logger.debug(io_glob.LOGGER_START)

    filename_int = (
        stem_name if file_extension == "" else stem_name + "." + file_extension
    )

    if directory_name == "" and filename_int == "":
        return ""

    if isinstance(directory_name, pathlib.Path):
        directory_name_int = str(directory_name)
    else:
        directory_name_int = directory_name

    logger.debug(io_glob.LOGGER_END)

    return get_os_independent_name(str(os.path.join(directory_name_int, filename_int)))


# ------------------------------------------------------------------
# Get the platform-independent name.
# ------------------------------------------------------------------
@pytest.helpers.register
def get_os_independent_name(filename: pathlib.Path | str) -> str:
    """Get the platform-independent name.

    Args:
        filename (pathlib.Path | str): File name or file path.

    Returns:
        str: Platform-independent name.

    """
    logger.debug(io_glob.LOGGER_START)
    logger.debug(io_glob.LOGGER_END)

    return filename.replace(("\\" if os.sep == "/" else "/"), os.sep)


# -----------------------------------------------------------------------------
# Provide the file directory name where the test files are located.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_test_files_source_directory_name():
    """Provide test file directory.

    Provide the file directory name where the test files are located.

    """
    logger.debug(io_glob.LOGGER_START)
    logger.debug(io_glob.LOGGER_END)

    return "tests/__PYTEST_FILES__/"
