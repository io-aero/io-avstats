@echo off

rem ------------------------------------------------------------------------------
rem
rem run_setup_postgresql.bat: Set up a PostgreSQL Docker container.
rem
rem ------------------------------------------------------------------------------

setlocal EnableDelayedExpansion

echo ================================================================================
echo Start %0
echo --------------------------------------------------------------------------------
echo IO-AVSTATS - Set up a PostgreSQL Docker container.
echo --------------------------------------------------------------------------------
rem set IO_AERO_POSTGRES_CONNECTION_PORT=5432
rem set IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db
rem set IO_AERO_POSTGRES_DBNAME_ADMIN=postgres
rem set IO_AERO_POSTGRES_PASSWORD_ADMIN=V3s8m4x*MYbHrX*UuU6X
rem set IO_AERO_POSTGRES_USER_ADMIN=postgres
rem set IO_AERO_POSTGRES_VERSION=16.1
rem echo --------------------------------------------------------------------------------
rem set IO_AERO_POSTGRES_PGDATA=data\postgres
rem echo --------------------------------------------------------------------------------
echo POSTGRES_CONNECTION_PORT : %IO_AERO_POSTGRES_CONNECTION_PORT%
echo POSTGRES_CONTAINER_NAME  : %IO_AERO_POSTGRES_CONTAINER_NAME%
echo POSTGRES_DBNAME_ADMIN    : %IO_AERO_POSTGRES_DBNAME_ADMIN%
echo POSTGRES_PASSWORD_ADMIN  : %IO_AERO_POSTGRES_PASSWORD_ADMIN%
echo POSTGRES_PGDATA          : %IO_AERO_POSTGRES_PGDATA%
echo POSTGRES_USER_ADMIN      : %IO_AERO_POSTGRES_USER_ADMIN%
echo POSTGRES_VERSION         : %IO_AERO_POSTGRES_VERSION%
echo --------------------------------------------------------------------------------
echo:| TIME
echo ================================================================================

echo Docker stop/rm %IO_AERO_POSTGRES_CONTAINER_NAME% .................... before:
docker ps -a
docker ps    | find "%IO_AERO_POSTGRES_CONTAINER_NAME%" && docker stop %IO_AERO_POSTGRES_CONTAINER_NAME%
docker ps -a | find "%IO_AERO_POSTGRES_CONTAINER_NAME%" && docker rm --force %IO_AERO_POSTGRES_CONTAINER_NAME%
echo ............................................................. after:
docker ps -a

resources\Gammadyne\timer.exe

rem ------------------------------------------------------------------------------
rem PostgreSQL                          https://hub.docker.com/_/postgres
rem ------------------------------------------------------------------------------

echo PostgreSQL
echo --------------------------------------------------------------------------------
echo Docker create %IO_AERO_POSTGRES_CONTAINER_NAME% (PostgreSQL %IO_AERO_POSTGRES_VERSION%)

if not exist %IO_AERO_POSTGRES_PGDATA%\ (
    mkdir %IO_AERO_POSTGRES_PGDATA%
)

docker create -e        POSTGRES_DB=%IO_AERO_POSTGRES_DBNAME_ADMIN% ^
              -e        POSTGRES_HOST_AUTH_METHOD=password ^
              -e        POSTGRES_PASSWORD=%IO_AERO_POSTGRES_PASSWORD_ADMIN% ^
              -e        POSTGRES_USER=%IO_AERO_POSTGRES_USER_ADMIN% ^
              --name    %IO_AERO_POSTGRES_CONTAINER_NAME% ^
              -p        %IO_AERO_POSTGRES_CONNECTION_PORT%:5432 ^
              -v        "%cd%\%IO_AERO_POSTGRES_PGDATA%":/var/lib/postgresql/data ^
              --restart always ^
              postgres:%IO_AERO_POSTGRES_VERSION%

echo Docker start %IO_AERO_POSTGRES_CONTAINER_NAME% (PostgreSQL %O-AVSTATS_POSTGRES_VERSION%) ...
docker start %IO_AERO_POSTGRES_CONTAINER_NAME%

ping -n 30 127.0.0.1>nul

for /f "delims=" %%A in ('resources\Gammadyne\timer.exe /s') do set "CONSUMED=%%A"
echo DOCKER PostgreSQL was ready in %CONSUMED%

docker ps

echo --------------------------------------------------------------------------------
echo:| TIME
echo --------------------------------------------------------------------------------
echo End   %0
echo ================================================================================
