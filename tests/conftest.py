# pylint: disable=E1101

# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test configuration and store fixtures.

Returns
-------
    [type]: None.

"""
import logging
import logging.config
import os
import pathlib
import shutil

import pytest
from iocommon import io_glob, io_logger

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

io_logger.initialise_logger()


# -----------------------------------------------------------------------------
# Fixture - Before any test.
# -----------------------------------------------------------------------------
# pylint: disable=protected-access
@pytest.fixture(scope="session", autouse=True)
def _fxtr_before_any_test() -> None:
    """Fixture Factory: Before and after any test."""
    logging.debug(io_glob.LOGGER_START)

    # Setup environment for testing
    os.environ["ENV_FOR_DYNACONF"] = "test"

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
def copy_files_4_pytest(
    file_list: list[
        tuple[tuple[str, str | None], tuple[pathlib.Path, list[str], str | None]]
    ],
) -> None:
    """Copy files from the sample test file directory to a specified destination.

    This function takes a list of tuples, each describing a file copy operation.
    Each tuple specifies the source and destination paths, along with optional
    filters and modifications for the copy operation.

    Args:
    ----
        file_list: A list of tuples, where each tuple contains:
            - A tuple specifying the source directory and an optional subdirectory.
            - A tuple specifying the destination directory (as a pathlib.Path object),
              a list of filename patterns to include, and an optional destination subdirectory.

    Each element of `file_list` is structured as:
    ((source_dir, sub_dir), (destination_dir, [patterns], dest_sub_dir))
    where:
    - `source_dir` is a string specifying the directory containing the source files.
    - `sub_dir` is an optional string specifying a subdirectory within the source directory.
    - `destination_dir` is a pathlib.Path object specifying the directory where files
      will be copied to.
    - `[patterns]` is a list of strings specifying filename patterns to include
      in the copy operation.
    - `dest_sub_dir` is an optional string specifying a subdirectory within the
      destination directory for the copied files.

    """
    assert pathlib.Path(
        get_os_independent_name(get_test_files_source_directory_name()),
    ).is_dir(), (
        "source directory '" + get_test_files_source_directory_name() + "' missing"
    )

    for (
        (source_stem, source_ext),
        (target_dir, target_file_comp, target_ext),
    ) in file_list:
        source_file_name = (
            source_stem if source_ext is None else source_stem + "." + source_ext
        )
        source_file = get_full_name_from_components(
            get_test_files_source_directory_name(),
            source_file_name,
        )
        assert pathlib.Path(source_file).is_file(), (
            "source file '" + str(source_file) + "' missing"
        )

        assert pathlib.Path(get_os_independent_name(target_dir)).is_dir(), (
            "target directory '" + str(target_dir.absolute()) + "' missing"
        )
        target_file_name = (
            "_".join(target_file_comp)
            if target_ext is None
            else "_".join(target_file_comp) + "." + target_ext
        )
        target_file = get_full_name_from_components(target_dir, target_file_name)
        assert pathlib.Path(target_file).is_file() is False, (
            "target file '" + str(target_file) + "' already existing"
        )

        shutil.copy(source_file, target_file)
        assert pathlib.Path(target_file).is_file(), (
            "target file '" + str(target_file) + "' is missing"
        )


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
def copy_files_4_pytest_2_dir(
    source_files: list[tuple[str, str | None]],
    target_path: pathlib.Path,
) -> None:
    """Copy files from the sample test file directory.

    Args:
    ----
        source_files: list[tuple[str, str | None]]: Source file names.
        target_path: Path: Target directory.

    """
    for source_file in source_files:
        (source_stem, source_ext) = source_file
        copy_files_4_pytest([(source_file, (target_path, [source_stem], source_ext))])


# ------------------------------------------------------------------
# Get the full name of a file from its components.
# ------------------------------------------------------------------
def get_full_name_from_components(
    directory_name: pathlib.Path | str,
    stem_name: str = "",
    file_extension: str = "",
) -> str:
    """Get the full name of a file from its components.

    The possible components are directory name, stem name and file extension.

    Args:
    ----
        directory_name (pathlib.Path or str): Directory name or directory path.
        stem_name (str, optional): Stem name or file name including file extension.
            Defaults to "".
        file_extension (str, optional): File extension.
            Defaults to "".

    Returns:
    -------
        str: Full file name.

    """
    file_name_int = (
        stem_name if file_extension == "" else stem_name + "." + file_extension
    )

    if directory_name == "" and file_name_int == "":
        return ""

    directory_name_int = (
        str(directory_name)
        if isinstance(directory_name, pathlib.Path)
        else directory_name
    )

    return get_os_independent_name(
        str(directory_name_int / file_name_int),  # type: ignore
    )


# ------------------------------------------------------------------
# Get the platform-independent name.
# ------------------------------------------------------------------
def get_os_independent_name(file_name: pathlib.Path | str) -> str:
    """Get the platform-independent name.

    Args:
    ----
        file_name (pathlib.Path | str): File name or file path.

    Returns:
    -------
        str: Platform-independent name.

    """
    return file_name.replace(
        ("\\" if os.sep == "/" else "/"),
        os.sep,
    )  # type: ignore[call-arg,return-value]


# -----------------------------------------------------------------------------
# Provide the file directory name where the test files are located.
# -----------------------------------------------------------------------------
def get_test_files_source_directory_name() -> str:
    """Provide test file directory.

    Provide the file directory name where the test files are located.

    Returns
    -------
        str: test files directory name.

    """
    return "tests/__PYTEST_FILES__/"
