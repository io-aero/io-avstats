#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_IO_AERO_pytest.sh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------------

if [ -z "${ENV_FOR_DYNACONF}" ]; then
    export ENV_FOR_DYNACONF=test
fi

export IO_AERO_AVIATION_EVENT_STATISTICS=data/AviationAccidentStatistics
export IO_AERO_CORRECTION_WORK_DIR=data/correction
export IO_AERO_NTSB_WORK_DIR=data/download

if [ -z "${IO_AERO_POSTGRES_CONNECTION_PORT}" ]; then
    export IO_AERO_POSTGRES_CONNECTION_PORT=5433
fi

export IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db_test
export IO_AERO_POSTGRES_DBNAME_ADMIN=postgres
export IO_AERO_POSTGRES_PASSWORD_ADMIN=postgres_password_admin
export IO_AERO_POSTGRES_PGDATA=data/postgres_test
export IO_AERO_POSTGRES_USER_ADMIN=postgres
export IO_AERO_POSTGRES_VERSION=16.2

export IO_AERO_MSEXCEL=
export IO_AERO_TASK=
export IO_AERO_TASK_DEFAULT=version

export PYTHONPATH=.

shopt -s nocasematch

if [ -z "$1" ]; then
    echo "==================================================================="
    echo "u_p_d   - Complete processing of a modifying MS Access file"
    echo "l_n_a   - Load NTSB MS Access database data into PostgreSQL"
    echo "-------------------------------------------------------------------"
    echo "c_p_d   - Cleansing PostgreSQL data"
    echo "c_l_l   - Correct decimal US latitudes and longitudes"
    echo "f_n_a   - Find the nearest airports"
    echo "v_n_d   - Verify selected NTSB data"
    echo "-------------------------------------------------------------------"
    echo "l_a_p   - Load airport data into PostgreSQL"
    echo "a_o_c   - Load aviation occurrence categories into PostgreSQL"
    echo "l_c_s   - Load country and state data into PostgreSQL"
    echo "l_c_d   - Load data from a correction file into PostgreSQL"
    echo "l_s_e   - Load sequence of events data into PostgreSQL"
    echo "l_s_d   - Load simplemaps data into PostgreSQL"
    echo "l_z_d   - Load ZIP Code Database data into PostgreSQL"
    echo "-------------------------------------------------------------------"
    echo "d_d_c   - Delete the PostgreSQL database container"
    echo "d_d_f   - Delete the PostgreSQL database files"
    echo "s_d_c   - Set up the PostgreSQL database container"
    echo "c_d_s   - Create the PostgreSQL database schema"
    echo "u_d_s   - Update the PostgreSQL database schema"
    echo "r_d_s   - Refresh the PostgreSQL database schema"
    echo "-------------------------------------------------------------------"
    echo "c_d_l   - Run Docker Compose tasks - Local"
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

if [ "${IO_AERO_TASK}" = "c_d_l" ]; then
    if [ -z "$2" ]; then
        echo "==================================================================="
        echo "clean - Remove all containers and images"
        echo "down  - Stop  Docker Compose"
        echo "logs  - Fetch the logs of a container"
        echo "up    - Start Docker Compose"
        echo "-------------------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the desired Docker Compose task [default: ${IO_AERO_COMPOSE_TASK_DEFAULT}] " IO_AERO_COMPOSE_TASK
        export IO_AERO_COMPOSE_TASK=${IO_AERO_COMPOSE_TASK}
    else
        export IO_AERO_COMPOSE_TASK=$2
    fi
fi

if [ "${IO_AERO_TASK}" = "l_c_d" ]; then
    if [ -z "$2" ]; then
        echo "==================================================================="
        ls -ll ${IO_AERO_CORRECTION_WORK_DIR}/*.xlsx
        echo "-------------------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the stem name of the desired correction file " IO_AERO_MSEXCEL
        export IO_AERO_MSEXCEL=${IO_AERO_MSEXCEL}
    else
        export IO_AERO_MSEXCEL=$2
    fi
fi

if [ "${IO_AERO_TASK}" = "l_n_a" ]; then
    if [ -z "$2" ]; then
        echo "==================================================================="
        ls -ll ${IO_AERO_NTSB_WORK_DIR}/*.mdb
        echo "-------------------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the stem name of the desired MS Access database file " IO_AERO_MSACCESS
        export IO_AERO_MSACCESS=${IO_AERO_MSACCESS}
    else
        export IO_AERO_MSACCESS=$2
    fi
fi

if [ "${IO_AERO_TASK}" = "u_p_d" ]; then
    if [ -z "$2" ]; then
        echo "==================================================================="
        echo "avall   - Data from January 1, 2008 to today"
        echo "Pre2008 - Data from January 1, 1982 to December 31, 2007"
        echo "upDDMON - New additions and updates until DD day in the month MON"
        echo "-------------------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the stem name of the desired MS Access database file " IO_AERO_MSACCESS
        export IO_AERO_MSACCESS=${IO_AERO_MSACCESS}
    else
        export IO_AERO_MSACCESS=$2
    fi
fi

# Path to the log file
log_file="run_io_avstats_pytest_${IO_AERO_TASK}.log"

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
echo "COMPOSE_TASK             : ${IO_AERO_COMPOSE_TASK}"
echo "MSACCESS                 : ${IO_AERO_MSACCESS}"
echo "MSEXCEL                  : ${IO_AERO_MSEXCEL}"
echo "-------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "==================================================================="

# -----------------------------------------------------------------------
# a_o_c  : Load aviation occurrence categories into PostgreSQL.
# c_d_s  : Create the PostgreSQL database schema.
# c_l_l  : Correct decimal US latitudes and longitudes.
# c_p_d  : Cleansing PostgreSQL data.
# f_n_a  : Find the nearest airports.
# l_a_p  : Load airport data into PostgreSQL.
# l_c_s  : Load country and state data into PostgreSQL.
# l_s_d  : Load simplemaps data into PostgreSQL.
# l_s_e  : Load sequence of events data into PostgreSQL.
# l_z_d  : Load US Zip code data.
# r_d_s  : Refresh the PostgreSQL database schema.
# u_d_s  : Update the PostgreSQL database schema.
# version: Show the IO-AVSTATS version
# v_n_d  : Verify selected NTSB data.
# ---------------------------------------------------------------------------
# Task handling
if [[ "${IO_AERO_TASK}" = @("a_o_c"|"c_d_s"|"c_l_l"|"c_p_d"|"f_n_a"|"l_a_p"|"l_c_s"|"l_s_d"|"l_s_e"|"l_z_d"|"r_d_s"|"u_d_s"|"v_n_d"|"version") ]]; then
    if ! ( pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}" ); then
        exit 255
    fi

# ---------------------------------------------------------------------------
# Run Docker Compose tasks (Local).
# ---------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "c_d_l" ]; then
    if ! ( ./scripts/run_docker_compose_local.sh "${IO_AERO_COMPOSE_TASK}" ); then
        exit 255
    fi

# ---------------------------------------------------------------------------
# Delete the PostgreSQL database container.
# ---------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "d_d_c" ]; then
    if ! ( ./scripts/run_delete_postgresql_container.sh ); then
        exit 255
    fi

# ---------------------------------------------------------------------------
# Delete the PostgreSQL database files.
# ---------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "d_d_f" ]; then
    if ! ( ./scripts/run_delete_postgresql_files.sh ); then
        exit 255
    fi

# ---------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# ---------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "l_c_d" ]; then
    if ! ( pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}" -e "${IO_AERO_MSEXCEL}".xlsx ); then
        exit 255
    fi

# ---------------------------------------------------------------------------
# Load NTSB MS Access database data into PostgreSQL.
# ---------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "l_n_a" ]; then
    if ! ( pipenv run python scripts/launcher.py -t d_n_a -m "${IO_AERO_MSACCESS}" ); then
        exit 255
    fi
    if ! ( pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}" -m "${IO_AERO_MSACCESS}" ); then
        exit 255
    fi

# ---------------------------------------------------------------------------
# Setting up the PostgreSQL database container.
# ---------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "s_d_c" ]; then
    if ! ( ./scripts/run_setup_postgresql.sh ); then
        exit 255
    fi

# ---------------------------------------------------------------------------
# Complete processing of a modifying MS Access file.
# ---------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "u_p_d" ]; then
    if ! ( pipenv run python scripts/launcher.py -t d_n_a -m "${IO_AERO_MSACCESS}" ); then
        exit 255
    fi
    if ! ( pipenv run python scripts/launcher.py -t l_n_a -m "${IO_AERO_MSACCESS}" ); then
        exit 255
    fi
    if ! ( pipenv run python scripts/launcher.py -t c_l_L ); then
        exit 255
    fi
    if ! ( pipenv run python scripts/launcher.py -t f_n_a ); then
        exit 255
    fi
    if ! ( pipenv run python scripts/launcher.py -t v_n_d ); then
        exit 255
    fi
    if ! ( pipenv run python scripts/launcher.py -t r_d_s ); then
        exit 255
    fi

# ---------------------------------------------------------------------------
# Program abort due to wrong input.
# ---------------------------------------------------------------------------
else
    echo "The processing of the script run_io_avstats is aborted: unknown task='${IO_AERO_TASK}'"
    exit 255
fi

echo "-----------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "-----------------------------------------------------------------------"
echo "End   $0"
echo "======================================================================="

# Closing the log file
exec > >(while read -r line; do echo "$line"; done) 2> >(while read -r line; do echo "ERROR: $line"; done)

# Closing the log file
log_message "Script finished."
