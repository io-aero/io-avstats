@echo off

rem ------------------------------------------------------------------------------
rem
rem run_setup_postgresql_keycloak.bat: Set up a Keycloak PostgreSQL container.
rem
rem ------------------------------------------------------------------------------

setlocal EnableDelayedExpansion

echo ================================================================================
echo Start %0
echo --------------------------------------------------------------------------------
echo IO-AVSTATS - Set up a Keycloak PostgreSQL Docker container.
echo --------------------------------------------------------------------------------
echo POSTGRES_KEYCLOAK_CONNECTION_PORT : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT%
echo POSTGRES_KEYCLOAK_CONTAINER_NAME  : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
echo POSTGRES_KEYCLOAK_CONTAINER_PORT  : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT%
echo POSTGRES_KEYCLOAK_DBNAME_ADMIN    : %IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN%
echo POSTGRES_KEYCLOAK_PASSWORD_ADMIN  : "%IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN%"
echo POSTGRES_KEYCLOAK_PGDATA          : %IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA%
echo POSTGRES_KEYCLOAK_USER_ADMIN      : %IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN%
echo POSTGRES_VERSION                  : %IO_AVSTATS_POSTGRES_VERSION%
echo --------------------------------------------------------------------------------
echo:| TIME
echo ================================================================================

echo Docker stop/rm %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME% ............ before:
docker ps -a
docker ps    | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker stop       %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
docker ps -a | find "%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" && docker rm --force %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
echo ............................................................. after:
docker ps -a

resources\Gammadyne\timer.exe

rem ------------------------------------------------------------------------------
rem PostgreSQL                          https://hub.docker.com/_/postgres
rem ------------------------------------------------------------------------------

echo PostgreSQL
echo --------------------------------------------------------------------------------
echo Docker create %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME% (PostgreSQL %IO_AVSTATS_POSTGRES_VERSION%)

if not exist %IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA%\ (
    mkdir %IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA%
)

docker create -e        POSTGRES_DB=%IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN% ^
              -e        POSTGRES_HOST_AUTH_METHOD=password ^
              -e        POSTGRES_PASSWORD=%IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN% ^
              -e        POSTGRES_USER=%IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN% ^
              --expose  %IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT% ^
              -h        %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME% ^
              --name    %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME% ^
              -p        %IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT%:%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_PORT% ^
              -v        "%cd%\%IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA%":/var/lib/postgresql/data ^
              --restart always ^
              postgres:%IO_AVSTATS_POSTGRES_VERSION%

echo Docker start %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME% (PostgreSQL %O-AVSTATS_POSTGRES_KEYCLOAK_VERSION%) ...
docker start %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%

ping -n 30 127.0.0.1>nul

for /f "delims=" %%A in ('resources\Gammadyne\timer.exe /s') do set "CONSUMED=%%A"
echo DOCKER Keycloak PostgreSQL was ready in %CONSUMED%

docker ps

echo --------------------------------------------------------------------------------
echo:| TIME
echo --------------------------------------------------------------------------------
echo End   %0
echo ================================================================================