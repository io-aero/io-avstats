#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_setup_postgresql.zsh: Set up a PostgreSQL Docker container.
#
# ------------------------------------------------------------------------------

print "\n================================================================================"
print "\nStart $0"
print "\n--------------------------------------------------------------------------------"
print "\nIO-AVSTATS - Set up a PostgreSQL Docker container."
print "\n--------------------------------------------------------------------------------"
# export IO_AERO_POSTGRES_CONNECTION_PORT=5432
# export IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db
# export IO_AERO_POSTGRES_DBNAME_ADMIN=postgres
# export IO_AERO_POSTGRES_PASSWORD_ADMIN="V3s8m4x*MYbHrX*UuU6X"
# export IO_AERO_POSTGRES_USER_ADMIN=postgres
# export IO_AERO_POSTGRES_VERSION=16.0
# print "\n--------------------------------------------------------------------------------"
# export IO_AERO_POSTGRES_PGDATA=data/postgres
# print "\n--------------------------------------------------------------------------------"
print "\nPOSTGRES_CONNECTION_PORT : ${IO_AERO_POSTGRES_CONNECTION_PORT}"
print "\nPOSTGRES_CONTAINER_NAME  : ${IO_AERO_POSTGRES_CONTAINER_NAME}"
print "\nPOSTGRES_DBNAME_ADMIN    : ${IO_AERO_POSTGRES_DBNAME_ADMIN}"
print "\nPOSTGRES_PGDATA          : ${IO_AERO_POSTGRES_PGDATA}"
print "\nPOSTGRES_USER_ADMIN      : ${IO_AERO_POSTGRES_USER}"
print "\nPOSTGRES_VERSION         : ${IO_AERO_POSTGRES_VERSION}"
echo --------------------------------------------------------------------------------

print "\nDocker stop/rm ${IO_AERO_POSTGRES_CONTAINER_NAME} ...................................... before:"
docker ps -a
docker ps | grep "${IO_AERO_POSTGRES_CONTAINER_NAME}" && docker stop ${IO_AERO_POSTGRES_CONTAINER_NAME}
docker ps -a | grep "${IO_AERO_POSTGRES_CONTAINER_NAME}" && docker rm --force ${IO_AERO_POSTGRES_CONTAINER_NAME}
print "\n............................................................. after:"
docker ps -a

start=$(date +%s)

# ------------------------------------------------------------------------------
# PostgreSQL                                   https://hub.docker.com/_/postgres
# ------------------------------------------------------------------------------

print "\nPostgreSQL."
print "\n--------------------------------------------------------------------------------"
print "\nDocker create ${IO_AERO_POSTGRES_CONTAINER_NAME} (PostgreSQL ${IO_AERO_POSTGRES_VERSION})"

mkdir -p "${PWD}/${IO_AERO_POSTGRES_PGDATA}"

docker create -e        POSTGRES_DB=${IO_AERO_POSTGRES_DBNAME_ADMIN} \
              -e        POSTGRES_HOST_AUTH_METHOD=password \
              -e        POSTGRES_PASSWORD=${IO_AERO_POSTGRES_PASSWORD_ADMIN} \
              -e        POSTGRES_USER=${IO_AERO_POSTGRES_USER_ADMIN} \
              --name    ${IO_AERO_POSTGRES_CONTAINER_NAME} \
              -p        ${IO_AERO_POSTGRES_CONNECTION_PORT}:5432 \
              -v        "${PWD}/${IO_AERO_POSTGRES_PGDATA}":/var/lib/postgresql/data \
              --restart always \
              postgres:${IO_AERO_POSTGRES_VERSION}

print "\nDocker start ${IO_AERO_POSTGRES_CONTAINER_NAME} (PostgreSQL ${IO_AERO_POSTGRES_VERSION}) ..."
if ! docker start ${IO_AERO_POSTGRES_CONTAINER_NAME}; then
    exit 255
fi

sleep 30

end=$(date +%s)
print "\nDOCKER PostgreSQL was ready in $((end - start)) seconds"

docker ps

print "\n--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n--------------------------------------------------------------------------------"
print "\nEnd   $0"
print "\n================================================================================"
