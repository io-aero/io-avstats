@echo off

rem ------------------------------------------------------------------------------
rem
rem run_delete_postgresql_container.bat: Delete the PostgreSQL database container.
rem
rem ------------------------------------------------------------------------------

setlocal EnableDelayedExpansion

echo ================================================================================
echo Start %0
echo --------------------------------------------------------------------------------
echo IO-AVSTATS - Delete the PostgreSQL database container.
echo --------------------------------------------------------------------------------
echo POSTGRES_CONTAINER_NAME  : %IO_AERO_POSTGRES_CONTAINER_NAME%
echo --------------------------------------------------------------------------------
echo:| TIME
echo ================================================================================

echo Docker stop/rm %IO_AERO_POSTGRES_CONTAINER_NAME% .................... before:
docker ps -a
docker ps    | find "%IO_AERO_POSTGRES_CONTAINER_NAME%" && docker stop %IO_AERO_POSTGRES_CONTAINER_NAME%
docker ps -a | find "%IO_AERO_POSTGRES_CONTAINER_NAME%" && docker rm --force %IO_AERO_POSTGRES_CONTAINER_NAME%
echo ............................................................. after:
docker ps -a

echo --------------------------------------------------------------------------------
echo:| TIME
echo --------------------------------------------------------------------------------
echo End   %0
echo ================================================================================
