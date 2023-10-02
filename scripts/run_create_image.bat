@echo off

rem ----------------------------------------------------------------------------
rem
rem run_create_image.bat: Create a Docker image.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set APPLICATION_DEFAULT=ae1982
set DOCKER_CLEAR_CACHE_DEFAULT=yes
set DOCKER_HUB_PUSH_DEFAULT=yes
set IO_AERO_STREAMLIT_SERVER_PORT=8501
set MODE=n/a

if ["%1"] EQU [""] (
    echo =========================================================
    echo all      - All Streamlit applications
    echo ---------------------------------------------------------
    echo ae1982  - Aircraft Accidents in the US since 1982
    echo pd1982  - Profiling Data for the US since 1982
    echo slara   - Association Rule Analysis
    echo ---------------------------------------------------------
    set /P APPLICATION="Enter the desired application name [default: %APPLICATION_DEFAULT%] "

    if ["!APPLICATION!"] EQU [""] (
        set APPLICATION=%APPLICATION_DEFAULT%
    )
) else (
    set APPLICATION=%1
)

if ["%2"] EQU [""] (
    set /P DOCKER_HUB_PUSH="Push image to Docker Hub (yes / no) [default: %DOCKER_HUB_PUSH_DEFAULT%] "

    if ["!DOCKER_HUB_PUSH!"] EQU [""] (
        set DOCKER_HUB_PUSH=%DOCKER_HUB_PUSH_DEFAULT%
    )
) else (
    set DOCKER_HUB_PUSH=%2
)

if ["%3"] EQU [""] (
    set /P DOCKER_CLEAR_CACHE="Clear Docker cache (yes / no) [default: %DOCKER_CLEAR_CACHE_DEFAULT%] "

    if ["!DOCKER_CLEAR_CACHE!"] EQU [""] (
        set DOCKER_CLEAR_CACHE=%DOCKER_CLEAR_CACHE_DEFAULT%
    )
) else (
    set DOCKER_CLEAR_CACHE=%3
)

echo.
echo Script %0 is now running - Application: %APPLICATION%
set LOG_FILE=run_create_image.log
echo.
echo You can find the run log in the file %LOG_FILE%
echo.
echo Please wait ...
echo.

rem > %LOG_FILE% 2>&1 (

    echo =======================================================================
    echo Start %0
    echo -----------------------------------------------------------------------

    echo Create a Docker image for application %APPLICATION%

    echo -----------------------------------------------------------------------
    echo DOCKER_CLEAR_CACHE       : %DOCKER_CLEAR_CACHE%
    echo DOCKER_HUB_PUSH          : %DOCKER_HUB_PUSH%
    echo STREAMLIT_SERVER_PORT    : %IO_AERO_STREAMLIT_SERVER_PORT%
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo =======================================================================

    if ["!APPLICATION!"] EQU ["all"]  (
        call scripts\run_create_image ae1982  !DOCKER_HUB_PUSH! !DOCKER_CLEAR_CACHE!
        call scripts\run_create_image pd1982  !DOCKER_HUB_PUSH! !DOCKER_CLEAR_CACHE!
        call scripts\run_create_image slara   !DOCKER_HUB_PUSH! !DOCKER_CLEAR_CACHE!
        goto END_OF_SCRIPT
    )

    if exist tmp\upload rmdir /s /q tmp\upload
    mkdir tmp\upload

    if exist tmp\docs\img rmdir /s /q tmp\docs\img
    mkdir tmp\docs\img

    if ["%DOCKER_CLEAR_CACHE%"] EQU ["yes"]  (
        docker builder prune --all --force
    )

    echo Docker stop/rm !APPLICATION! ................................ before containers:
    docker ps -a
    docker ps       | find "!APPLICATION!" && docker stop        !APPLICATION!
    docker ps -a    | find "!APPLICATION!" && docker rm  --force !APPLICATION!
    echo ............................................................. after containers:
    docker ps -a
    echo ............................................................. before images:
    docker image ls
    docker image ls | find "!APPLICATION!" && docker rmi --force ioaero/!APPLICATION!
    echo ............................................................. after images:
    docker image ls


    if ["!APPLICATION!"] EQU ["ae1982"]  (
        set MODE=Std
    )

    docker build --build-arg APP=!APPLICATION! ^
                 --build-arg MODE=%MODE% ^
                 --build-arg SERVER_PORT=%IO_AERO_STREAMLIT_SERVER_PORT% ^
                 -t ioaero/!APPLICATION! .

    docker tag ioaero/!APPLICATION! ioaero/!APPLICATION!

    if ["%DOCKER_HUB_PUSH%"] EQU ["yes"]  (
        docker push ioaero/!APPLICATION!
    )

    docker images -q -f "dangling=true" -f "label=autodelete=true"

    for /F %%I in ('docker images -q -f "dangling=true" -f "label=autodelete=true"') do (docker rmi -f %%I)

    rmdir /s /q tmp\upload
    rmdir /s /q tmp\docs\img

    :END_OF_SCRIPT
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo -----------------------------------------------------------------------
    echo End   %0
    echo =======================================================================
rem )
