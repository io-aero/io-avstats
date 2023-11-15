#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_IO_AERO_pytest.zsh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------------

if [[ -z "${ENV_FOR_DYNACONF}" ]]; then
    export ENV_FOR_DYNACONF=test
fi

export IO_AERO_AVIATION_EVENT_STATISTICS=data/AviationAccidentStatistics
export IO_AERO_CORRECTION_WORK_DIR=data/correction
export IO_AERO_NTSB_WORK_DIR=data/download

if [[ -z "${IO_AERO_POSTGRES_CONNECTION_PORT}" ]]; then
    export IO_AERO_POSTGRES_CONNECTION_PORT=5433
fi

export IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db_test
export IO_AERO_POSTGRES_DBNAME_ADMIN=postgres
export IO_AERO_POSTGRES_PASSWORD_ADMIN="V3s8m4x*MYbHrX*UuU6X"
export IO_AERO_POSTGRES_PGDATA=data/postgres_test
export IO_AERO_POSTGRES_USER_ADMIN=postgres
export IO_AERO_POSTGRES_VERSION=16.1

export IO_AERO_MSACCESS=
export IO_AERO_MSEXCEL=
export IO_AERO_TASK=

export PYTHONPATH=.

if [[ -z "$1" ]]; then
    print "\n========================================================="
    print "\nc_l_l   - Correct decimal US latitudes and longitudes"
    print "\nv_n_d   - Verify selected NTSB data"
    print "\nr_d_s   - Refresh the PostgreSQL database schema"
    print "\n---------------------------------------------------------"
    print "\na_o_c   - Load aviation occurrence categories into PostgreSQL"
    print "\nl_a_p   - Load airport data into PostgreSQL"
    print "\nl_c_d   - Load data from a correction file into PostgreSQL"
    print "\nl_c_s   - Load country and state data into PostgreSQL"
    print "\nl_s_d   - Load simplemaps data into PostgreSQL"
    print "\nl_s_e   - Load sequence of events data into PostgreSQL"
    print "\nl_z_d   - Load ZIP Code Database data into PostgreSQL"
    print "\n---------------------------------------------------------"
    print "\nc_d_s   - Create the PostgreSQL database schema"
    print "\nc_p_d   - Cleansing PostgreSQL data"
    print "\nd_d_c   - Delete the PostgreSQL database container"
    print "\nd_d_f   - Delete the PostgreSQL database files"
    print "\nf_n_a   - Find the nearest airports"
    print "\ns_d_c   - Set up the PostgreSQL database container"
    print "\nu_d_s   - Update the PostgreSQL database schema"
    print "\n---------------------------------------------------------"
    read "IO_AERO_TASK?Enter the desired task "
    export IO_AERO_TASK=${IO_AERO_TASK:-${IO_AERO_TASK_DEFAULT}}
else
    export IO_AERO_TASK=$1
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
print "\nPYTHONPATH : ${PYTHONPATH}"
print "\n--------------------------------------------------------------------------------"
print "\nTASK       : ${IO_AERO_TASK}"
print "\nMSACCESS   : ${IO_AERO_MSACCESS}"
print "\nMSEXCEL    : ${IO_AERO_MSEXCEL}"
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
        if ! ( pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}" ); then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Delete the PostgreSQL database container.
# ------------------------------------------------------------------------------
    "d_d_c")
        if ! ( ./scripts/run_delete_postgresql_container.zsh ); then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Delete the PostgreSQL database files.
# ------------------------------------------------------------------------------
    "d_d_f")
        if ! ( ./scripts/run_delete_postgresql_files.zsh ); then
            exit 255
        fi
        ;;
# ------------------------------------------------------------------------------
# Load data from a correction file into PostgreSQL.
# ------------------------------------------------------------------------------
    "l_c_d")
        if ! ( pipenv run python scripts/launcher.py -t "${IO_AERO_TASK}" -e "${IO_AERO_MSEXCEL}".xlsx ); then
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
        print "\nProcessing of the script run_IO_AERO_pytest is aborted: unknown task='${IO_AERO_TASK}'"
        exit 255
        ;;
esac

print "\n--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n--------------------------------------------------------------------------------"
print "\nEnd   $0"
print "\n================================================================================"
