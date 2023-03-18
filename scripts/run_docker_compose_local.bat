@echo off

rem ----------------------------------------------------------------------------
rem
rem run_docker_compose.bat: Manage a multi-container Docker application (Local).
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set ERRORLEVEL=

set IO_AVSTATS_KEYCLOAK_CONNECTION_PORT=8080
set IO_AVSTATS_KEYCLOAK_CONTAINER_NAME=keycloak
set IO_AVSTATS_KEYCLOAK_CONTAINER_PORT=8080
set IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN="RsxAG^&hpCcuXsB2cbxSS"
set IO_AVSTATS_KEYCLOAK_USER_ADMIN=admin
set IO_AVSTATS_KEYCLOAK_VERSION=21.0.1

set IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
set IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
set IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
set IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres

set IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT=5442
set IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME=keycloak_db
set IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT=5432
set IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN=postgres
set IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN="twAuk3VM2swt#Z96#zM#"
set IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA=data/postgres_keycloak
set IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN=postgres

set IO_AVSTATS_POSTGRES_PASSWORD_ADMIN="V3s8m4x*MYbHrX*UuU6X"
set IO_AVSTATS_POSTGRES_PGDATA=data/postgres
set IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
set IO_AVSTATS_POSTGRES_USER_GUEST=guest
set IO_AVSTATS_POSTGRES_VERSION=latest

set IO_AVSTATS_CONTAINER=
set IO_AVSTATS_CONTAINER_DEFAULT=*
set IO_AVSTATS_COMPOSE_TASK=
set IO_AVSTATS_COMPOSE_TASK_DEFAULT=up

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
echo KEYCLOAK_CONNECTION_PORT          : %IO_AVSTATS_KEYCLOAK_CONNECTION_PORT%
echo KEYCLOAK_CONTAINER_NAME           : %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
echo KEYCLOAK_CONTAINER_PORT           : %IO_AVSTATS_KEYCLOAK_CONTAINER_PORT%
echo KEYCLOAK_PASSWORD_ADMIN           : %IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN%
echo KEYCLOAK_USER_ADMIN               : %IO_AVSTATS_KEYCLOAK_USER_ADMIN%
echo KEYCLOAK_VERSION                  : %IO_AVSTATS_KEYCLOAK_VERSION%
echo POSTGRES_CONNECTION_PORT          : %IO_AVSTATS_POSTGRES_CONNECTION_PORT%
echo POSTGRES_CONTAINER_NAME           : %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
echo POSTGRES_CONTAINER_PORT           : %IO_AVSTATS_POSTGRES_CONTAINER_PORT%
echo POSTGRES_DBNAME_ADMIN             : %IO_AVSTATS_POSTGRES_DBNAME_ADMIN%
echo POSTGRES_PASSWORD_ADMIN           : %IO_AVSTATS_POSTGRES_PASSWORD_ADMIN%
echo POSTGRES_PGDATA                   : %IO_AVSTATS_POSTGRES_PGDATA%
echo POSTGRES_USER_ADMIN               : %IO_AVSTATS_POSTGRES_USER_ADMIN%
echo POSTGRES_VERSION                  : %IO_AVSTATS_POSTGRES_VERSION%
echo POSTGRES_KEYCLOAK_CONNECTION_PORT : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT%
echo POSTGRES_KEYCLOAK_CONTAINER_NAME  : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
echo POSTGRES_KEYCLOAK_CONTAINER_PORT  : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT%
echo POSTGRES_KEYCLOAK_DBNAME_ADMIN    : %IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN%
echo POSTGRES_KEYCLOAK_PASSWORD_ADMIN  : %IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN%
echo POSTGRES_KEYCLOAK_PGDATA          : %IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA%
echo POSTGRES_KEYCLOAK_USER_ADMIN      : %IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["clean"] (
    echo Docker Containers ........................................... before containers:
    docker ps
    docker ps -a
    docker ps       | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker stop        %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker rm  --force %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    echo ............................................................. after containers:
    docker ps
    docker ps -a
    echo ............................................................. before images:
    docker images
    docker image ls | find "postgres"                  && docker rmi --force postgres:%IO_AVSTATS_POSTGRES_VERSION%
    docker image ls | find "quay.io/keycloak/keycloak" && docker rmi --force quay.io/keycloak/keycloak:%IO_AVSTATS_KEYCLOAK_VERSION%
    echo ............................................................. after images:
    docker images
    goto END_OF_SCRIPT
)

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["down"] (
    docker compose -f docker-compose_local.yml down

    echo ............................................................. after containers:
    docker ps
    docker ps -a
    echo ............................................................. after images:
    docker images
    goto END_OF_SCRIPT
)

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["logs"] (
    if ["%IO_AVSTATS_CONTAINER%"] EQU ["*"] (
        docker-compose -f docker-compose_local.yml logs --tail=0 --follow
    ) else (
        docker-compose -f docker-compose_local.yml logs --tail=0 --follow %IO_AVSTATS_CONTAINER%
    )
)

if ["%IO_AVSTATS_COMPOSE_TASK%"] EQU ["up"] (
    echo Docker Containers ........................................... before containers:
    docker ps
    docker ps -a
    echo ............................................................. before images:
    docker images

    start /B docker compose -f docker-compose_local.yml up
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
