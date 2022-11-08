#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_io_avstats.sh: Process IO-AVSTATS tasks.
#
# ------------------------------------------------------------------------------

export ENV_FOR_DYNACONF=dev

export IO_AVSTATS_TASK=
export IO_AVSTATS_TASK_DEFAULT=version

if [ -z "$1" ]; then
    echo "========================================================="
    echo "version - Show the IO-AVSTATS version"
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
# Show the IO-AVSTATS version.
# ------------------------------------------------------------------------------

elif [ "${IO_AVSTATS_TASK}" = "version" ]; then
    if ! ( pipenv run python src/launcher.py -t "${IO_AVSTATS_TASK}" ); then
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
