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
echo "KEYCLOAK_PASSWORD_ADMIN           : ${IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN%}"
echo "KEYCLOAK_USER_ADMIN               : ${IO_AVSTATS_KEYCLOAK_USER_ADMIN}"
echo "KEYCLOAK_VERSION                  : ${IO_AVSTATS_KEYCLOAK_VERSION}"
echo "POSTGRES_KEYCLOAK_CONNECTION_PORT : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT}"
echo "POSTGRES_KEYCLOAK_CONTAINER_NAME  : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}"
echo "POSTGRES_KEYCLOAK_DBNAME_ADMIN    : ${IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN}"
echo "POSTGRES_KEYCLOAK_PASSWORD_ADMIN  : ${IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN}"
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

echo "--------------------------------------------------------------------------------"
echo "Docker create ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME} (Keycloak ${IO_AVSTATS_KEYCLOAK_VERSION})"

export KC_HTTP_ENABLED=true
export KC_HTTP_HOST=0.0.0.0
export KC_HTTPS_CLIENT_AUTH=none
export KC_HOSTNAME_STRICT=false
export KC_HOSTNAME_URL=http://auth.io-aero.com:8080/
export KC_DB=postgres
export KC_DB_URL_HOST="${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}"
export KC_DB_URL_PORT="${IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT}"
export KC_DB_URL_DATABASE="${IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN}"
export KC_DB_USERNAME="${IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN}"
export KC_DB_PASSWORD="${IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN}"
export KC_PROXY=edge

echo "================================================================================"
echo "KC_HTTP_ENABLED                   : ${KC_HTTP_ENABLED}"
echo "KC_HTTP_HOST                      : ${KC_HTTP_HOST}"
echo "KC_HTTPS_CLIENT_AUTH              : ${KC_HTTPS_CLIENT_AUTH}"
echo "KC_HOSTNAME_STRICT                : ${KC_HOSTNAME_STRICT}"
echo "KC_HOSTNAME_URL                   : ${KC_HOSTNAME_URL}"
echo "KC_DB                             : ${KC_DB}"
echo "KC_DB_URL_HOST                    : ${KC_DB_URL_HOST}"
echo "KC_DB_URL_PORT                    : ${KC_DB_URL_PORT}"
echo "KC_DB_URL_DATABASE                : ${KC_DB_URL_DATABASE}"
echo "KC_DB_USERNAME                    : ${KC_DB_USERNAME}"
echo "KC_DB_PASSWORD                    : ${KC_DB_PASSWORD}"
echo "KC_PROXY                          : ${KC_PROXY}"
echo "================================================================================"

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
