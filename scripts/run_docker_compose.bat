@echo off

rem ----------------------------------------------------------------------------
rem
rem run_docker_compose.bat: Manage a multi-container Docker application.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set ERRORLEVEL=

set IO_AVSTATS_KEYCLOAK_CONNECTION_PORT=8080
set IO_AVSTATS_KEYCLOAK_CONTAINER_NAME=keycloak
set IO_AVSTATS_KEYCLOAK_CONTAINER_PORT=8080
set IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN=RsxAG&hpCcuXsB2cbxSS
set IO_AVSTATS_KEYCLOAK_USER_ADMIN=admin
set IO_AVSTATS_KEYCLOAK_VERSION=latest

set IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
set IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
set IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
set IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres

set IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT=5442
set IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME=keycloak_db
set IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT=5432
set IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN=postgres
set IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN=twAuk3VM2swt#Z96#zM#
set IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA=data/postgres_keycloak
set IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN=postgres
set IO_AVSTATS_POSTGRES_KEYCLOAK_VERSION=latest

set IO_AVSTATS_POSTGRES_PASSWORD_ADMIN=V3s8m4x*MYbHrX*UuU6X
set IO_AVSTATS_POSTGRES_PGDATA=data/postgres
set IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
set IO_AVSTATS_POSTGRES_USER_GUEST=guest
set IO_AVSTATS_POSTGRES_VERSION=latest

set IO_AVSTATS_STREAMLIT_SERVER_PORT=8501
set IO_AVSTATS_STREAMLIT_SERVER_PORT_AE1982=8501
set IO_AVSTATS_STREAMLIT_SERVER_PORT_PD1982=8502
set IO_AVSTATS_STREAMLIT_SERVER_PORT_SLARA=8503
set IO_AVSTATS_STREAMLIT_SERVER_PORT_STATS=8599

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
echo TASK                         : %IO_AVSTATS_TASK%
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
echo POSTGRES_KEYCLOAK_VERSION         : %IO_AVSTATS_POSTGRES_KEYCLOAK_VERSION%
echo STREAMLIT_SERVER_PORT             : %IO_AVSTATS_STREAMLIT_SERVER_PORT%
echo STREAMLIT_SERVER_PORT_AE1982      : %IO_AVSTATS_STREAMLIT_SERVER_PORT_AE1982%
echo STREAMLIT_SERVER_PORT_PD1982      : %IO_AVSTATS_STREAMLIT_SERVER_PORT_PD1982%
echo STREAMLIT_SERVER_PORT_SLARA       : %IO_AVSTATS_STREAMLIT_SERVER_PORT_SLARA%
echo STREAMLIT_SERVER_PORT_STATS       : %IO_AVSTATS_STREAMLIT_SERVER_PORT_STATS%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

if ["%IO_AVSTATS_TASK%"] EQU ["clean"] (
    echo Docker Containers ........................................... before containers:
    docker ps -a
    docker ps       | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker stop        %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker rm  --force %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps       | find "ae1982"                                        && docker stop        ae1982
    docker ps -a    | find "ae1982"                                        && docker rm  --force ae1982
    docker ps       | find "load_balancer"                                 && docker stop        load_balancer
    docker ps -a    | find "load_balancer"                                 && docker rm  --force load_balancer
    docker ps       | find "pd1982"                                        && docker stop        pd1982
    docker ps -a    | find "pd1982"                                        && docker rm  --force pd1982
    docker ps       | find "slara"                                         && docker stop        slara
    docker ps -a    | find "slara"                                         && docker rm  --force slara
    docker ps       | find "stats"                                         && docker stop        stats
    docker ps -a    | find "stats"                                         && docker rm  --force stats
    echo ............................................................. after containers:
    docker ps -a
    echo ............................................................. before images:
    docker images
    docker image ls | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"        && docker rmi --force %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%:latest
    docker image ls | find "%IO_AVSTATS_POSTGRES_DBNAME_ADMIN%"          && docker rmi --force %IO_AVSTATS_POSTGRES_DBNAME_ADMIN%:latest
    docker image ls | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN%" && docker rmi --force %IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN%:latest
    docker image ls | find "ae1982"                                      && docker rmi --force ioaero/ae1982:latest
    docker image ls | find "keycloak"                                    && docker rmi --force quay.io/keycloak/keycloak:latest
    docker image ls | find "nginx"                                       && docker rmi --force nginx:alpine
    docker image ls | find "pd1982"                                      && docker rmi --force ioaero/pd1982:latest
    docker image ls | find "slara"                                       && docker rmi --force ioaero/slara:latest
    docker image ls | find "stats"                                       && docker rmi --force ioaero/stats:latest
    echo ............................................................. after images:
    docker images
    goto END_OF_SCRIPT
)

if ["%IO_AVSTATS_TASK%"] EQU ["down"] (
    docker compose down

    echo Docker Containers ........................................... before containers:
    docker ps -a
    docker ps -a
    docker ps       | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker stop        %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker rm  --force %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps       | find "ae1982"                                        && docker stop        ae1982
    docker ps -a    | find "ae1982"                                        && docker rm  --force ae1982
    docker ps       | find "load_balancer"                                 && docker stop        load_balancer
    docker ps -a    | find "load_balancer"                                 && docker rm  --force load_balancer
    docker ps       | find "pd1982"                                        && docker stop        pd1982
    docker ps -a    | find "pd1982"                                        && docker rm  --force pd1982
    docker ps       | find "slara"                                         && docker stop        slara
    docker ps -a    | find "slara"                                         && docker rm  --force slara
    docker ps       | find "stats"                                         && docker stop        stats
    docker ps -a    | find "stats"                                         && docker rm  --force stats
    echo ............................................................. after containers:
    docker ps -a
    echo ............................................................. before images:
    docker images
    docker image ls | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"        && docker rmi --force %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%:latest
    docker image ls | find "%IO_AVSTATS_POSTGRES_DBNAME_ADMIN%"          && docker rmi --force %IO_AVSTATS_POSTGRES_DBNAME_ADMIN%:latest
    docker image ls | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN%" && docker rmi --force %IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN%:latest
    docker image ls | find "ae1982"                                      && docker rmi --force ioaero/ae1982:latest
    docker image ls | find "keycloak"                                    && docker rmi --force quay.io/keycloak/keycloak:latest
    docker image ls | find "nginx"                                       && docker rmi --force nginx:alpine
    docker image ls | find "pd1982"                                      && docker rmi --force ioaero/pd1982:latest
    docker image ls | find "slara"                                       && docker rmi --force ioaero/slara:latest
    docker image ls | find "stats"                                       && docker rmi --force ioaero/stats:latest
    echo ............................................................. after images:
    docker images
    goto END_OF_SCRIPT
)

if ["%IO_AVSTATS_TASK%"] EQU ["up"] (
    docker compose down
    echo Docker Containers ........................................... before containers:
    docker ps -a
    docker ps -a
    docker ps       | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker stop        %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker rm  --force %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
    docker ps       | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker stop        %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps -a    | find "%IO_AVSTATS_POSTGRES_CONTAINER_NAME%"          && docker rm  --force %IO_AVSTATS_POSTGRES_CONTAINER_NAME%
    docker ps       | find "ae1982"                                        && docker stop        ae1982
    docker ps -a    | find "ae1982"                                        && docker rm  --force ae1982
    docker ps       | find "load_balancer"                                 && docker stop        load_balancer
    docker ps -a    | find "load_balancer"                                 && docker rm  --force load_balancer
    docker ps       | find "pd1982"                                        && docker stop        pd1982
    docker ps -a    | find "pd1982"                                        && docker rm  --force pd1982
    docker ps       | find "slara"                                         && docker stop        slara
    docker ps -a    | find "slara"                                         && docker rm  --force slara
    docker ps       | find "stats"                                         && docker stop        stats
    docker ps -a    | find "stats"                                         && docker rm  --force stats
    echo ............................................................. after containers:
    docker ps -a

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
