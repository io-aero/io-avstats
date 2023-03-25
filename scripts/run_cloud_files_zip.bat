@echo off

rem ----------------------------------------------------------------------------
rem
rem run_cloud_files_zip.sh: File Collection for AWS.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set AWS_FILE_NAME=cloud.zip
set AWS_PROG_ZIP=7za

echo =======================================================================
echo Start %0
echo -----------------------------------------------------------------------
echo File Collection for AWS
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

IF EXIST %AWS_FILE_NAME% DEL /F %AWS_FILE_NAME%

copy /Y data\latest_postgrep.zip download\IO-AVSTATS-DB.zip

%AWS_PROG_ZIP% a -spd -tzip %AWS_FILE_NAME% data\latest_postgres.zip ^
                                            config\docker-compose_cloud.yml ^
                                            config\nginx.conf ^
                                            scripts\run_cloud_setup_instance.sh ^
                                            scripts\run_docker_compose_cloud.sh

echo.
echo =======================================================================
echo Archive Content
echo -----------------------------------------------------------------------
%AWS_PROG_ZIP% l %AWS_FILE_NAME%
echo =======================================================================

echo.
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================
