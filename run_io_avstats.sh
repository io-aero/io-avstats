#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_io_avstats.sh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------------

if [ -z "${ENV_FOR_DYNACONF}" ]; then
    export ENV_FOR_DYNACONF=prod
fi

export IO_AVSTATS_CORRECTION_WORK_DIR=data/correction
export IO_AVSTATS_NTSB_WORK_DIR=data/download

if [ -z "${IO_AVSTATS_POSTGRES_CONNECTION_PORT}" ]; then
    export IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
fi

export IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
export IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
export IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres
export IO_AVSTATS_POSTGRES_PASSWORD_ADMIN=V3s8m4x*MYbHrX*UuU6X
export IO_AVSTATS_POSTGRES_PGDATA=data/postgres
export IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
export IO_AVSTATS_POSTGRES_VERSION=latest

export IO_AVSTATS_APPLICATION=
export IO_AVSTATS_COMPOSE_TASK_DEFAULT=up
export IO_AVSTATS_MSACCESS=
export IO_AVSTATS_MSEXCEL=
export IO_AVSTATS_TASK=
export IO_AVSTATS_TASK_DEFAULT=r_s_a

if [ -z "$1" ]; then
    echo "========================================================="
    echo "r_s_a   - Run a Streamlit application"
    echo "---------------------------------------------------------"
    echo "c_l_l   - Correct decimal US latitudes and longitudes"
    echo "v_n_d   - Verify selected NTSB data"
    echo "r_d_s   - Refresh the PostgreSQL database schema"
    echo "---------------------------------------------------------"
    echo "d_s_f   - Download basic simplemaps files"
    echo "l_s_d   - Load simplemaps data into PostgreSQL"
#   echo "d_z_f   - Download the ZIP Code Database file"
    echo "l_z_d   - Load ZIP Code Database data into PostgreSQL"
    echo "l_c_d   - Load data from a correction file into PostgreSQL"
    echo "---------------------------------------------------------"
    echo "a_o_c   - Load aviation occurrence categories into PostgreSQL"
    echo "c_d_s   - Create the PostgreSQL database schema"
    echo "c_p_d   - Cleansing PostgreSQL data"
    echo "d_d_f   - Delete the PostgreSQL database files"
    echo "l_n_s   - Load NTSB MS Excel statistic data into PostgreSQL"
    echo "d_d_s   - Drop the PostgreSQL database schema"
    echo "l_c_s   - Load country and state data into PostgreSQL"
    echo "l_s_e   - Load sequence of events data into PostgreSQL"
    echo "p_p_k   - Process NTSB data deletions in PostgreSQL"
    echo "s_d_c   - Set up the PostgreSQL database container"
    echo "u_d_s   - Update the PostgreSQL database schema"
    echo "---------------------------------------------------------"
    echo "c_d_i   - Create or update a Docker image"
    echo "c_d_c   - Run Docker Compose tasks"
    echo "c_f_z   - Zip the files for the cloud"
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

if [ "${IO_AVSTATS_TASK}" = "c_d_c" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        echo "clean - Remove all containers and images"
        echo "down  - Stop  Docker Compose"
        echo "up    - Start Docker Compose"
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the desired Docker Compose task [default: ${IO_AVSTATS_COMPOSE_TASK_DEFAULT}] " IO_AVSTATS_COMPOSE_TASK
        export IO_AVSTATS_COMPOSE_TASK=${IO_AVSTATS_COMPOSE_TASK}

        if [ -z "${IO_AVSTATS_COMPOSE_TASK}" ]; then
            export IO_AVSTATS_COMPOSE_TASK=${IO_AVSTATS_COMPOSE_TASK_DEFAULT}
        fi
    else
        export IO_AVSTATS_COMPOSE_TASK=$2
    fi
fi

if [ "${IO_AVSTATS_TASK}" = "c_d_i" ] || [ "${IO_AVSTATS_TASK}" = "r_s_a" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        echo "all    - All Streamlit applications"
        echo "---------------------------------------------------------"
        echo "ae1982 - Aircraft Accidents in the US since 1982"
        echo "pd1982 - Profiling Data for the US since 1982"
        echo "stats  - Aircraft Accidents in the US since 1982 - limited"
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the Streamlit application name " IO_AVSTATS_APPLICATION
        export IO_AVSTATS_APPLICATION=${IO_AVSTATS_APPLICATION}
    else
        export IO_AVSTATS_APPLICATION=$2
    fi
fi

if [ "${IO_AVSTATS_TASK}" = "l_c_d" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        ls -ll ${IO_AVSTATS_CORRECTION_WORK_DIR}/*.xlsx
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the stem name of the desired correction file " IO_AVSTATS_MSEXCEL
        export IO_AVSTATS_MSEXCEL=${IO_AVSTATS_MSEXCEL}
    else
        export IO_AVSTATS_MSEXCEL=$2
    fi
fi

if [ "${IO_AVSTATS_TASK}" = "l_n_s" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        ls -ll ${IO_AVSTATS_NTSB_WORK_DIR}/*.xlsx
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the stem name of the desired desired NTSB statistic file " IO_AVSTATS_MSEXCEL
        export IO_AVSTATS_MSEXCEL=${IO_AVSTATS_MSEXCEL}
    else
        export IO_AVSTATS_MSEXCEL=$2
    fi
fi

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "IO-AVSTATS - Aviation Event Statistics."
echo "--------------------------------------------------------------------------------"
echo "PYTHONPATH : ${PYTHONPATH}"
echo "--------------------------------------------------------------------------------"
echo "TASK       : ${IO_AVSTATS_TASK}"
echo "MSACCESS   : ${IO_AVSTATS_MSACCESS}"
echo "MSEXCEL    : ${IO_AVSTATS_MSEXCEL}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

# ------------------------------------------------------------------------------
# a_o_c: Load aviation occurrence categories into PostgreSQL.
# c_d_s: Create the PostgreSQL database schema.
# c_l_l: Correct decimal US latitudes and longitudes.
# c_p_d: Cleansing PostgreSQL data.
# d_d_s: Drop the PostgreSQL database schema.
# d_s_f: Download basic simplemaps files.
# d_z_f: Download the ZIP Code Database file.
# l_c_s: Load country and state data into PostgreSQL.
# l_s_d: Load simplemaps data into PostgreSQL.
# l_s_e: Load sequence of events data into PostgreSQL.
# l_z_d: Load US Zip code data.
# p_p_k: Process NTSB data deletions in PostgreSQL.
# r_d_s: Refresh the PostgreSQL database schema.
# u_d_s: Update the PostgreSQL database schema.
# v_n_d: Verify selected NTSB data.
# version: Show the IO-AVSTATS-DB version.
# ------------------------------------------------------------------------------
if [[ "${IO_AVSTATS_TASK}" = @("a_o_c"|"c_d_s"|"c_l_l"|"c_p_d"|"d_d_s"|"d_s_f"|"d_z_f"|"l_c_s"|"l_s_d"|"l_s_e"|"l_z_d"|"p_p_k"|"r_d_s"|"u_d_s"|"v_n_d"|"version") ]]; then
    if ! ( pipenv run python src/launcher.py -t "${IO_AVSTATS_TASK}" ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Run Docker Compose tasks.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "c_d_c" ]; then
    if ! ( ./scripts/run_docker_compose.sh ${IO_AVSTATS_COMPOSE_TASK} ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Create or update a Docker image.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "c_d_i" ]; then
    if ! ( ./scripts/run_create_image.sh ${IO_AVSTATS_APPLICATION} yes yes ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Zip the files for the cloud.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "c_f_z" ]; then
    if ! ( ./scripts/run_cloud_files_zip.sh ); then
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
# Load data from a correction file into PostgreSQL.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "l_c_d" ]; then
    if ! ( pipenv run python src/launcher.py -t "${IO_AVSTATS_TASK}" -e "${IO_AVSTATS_MSEXCEL}".xlsx ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Load NTSB MS Excel statistic data into PostgreSQL.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "l_n_s" ]; then
    if ! ( pipenv run python src/launcher.py -t "${IO_AVSTATS_TASK}" -e "${IO_AVSTATS_MSEXCEL}".xlsx ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Run a Streamlit application.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "r_s_a" ]; then
    if [ "${IO_AVSTATS_APPLICATION}" = "ae1982" ]; then
        if ! ( pipenv run streamlit run src/ioavstats/${IO_AVSTATS_APPLICATION}.py -- --mode Std ); then
            exit 255
        fi
    elif [ "${IO_AVSTATS_APPLICATION}" = "stats" ]; then
        if ! ( pipenv run streamlit run src/ioavstats/ae1982.py ); then
            exit 255
        fi
    else
        if ! ( pipenv run streamlit run src/ioavstats/${IO_AVSTATS_APPLICATION}.py ); then
            exit 255
        fi
    fi

# ------------------------------------------------------------------------------
# Set up the database container.
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
