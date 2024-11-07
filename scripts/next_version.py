# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Module iocommon: Entry Point Functionality.

This is the entry point to the library IO-COMMON.
"""

from iocommon.io_utils import incr_version_pyproject

# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    incr_version_pyproject()
