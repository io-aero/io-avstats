#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_docker_compose.sh: Manage a multi-container Docker application.
#
# ------------------------------------------------------------------------------

export IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
export IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
export IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
export IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres
export IO_AVSTATS_POSTGRES_PASSWORD_ADMIN=postgresql
export IO_AVSTATS_POSTGRES_PGDATA=data/postgres
export IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
export IO_AVSTATS_POSTGRES_VERSION=latest
export IO_AVSTATS_STREAMLIT_SERVER_PORT=8501
export IO_AVSTATS_STREAMLIT_SERVER_PORT_AAUS1982=8501
export IO_AVSTATS_STREAMLIT_SERVER_PORT_PDUS1982=8502

export IO_AVSTATS_TASK=
export IO_AVSTATS_TASK_DEFAULT=up

if [ -z "$1" ]; then
    echo "========================================================="
    echo "clean - Remove all containers and images"
    echo "down  - Stop  Docker Compose"
    echo "up    - Start Docker Compose"
    echo "---------------------------------------------------------"
    # shellcheck disable=SC2162
    read -p "Enter the desired task [default: ${IO_AVSTATS_TASK_DEFAULT}] " IO_AVSTATS_TASK
    export IO_AVSTATS_TASK=${IO_AVSTATS_TASK}

    if [ -z "${IO_AVSTATS_TASK}" ]; then
        export IO_AVSTATS_TASK=${IO_AVSTATS_TASK_DEFAULT}
    fi
else
    export IO_AVSTATS_TASK=$1
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
echo TASK                            : %IO_AVSTATS_TASK%
echo "--------------------------------------------------------------------------------"
echo "POSTGRES_CONNECTION_PORT        : ${IO_AVSTATS_POSTGRES_CONNECTION_PORT}"
echo "POSTGRES_CONTAINER_NAME         : ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}"
echo "POSTGRES_CONTAINER_NAME         : ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}"
echo "POSTGRES_CONTAINER_PORT         : ${IO_AVSTATS_POSTGRES_CONTAINER_PORT}"
echo "POSTGRES_DBNAME_ADMIN           : ${IO_AVSTATS_POSTGRES_DBNAME_ADMIN}"
echo "POSTGRES_PASSWORD_ADMIN         : ${IO_AVSTATS_POSTGRES_PASSWORD_ADMIN}"
echo "POSTGRES_PGDATA                 : ${IO_AVSTATS_POSTGRES_PGDATA}"
echo "POSTGRES_USER_ADMIN             : ${IO_AVSTATS_POSTGRES_USER_ADMIN}"
echo "POSTGRES_VERSION                : ${IO_AVSTATS_POSTGRES_VERSION}"
echo "STREAMLIT_SERVER_PORT           : ${IO_AVSTATS_STREAMLIT_SERVER_PORT}"
echo "STREAMLIT_SRRVER_PORT_AAUS1982  : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_AAUS1982}"
echo "STREAMLIT_SERVER_PORT_PDUS1982  : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_PDUS1982}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

# ------------------------------------------------------------------------------
# Stop Docker Compose.
# ------------------------------------------------------------------------------
if [ "${IO_AVSTATS_TASK}" = "clean" ]; then
    echo "Docker Containers ........................................... before containers:"
    docker ps -a
    docker ps -q --filter "name=${IO_AVSTATS_POSTGRES_CONTAINER_NAME}" | grep -q . && docker stop ${IO_AVSTATS_POSTGRES_CONTAINER_NAME} && docker rm -fv ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}
    docker ps -q --filter "name=ae1982"                              | grep -q . && docker stop ae1982                              && docker rm -fv ae1982
    docker ps -q --filter "name=pd1982"                              | grep -q . && docker stop pd1982                              && docker rm -fv pd1982
    echo ............................................................. after containers:
    docker ps -a
    echo ............................................................. before images:
    docker images
    docker images -q --filter "reference=postgres:latest"              | grep -q . && docker rmi --force postgres:latest
    docker images -q --filter "reference=ioaero/ae1982:latest"       | grep -q . && docker rmi --force ioaero/ae1982:latest
    docker images -q --filter "reference=ioaero/pd1982:latest"       | grep -q . && docker rmi --force ioaero/pd1982:latest
    echo ............................................................. after images:
    docker images

# ------------------------------------------------------------------------------
# Stop Docker Compose.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "down" ]; then
    docker-compose down

    echo "Docker Containers ........................................... before containers:"
    docker ps -a
    docker ps -q --filter "name=${IO_AVSTATS_POSTGRES_CONTAINER_NAME}" | grep -q . && docker stop ${IO_AVSTATS_POSTGRES_CONTAINER_NAME} && docker rm -fv ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}
    docker ps -q --filter "name=ae1982"                              | grep -q . && docker stop ae1982                              && docker rm -fv ae1982
    docker ps -q --filter "name=pd1982"                              | grep -q . && docker stop pd1982                              && docker rm -fv pd1982
    echo ............................................................. after containers:
    docker ps -a
    echo ............................................................. before images:
    docker images
    docker images -q --filter "reference=postgres:latest"              | grep -q . && docker rmi --force postgres:latest
    docker images -q --filter "reference=ioaero/ae1982:latest"       | grep -q . && docker rmi --force ioaero/ae1982:latest
    docker images -q --filter "reference=ioaero/pd1982:latest"       | grep -q . && docker rmi --force ioaero/pd1982:latest
    echo ............................................................. after images:
    docker images

# ------------------------------------------------------------------------------
# Start Docker Compose.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "up" ]; then
    echo "Docker Containers ........................................... before containers:"
    docker ps -a
    docker ps -q --filter "name=${IO_AVSTATS_POSTGRES_CONTAINER_NAME}" | grep -q . && docker stop ${IO_AVSTATS_POSTGRES_CONTAINER_NAME} && docker rm -fv ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}
    docker ps -q --filter "name=ae1982"                              | grep -q . && docker stop ae1982                              && docker rm -fv ae1982
    docker ps -q --filter "name=pd1982"                              | grep -q . && docker stop pd1982                              && docker rm -fv pd1982
    echo ............................................................. after containers:
    docker ps -a

    docker-compose up &

# ------------------------------------------------------------------------------
# Program abort due to wrong input.
# ------------------------------------------------------------------------------

else
    echo "Processing of the script run_io_avstats is aborted: unknown task='${IO_AVSTATS_TASK}'"
    exit 255
fi

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
