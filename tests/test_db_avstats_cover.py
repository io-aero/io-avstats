# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

# pylint: disable=R0801
# pylint: disable=unused-argument
"""io_config: coverage testing."""
from io_avstats_db import avstats  # pylint: disable=import-error
from io_avstats_db import io_glob  # pylint: disable=import-error

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test case: version() - Return the IO-AVSTATS-DB version.
# -----------------------------------------------------------------------------
def test_version():
    """Test case: version() - Return the IO-AVSTATS-DB version."""
    io_glob.logger.debug(io_glob.LOGGER_START)

    assert io_glob.IO_AVSTATS_DB_VERSION == avstats.version(), "IO-AVSTATS-DB version"

    io_glob.logger.debug(io_glob.LOGGER_END)
