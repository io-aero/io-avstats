@echo off

rem ----------------------------------------------------------------------------
rem
rem run_docker_compose.bat: Manage a multi-container Docker application (Cloud).
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set ERRORLEVEL=

set IO_AVSTATS_KEYCLOAK_CONNECTION_PORT=8080
set IO_AVSTATS_KEYCLOAK_CONTAINER_NAME=keycloak
set IO_AVSTATS_KEYCLOAK_CONTAINER_PORT=8080
set IO_AVSTATS_KEYCLOAK_PASSWORD=RsxAG^&hpCcuXsB2cbxSS
set IO_AVSTATS_KEYCLOAK_USER=admin
set IO_AVSTATS_KEYCLOAK_VERSION=latest

set IO_AVSTATS_NGINX_CONNECTION_PORT=8080
set IO_AVSTATS_NGINX_CONTAINER_PORT=8080

set IO_AVSTATS_POSTGRES_CONNECTION_PORT=5442
set IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
set IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
set IO_AVSTATS_POSTGRES_DBNAME=postgres
set IO_AVSTATS_POSTGRES_PASSWORD=V3s8m4x*MYbHrX*UuU6X
set IO_AVSTATS_POSTGRES_PGDATA=data/postgres
set IO_AVSTATS_POSTGRES_USER=guest
set IO_AVSTATS_POSTGRES_VERSION=latest

set IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT=5432
set IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME=keycloak_db
set IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT=5432
set IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME=postgres
set IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD=twAuk3VM2swt#Z96#zM#
set IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA=data/postgres_keycloak
set IO_AVSTATS_POSTGRES_KEYCLOAK_USER=postgres

set IO_AVSTATS_STREAMLIT_SERVER_PORT=8501

set IO_AVSTATS_COMPOSE_TASK=
set IO_AVSTATS_COMPOSE_TASK_DEFAULT=logs
set IO_AVSTATS_CONTAINER=
set IO_AVSTATS_CONTAINER_DEFAULT=*

if ["%1"] EQU [""] (
    echo =========================================================
    echo clean - Remove all containers and images
    echo down  - Stop  Docker Compose
    echo logs  - Fetch the logs of a container
    echo up    - Start Docker Compose
    echo ---------------------------------------------------------
    set /P IO_AVSTATS_COMPOSE_TASK="Enter the desired task [default: %IO_AVSTATS_COMPOSE_TASK_DEFAULT%] "

    if ["!IO_AVSTATS_COMPOSE_TASK!"] EQU [""] (
        set IO_AVSTATS_COMPOSE_TASK=%IO_AVSTATS_COMPOSE_TASK_DEFAULT%
    )
) else (
    set IO_AVSTATS_COMPOSE_TASK=%1
)

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["logs"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo *             - All Containers
        echo ae1982        - Aviation Event Analysis
        echo io_avstats_db - Database Profiling
        echo keycloak      - Keycloak Server
        echo keycloak_db   - Keycloak Database
        echo members       - IO-Aero Member Service
        echo pd1982        - Database Profiling
        echo slara         - Association Rule Analysis
        echo stats         - US Aviation Fatal Accidents
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_CONTAINER="Enter the desired container [default: %IO_AVSTATS_CONTAINER_DEFAULT%] "

        if ["!IO_AVSTATS_CONTAINER!"] EQU [""] (
            set IO_AVSTATS_CONTAINER=%IO_AVSTATS_CONTAINER_DEFAULT%
        )
    ) else (
        set IO_AVSTATS_CONTAINER=%2
    )
)

echo =======================================================================
echo Start %0
echo -----------------------------------------------------------------------
echo Manage a multi-container Docker application
echo -----------------------------------------------------------------------
echo COMPOSE_TASK                      : %IO_AVSTATS_COMPOSE_TASK%
echo CONTAINER                         : %IO_AVSTATS_CONTAINER%
echo -----------------------------------------------------------------------
echo KEYCLOAK_CONTAINER_NAME           : %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
echo KEYCLOAK_PASSWORD                 : "%IO_AVSTATS_KEYCLOAK_PASSWORD%"
echo KEYCLOAK_USER                     : %IO_AVSTATS_KEYCLOAK_USER%
echo KEYCLOAK_VERSION                  : %IO_AVSTATS_KEYCLOAK_VERSION%
echo -----------------------------------------------------------------------
echo NGINX_CONNECTION_PORT             : %IO_AVSTATS_NGINX_CONNECTION_PORT%
echo NGINX_CONTAINER_PORT              : %IO_AVSTATS_NGINX_CONTAINER_PORT%
echo -----------------------------------------------------------------------
echo POSTGRES_CONNECTION_PORT          : %IO_AVSTATS_POSTGRES_CONNECTION_PORT%
echo POSTGRES_CONTAINER_NAME           : %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
echo POSTGRES_CONTAINER_PORT           : %IO_AVSTATS_POSTGRES_CONTAINER_PORT%
echo POSTGRES_DBNAME                   : %IO_AVSTATS_POSTGRES_DBNAME%
echo POSTGRES_PASSWORD                 : %IO_AVSTATS_POSTGRES_PASSWORD%
echo POSTGRES_PGDATA                   : %IO_AVSTATS_POSTGRES_PGDATA%
echo POSTGRES_USER                     : %IO_AVSTATS_POSTGRES_USER%
echo POSTGRES_VERSION                  : %IO_AVSTATS_POSTGRES_VERSION%
echo -----------------------------------------------------------------------
echo POSTGRES_KEYCLOAK_CONNECTION_PORT : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT%
echo POSTGRES_KEYCLOAK_CONTAINER_NAME  : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
echo POSTGRES_KEYCLOAK_CONTAINER_PORT  : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT%
echo POSTGRES_KEYCLOAK_DBNAME          : %IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME%
echo POSTGRES_KEYCLOAK_PASSWORD        : %IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD%
echo POSTGRES_KEYCLOAK_PGDATA          : %IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA%
echo POSTGRES_KEYCLOAK_USER            : %IO_AVSTATS_POSTGRES_KEYCLOAK_USER%
echo STREAMLIT_SERVER_PORT             : %IO_AVSTATS_STREAMLIT_SERVER_PORT%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["clean"] (
    echo Docker Containers .......................... before containers running:
    docker ps
    echo Docker Containers .................................. before containers:
    docker ps -a
    docker ps       | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker stop        %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker rm  --force %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps       | find "load_balancer"                                 && docker stop        load_balancer
    docker ps -a    | find "load_balancer"                                 && docker rm  --force load_balancer
    docker ps       | find "members"                                       && docker stop        members
    docker ps -a    | find "members"                                       && docker rm  --force members
    docker ps       | find "pd1982"                                        && docker stop        pd1982
    docker ps -a    | find "pd1982"                                        && docker rm  --force pd1982
    docker ps       | find "slara"                                         && docker stop        slara
    docker ps -a    | find "slara"                                         && docker rm  --force slara
    docker ps       | find "stats"                                         && docker stop        stats
    docker ps -a    | find "stats"                                         && docker rm  --force stats
    echo ............................................. after containers running:
    docker ps
    echo ..................................................... after containers:
    docker ps -a
    echo ........................................................ before images:
    docker images
    docker image ls | find "ae1982"                    && docker rmi --force ioaero/ae1982:latest
    docker image ls | find "members"                   && docker rmi --force ioaero/members:latest
    docker image ls | find "nginx"                     && docker rmi --force nginx:stable-alpine
    docker image ls | find "pd1982"                    && docker rmi --force ioaero/pd1982:latest
    docker image ls | find "postgres"                  && docker rmi --force postgres:%IO_AVSTATS_POSTGRES_VERSION%
    docker image ls | find "quay.io/keycloak/keycloak" && docker rmi --force quay.io/keycloak/keycloak:%IO_AVSTATS_KEYCLOAK_VERSION%
    docker image ls | find "slara"                     && docker rmi --force ioaero/slara:latest
    docker image ls | find "stats"                     && docker rmi --force ioaero/stats:latest
    echo ......................................................... after images:
    docker images
    goto END_OF_SCRIPT
)

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["down"] (
    echo Docker Containers .......................... before containers running:
    docker ps
    echo Docker Containers .................................. before containers:
    docker ps -a

    docker compose -f config/docker-compose_cloud.yml down

    echo ............................................. after containers running:
    docker ps
    echo ..................................................... after containers:
    docker ps -a
    goto END_OF_SCRIPT
)

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["logs"] (
    if ["%IO_AVSTATS_CONTAINER%"] EQU ["*"] (
        docker-compose -f config/docker-compose_cloud.yml logs --tail=0 --follow
    ) else (
        docker-compose -f config/docker-compose_cloud.yml logs --tail=0 --follow %IO_AVSTATS_CONTAINER%
    )
)

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["up"] (
    echo Docker Containers .......................... before containers running:
    docker ps
    echo Docker Containers .................................. before containers:
    docker ps -a
    echo ........................................................ before images:
    docker images

    start /B docker compose -f config/docker-compose_cloud.yml up
    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Program abort due to wrong input.
rem ----------------------------------------------------------------------------

echo Processing of the script run_io_avstats is aborted: unknown task='%IO_AVSTATS_COMPOSE_TASK%'
exit 1

:END_OF_SCRIPT
echo.
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================
