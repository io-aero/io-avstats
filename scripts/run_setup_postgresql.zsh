#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_setup_postgresql.zsh: Set up a PostgreSQL Docker container.
#
# ------------------------------------------------------------------------------

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "IO-AVSTATS - Set up a PostgreSQL Docker container."
echo "--------------------------------------------------------------------------------"
echo "POSTGRES_CONNECTION_PORT : ${IO_AERO_POSTGRES_CONNECTION_PORT}"
echo "POSTGRES_CONTAINER_NAME  : ${IO_AERO_POSTGRES_CONTAINER_NAME}"
echo "POSTGRES_DBNAME_ADMIN    : ${IO_AERO_POSTGRES_DBNAME_ADMIN}"
echo "POSTGRES_PGDATA          : ${IO_AERO_POSTGRES_PGDATA}"
echo "POSTGRES_USER_ADMIN      : ${IO_AERO_POSTGRES_USER_ADMIN}"
echo "POSTGRES_VERSION         : ${IO_AERO_POSTGRES_VERSION}"
echo "--------------------------------------------------------------------------------"

echo "Docker stop/rm ${IO_AERO_POSTGRES_CONTAINER_NAME} ...................................... before:"
docker ps -a
docker ps    | grep ${IO_AERO_POSTGRES_CONTAINER_NAME} && docker stop       ${IO_AERO_POSTGRES_CONTAINER_NAME}
docker ps -a | grep ${IO_AERO_POSTGRES_CONTAINER_NAME} && docker rm --force ${IO_AERO_POSTGRES_CONTAINER_NAME}
echo "............................................................. after:"
docker ps -a

start=$(date +%s)

# ------------------------------------------------------------------------------
# PostgreSQL                                   https://hub.docker.com/_/postgres
# ------------------------------------------------------------------------------

echo "PostgreSQL."
echo "--------------------------------------------------------------------------------"
echo "Docker create ${IO_AERO_POSTGRES_CONTAINER_NAME} (PostgreSQL ${IO_AERO_POSTGRES_VERSION})"

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

echo "Docker start ${IO_AERO_POSTGRES_CONTAINER_NAME} (PostgreSQL ${IO_AERO_POSTGRES_VERSION}) ..."
if ! docker start ${IO_AERO_POSTGRES_CONTAINER_NAME}; then
    exit 255
fi

echo "Waiting for PostgreSQL to be ready..."
until docker exec ${IO_AERO_POSTGRES_CONTAINER_NAME} pg_isready -q -d ${IO_AERO_POSTGRES_DBNAME_ADMIN}; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done
echo "PostgreSQL is ready."

end=$(date +%s)
echo "DOCKER PostgreSQL was ready in $((end - start)) seconds"

docker ps

echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
