# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Global constants and variables."""
import logging.config

ARG_TASK = "task"
ARG_TASK_DEMO = "demo"
ARG_TASK_VERSION = "version"

# Error messages.
ERROR_00_901 = (
    "ERROR.00.901 The task '{task}' requires valid argument '-m' or '--msaccess'"
)

# Default file encoding UTF-8.
FILE_ENCODING_DEFAULT = "utf-8"

# Informational messages.
INFO_00_001 = "INFO.00.001 The logger is configured and ready"
INFO_00_002 = (
    "INFO.00.002 The configuration parameters (io_avstats_db) are checked and loaded"
)
INFO_00_003 = (
    "INFO.00.003 Initialize the configuration parameters using the file '{file}'"
)
INFO_00_004 = "INFO.00.004 Start Launcher"
INFO_00_005 = "INFO.00.005 Argument {task}='{value_task}'"
INFO_00_006 = "INFO.00.006 End   Launcher"

INFORMATION_NOT_YET_AVAILABLE = "n/a"

# Library version number.
IO_AVSTATS_VERSION = "1.0.0"

LOCALE = "en_US.UTF-8"
# Logging constants.
LOGGER_END = "End"
LOGGER_NAME = "io_avstats_db"
LOGGER_START = "Start"

# Logger instance.
logger: logging.Logger = logging.getLogger(LOGGER_NAME)
