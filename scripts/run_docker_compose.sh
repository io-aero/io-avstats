#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_docker_compose.sh: Manage a multi-container Docker application.
#
# ------------------------------------------------------------------------------

export IO_AVSTATS_KEYCLOAK_CONNECTION_PORT=8080
export IO_AVSTATS_KEYCLOAK_CONTAINER_NAME=keycloak
export IO_AVSTATS_KEYCLOAK_CONTAINER_PORT=8080
export IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN="RsxAG&hpCcuXsB2cbxSS"
export IO_AVSTATS_KEYCLOAK_USER_ADMIN=admin
export IO_AVSTATS_KEYCLOAK_VERSION=latest

export IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
export IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
export IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
export IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres

export IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT=5442
export IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME=keycloak_db
export IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT=5432
export IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN=postgres
export IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN="twAuk3VM2swt#Z96#zM#"
export IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA=data/postgres_keycloak
export IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN=postgres

export IO_AVSTATS_POSTGRES_PASSWORD_ADMIN="V3s8m4x*MYbHrX*UuU6X"
export IO_AVSTATS_POSTGRES_PGDATA=data/postgres
export IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
export IO_AVSTATS_POSTGRES_USER_GUEST=guest
export IO_AVSTATS_POSTGRES_VERSION=latest

export IO_AVSTATS_STREAMLIT_SERVER_PORT=8501
export IO_AVSTATS_STREAMLIT_SERVER_PORT_AE1982=8501
export IO_AVSTATS_STREAMLIT_SERVER_PORT_MEMBERS=8598
export IO_AVSTATS_STREAMLIT_SERVER_PORT_PD1982=8502
export IO_AVSTATS_STREAMLIT_SERVER_PORT_SLARA=8503
export IO_AVSTATS_STREAMLIT_SERVER_PORT_STATS=8599

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
echo TASK                          : %IO_AVSTATS_TASK%
echo "--------------------------------------------------------------------------------"
echo "KEYCLOAK_CONNECTION_PORT          : ${IO_AVSTATS_KEYCLOAK_CONNECTION_PORT}"
echo "KEYCLOAK_CONTAINER_NAME           : ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}"
echo "KEYCLOAK_CONTAINER_PORT           : ${IO_AVSTATS_KEYCLOAK_CONTAINER_PORT}"
echo "KEYCLOAK_PASSWORD_ADMIN           : ${IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN}"
echo "KEYCLOAK_USER_ADMIN               : ${IO_AVSTATS_KEYCLOAK_USER_ADMIN}"
echo "KEYCLOAK_VERSION                  : ${IO_AVSTATS_KEYCLOAK_VERSION}"
echo "POSTGRES_CONNECTION_PORT          : ${IO_AVSTATS_POSTGRES_CONNECTION_PORT}"
echo "POSTGRES_CONTAINER_NAME           : ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}"
echo "POSTGRES_CONTAINER_PORT           : ${IO_AVSTATS_POSTGRES_CONTAINER_PORT}"
echo "POSTGRES_DBNAME_ADMIN             : ${IO_AVSTATS_POSTGRES_DBNAME_ADMIN}"
echo "POSTGRES_PASSWORD_ADMIN           : ${IO_AVSTATS_POSTGRES_PASSWORD_ADMIN}"
echo "POSTGRES_PGDATA                   : ${IO_AVSTATS_POSTGRES_PGDATA}"
echo "POSTGRES_USER_ADMIN               : ${IO_AVSTATS_POSTGRES_USER_ADMIN}"
echo "POSTGRES_VERSION                  : ${IO_AVSTATS_POSTGRES_VERSION}"
echo "POSTGRES_KEYCLOAK_CONNECTION_PORT : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT}"
echo "POSTGRES_KEYCLOAK_CONTAINER_NAME  : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}"
echo "POSTGRES_KEYCLOAK_CONTAINER_PORT  : ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT}"
echo "POSTGRES_KEYCLOAK_DBNAME_ADMIN    : ${IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN}"
echo "POSTGRES_KEYCLOAK_PASSWORD_ADMIN  : ${IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN}"
echo "POSTGRES_KEYCLOAK_PGDATA          : ${IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA}"
echo "POSTGRES_KEYCLOAK_USER_ADMIN      : ${IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN}"
echo "STREAMLIT_SERVER_PORT             : ${IO_AVSTATS_STREAMLIT_SERVER_PORT}"
echo "STREAMLIT_SERVER_PORT_AE1982      : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_AE1982}"
echo "STREAMLIT_SERVER_PORT_MEMBERS     : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_MEMBERS}"
echo "STREAMLIT_SERVER_PORT_PD1982      : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_PD1982}"
echo "STREAMLIT_SERVER_PORT_SLARA       : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_SLARA}"
echo "STREAMLIT_SERVER_PORT_STATS       : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_STATS}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

# ------------------------------------------------------------------------------
# Stop Docker Compose.
# ------------------------------------------------------------------------------
if [ "${IO_AVSTATS_TASK}" = "clean" ]; then
    echo "............................................................. before containers:"
    docker ps
    docker ps -a
    docker ps -q --filter "name=${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}"          | grep -q . && docker stop ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}          && docker rm -fv ${IO_AVSTATS_KEYCLOAK_CONTAINER_NAME}
    docker ps -q --filter "name=${IO_AVSTATS_POSTGRES_CONTAINER_NAME}"          | grep -q . && docker stop ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}          && docker rm -fv ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}
    docker ps -q --filter "name=${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}" | grep -q . && docker stop ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME} && docker rm -fv ${IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME}
    docker ps -q --filter "name=ae1982"                                         | grep -q . && docker stop ae1982                                         && docker rm -fv ae1982
    docker ps -q --filter "name=load_balancer"                                  | grep -q . && docker stop load_balancer                                  && docker rm -fv load_balancer
    docker ps -q --filter "name=members"                                        | grep -q . && docker stop members                                        && docker rm -fv members
    docker ps -q --filter "name=pd1982"                                         | grep -q . && docker stop pd1982                                         && docker rm -fv pd1982
    docker ps -q --filter "name=slara"                                          | grep -q . && docker stop slara                                          && docker rm -fv slara
    docker ps -q --filter "name=stats"                                          | grep -q . && docker stop stats                                          && docker rm -fv stats
    echo "............................................................ after containers:"
    docker ps
    docker ps -a
    echo "............................................................ before images:"
    docker images
    docker images -q --filter "reference=ioaero/ae1982:latest"                                     | grep -q . && docker rmi --force ioaero/ae1982:latest
    docker images -q --filter "reference=ioaero/members:latest"                                    | grep -q . && docker rmi --force ioaero/members:latest
    docker images -q --filter "reference=ioaero/pd1982:latest"                                     | grep -q . && docker rmi --force ioaero/pd1982:latest
    docker images -q --filter "reference=ioaero/slara:latest"                                      | grep -q . && docker rmi --force ioaero/slara:latest
    docker images -q --filter "reference=ioaero/stats:latest"                                      | grep -q . && docker rmi --force ioaero/stats:latest
    docker images -q --filter "reference=nginx:alpine"                                             | grep -q . && docker rmi --force nginx:alpine
    docker images -q --filter "reference=postgres:${IO_AVSTATS_POSTGRES_VERSION}"                  | grep -q . && docker rmi --force postgres:"${IO_AVSTATS_POSTGRES_VERSION}"
    docker images -q --filter "reference=quay.io/keycloak/keycloak:${IO_AVSTATS_KEYCLOAK_VERSION}" | grep -q . && docker rmi --force quay.io/keycloak/keycloak:"${IO_AVSTATS_KEYCLOAK_VERSION}"
    echo "............................................................ after images:"
    docker images

# ------------------------------------------------------------------------------
# Stop Docker Compose.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "down" ]; then
    docker-compose down

    echo "............................................................ after containers:"
    docker ps
    docker ps -a
    echo "............................................................ after images:"
    docker images

# ------------------------------------------------------------------------------
# Start Docker Compose.
# ------------------------------------------------------------------------------
elif [ "${IO_AVSTATS_TASK}" = "up" ]; then
    echo "............................................................ before containers:"
    docker ps
    docker ps -a
    echo "............................................................ before images:"
    docker images

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
