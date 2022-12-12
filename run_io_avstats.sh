#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_io_avstats.sh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------------

export ENV_FOR_DYNACONF=dev

export IO_AVSTATS_NTSB_WORK_DIR=data/download
export IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
export IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
export IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
export IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres
export IO_AVSTATS_POSTGRES_PASSWORD_ADMIN=postgresql
export IO_AVSTATS_POSTGRES_PGDATA=data/postgres
export IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
export IO_AVSTATS_POSTGRES_VERSION=latest

export IO_AVSTATS_CORRECTION=
export IO_AVSTATS_TASK=
export IO_AVSTATS_TASK_DEFAULT=faaus2008

if [ -z "$1" ]; then
    echo "========================================================="
    echo "faaus2008 - Fatal Aircraft Accidents in the US since 2008"
    echo "pdus2008  - Profiling Data for the US since 2008"
    echo "---------------------------------------------------------"
    echo "c_l_l     - Correct decimal US latitudes and longitudes"
    echo "v_n_d     - Verify selected NTSB data"
    echo "---------------------------------------------------------"
    echo "c_p_d     - Cleansing PostgreSQL data"
    echo "d_s_f     - Download basic simplemaps files"
#   echo "d_z_f     - Download the ZIP Code Database file"
    echo "l_c_d     - Load data from a correction file into PostgreSQL"
    echo "l_c_s     - Load country and state data into PostgreSQL"
    echo "l_s_d     - Load simplemaps data into PostgreSQL"
    echo "l_z_d     - Load ZIP Code Database data into PostgreSQL"
    echo "---------------------------------------------------------"
    echo "c_d_s     - Create the PostgreSQL database schema"
    echo "d_d_f     - Delete the PostgreSQL database files"
    echo "d_d_s     - Drop the PostgreSQL database schema"
    echo "s_d_c     - Set up the PostgreSQL database container"
    echo "u_d_s     - Update the PostgreSQL database schema"
    echo "---------------------------------------------------------"
    echo "version - Show the IO-AVSTATS-DB version"
    echo "---------------------------------------------------------"
    # shellcheck disable=SC2162
    read -p "Enter the desired task [default: ${IO_AVSTATS_TASK_DEFAULT}] " IO_AVSTATS_TASK
    export IO_AVSTATS_TASK=${IO_AVSTATS_TASK}

    if [ -z "${IO_AVSTATS_TASK}" ]; then
        export IO_AVSTATS_TASK=${IO_AVSTATS_TASK_DEFAULT}
    fi
else
    export IO_AVSTATS_TASK=$1
fi

if [ "${IO_AVSTATS_TASK}" = "l_c_d" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        ls -ll data/correction/*.mdb
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the stem name of the desired correction file " IO_AVSTATS_CORRECTION
        export IO_AVSTATS_CORRECTION=${IO_AVSTATS_CORRECTION}
    else
        export IO_AVSTATS_CORRECTION=$2
    fi
fi

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "IO-AVSTATS - Aviation Accident Statistics."
echo "--------------------------------------------------------------------------------"
echo "PYTHONPATH : ${PYTHONPATH}"
echo "--------------------------------------------------------------------------------"
echo "TASK       : ${IO_AVSTATS_TASK}"
echo "TASK       : ${IO_AVSTATS_TASK}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

# ------------------------------------------------------------------------------
# c_d_s: Create the PostgreSQL database schema.
# c_l_i: Correct decimal US latitudes and longitudes.
# d_d_s: Drop the PostgreSQL database schema.
# d_s_f: Download basic simplemaps files.
# d_z_f: Download the ZIP Code Database file.
# l_c_s: Load country and state data into PostgreSQL.
# l_s_d: Load simplemaps data into PostgreSQL.
# l_z_d: Load US Zip code data.
# u_d_s: Update the PostgreSQL database schema.
# v_n_d: Verify selected NTSB data.
# version: Show the IO-AVSTATS-DB version.
# ------------------------------------------------------------------------------
if [[ "${IO_AVSTATS_TASK}" = @("c_d_s"|"c_l_l"|"c_p_d"|"d_d_s"|"d_s_f"|"d_z_f"|"l_c_s"|"l_s_d"|"l_z_d"|"u_d_s"|"v_n_d"|"version") ]]; then
    if ! ( pipenv run python src/launcher.py -t "${IO_AVSTATS_TASK}" ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Delete the PostgreSQL database files.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "d_d_f" ]; then
    if [ -d "${IO_AVSTATS_POSTGRES_PGDATA}" ]; then
        sudo ls -ll "${IO_AVSTATS_POSTGRES_PGDATA}"
        if ! ( sudo rm -rf ${IO_AVSTATS_POSTGRES_PGDATA} ); then
            exit 255
        fi
    fi

# ------------------------------------------------------------------------------
# Show the IO-AVSTATS faaus2008 application.
# ------------------------------------------------------------------------------

elif [ "${IO_AVSTATS_TASK}" = "faaus2008" ]; then
    if ! ( pipenv run streamlit run src/faaus2008_app/faaus2008.py ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "l_c_d" ]; then
    if ! ( pipenv run python src/launcher.py -t "${IO_AVSTATS_TASK}" -c "${IO_AVSTATS_CORRECTION}" ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Show the IO-AVSTATS pdus2008 application.
# ------------------------------------------------------------------------------

elif [ "${IO_AVSTATS_TASK}" = "pdus2008" ]; then
    if ! ( pipenv run streamlit run src/pdus2008_app/pdus2008.py ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Setup the database container.
# ------------------------------------------------------------------------------

elif [ "${IO_AVSTATS_TASK}" = "s_d_c" ]; then
    if ! ( ./scripts/run_setup_postgresql.sh ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Program abort due to wrong input.
# ------------------------------------------------------------------------------

else
    echo "Processing of the script run_io_avstats is aborted: unknown task='${IO_AVSTATS_TASK}'"
    exit 255
fi

echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
