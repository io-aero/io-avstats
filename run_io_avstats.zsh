#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_io_avstats.zsh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------------

if [[ -z "${ENV_FOR_DYNACONF}" ]]; then
    export ENV_FOR_DYNACONF=prod
fi

export IO_AERO_AVIATION_EVENT_STATISTICS=data/AviationAccidentStatistics
export IO_AERO_CORRECTION_WORK_DIR=data/correction
export IO_AERO_NTSB_WORK_DIR=data/download

if [[ -z "${IO_AERO_POSTGRES_CONNECTION_PORT}" ]]; then
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
export IO_AERO_MSACCESS=
export IO_AERO_MSEXCEL=
export IO_AERO_TASK=
export IO_AERO_TASK_DEFAULT=r_s_a

export PYTHONPATH=.

if [[ -z "$1" ]]; then
    print "\n========================================================="
    print "\nr_s_a   - Run the IO-AVSTATS application"
    print "\n---------------------------------------------------------"
    print "\nc_l_l   - Correct decimal US latitudes and longitudes"
    print "\nv_n_d   - Verify selected NTSB data"
    print "\nr_d_s   - Refresh the PostgreSQL database schema"
    print "\n---------------------------------------------------------"
    print "\nl_s_d   - Load simplemaps data into PostgreSQL"
    print "\nl_z_d   - Load ZIP Code Database data into PostgreSQL"
    print "\nl_c_d   - Load data from a correction file into PostgreSQL"
    print "\n---------------------------------------------------------"
    print "\na_o_c   - Load aviation occurrence categories into PostgreSQL"
    print "\nc_d_s   - Create the IO-AVSTATS-DB PostgreSQL database schema"
    print "\nc_p_d   - Cleansing PostgreSQL data"
    print "\nf_n_a   - Find the nearest airports"
    print "\nl_a_p   - Load airport data into PostgreSQL"
    print "\nl_c_s   - Load country and state data into PostgreSQL"
    print "\nl_s_e   - Load sequence of events data into PostgreSQL"
    print "\ns_d_c   - Set up the IO-AVSTATS-DB PostgreSQL database container"
    print "\nu_d_s   - Update the IO-AVSTATS-DB PostgreSQL database schema"
    print "\n---------------------------------------------------------"
    print "\nc_d_i   - Create or update a Docker image"
    print "\nc_d_c   - Run Docker Compose tasks - Cloud"
    print "\n---------------------------------------------------------"
    read "IO_AERO_TASK?Enter the desired task [default: ${IO_AERO_TASK_DEFAULT}] "
    export IO_AERO_TASK=${IO_AERO_TASK:-${IO_AERO_TASK_DEFAULT}}
else
    export IO_AERO_TASK=$1
fi

if [[ "${IO_AERO_TASK}" = "c_d_c" ]]; then
    if [[ -z "$2" ]]; then
        print "\n========================================================="
        print "\nclean - Remove all containers and images"
        print "\ndown  - Stop  Docker Compose"
        print "\nlogs  - Fetch the logs of a container"
        print "\nup    - Start Docker Compose"
        print "\n---------------------------------------------------------"
        read "IO_AERO_COMPOSE_TASK?Enter the desired Docker Compose task [default: ${IO_AERO_COMPOSE_TASK_DEFAULT}] "
        export IO_AERO_COMPOSE_TASK=${IO_AERO_COMPOSE_TASK:-${IO_AERO_COMPOSE_TASK_DEFAULT}}
    else
        export IO_AERO_COMPOSE_TASK=$2
    fi
fi

if [[ "${IO_AERO_TASK}" = "c_d_i" ]]; then
    if [[ -z "$2" ]]; then
        print "\n========================================================="
        print "\nall    - All Streamlit applications"
        print "\n---------------------------------------------------------"
        print "\nae1982  - Aircraft Accidents in the US since 1982"
        print "\npd1982  - Profiling Data for the US since 1982"
        print "\nslara   - Association Rule Analysis"
        print "\n---------------------------------------------------------"
        read "IO_AERO_APPLICATION?Enter the Streamlit application name "
        export IO_AERO_APPLICATION=${IO_AERO_APPLICATION}
    else
        export IO_AERO_APPLICATION=$2
    fi
fi

if [[ "${IO_AERO_TASK}" = "l_c_d" ]]; then
    if [[ -z "$2" ]]; then
        print "\n========================================================="
        ls -ll ${IO_AERO_CORRECTION_WORK_DIR}/*.xlsx
        print "\n---------------------------------------------------------"
        read "IO_AERO_MSEXCEL?Enter the stem name of the desired correction file "
        export IO_AERO_MSEXCEL=${IO_AERO_MSEXCEL}
    else
        export IO_AERO_MSEXCEL=$2
    fi
fi

rm -f logging_io_aero.log

print "\n================================================================================"
print "\nStart $0"
print "\n--------------------------------------------------------------------------------"
print "\nIO-AVSTATS - Aviation Event Statistics."
print "\n--------------------------------------------------------------------------------"
print "\nPYTHONPATH   : ${PYTHONPATH}"
print "\n--------------------------------------------------------------------------------"
print "\nTASK         : ${IO_AERO_TASK}"
print "\nAPPLICATION  : ${IO_AERO_APPLICATION}"
print "\nCOMPOSE_TASK : ${IO_AERO_COMPOSE_TASK}"
print "\nMSACCESS     : ${IO_AERO_MSACCESS}"
print "\nMSEXCEL      : ${IO_AERO_MSEXCEL}"
print "\n--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n================================================================================"

# ------------------------------------------------------------------------------
# a_o_c: Load aviation occurrence categories into PostgreSQL.
# c_d_s: Create the PostgreSQL database schema.
# c_l_l: Correct decimal US latitudes and longitudes.
# c_p_d: Cleansing PostgreSQL data.
# f_n_a: Find the nearest airports.
# l_a_p: Load airport data into PostgreSQL.
# l_c_s: Load country and state data into PostgreSQL.
# l_s_d: Load simplemaps data into PostgreSQL.
# l_s_e: Load sequence of events data into PostgreSQL.
# l_z_d: Load US Zip code data.
# r_d_s: Refresh the PostgreSQL database schema.
# u_d_s: Update the PostgreSQL database schema.
# v_n_d: Verify selected NTSB data.
# ------------------------------------------------------------------------------
case "${IO_AERO_TASK}" in
    "a_o_c"|"c_d_s"|"c_l_l"|"c_p_d"|"f_n_a"|"l_a_p"|"l_c_s"|"l_s_d"|"l_s_e"|"l_z_d"|"r_d_s"|"u_d_s"|"v_n_d")
        if ! pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}"; then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Run Docker Compose tasks (Cloud).
# ------------------------------------------------------------------------------
    "c_d_c")
        if ! ./scripts/run_docker_compose_cloud.zsh "${IO_AERO_COMPOSE_TASK}"; then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Create or update a Docker image.
# ------------------------------------------------------------------------------
    "c_d_i")
        if ! ./scripts/run_create_image.zsh "${IO_AERO_APPLICATION}" yes yes; then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# ------------------------------------------------------------------------------
    "l_c_d")
        if ! pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}" -e "${IO_AERO_MSEXCEL}".xlsx; then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Run a Streamlit application.
# ------------------------------------------------------------------------------
    "r_s_a")
        if ! pipenv run streamlit run "ioavstats/Menu.py" --server.port 8501; then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Set up the IO-AVSTATS-DB PostgreSQL database container.
# ------------------------------------------------------------------------------
    "s_d_c")
        if ! ./scripts/run_setup_postgresql.zsh; then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Program abort due to wrong input.
# ------------------------------------------------------------------------------
    *)
        print "\nProcessing of the script run_io_avstats is aborted: unknown task='${IO_AERO_TASK}'"
        exit 255
        ;;
esac

print "\n--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n--------------------------------------------------------------------------------"
print "\nEnd   $0"
print "\n================================================================================"
