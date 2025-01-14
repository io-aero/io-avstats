#!/bin/bash

set -e

# -----------------------------------------------------------------------------
#
# run_io_avstats_test.sh: Process IO-AVSTATS tasks.
#
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Set environment name
# -----------------------------------------------------------------------------
export MODULE=ioavstats

# -----------------------------------------------------------------------------
# Set environment for Dynaconf
# -----------------------------------------------------------------------------
export ENV_FOR_DYNACONF=test

# -----------------------------------------------------------------------------
# Set data directories
# -----------------------------------------------------------------------------
export IO_AERO_AVIATION_EVENT_STATISTICS=data/AviationAccidentStatistics
export IO_AERO_CORRECTION_WORK_DIR=data/correction
export IO_AERO_NTSB_WORK_DIR=data/download

# -----------------------------------------------------------------------------
# Set PostgreSQL related environment variables
# -----------------------------------------------------------------------------
export IO_AERO_POSTGRES_CONNECTION_PORT=5433
export IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db_test
export IO_AERO_POSTGRES_DBNAME_ADMIN=postgres
export IO_AERO_POSTGRES_PASSWORD_ADMIN=postgres_password_admin
export IO_AERO_POSTGRES_PGDATA=data/postgres_test
export IO_AERO_POSTGRES_USER_ADMIN=postgres
export IO_AERO_POSTGRES_VERSION=16.3

# -----------------------------------------------------------------------------
# Initialize task variables
# -----------------------------------------------------------------------------
export IO_AERO_TASK=${1:-} # Default to empty if no argument is passed
export IO_AERO_TASK_DEFAULT=r_s_a

# -----------------------------------------------------------------------------
# Set Python path
# -----------------------------------------------------------------------------
export PYTHONPATH=.

# -----------------------------------------------------------------------------
# Handle task input
# -----------------------------------------------------------------------------
if [ -z "$1" ]; then
    echo "===================================================================="
    echo "l_a_p   - Load airport data into PostgreSQL"
    echo "a_o_c   - Load aviation occurrence categories into PostgreSQL"
    echo "l_c_s   - Load country and state data into PostgreSQL"
    echo "l_c_d   - Load data from a correction file into PostgreSQL"
    echo "l_s_e   - Load sequence of events data into PostgreSQL"
    echo "l_s_d   - Load simplemaps data into PostgreSQL"
    echo "l_z_d   - Load ZIP Code Database data into PostgreSQL"
    echo "--------------------------------------------------------------------"
    echo "s_d_c   - Set up the PostgreSQL database container"
    echo "c_d_s   - Create or update the PostgreSQL database schema"
    echo "u_d_s   - Update the PostgreSQL database schema"
    echo "r_d_s   - Refresh the PostgreSQL database schema"
    echo "--------------------------------------------------------------------"
    echo "d_d_c   - Delete the PostgreSQL database container"
    echo "d_d_f   - Delete the PostgreSQL database files"
    echo "--------------------------------------------------------------------"
    echo "version - Show the IO-AVSTATS version"
    echo "--------------------------------------------------------------------"
    # shellcheck disable=SC2162
    read -p "Enter the desired task [default: ${IO_AERO_TASK_DEFAULT}]: " IO_AERO_TASK
    export IO_AERO_TASK=${IO_AERO_TASK}

    if [ -z "${IO_AERO_TASK}" ]; then
        export IO_AERO_TASK=${IO_AERO_TASK_DEFAULT}
    fi
else
    export IO_AERO_TASK=$1
fi

if [[ "${IO_AERO_TASK}" = "l_c_d" ]]; then
    if [ -z "$2" ]; then
        echo "==============================================================="
        find "$IO_AERO_CORRECTION_WORK_DIR" -maxdepth 1 -type f -name '*.xlsx' -printf '%f\n'
        echo "---------------------------------------------------------------"
        read -p "Enter the stem name of the desired correction file: " IO_AERO_MSEXCEL
    else
        export IO_AERO_MSEXCEL=$2
    fi
fi

# -----------------------------------------------------------------------------
# Path to the log file
# -----------------------------------------------------------------------------
log_file="run_io_avstats_test_${IO_AERO_TASK}.log"

# -----------------------------------------------------------------------------
# Function for logging messages
# -----------------------------------------------------------------------------
log_message() {
    local message="$1"
    # Format current date and time with timestamp
    timestamp=$(date +"%d.%m.%Y %H:%M:%S")
    # Write message with timestamp in the log file
    echo "$timestamp: $message" >> "$log_file"
}

# -----------------------------------------------------------------------------
# Clean up old log files
# -----------------------------------------------------------------------------
if [ -f logging_io_aero.log ]; then
    rm -f logging_io_aero.log
fi

# Check if the file specified in logfile exists and delete it
if [ -f "${log_file}" ]; then
    rm -f "${log_file}"
fi

# -----------------------------------------------------------------------------
# Redirect stdout and stderr to both terminal and log file
# -----------------------------------------------------------------------------
exec > >(tee -a "$log_file") 2> >(tee -a "$log_file" >&2)

echo "========================================================================"
echo "Start $0"
echo "------------------------------------------------------------------------"
echo "IO-AVSTATS - Aviation Event Statistics."
echo "------------------------------------------------------------------------"
echo "ENV_FOR_DYNACONF         : ${ENV_FOR_DYNACONF}"
echo "POSTGRES_CONNECTION_PORT : ${IO_AERO_POSTGRES_CONNECTION_PORT}"
echo "PYTHONPATH               : ${PYTHONPATH}"
echo "------------------------------------------------------------------------"
if [ -n "$CONDA_PREFIX" ]; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate ${MODULE}
    conda_env=$(basename "$CONDA_PREFIX")
    echo "Running in conda environment: $conda_env"
else
    echo "FATAL ERROR: Not running in a conda environment"
fi
echo "------------------------------------------------------------------------"
echo "TASK                     : ${IO_AERO_TASK}"
echo "------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "========================================================================"

# -----------------------------------------------------------------------------
# Task handling
# -----------------------------------------------------------------------------
# a_o_c  : Load aviation occurrence categories into PostgreSQL.
# l_a_p  : Load airport data into PostgreSQL.
# l_c_s  : Load country and state data into PostgreSQL.
# l_s_d  : Load simplemaps data into PostgreSQL.
# l_s_e  : Load sequence of events data into PostgreSQL.
# l_z_d  : Load ZIP Code Database data into PostgreSQL.
# r_d_s  : Refresh the PostgreSQL database schema.
# u_d_s  : Update the PostgreSQL database schema.
# version: Show the IO-AVSTATS version.
# -----------------------------------------------------------------------------
if [[ "${IO_AERO_TASK}" =~ ^(a_o_c|l_a_p|l_c_s|l_s_d|l_s_e|l_z_d|r_d_s|u_d_s|version)$ ]]; then
    if ! python scripts/launcher.py -t "${IO_AERO_TASK}"; then
        exit 255
    fi

# -----------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# -----------------------------------------------------------------------------
elif [[ "${IO_AERO_TASK}" = "c_d_s" ]]; then
    if ! python scripts/launcher.py -t "${IO_AERO_TASK}"; then
        exit 255
    fi

    if ! python scripts/launcher.py -t "u_d_s"; then
        exit 255
    fi

# -----------------------------------------------------------------------------
# Delete the PostgreSQL database container.
# -----------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "d_d_c" ]; then
    if ! ./scripts/run_delete_postgresql_container.sh; then
        exit 255
    fi

# -----------------------------------------------------------------------------
# Delete the PostgreSQL database files.
# -----------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "d_d_f" ]; then
    if ! ./scripts/run_delete_postgresql_files.sh; then
        exit 255
    fi

# -----------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# -----------------------------------------------------------------------------
elif [[ "${IO_AERO_TASK}" = "l_c_d" ]]; then
    if ! python scripts/launcher.py -t "${IO_AERO_TASK}" -e "${IO_AERO_MSEXCEL}".xlsx; then
        exit 255
    fi

# -----------------------------------------------------------------------------
# Set up the PostgreSQL database container.
# -----------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "s_d_c" ]; then
    if ! ./scripts/run_setup_postgresql.sh; then
        exit 255
    fi

# -----------------------------------------------------------------------------
# Program abort due to wrong input.
# -----------------------------------------------------------------------------
else
    echo "Unknown task '${IO_AERO_TASK}'" >&2
    exit 255
fi

echo "------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------"
echo "End   $0"
echo "========================================================================"

# Close the log file
exec > >(while read -r line; do echo "$line"; done) 2> >(while read -r line; do echo "ERROR: $line"; done)

# Closing the log file
log_message "Script finished."
