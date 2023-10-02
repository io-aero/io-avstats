@echo off

rem ----------------------------------------------------------------------------
rem
rem run_docker_compose.bat: Manage a multi-container Docker application (Local).
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set AWS_PROG_ZIP=7za

set ERRORLEVEL=

set IO_AERO_POSTGRES_CONNECTION_PORT=5432
set IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db
set IO_AERO_POSTGRES_DBNAME=postgres
set IO_AERO_POSTGRES_PASSWORD=V3s8m4x*MYbHrX*UuU6X
set IO_AERO_POSTGRES_PGDATA=data\postgres
set IO_AERO_POSTGRES_USER=guest

if ["%IO_AERO_POSTGRES_VERSION%"] EQU [""] (
    set IO_AERO_POSTGRES_VERSION=latest
)

set IO_AERO_COMPOSE_TASK=
set IO_AERO_COMPOSE_TASK_DEFAULT=logs
set IO_AERO_CONTAINER=
set IO_AERO_CONTAINER_DEFAULT=*

if ["%1"] EQU [""] (
    echo =========================================================
    echo clean - Remove all containers and images
    echo down  - Stop  Docker Compose
    echo logs  - Fetch the logs of a container
    echo up    - Start Docker Compose
    echo ---------------------------------------------------------
    set /P IO_AERO_COMPOSE_TASK="Enter the desired task [default: %IO_AERO_COMPOSE_TASK_DEFAULT%] "

    if ["!IO_AERO_COMPOSE_TASK!"] EQU [""] (
        set IO_AERO_COMPOSE_TASK=%IO_AERO_COMPOSE_TASK_DEFAULT%
    )
) else (
    set IO_AERO_COMPOSE_TASK=%1
)

if ["%IO_AERO_COMPOSE_TASK%"] EQU ["logs"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo *             - All Containers
        echo io_avstats_db - Database Profiling
        echo ---------------------------------------------------------
        set /P IO_AERO_CONTAINER="Enter the desired container [default: %IO_AERO_CONTAINER_DEFAULT%] "

        if ["!IO_AERO_CONTAINER!"] EQU [""] (
            set IO_AERO_CONTAINER=%IO_AERO_CONTAINER_DEFAULT%
        )
    ) else (
        set IO_AERO_CONTAINER=%2
    )
)

echo =======================================================================
echo Start %0
echo -----------------------------------------------------------------------
echo Manage a multi-container Docker application
echo -----------------------------------------------------------------------
echo COMPOSE_TASK                      : %IO_AERO_COMPOSE_TASK%
echo CONTAINER                         : %IO_AERO_CONTAINER%
echo -----------------------------------------------------------------------
echo POSTGRES_CONNECTION_PORT          : %IO_AERO_POSTGRES_CONNECTION_PORT%
echo POSTGRES_CONTAINER_NAME           : %IO_AERO_POSTGRES_CONTAINER_NAME%
echo POSTGRES_DBNAME                   : %IO_AERO_POSTGRES_DBNAME%
echo POSTGRES_PASSWORD                 : %IO_AERO_POSTGRES_PASSWORD%
echo POSTGRES_PGDATA                   : %IO_AERO_POSTGRES_PGDATA%
echo POSTGRES_USER                     : %IO_AERO_POSTGRES_USER%
echo POSTGRES_VERSION                  : %IO_AERO_POSTGRES_VERSION%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

if ["%IO_AERO_COMPOSE_TASK%"] EQU ["clean"] (
    echo Docker Containers .......................... before containers running:
    docker ps
    echo Docker Containers .................................. before containers:
    docker ps -a
    docker ps       | find "%IO_AERO_POSTGRES_CONTAINER_NAME%" && docker stop        %IO_AERO_POSTGRES_CONTAINER_NAME%
    docker ps -a    | find "%IO_AERO_POSTGRES_CONTAINER_NAME%" && docker rm  --force %IO_AERO_POSTGRES_CONTAINER_NAME%
    echo ............................................. after containers running:
    docker ps
    echo ..................................................... after containers:
    docker ps -a
    echo ........................................................ before images:
    docker images
    docker image ls | find "postgres"                  && docker rmi --force postgres:%IO_AERO_POSTGRES_VERSION%
    echo ......................................................... after images:
    docker images

    goto END_OF_SCRIPT
)

if ["%IO_AERO_COMPOSE_TASK%"] EQU ["down"] (
    echo Docker Containers .......................... before containers running:
    docker ps
    echo Docker Containers .................................. before containers:
    docker ps -a

    docker compose -f docker-compose_local.yml down

    echo ............................................. after containers running:
    docker ps
    echo ..................................................... after containers:
    docker ps -a

    goto END_OF_SCRIPT
)

if ["%IO_AERO_COMPOSE_TASK%"] EQU ["logs"] (
    if ["%IO_AERO_CONTAINER%"] EQU ["*"] (
        docker compose -f docker-compose_local.yml logs --tail=0 --follow
    ) else (
        docker compose -f docker-compose_local.yml logs --tail=0 --follow %IO_AERO_CONTAINER%
    )
)

if ["%IO_AERO_COMPOSE_TASK%"] EQU ["up"] (
    echo Docker Containers .......................... before containers running:
    docker ps
    echo Docker Containers .................................. before containers:
    docker ps -a
    echo ........................................................ before images:
    docker images

    start /B docker compose -f docker-compose_local.yml up
    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Program abort due to wrong input.
rem ----------------------------------------------------------------------------

echo Processing of the script run_io_avstats is aborted: unknown task='%IO_AERO_COMPOSE_TASK%'
exit 1

:END_OF_SCRIPT
echo.
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================
