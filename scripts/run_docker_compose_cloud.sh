#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_docker_compose_cloud.sh: Manage a multi-container Docker application (Cloud).
#
# ------------------------------------------------------------------------------

export IO_AERO_NGINX_CONNECTION_PORT=80

export IO_AERO_POSTGRES_CONNECTION_PORT=5432
export IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db
export IO_AERO_POSTGRES_DBNAME=postgres
export IO_AERO_POSTGRES_PASSWORD="V3s8m4x*MYbHrX*UuU6X"
export IO_AERO_POSTGRES_PGDATA=data/postgres
export IO_AERO_POSTGRES_USER=guest

if [ -z "${IO_AERO_POSTGRES_VERSION}" ]; then
    export IO_AERO_POSTGRES_VERSION=latest
fi

export IO_AERO_STREAMLIT_SERVER_PORT=8501

export IO_AERO_COMPOSE_TASK=
export IO_AERO_COMPOSE_TASK_DEFAULT=logs
export IO_AERO_CONTAINER=
export IO_AERO_CONTAINER_DEFAULT="*"

if [ -z "$1" ]; then
    echo "========================================================="
    echo "clean - Remove all containers and images"
    echo "down  - Stop  Docker Compose"
    echo "logs  - Fetch the logs of a container"
    echo "up    - Start Docker Compose"
    echo "---------------------------------------------------------"
    # shellcheck disable=SC2162
    read -p "Enter the desired task [default: ${IO_AERO_COMPOSE_TASK_DEFAULT}] " IO_AERO_COMPOSE_TASK
    export IO_AERO_COMPOSE_TASK=${IO_AERO_COMPOSE_TASK}

    if [ -z "${IO_AERO_COMPOSE_TASK}" ]; then
        export IO_AERO_COMPOSE_TASK=${IO_AERO_COMPOSE_TASK_DEFAULT}
    fi
else
    export IO_AERO_COMPOSE_TASK=$1
fi

if [ "${IO_AERO_COMPOSE_TASK}" = "logs" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        echo "*             - All Containers"
        echo "ae1982        - Aviation Event Analysis"
        echo "io_avstats_db - Database Profiling"
        echo "pd1982        - Database Profiling"
        echo "slara         - Association Rule Analysis"
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the desired container [default: ${IO_AERO_CONTAINER_DEFAULT}] " IO_AERO_CONTAINER
        export IO_AERO_CONTAINER=${IO_AERO_CONTAINER}

        if [ -z "${IO_AERO_CONTAINER}" ]; then
            export IO_AERO_CONTAINER=${IO_AERO_CONTAINER_DEFAULT}
        fi
    else
        export IO_AERO_CONTAINER=$2
  fi
fi

echo ""
echo "Script $0 is now running"

now=$(date +"%Y_%m_%d")
export LOG_FILE=run_docker_compose.log

echo ""
echo "You can find the run log in the file ${LOG_FILE}"
echo ""
echo "Please wait ..."
echo ""

exec &>> >(tee -a -i "${LOG_FILE}") 2>&1
sleep .1

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "Manage a multi-container Docker application"
echo "--------------------------------------------------------------------------------"
echo "COMPOSE_TASK                      : ${IO_AERO_COMPOSE_TASK}"
echo "CONTAINER                         : ${IO_AERO_CONTAINER}"
echo "--------------------------------------------------------------------------------"
echo "NGINX_CONNECTION_PORT             : ${IO_AERO_NGINX_CONNECTION_PORT}"
echo "--------------------------------------------------------------------------------"
echo "POSTGRES_CONNECTION_PORT          : ${IO_AERO_POSTGRES_CONNECTION_PORT}"
echo "POSTGRES_CONTAINER_NAME           : ${IO_AERO_POSTGRES_CONTAINER_NAME}"
echo "POSTGRES_DBNAME                   : ${IO_AERO_POSTGRES_DBNAME}"
echo "POSTGRES_PASSWORD                 : ${IO_AERO_POSTGRES_PASSWORD}"
echo "POSTGRES_PGDATA                   : ${IO_AERO_POSTGRES_PGDATA}"
echo "POSTGRES_USER                     : ${IO_AERO_POSTGRES_USER}"
echo "--------------------------------------------------------------------------------"
echo "POSTGRES_VERSION                  : ${IO_AERO_POSTGRES_VERSION}"
echo "--------------------------------------------------------------------------------"
echo "STREAMLIT_SERVER_PORT             : ${IO_AERO_STREAMLIT_SERVER_PORT}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

# ------------------------------------------------------------------------------
# Remove all containers and images.
# ------------------------------------------------------------------------------
if [ "${IO_AERO_COMPOSE_TASK}" = "clean" ]; then
    echo "........................................... before containers running:"
    docker ps
    echo "................................................... before containers:"
    docker ps -a
    docker ps -q --filter "name=${IO_AERO_POSTGRES_CONTAINER_NAME}" | grep -q . && docker stop ${IO_AERO_POSTGRES_CONTAINER_NAME} && docker rm -fv ${IO_AERO_POSTGRES_CONTAINER_NAME}
    docker ps -q --filter "name=ae1982"                             | grep -q . && docker stop ae1982                             && docker rm -fv ae1982
    docker ps -q --filter "name=load_balancer"                      | grep -q . && docker stop load_balancer                      && docker rm -fv load_balancer
    docker ps -q --filter "name=pd1982"                             | grep -q . && docker stop pd1982                             && docker rm -fv pd1982
    docker ps -q --filter "name=portainer"                          | grep -q . && docker stop portainer                          && docker rm -fv portainer
    docker ps -q --filter "name=slara"                              | grep -q . && docker stop slara                              && docker rm -fv slara
    echo "............................................ after containers running:"
    docker ps
    echo ".................................................... after containers:"
    docker ps
    docker ps -a
    echo "....................................................... before images:"
    docker images
    docker images -q --filter "reference=ioaero/ae1982:latest"                 | grep -q . && docker rmi --force ioaero/ae1982:latest
    docker images -q --filter "reference=ioaero/pd1982:latest"                 | grep -q . && docker rmi --force ioaero/pd1982:latest
    docker images -q --filter "reference=ioaero/slara:latest"                  | grep -q . && docker rmi --force ioaero/slara:latest
    docker images -q --filter "reference=nginx:stable-alpine"                  | grep -q . && docker rmi --force nginx:stable-alpine
    docker images -q --filter "reference=portainer/portainer-ce"               | grep -q . && docker rmi --force portainer/portainer-ce:latest
    docker images -q --filter "reference=postgres:${IO_AERO_POSTGRES_VERSION}" | grep -q . && docker rmi --force postgres:"${IO_AERO_POSTGRES_VERSION}"
    echo "........................................................ after images:"
    docker images

# ------------------------------------------------------------------------------
# Stop Docker Compose.
# ------------------------------------------------------------------------------
elif [ "${IO_AERO_COMPOSE_TASK}" = "down" ]; then
    echo "........................................... before containers running:"
    docker ps
    echo "................................................... before containers:"
    docker ps -a

    docker compose -f docker-compose_cloud.yml down

    echo "............................................ after containers running:"
    docker ps
    echo ".................................................... after containers:"
    docker ps
    docker images

    now=$(date +"%Y.%m.%d")

# ------------------------------------------------------------------------------
# View Container Output.
# ------------------------------------------------------------------------------
elif [ "${IO_AERO_COMPOSE_TASK}" = "logs" ]; then
    if [ "${IO_AERO_CONTAINER}" = "*" ]; then
        docker compose -f docker-compose_cloud.yml logs --tail=0 --follow
    else
        docker compose -f docker-compose_cloud.yml logs --tail=0 --follow "${IO_AERO_CONTAINER}"
    fi

# ------------------------------------------------------------------------------
# Start Docker Compose.
# ------------------------------------------------------------------------------
elif [ "${IO_AERO_COMPOSE_TASK}" = "up" ]; then
    echo "........................................... before containers running:"
    docker ps
    echo "................................................... before containers:"
    docker ps -a
    echo "....................................................... before images:"
    docker images

    docker compose -f docker-compose_cloud.yml up --quiet-pull &

# ------------------------------------------------------------------------------
# Program abort due to wrong input.
# ------------------------------------------------------------------------------

else
    echo "Processing of the script run_io_avstats is aborted: unknown task='${IO_AERO_COMPOSE_TASK}'"
    exit 255
fi

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
