@echo off

rem ------------------------------------------------------------------------------
rem
rem run_setup_keycloak_server.bat: Set up a Keycloak server container.
rem
rem ------------------------------------------------------------------------------

setlocal EnableDelayedExpansion

echo ================================================================================
echo Start %0
echo --------------------------------------------------------------------------------
echo IO-AVSTATS - Set up a Keycloak server container.
echo --------------------------------------------------------------------------------
echo KEYCLOAK_CONNECTION_PORT          : %IO_AVSTATS_KEYCLOAK_CONNECTION_PORT%
echo KEYCLOAK_CONTAINER_NAME           : %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
echo KEYCLOAK_CONTAINER_PORT           : %IO_AVSTATS_KEYCLOAK_CONTAINER_PORT%
echo KEYCLOAK_PASSWORD_ADMIN           : "%IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN%"
echo KEYCLOAK_USER_ADMIN               : %IO_AVSTATS_KEYCLOAK_USER_ADMIN%
echo KEYCLOAK_VERSION                  : %IO_AVSTATS_KEYCLOAK_VERSION%
echo POSTGRES_KEYCLOAK_CONNECTION_PORT : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT%
echo POSTGRES_KEYCLOAK_CONTAINER_NAME  : %IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%
echo POSTGRES_KEYCLOAK_DBNAME_ADMIN    : %IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN%
echo POSTGRES_KEYCLOAK_PASSWORD_ADMIN  : %IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN%
echo POSTGRES_KEYCLOAK_USER_ADMIN      : %IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN%
echo --------------------------------------------------------------------------------
echo:| TIME
echo ================================================================================

echo Docker stop/rm %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME% .................... before:
docker ps -a
docker ps    | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%" && docker stop       %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
docker ps -a | find "%IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%" && docker rm --force %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%
echo ............................................................. after:
docker ps -a

resources\Gammadyne\timer.exe

rem ------------------------------------------------------------------------------
rem PostgreSQL                                   https://hub.docker.com/_/postgres
rem ------------------------------------------------------------------------------

echo --------------------------------------------------------------------------------
echo Docker create %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME% (Keycloak %IO_AVSTATS_KEYCLOAK_VERSION%)

docker create -e        KC_HTTP_ENABLED=true ^
              -e        KC_HTTP_HOST=0.0.0.0 ^
              -e        KC_HTTPS_CLIENT_AUTH=none ^
              -e        KC_HOSTNAME_STRICT=false ^
              -e        KC_HOSTNAME_URL=http://auth.io-aero.com:8080/ ^
              -e        KEYCLOAK_ADMIN=%IO_AVSTATS_KEYCLOAK_USER_ADMIN% ^
              -e        KEYCLOAK_ADMIN_PASSWORD="%IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN%" ^
              -e        KC_DB=postgres ^
              -e        KC_DB_URL_HOST="%IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME%" ^
              -e        KC_DB_URL_PORT="%IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT%" ^
              -e        KC_DB_URL_DATABASE="%IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN%" ^
              -e        KC_DB_USERNAME="%IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN%" ^
              -e        KC_DB_PASSWORD="%IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN%" ^
              -e        KC_PROXY=edge ^
              --name    %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME% ^
              --restart always ^
              quay.io/keycloak/keycloak:%IO_AVSTATS_KEYCLOAK_VERSION% ^
              start

echo Docker start %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME% (Keycloak %O-AVSTATS_KEYCLOAK_VERSION%) ...
docker start %IO_AVSTATS_KEYCLOAK_CONTAINER_NAME%

ping -n 30 127.0.0.1>nul

for /f "delims=" %%A in ('resources\Gammadyne\timer.exe /s') do set "CONSUMED=%%A"
echo DOCKER Keycloak was ready in %CONSUMED%

docker ps

echo --------------------------------------------------------------------------------
echo:| TIME
echo --------------------------------------------------------------------------------
echo End   %0
echo ================================================================================
