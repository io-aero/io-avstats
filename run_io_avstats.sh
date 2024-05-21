#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_io_avstats.sh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------------

export ENV_FOR_DYNACONF=prod

export IO_AERO_AVIATION_EVENT_STATISTICS=data/AviationAccidentStatistics
export IO_AERO_CORRECTION_WORK_DIR=data/correction
export IO_AERO_NTSB_WORK_DIR=data/download

if [ -z "${IO_AERO_POSTGRES_CONNECTION_PORT}" ]; then
    export IO_AERO_POSTGRES_CONNECTION_PORT=5432
fi

export IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db
export IO_AERO_POSTGRES_DBNAME_ADMIN=postgres
export IO_AERO_POSTGRES_PASSWORD_ADMIN="V3s8m4x*MYbHrX*UuU6X"
export IO_AERO_POSTGRES_PGDATA=data/postgres
export IO_AERO_POSTGRES_USER_ADMIN=postgres
export IO_AERO_POSTGRES_VERSION=16.3

export IO_AERO_TASK=
export IO_AERO_TASK_DEFAULT=r_s_a

export PYTHONPATH=.

shopt -s nocasematch

if [ -z "$1" ]; then
    echo "==================================================================="
    echo "r_s_a   - Run the IO-AVSTATS application"
    echo "-------------------------------------------------------------------"
    echo "s_d_c   - Set up the PostgreSQL database container"
    echo "-------------------------------------------------------------------"
    echo "version - Show the IO-AVSTATS version"
    echo "-------------------------------------------------------------------"
    # shellcheck disable=SC2162
    read -p "Enter the desired task [default: ${IO_AERO_TASK_DEFAULT}] " IO_AERO_TASK
    export IO_AERO_TASK=${IO_AERO_TASK}

    if [ -z "${IO_AERO_TASK}" ]; then
        export IO_AERO_TASK=${IO_AERO_TASK_DEFAULT}
    fi
else
    export IO_AERO_TASK=$1
fi

# Path to the log file
log_file="run_io_avstats_${IO_AERO_TASK}.log"

# Function for logging messages
log_message() {
  local message="$1"
  # Format current date and time with timestamp
  timestamp=$(date +"%d.%m.%Y %H:%M:%S")
  # Write message with timestamp in the log file
  echo "$timestamp: $message" >> "$log_file"
}

# Check if logging_io_aero.log exists and delete it
if [ -f logging_io_aero.log ]; then
    rm -f logging_io_aero.log
fi

# Check if the file specified in logfile exists and delete it
if [ -f "${log_file}" ]; then
    rm -f "${log_file}"
fi

# Redirection of the standard output and the standard error output to the log file
exec > >(while read -r line; do log_message "$line"; done) 2> >(while read -r line; do log_message "ERROR: $line"; done)

echo "==================================================================="
echo "Start $0"
echo "-------------------------------------------------------------------"
echo "IO-AVSTATS - Aviation Event Statistics."
echo "-------------------------------------------------------------------"
echo "ENV_FOR_DYNACONF         : ${ENV_FOR_DYNACONF}"
echo "POSTGRES_CONNECTION_PORT : ${IO_AERO_POSTGRES_CONNECTION_PORT}"
echo "PYTHONPATH               : ${PYTHONPATH}"
echo "-------------------------------------------------------------------"
echo "TASK                     : ${IO_AERO_TASK}"
echo "-------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "==================================================================="

# ---------------------------------------------------------------------------
# Task handling
# ---------------------------------------------------------------------------
case "${IO_AERO_TASK}" in
    # ---------------------------------------------------------------------------
    # Running a Streamlit application.
    # ---------------------------------------------------------------------------
    r_s_a)
        if ! streamlit run "ioavstats/Menu.py" --server.port 8501; then
            exit 255
        fi
        ;;

    # ---------------------------------------------------------------------------
    # Setting up the PostgreSQL database container.
    # ---------------------------------------------------------------------------
    s_d_c)
        if ! ./scripts/run_setup_postgresql.sh; then
            exit 255
        fi
        ;;

    # ---------------------------------------------------------------------------
    # Show the IO-AVSTATS version.
    # ---------------------------------------------------------------------------
    version)
        if ! python scripts/launcher.py -t "${IO_AERO_TASK}"; then
            exit 255
        fi
        ;;

    # ---------------------------------------------------------------------------
    # Program termination due to incorrect input.
    # ---------------------------------------------------------------------------
    *)
        echo "The processing of the script run_io_avstats is aborted: unknown task='${IO_AERO_TASK}'"
        exit 255
        ;;
esac

echo "-----------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "-----------------------------------------------------------------------"
echo "End   $0"
echo "======================================================================="

# Closing the log files
exec > >(while read -r line; do echo "$line"; done) 2> >(while read -r line; do echo "ERROR: $line"; done)

log_message "Script finished."
