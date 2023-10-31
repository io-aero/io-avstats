#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_delete_postgresql_container.zsh: Delete the PostgreSQL database container.
#
# ------------------------------------------------------------------------------

print "\n================================================================================"
print "\nStart $0"
print "\n--------------------------------------------------------------------------------"
print "\nIO-AVSTATS - Delete the PostgreSQL database container."
print "\n--------------------------------------------------------------------------------"
print "\nPOSTGRES_CONTAINER_NAME  : ${IO_AERO_POSTGRES_CONTAINER_NAME}"
echo --------------------------------------------------------------------------------

print "\nDocker stop/rm ${IO_AERO_POSTGRES_CONTAINER_NAME} ...................................... before:"
docker ps -a
docker ps | grep -- "${IO_AERO_POSTGRES_CONTAINER_NAME}" && docker stop "${IO_AERO_POSTGRES_CONTAINER_NAME}"
docker ps -a | grep -- "${IO_AERO_POSTGRES_CONTAINER_NAME}" && docker rm --force "${IO_AERO_POSTGRES_CONTAINER_NAME}"
print "\n............................................................. after:"
docker ps -a


print "\n--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n--------------------------------------------------------------------------------"
print "\nEnd   $0"
print "\n================================================================================"
