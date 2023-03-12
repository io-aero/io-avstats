#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_setup_postgresql_keycloak.sh: Set up a Keycloak PostgreSQL Docker container.
#
# ------------------------------------------------------------------------------

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "IO-AVSTATS - Set up a Keycloak server container."
echo "--------------------------------------------------------------------------------"
echo "KEYCLOAK_CONNECTION_PORT          : ${IO_AVSTATS_KEYCLOAK_CONNECTION_PORT}"
echo "KEYCLOAK_CONTAINER_NAME           : ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}"
echo "KEYCLOAK_CONTAINER_PORT           : ${IO_AVSTATS_KEYCLOAK_CONTAINER_PORT}"
echo "KEYCLOAK_USER_ADMIN               : ${IO_AVSTATS_KEYCLOAK_USER_ADMIN}"
echo "KEYCLOAK_VERSION                  : ${IO_AVSTATS_KEYCLOAK_VERSION}"
echo "POSTGRES_KEYCLOAK_CONNECTION_PORT : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT}"
echo "POSTGRES_KEYCLOAK_CONTAINER_NAME  : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}"
echo "POSTGRES_KEYCLOAK_DBNAME_ADMIN    : ${IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN}"
echo "POSTGRES_KEYCLOAK_USER_ADMIN      : ${IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN}"

echo --------------------------------------------------------------------------------

echo "Docker stop/rm ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME} ................. before:"
docker ps -a
docker ps    | grep "${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}" && docker stop       "${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}"
docker ps -a | grep "${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}" && docker rm --force "${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}"
echo "............................................................. after:"
docker ps -a

start=$(date +%s)

# ------------------------------------------------------------------------------
# PostgreSQL                                   https://hub.docker.com/_/postgres
# ------------------------------------------------------------------------------

echo "Keycloak"
echo "--------------------------------------------------------------------------------"
echo "Docker create ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME} (Keycloak ${IO_AVSTATS_KEYCLOAK_VERSION})"

export KC_DB=postgres
export KC_DB_PASSWORD="${IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN}"
export KC_DB_URL="jdbc:postgresql://${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}:${IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT}/${IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN}"
export KC_DB_USERNAME="${IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN}"
export KC_FEATURES=token-exchange
export KC_HOSTNAME_STRICT=false

echo KEYCLOAK_ADMIN="${IO_AVSTATS_KEYCLOAK_ADMIN}"

docker create -e        KEYCLOAK_ADMIN="${IO_AVSTATS_KEYCLOAK_USER_ADMIN}" \
              -e        KEYCLOAK_ADMIN_PASSWORD="${IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN}" \
              --name    "${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}" \
              -p        "${IO_AVSTATS_KEYCLOAK_CONNECTION_PORT}":"${IO_AVSTATS_KEYCLOAK_CONTAINER_PORT}" \
              --restart always \
              quay.io/keycloak/keycloak:"${IO_AVSTATS_KEYCLOAK_VERSION}" \
              start-dev

echo "Docker start ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME} (Keycloak ${IO_AVSTATS_KEYCLOAK_VERSION}) ..."
if ! docker start "${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}"; then
    exit 255
fi

sleep 30

end=$(date +%s)
echo "DOCKER Keycloak was ready in $((end - start)) seconds"

docker ps

echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
