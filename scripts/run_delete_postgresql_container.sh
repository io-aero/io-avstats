#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_delete_postgresql_container.sh: Delete the PostgreSQL database container.
#
# ------------------------------------------------------------------------------

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "IO-AVSTATS - Delete the PostgreSQL database container."
echo "--------------------------------------------------------------------------------"
echo "POSTGRES_CONTAINER_NAME  : ${IO_AERO_POSTGRES_CONTAINER_NAME}"
echo --------------------------------------------------------------------------------

echo "Docker stop/rm ${IO_AERO_POSTGRES_CONTAINER_NAME} ...................................... before:"
docker ps -a
docker ps | grep "${IO_AERO_POSTGRES_CONTAINER_NAME}" && docker stop "${IO_AERO_POSTGRES_CONTAINER_NAME}"
docker ps -a | grep "${IO_AERO_POSTGRES_CONTAINER_NAME}" && docker rm --force "${IO_AERO_POSTGRES_CONTAINER_NAME}"
echo "............................................................. after:"
docker ps -a


echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
