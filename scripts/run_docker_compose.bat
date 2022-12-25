@echo off

rem ----------------------------------------------------------------------------
rem
rem run_docker_compose.bat: Manage a multi-container Docker application.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set ERRORLEVEL=

set IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
set IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
set IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
set IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres
set IO_AVSTATS_POSTGRES_PASSWORD_ADMIN=postgresql
set IO_AVSTATS_POSTGRES_PGDATA=data/postgres
set IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
set IO_AVSTATS_POSTGRES_VERSION=latest
set IO_AVSTATS_STREAMLIT_SERVER_PORT=8501
set IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008=8501
set IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008=8502

set IO_AVSTATS_TASK=
set IO_AVSTATS_TASK_DEFAULT=up

if ["%1"] EQU [""] (
    echo =========================================================
    echo clean - Remove all containers and images
    echo down  - Stop  Docker Compose
    echo up    - Start Docker Compose
    echo ---------------------------------------------------------
    set /P IO_AVSTATS_TASK="Enter the desired task [default: %IO_AVSTATS_TASK_DEFAULT%] "

    if ["!IO_AVSTATS_TASK!"] EQU [""] (
        set IO_AVSTATS_TASK=%IO_AVSTATS_TASK_DEFAULT%
    )
) else (
    set IO_AVSTATS_TASK=%1
)

echo =======================================================================
echo Start %0
echo -----------------------------------------------------------------------
echo Manage a multi-container Docker application
echo -----------------------------------------------------------------------
echo TASK                            : %IO_AVSTATS_TASK%
echo -----------------------------------------------------------------------
echo POSTGRES_CONNECTION_PORT        : %IO_AVSTATS_POSTGRES_CONNECTION_PORT%
echo POSTGRES_CONTAINER_NAME         : %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
echo POSTGRES_CONTAINER_PORT         : %IO_AVSTATS_POSTGRES_CONTAINER_PORT%
echo POSTGRES_DBNAME_ADMIN           : %IO_AVSTATS_POSTGRES_DBNAME_ADMIN%
echo POSTGRES_PASSWORD_ADMIN         : %IO_AVSTATS_POSTGRES_PASSWORD_ADMIN%
echo POSTGRES_PGDATA                 : %IO_AVSTATS_POSTGRES_PGDATA%
echo POSTGRES_USER_ADMIN             : %IO_AVSTATS_POSTGRES_USER_ADMIN%
echo POSTGRES_VERSION                : %IO_AVSTATS_POSTGRES_VERSION%
echo STREAMLIT_SERVER_PORT           : %IO_AVSTATS_STREAMLIT_SERVER_PORT%
echo STREAMLIT_SRRVER_PORT_faaus2008 : %IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008%
echo STREAMLIT_SERVER_PORT_pdus2008  : %IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

if ["%IO_AVSTATS_TASK%"] EQU ["clean"] (
    echo Docker Containers ........................................... before containers:
    docker ps -a
    docker ps       | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%" && docker stop %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%" && docker rm  --force %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps       | find "faaus2008"                            && docker stop faaus2008
    docker ps -a    | find "faaus2008"                            && docker rm  --force faaus2008
    docker ps       | find "pdus2008"                             && docker stop pdus2008
    docker ps -a    | find "pdus2008"                             && docker rm  --force pdus2008
    echo ............................................................. after containers:
    docker ps -a
    echo ............................................................. before images:
    docker images
    docker image ls | find "%IO_AVSTATS_POSTGRES_DBNAME_ADMIN%" && docker rmi --force %IO_AVSTATS_POSTGRES_DBNAME_ADMIN%:latest
    docker image ls | find "faaus2008"                          && docker rmi --force ioaero/faaus2008:latest
    docker image ls | find "pdus2008"                           && docker rmi --force ioaero/pdus2008:latest
    echo ............................................................. after images:
    docker images
    goto END_OF_SCRIPT
)

if ["%IO_AVSTATS_TASK%"] EQU ["down"] (
    docker compose down
    echo Docker Containers ........................................... before containers:
    docker ps -a
    docker ps       | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%" && docker stop %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%" && docker rm  --force %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps       | find "faaus2008"                            && docker stop faaus2008
    docker ps -a    | find "faaus2008"                            && docker rm  --force faaus2008
    docker ps       | find "pdus2008"                             && docker stop pdus2008
    docker ps -a    | find "pdus2008"                             && docker rm  --force pdus2008
    echo ............................................................. after containers:
    docker ps -a
    echo ............................................................. before images:
    docker images
    rem docker rmi (docker images -a -q)
    docker image ls | find "%IO_AVSTATS_POSTGRES_DBNAME_ADMIN%" && docker rmi --force %IO_AVSTATS_POSTGRES_DBNAME_ADMIN%:latest
    docker image ls | find "faaus2008"                          && docker rmi --force ioaero/faaus2008:latest
    docker image ls | find "pdus2008"                           && docker rmi --force ioaero/pdus2008:latest
    echo ............................................................. after images:
    docker images
    goto END_OF_SCRIPT
)

if ["%IO_AVSTATS_TASK%"] EQU ["up"] (
    docker compose up
    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Program abort due to wrong input.
rem ----------------------------------------------------------------------------

echo Processing of the script run_io_avstats is aborted: unknown task='%IO_AVSTATS_TASK%'
exit 1

:END_OF_SCRIPT
echo.
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================
