#!/bin/bash

set -e

# ------------------------------------------------------------------------
#
# run_io_avstats_dev.sh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# Set environment name
# ------------------------------------------------------------------------
export MODULE=ioavstats

# ------------------------------------------------------------------------
# Set environment for Dynaconf
# ------------------------------------------------------------------------
export ENV_FOR_DYNACONF=dev

# ------------------------------------------------------------------------
# Set data directories
# ------------------------------------------------------------------------
export IO_AERO_AVIATION_EVENT_STATISTICS=data/AviationAccidentStatistics
export IO_AERO_CORRECTION_WORK_DIR=data/correction
export IO_AERO_NTSB_WORK_DIR=data/download

# ------------------------------------------------------------------------
# Set PostgreSQL related environment variables
# ------------------------------------------------------------------------
export IO_AERO_POSTGRES_CONNECTION_PORT=5432
export IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db
export IO_AERO_POSTGRES_DBNAME_ADMIN=postgres
export IO_AERO_POSTGRES_PASSWORD_ADMIN=${POSTGRES_PASSWORD_ADMIN_IO_AVSTATS_DB}
export IO_AERO_POSTGRES_PGDATA=data/postgres
export IO_AERO_POSTGRES_USER_ADMIN=postgres
export IO_AERO_POSTGRES_VERSION=16.3

# ------------------------------------------------------------------------
# Initialize task variables
# ------------------------------------------------------------------------
export IO_AERO_TASK=${1:-} # Default to empty if no argument is passed
export IO_AERO_TASK_DEFAULT=r_s_a

# ------------------------------------------------------------------------
# Set Python path
# ------------------------------------------------------------------------
export PYTHONPATH=.

# ------------------------------------------------------------------------
# Handle task input
# ------------------------------------------------------------------------
if [ -z "$1" ]; then
    echo "==================================================================="
    echo "r_s_a   - Run the IO-AVSTATS application"
    echo "-------------------------------------------------------------------"
    echo "u_p_d   - Complete processing of a modifying MS Access file"
    echo "l_n_a   - Load NTSB MS Access database data into PostgreSQL"
    echo "-------------------------------------------------------------------"
    echo "l_a_p   - Load airport data into PostgreSQL"
    echo "a_o_c   - Load aviation occurrence categories into PostgreSQL"
    echo "l_c_s   - Load country and state data into PostgreSQL"
    echo "l_c_d   - Load data from a correction file into PostgreSQL"
    echo "l_s_e   - Load sequence of events data into PostgreSQL"
    echo "l_s_d   - Load simplemaps data into PostgreSQL"
    echo "l_z_d   - Load ZIP Code Database data into PostgreSQL"
    echo "-------------------------------------------------------------------"
    echo "s_d_c   - Set up the PostgreSQL database container"
    echo "c_d_s   - Create or update the PostgreSQL database schema"
    echo "u_d_s   - Update the PostgreSQL database schema"
    echo "r_d_s   - Refresh the PostgreSQL database schema"
    echo "-------------------------------------------------------------------"
    echo "version - Show the IO-AVSTATS version"
    echo "-------------------------------------------------------------------"
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
      echo "==================================================================="
      find "$IO_AERO_CORRECTION_WORK_DIR" -maxdepth 1 -type f -name '*.xlsx' -printf '%f\n'
      echo "-------------------------------------------------------------------"
      read -p "Enter the stem name of the desired correction file: " IO_AERO_MSEXCEL
  else
      export IO_AERO_MSEXCEL=$2
  fi
fi

if [[ "${IO_AERO_TASK}" = "l_n_a" || "${IO_AERO_TASK}" = "u_p_d" ]]; then
    if [ -z "$2" ]; then
        echo "==================================================================="
        echo "avall   - Data from January 1, 2008 to today"
        echo "Pre2008 - Data from January 1, 1982 to December 31, 2007"
        echo "upDDMON - New additions and updates until DD day in the month MON"
        echo "-------------------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the stem name of the desired MS Access database file: " IO_AERO_MSACCESS
        export IO_AERO_MSACCESS=${IO_AERO_MSACCESS}
    else
        export IO_AERO_MSACCESS=$2
    fi
fi

# ------------------------------------------------------------------------
# Path to the log file
# ------------------------------------------------------------------------
log_file="run_io_avstats_dev_${IO_AERO_TASK}.log"

# ------------------------------------------------------------------------
# Function for logging messages
# ------------------------------------------------------------------------
log_message() {
    local message="$1"
    echo "$(date +"%d.%m.%Y %H:%M:%S"): $message" >> "$log_file"
}

# ------------------------------------------------------------------------
# Clean up old log files
# ------------------------------------------------------------------------
[ -f logging_io_aero.log ] && rm -f logging_io_aero.log
[ -f "${log_file}" ] && rm -f "${log_file}"

# ------------------------------------------------------------------------
# Redirect standard output and error to log file
# ------------------------------------------------------------------------
exec > >(while read -r line; do log_message "$line"; done) 2> >(while read -r line; do log_message "$line"; done)

echo "==================================================================="
echo "Start $0"
echo "-------------------------------------------------------------------"
echo "IO-AVSTATS - Aviation Event Statistics."
echo "-------------------------------------------------------------------"
echo "ENV_FOR_DYNACONF         : ${ENV_FOR_DYNACONF}"
echo "POSTGRES_CONNECTION_PORT : ${IO_AERO_POSTGRES_CONNECTION_PORT}"
echo "PYTHONPATH               : ${PYTHONPATH}"
echo "-------------------------------------------------------------------"
if [ -n "$CONDA_PREFIX" ]; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate ${MODULE}
    conda_env=$(basename "$CONDA_PREFIX")
    echo "Running in conda environment: $conda_env"
else
    echo "FATAL ERROR: Not running in a conda environment"
fi
echo "-------------------------------------------------------------------"
echo "TASK                     : ${IO_AERO_TASK}"
echo "-------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "==================================================================="

# ------------------------------------------------------------------------
# Task handling
# ------------------------------------------------------------------------
# a_o_c  : Load aviation occurrence categories into PostgreSQL.
# l_a_p  : Load airport data into PostgreSQL.
# l_c_s  : Load country and state data into PostgreSQL.
# l_s_d  : Load simplemaps data into PostgreSQL.
# l_s_e  : Load sequence of events data into PostgreSQL.
# l_z_d  : Load ZIP Code Database data into PostgreSQL.
# r_d_s  : Refresh the PostgreSQL database schema.
# u_d_s  : Update the PostgreSQL database schema.
# version: Show the IO-AVSTATS version.
# ------------------------------------------------------------------------
if [[ "${IO_AERO_TASK}" =~ ^(a_o_c|l_a_p|l_c_s|l_s_d|l_s_e|l_z_d|r_d_s|u_d_s|version)$ ]]; then
    if ! python scripts/launcher.py -t "${IO_AERO_TASK}"; then
        exit 255
    fi

# ------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# ------------------------------------------------------------------------
elif [[ "${IO_AERO_TASK}" = "c_d_s" ]]; then
    if ! python scripts/launcher.py -t "${IO_AERO_TASK}"; then
        exit 255
    fi

    if ! python scripts/launcher.py -t "u_d_s"; then
        exit 255
    fi

# ------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# ------------------------------------------------------------------------
elif [[ "${IO_AERO_TASK}" = "l_c_d" ]]; then
    if ! python scripts/launcher.py -t "${IO_AERO_TASK}" -e "${IO_AERO_MSEXCEL}".xlsx; then
        exit 255
    fi

# ------------------------------------------------------------------------
# Load NTSB MS Access database data into PostgreSQL.
# ------------------------------------------------------------------------
elif [[ "${IO_AERO_TASK}" = "l_n_a" ]]; then
    if ! python scripts/launcher.py -t "d_n_a" -m "${IO_AERO_MSACCESS}"; then
        exit 255
    fi

    if ! python scripts/launcher.py -t "${IO_AERO_TASK}" -m "${IO_AERO_MSACCESS}"; then
        exit 255
    fi

# -----------------------------------------------------------------------
# Start the Streamlit application.
# ------------------------------------------------------------------------
elif [[ "${IO_AERO_TASK}" = "r_s_a" ]]; then
    if ! streamlit run iomapapps/Menu.py --server.port 8501; then
        exit 255
    fi

# ------------------------------------------------------------------------
# Set up the PostgreSQL database container.
# ------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "s_d_c" ]; then
    if ! ./scripts/run_setup_postgresql.sh; then
        exit 255
    fi

# ------------------------------------------------------------------------
# Complete processing of a modifying MS Access file.
# ------------------------------------------------------------------------
elif [[ "${IO_AERO_TASK}" = "u_p_d" ]]; then
    if ! python scripts/launcher.py -t "d_n_a" -m "${IO_AERO_MSACCESS}"; then
        exit 255
    fi

    if ! python scripts/launcher.py -t "l_n_a" -m "${IO_AERO_MSACCESS}"; then
        exit 255
    fi

    if ! python scripts/launcher.py -t "c_l_l"; then
        exit 255
    fi

    if ! python scripts/launcher.py -t "f_n_a"; then
        exit 255
    fi

    if ! python scripts/launcher.py -t "r_d_s"; then
        exit 255
    fi

# ------------------------------------------------------------------------
# Program abort due to wrong input.
# ------------------------------------------------------------------------
else
    echo "Unknown task '${IO_AERO_TASK}'" >&2
    exit 255
fi

echo "-------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "-------------------------------------------------------------------"
echo "End   $0"
echo "==================================================================="

# Close the log file
log_message "Script finished."
