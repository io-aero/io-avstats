# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""io_utils: coverage testing."""

from io_avstats_db import io_utils  # pylint: disable=import-error

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test case: initialise_logger() - Initialising the logging functionality.
# -----------------------------------------------------------------------------
def test_initialise_logger():
    """Test case: initialise_logger() - Initialising the logging functionality."""
    # pylint: disable=duplicate-code
    io_utils.initialise_logger()


# -----------------------------------------------------------------------------
# Test case: progress_msg() - Create a progress message.
# -----------------------------------------------------------------------------
def test_progress_msg():
    """Test case: progress_msg() - Create a progress message."""
    io_utils.progress_msg(msg="Hello World! (from progress_msg())")


# -----------------------------------------------------------------------------
# Test case: progress_msg_core() - Create a progress message.
# -----------------------------------------------------------------------------
def test_progress_msg_core():
    """Test case: progress_msg_core() - Create a progress message."""
    io_utils.progress_msg_core(msg="Hello World! (from progress_msg_core())")
