#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_docker_compose_cloud.sh: Manage a multi-container Docker application (Local).
#
# ------------------------------------------------------------------------------

export IO_AVSTATS_KEYCLOAK_CONNECTION_PORT=8080
export IO_AVSTATS_KEYCLOAK_CONTAINER_NAME=keycloak
export IO_AVSTATS_KEYCLOAK_CONTAINER_PORT=8080
export IO_AVSTATS_KEYCLOAK_PASSWORD="RsxAG&hpCcuXsB2cbxSS"
export IO_AVSTATS_KEYCLOAK_USER=admin
export IO_AVSTATS_KEYCLOAK_VERSION=latest

export IO_AVSTATS_POSTGRES_CONNECTION_PORT=5442
export IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
export IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
export IO_AVSTATS_POSTGRES_DBNAME=postgres
export IO_AVSTATS_POSTGRES_PASSWORD="V3s8m4x*MYbHrX*UuU6X"
export IO_AVSTATS_POSTGRES_PGDATA=data/postgres
export IO_AVSTATS_POSTGRES_USER=guest
export IO_AVSTATS_POSTGRES_VERSION=latest

export IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT=5432
export IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME=keycloak_db
export IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT=5432
export IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME=postgres
export IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD="twAuk3VM2swt#Z96#zM#"
export IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA=data/postgres_keycloak
export IO_AVSTATS_POSTGRES_KEYCLOAK_USER=postgres

export IO_AVSTATS_COMPOSE_TASK=
export IO_AVSTATS_COMPOSE_TASK_DEFAULT=logs
export IO_AVSTATS_CONTAINER=
export IO_AVSTATS_CONTAINER_DEFAULT="*"

if [ -z "$1" ]; then
    echo "========================================================="
    echo "clean - Remove all containers and images"
    echo "down  - Stop  Docker Compose"
    echo "logs  - Fetch the logs of a container"
    echo "up    - Start Docker Compose"
    echo "---------------------------------------------------------"
    # shellcheck disable=SC2162
    read -p "Enter the desired task [default: ${IO_AVSTATS_COMPOSE_TASK_DEFAULT}] " IO_AVSTATS_COMPOSE_TASK
    export IO_AVSTATS_COMPOSE_TASK=${IO_AVSTATS_COMPOSE_TASK}

    if [ -z "${IO_AVSTATS_COMPOSE_TASK}" ]; then
        export IO_AVSTATS_COMPOSE_TASK=${IO_AVSTATS_COMPOSE_TASK_DEFAULT}
    fi
else
    export IO_AVSTATS_COMPOSE_TASK=$1
fi

if [ "${IO_AVSTATS_COMPOSE_TASK}" = "logs" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        echo "*             - All Containers"
        echo "io_avstats_db - Database Profiling"
        echo "keycloak      - Keycloak Server"
        echo "keycloak_db   - Keycloak Database"
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the desired container [default: ${IO_AVSTATS_CONTAINER_DEFAULT}] " IO_AVSTATS_CONTAINER
        export IO_AVSTATS_CONTAINER=${IO_AVSTATS_CONTAINER}

        if [ -z "${IO_AVSTATS_CONTAINER}" ]; then
            export IO_AVSTATS_CONTAINER=${IO_AVSTATS_CONTAINER_DEFAULT}
        fi
    else
        export IO_AVSTATS_CONTAINER=$2
  fi
fi

echo ""
echo "Script $0 is now running"

now=$(date +"%Y_%m_%d")
export LOG_FILE=run_docker_compose_${now}.log

echo ""
echo "You can find the run log in the file ${LOG_FILE}"
echo ""
echo "Please wait ..."
echo ""

exec &> >(tee -i "${LOG_FILE}") 2>&1
sleep .1

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "Manage a multi-container Docker application"
echo "--------------------------------------------------------------------------------"
echo "COMPOSE_TASK                      : ${IO_AVSTATS_COMPOSE_TASK}"
echo "CONTAINER                         : ${IO_AVSTATS_CONTAINER}"
echo "--------------------------------------------------------------------------------"
echo "KEYCLOAK_CONNECTION_PORT          : ${IO_AVSTATS_KEYCLOAK_CONNECTION_PORT}"
echo "KEYCLOAK_CONTAINER_NAME           : ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}"
echo "KEYCLOAK_CONTAINER_PORT           : ${IO_AVSTATS_KEYCLOAK_CONTAINER_PORT}"
echo "KEYCLOAK_PASSWORD                 : ${IO_AVSTATS_KEYCLOAK_PASSWORD}"
echo "KEYCLOAK_USER                     : ${IO_AVSTATS_KEYCLOAK_USER}"
echo "KEYCLOAK_VERSION                  : ${IO_AVSTATS_KEYCLOAK_VERSION}"
echo "--------------------------------------------------------------------------------"
echo "POSTGRES_CONNECTION_PORT          : ${IO_AVSTATS_POSTGRES_CONNECTION_PORT}"
echo "POSTGRES_CONTAINER_NAME           : ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}"
echo "POSTGRES_CONTAINER_PORT           : ${IO_AVSTATS_POSTGRES_CONTAINER_PORT}"
echo "POSTGRES_DBNAME                   : ${IO_AVSTATS_POSTGRES_DBNAME}"
echo "POSTGRES_PASSWORD                 : ${IO_AVSTATS_POSTGRES_PASSWORD}"
echo "POSTGRES_PGDATA                   : ${IO_AVSTATS_POSTGRES_PGDATA}"
echo "POSTGRES_USER                     : ${IO_AVSTATS_POSTGRES_USER}"
echo "POSTGRES_VERSION                  : ${IO_AVSTATS_POSTGRES_VERSION}"
echo "--------------------------------------------------------------------------------"
echo "POSTGRES_KEYCLOAK_CONNECTION_PORT : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT}"
echo "POSTGRES_KEYCLOAK_CONTAINER_NAME  : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}"
echo "POSTGRES_KEYCLOAK_CONTAINER_PORT  : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT}"
echo "POSTGRES_KEYCLOAK_DBNAME          : ${IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME}"
echo "POSTGRES_KEYCLOAK_PASSWORD        : ${IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD}"
echo "POSTGRES_KEYCLOAK_PGDATA          : ${IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA}"
echo "POSTGRES_KEYCLOAK_USER            : ${IO_AVSTATS_POSTGRES_KEYCLOAK_USER}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

# ------------------------------------------------------------------------------
# Remove all containers and images.
# ------------------------------------------------------------------------------
if [ "${IO_AVSTATS_COMPOSE_TASK}" = "clean" ]; then
    echo "........................................... before containers running:"
    docker ps
    echo "................................................... before containers:"
    docker ps -a
    docker ps -q --filter "name=${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}"          | grep -q . && docker stop ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}          && docker rm -fv ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}
    docker ps -q --filter "name=${IO_AVSTATS_POSTGRES_CONTAINER_NAME}"          | grep -q . && docker stop ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}          && docker rm -fv ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}
    docker ps -q --filter "name=${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}" | grep -q . && docker stop ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME} && docker rm -fv ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}
    echo "............................................ after containers running:"
    docker ps
    echo ".................................................... after containers:"
    docker ps
    docker ps -a
    echo "....................................................... before images:"
    docker images
    docker images -q --filter "reference=postgres:${IO_AVSTATS_POSTGRES_VERSION}"                  | grep -q . && docker rmi --force postgres:"${IO_AVSTATS_POSTGRES_VERSION}"
    docker images -q --filter "reference=quay.io/keycloak/keycloak:${IO_AVSTATS_KEYCLOAK_VERSION}" | grep -q . && docker rmi --force quay.io/keycloak/keycloak:"${IO_AVSTATS_KEYCLOAK_VERSION}"
    echo "........................................................ after images:"
    docker images

# ------------------------------------------------------------------------------
# Stop Docker Compose.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_COMPOSE_TASK}" = "down" ]; then
    echo "........................................... before containers running:"
    docker ps
    echo "................................................... before containers:"
    docker ps -a

    docker-compose -f docker-compose_local.yml down

    echo "............................................ after containers running:"
    docker ps
    echo ".................................................... after containers:"
    docker ps
    docker images

# ------------------------------------------------------------------------------
# View Container Output.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_COMPOSE_TASK}" = "logs" ]; then
    if [ "${IO_AVSTATS_CONTAINER}" = "*" ]; then
        docker-compose -f docker-compose_local.yml logs --tail=0 --follow
    else
        docker-compose -f docker-compose_local.yml logs --tail=0 --follow "${IO_AVSTATS_CONTAINER}"
    fi

# ------------------------------------------------------------------------------
# Start Docker Compose.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_COMPOSE_TASK}" = "up" ]; then
    echo "........................................... before containers running:"
    docker ps
    echo "................................................... before containers:"
    docker ps -a
    echo "....................................................... before images:"
    docker images

    docker-compose -f docker-compose_local.yml up -d

# ------------------------------------------------------------------------------
# Program abort due to wrong input.
# ------------------------------------------------------------------------------

else
    echo "Processing of the script run_io_avstats is aborted: unknown task='${IO_AVSTATS_COMPOSE_TASK}'"
    exit 255
fi

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"