#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_io_avstats.sh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------------

export ENV_FOR_DYNACONF=dev

export IO_AVSTATS_TASK=
export IO_AVSTATS_TASK_DEFAULT=faaus2008

if [ -z "$1" ]; then
    echo "========================================================="
    echo "faaus2008 - Fatal Aircraft Accidents in the US since 2008"
    echo "pdus2008  - Profiling Data for the US since 2008"
    echo "---------------------------------------------------------"
    read -p "Enter the desired task [default: ${IO_AVSTATS_TASK_DEFAULT}] " IO_AVSTATS_TASK
    export IO_AVSTATS_TASK=${IO_AVSTATS_TASK}

    if [ -z "${IO_AVSTATS_TASK}" ]; then
        export IO_AVSTATS_TASK=${IO_AVSTATS_TASK_DEFAULT}
    fi
else
    export IO_AVSTATS_TASK=$1
fi

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "IO-AVSTATS - Aviation Accident Statistics."
echo "--------------------------------------------------------------------------------"
echo "PYTHONPATH : ${PYTHONPATH}"
echo "--------------------------------------------------------------------------------"
echo "TASK       : ${IO_AVSTATS_TASK}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

# ------------------------------------------------------------------------------
# Show the IO-AVSTATS faaus2008 application.
# ------------------------------------------------------------------------------

if [ "${IO_AVSTATS_TASK}" = "faaus2008" ]; then
    if ! ( pipenv run streamlit run src/faaus2008_app/faaus2008.py ); then
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
