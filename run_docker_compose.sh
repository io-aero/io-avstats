#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_docker_compose.sh: Create a multi-container Docker application.
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
export IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008=8501
export IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008=8502

echo ""
echo "Script $0 is now running"

export LOG_FILE=run_docker_compose.log

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

echo "Create a multi-container Docker application"

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
echo "STREAMLIT_SRRVER_PORT_faaus2008 : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008}"
echo "STREAMLIT_SERVER_PORT_pdus2008  : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

echo "Docker Containers ........................................... before containers:"
docker ps -a
docker ps       | find "${IO_AVSTATS_POSTGRES_CONTAINER_NAME}" && docker stop ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}
docker ps -a    | find "${IO_AVSTATS_POSTGRES_CONTAINER_NAME}" && docker rm --force ${IO_AVSTATS_POSTGRES_CONTAINER_NAME}
docker ps       | find "faaus2008"                             && docker stop faaus2008
docker ps -a    | find "faaus2008"                             && docker rm --force faaus2008
docker ps       | find "pdus2008"                              && docker stop pdus2008
docker ps -a    | find "pdus2008"                              && docker rm --force pdus2008
echo "............................................................. after containers:"
docker ps -a
echo "............................................................. before images:"
docker image ls
docker image ls | find "${IO_AVSTATS_POSTGRES_DBNAME_ADMIN}" && docker rmi --force ${IO_AVSTATS_POSTGRES_DBNAME_ADMIN}
docker image ls | find "faaus2008"                           && docker rmi --force ioaero/faaus2008
docker image ls | find "pdus2008"                            && docker rmi --force ioaero/pdus2008
echo "............................................................. after images:"
docker image ls

docker compose up

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
