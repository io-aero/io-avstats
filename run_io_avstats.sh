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
export IO_AERO_POSTGRES_VERSION=16.1

export IO_AERO_APPLICATION=
export IO_AERO_COMPOSE_TASK=
export IO_AERO_COMPOSE_TASK_DEFAULT=logs
export IO_AERO_CONTAINER=
export IO_AERO_CONTAINER_DEFAULT="*"
export IO_AERO_MSEXCEL=
export IO_AERO_TASK=
export IO_AERO_TASK_DEFAULT=r_s_a

export PYTHONPATH=.

if [ -z "$1" ]; then
    echo "========================================================="
    echo "r_s_a   - Run the IO-AVSTATS application"
    echo "---------------------------------------------------------"
    echo "c_p_d   - Cleansing PostgreSQL data"
    echo "c_l_l   - Correct decimal US latitudes and longitudes"
    echo "f_n_a   - Find the nearest airports"
    echo "v_n_d   - Verify selected NTSB data"
    echo "---------------------------------------------------------"
    echo "l_a_p   - Load airport data into PostgreSQL"
    echo "a_o_c   - Load aviation occurrence categories into PostgreSQL"
    echo "l_c_s   - Load country and state data into PostgreSQL"
    echo "l_c_d   - Load data from a correction file into PostgreSQL"
    echo "l_s_e   - Load sequence of events data into PostgreSQL"
    echo "l_s_d   - Load simplemaps data into PostgreSQL"
    echo "l_z_d   - Load ZIP Code Database data into PostgreSQL"
    echo "---------------------------------------------------------"
    echo "s_d_c   - Set up the PostgreSQL database container"
    echo "c_d_s   - Create the PostgreSQL database schema"
    echo "u_d_s   - Update the PostgreSQL database schema"
    echo "r_d_s   - Refresh the PostgreSQL database schema"
    echo "---------------------------------------------------------"
    echo "c_f_z   - Zip the files for the cloud"
    echo "c_d_i   - Create or update a Docker image"
    echo "c_d_c   - Run Docker Compose tasks - Cloud"
    echo "c_d_l   - Run Docker Compose tasks - Local"
    echo "---------------------------------------------------------"
    echo "version - Show the IO-AVSTATS version"
    echo "---------------------------------------------------------"
    # shellcheck disable=SC2162
    read -p "Enter the desired task [default: ${IO_AERO_TASK_DEFAULT}] " IO_AERO_TASK
    export IO_AERO_TASK=${IO_AERO_TASK}

    if [ -z "${IO_AERO_TASK}" ]; then
        export IO_AERO_TASK=${IO_AERO_TASK_DEFAULT}
    fi
else
    export IO_AERO_TASK=$1
fi

if [ "${IO_AERO_TASK}" = "c_d_c" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        echo "clean - Remove all containers and images"
        echo "down  - Stop  Docker Compose"
        echo "logs  - Fetch the logs of a container"
        echo "up    - Start Docker Compose"
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the desired Docker Compose task [default: ${IO_AERO_COMPOSE_TASK_DEFAULT}] " IO_AERO_COMPOSE_TASK
        export IO_AERO_COMPOSE_TASK=${IO_AERO_COMPOSE_TASK}

        if [ -z "${IO_AERO_COMPOSE_TASK}" ]; then
            export IO_AERO_COMPOSE_TASK=${IO_AERO_COMPOSE_TASK_DEFAULT}
        fi
    else
        export IO_AERO_COMPOSE_TASK=$2
    fi
fi

if [ "${IO_AERO_TASK}" = "c_d_i" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        echo "all    - All Streamlit applications"
        echo "---------------------------------------------------------"
        echo "ae1982  - Aircraft Accidents in the US since 1982"
        echo "pd1982  - Profiling Data for the US since 1982"
        echo "slara   - Association Rule Analysis"
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the Streamlit application name " IO_AERO_APPLICATION
        export IO_AERO_APPLICATION=${IO_AERO_APPLICATION}
    else
        export IO_AERO_APPLICATION=$2
    fi
fi

if [ "${IO_AERO_TASK}" = "c_d_l" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        echo "clean - Remove all containers and images"
        echo "down  - Stop  Docker Compose"
        echo "logs  - Fetch the logs of a container"
        echo "up    - Start Docker Compose"
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the desired Docker Compose task [default: ${IO_AERO_COMPOSE_TASK_DEFAULT}] " IO_AERO_COMPOSE_TASK
        export IO_AERO_COMPOSE_TASK=${IO_AERO_COMPOSE_TASK}

        if [ -z "${IO_AERO_COMPOSE_TASK}" ]; then
            export IO_AERO_COMPOSE_TASK=${IO_AERO_COMPOSE_TASK_DEFAULT}
        fi
    else
        export IO_AERO_COMPOSE_TASK=$2
    fi
fi

if [ "${IO_AERO_TASK}" = "l_c_d" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        ls -ll ${IO_AERO_CORRECTION_WORK_DIR}/*.xlsx
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the stem name of the desired correction file " IO_AERO_MSEXCEL
        export IO_AERO_MSEXCEL=${IO_AERO_MSEXCEL}
    else
        export IO_AERO_MSEXCEL=$2
    fi
fi

rm -f logging_io_aero.log

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "IO-AVSTATS - Aviation Event Statistics."
echo "--------------------------------------------------------------------------------"
echo "PYTHONPATH   : ${PYTHONPATH}"
echo "--------------------------------------------------------------------------------"
echo "TASK         : ${IO_AERO_TASK}"
echo "APPLICATION  : ${IO_AERO_APPLICATION}"
echo "COMPOSE_TASK : ${IO_AERO_COMPOSE_TASK}"
echo "MSEXCEL      : ${IO_AERO_MSEXCEL}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------
if [[ "${IO_AERO_TASK}" = @("a_o_c"|"c_d_s"|"c_l_l"|"c_p_d"|"f_n_a"|"l_a_p"|"l_c_s"|"l_s_d"|"l_s_e"|"l_z_d"|"r_d_s"|"u_d_s"|"v_n_d"|"version") ]]; then
    if ! ( pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}" ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Run Docker Compose tasks (Cloud).
# ------------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "c_d_c" ]; then
    if ! ( ./scripts/run_docker_compose_cloud.sh "${IO_AERO_COMPOSE_TASK}" ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Create or update a Docker image.
# ------------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "c_d_i" ]; then
    if ! ( ./scripts/run_create_image.sh "${IO_AERO_APPLICATION}" yes yes ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# ------------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "l_c_d" ]; then
    if ! ( pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}" -e "${IO_AERO_MSEXCEL}".xlsx ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Run a Streamlit application.
# ------------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "r_s_a" ]; then
    if ! ( pipenv run streamlit run "ioavstats/Menu.py" --server.port 8501 ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Set up the PostgreSQL database container.
# ------------------------------------------------------------------------------
elif [ "${IO_AERO_TASK}" = "s_d_c" ]; then
    if ! ( ./scripts/run_setup_postgresql.sh ); then
        exit 255
    fi

# ------------------------------------------------------------------------------
# Program abort due to wrong input.
# ------------------------------------------------------------------------------
else
    echo "Processing of the script run_io_avstats is aborted: unknown task='${IO_AERO_TASK}'"
    exit 255
fi

echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
