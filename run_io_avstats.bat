@echo off

rem ----------------------------------------------------------------------------
rem
rem run_io_avstats.bat: Process IO-AVSTATS tasks.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set ERRORLEVEL=

if ["!ENV_FOR_DYNACONF!"] EQU [""] (
    set ENV_FOR_DYNACONF=prod
)

set IO_AVSTATS_AVIATION_EVENT_STATISTICS=data\AviationAccidentStatistics
set IO_AVSTATS_CORRECTION_WORK_DIR=data\correction

set IO_AVSTATS_KEYCLOAK_CONTAINER_NAME=keycloak
set IO_AVSTATS_KEYCLOAK_PASSWORD_ADMIN=RsxAG^&hpCcuXsB2cbxSS
set IO_AVSTATS_KEYCLOAK_USER_ADMIN=admin
set IO_AVSTATS_KEYCLOAK_VERSION=latest

set IO_AVSTATS_NTSB_WORK_DIR=data\download

if ["!IO_AVSTATS_POSTGRES_CONNECTION_PORT!"] EQU [""] (
    set IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
)

set IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_db
set IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres
set IO_AVSTATS_POSTGRES_PASSWORD_ADMIN=V3s8m4x*MYbHrX*UuU6X
set IO_AVSTATS_POSTGRES_PGDATA=data\postgres
set IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
set IO_AVSTATS_POSTGRES_VERSION=latest

if ["!IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT!"] EQU [""] (
    set IO_AVSTATS_POSTGRES_KEYCLOAK_CONNECTION_PORT=5442
)

set IO_AVSTATS_POSTGRES_KEYCLOAK_CONTAINER_NAME=keycloak_db
set IO_AVSTATS_POSTGRES_KEYCLOAK_DBNAME_ADMIN=postgres
set IO_AVSTATS_POSTGRES_KEYCLOAK_PASSWORD_ADMIN=twAuk3VM2swt#Z96#zM#
set IO_AVSTATS_POSTGRES_KEYCLOAK_PGDATA=data\postgres_keycloak
set IO_AVSTATS_POSTGRES_KEYCLOAK_USER_ADMIN=postgres

set IO_AVSTATS_APPLICATION=
set IO_AVSTATS_COMPOSE_TASK=
set IO_AVSTATS_COMPOSE_TASK_DEFAULT=logs
set IO_AVSTATS_CONTAINER=
set IO_AVSTATS_CONTAINER_DEFAULT=*
set IO_AVSTATS_MSACCESS=
set IO_AVSTATS_MSEXCEL=
set IO_AVSTATS_TASK=
set IO_AVSTATS_TASK_DEFAULT=r_s_a

set PYTHONPATH=

if ["%1"] EQU [""] (
    echo =========================================================
    echo r_s_a   - Run a Streamlit application
    echo ---------------------------------------------------------
    echo u_p_d   - Complete processing of a modifying MS Access file
    echo ---------------------------------------------------------
    echo l_n_a   - Load NTSB MS Access database data into PostgreSQL
    echo c_l_l   - Correct decimal US latitudes and longitudes
    echo v_n_d   - Verify selected NTSB data
    echo r_d_s   - Refresh the PostgreSQL database schema
    echo ---------------------------------------------------------
    echo l_s_d   - Load simplemaps data into PostgreSQL
    echo l_z_d   - Load ZIP Code Database data into PostgreSQL
    echo l_c_d   - Load data from a correction file into PostgreSQL
    echo ---------------------------------------------------------
    echo a_o_c   - Load aviation occurrence categories into PostgreSQL
    echo c_d_l   - Run Docker Compose tasks - Local
    echo c_d_s   - Create the PostgreSQL database schema
    echo c_p_d   - Cleansing PostgreSQL data
    echo f_n_a   - Find the nearest airports
    echo l_a_p   - Load airport data into PostgreSQL
    echo l_c_s   - Load country and state data into PostgreSQL
    echo l_s_e   - Load sequence of events data into PostgreSQL
    echo u_d_s   - Update the PostgreSQL database schema
    echo ---------------------------------------------------------
    echo c_d_i   - Create or update a Docker image
    echo c_d_c   - Run Docker Compose tasks - Cloud
    echo c_f_z   - Zip the files for the cloud
    echo ---------------------------------------------------------
    echo version - Show the IO-AVSTATS-DB version
    echo ---------------------------------------------------------
    set /P IO_AVSTATS_TASK="Enter the desired task [default: %IO_AVSTATS_TASK_DEFAULT%] "

    if ["!IO_AVSTATS_TASK!"] EQU [""] (
        set IO_AVSTATS_TASK=%IO_AVSTATS_TASK_DEFAULT%
    )
) else (
    set IO_AVSTATS_TASK=%1
)

if ["%IO_AVSTATS_TASK%"] EQU ["c_d_c"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo clean - Remove all containers and images
        echo down  - Stop  Docker Compose
        echo logs  - Fetch the logs of a container
        echo up    - Start Docker Compose
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_COMPOSE_TASK="Enter the desired Docker Compose task [default: %IO_AVSTATS_COMPOSE_TASK_DEFAULT%] "

        if ["!IO_AVSTATS_COMPOSE_TASK!"] EQU [""] (
            set IO_AVSTATS_COMPOSE_TASK=%IO_AVSTATS_COMPOSE_TASK_DEFAULT%
        )
    ) else (
        set IO_AVSTATS_COMPOSE_TASK=%2
    )
)

if ["%IO_AVSTATS_TASK%"] EQU ["c_d_i"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo all     - All Streamlit applications
        echo ---------------------------------------------------------
        echo ae1982  - Aircraft Accidents in the US since 1982
        echo members - Members Only Area
        echo pd1982  - Profiling Data for the US since 1982
        echo slara   - Association Rule Analysis
        echo stats   - Aircraft Accidents in the US since 1982 - limited
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_APPLICATION="Enter the Streamlit application name "
    ) else (
        set IO_AVSTATS_APPLICATION=%2
    )
)

if ["%IO_AVSTATS_TASK%"] EQU ["c_d_l"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo clean - Remove all containers and images
        echo down  - Stop  Docker Compose
        echo logs  - Fetch the logs of a container
        echo up    - Start Docker Compose
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_COMPOSE_TASK="Enter the desired Docker Compose task [default: %IO_AVSTATS_COMPOSE_TASK_DEFAULT%] "

        if ["!IO_AVSTATS_COMPOSE_TASK!"] EQU [""] (
            set IO_AVSTATS_COMPOSE_TASK=%IO_AVSTATS_COMPOSE_TASK_DEFAULT%
        )
    ) else (
        set IO_AVSTATS_COMPOSE_TASK=%2
    )
)

if ["%IO_AVSTATS_TASK%"] EQU ["l_c_d"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        dir /A:-D /B %IO_AVSTATS_CORRECTION_WORK_DIR%\*.xlsx
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_MSEXCEL="Enter the stem name of the desired correction file "
    ) else (
        set IO_AVSTATS_MSEXCEL=%2
    )
)

if ["%IO_AVSTATS_TASK%"] EQU ["l_n_a"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        dir /A:-D /B %IO_AVSTATS_NTSB_WORK_DIR%\*.mdb
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_MSACCESS="Enter the stem name of the desired MS Access database file "
    ) else (
        set IO_AVSTATS_MSACCESS=%2
    )
)

if ["%IO_AVSTATS_TASK%"] EQU ["r_s_a"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo ae1982  - Aircraft Accidents in the US since 1982
        echo members - Members Only Area
        echo pd1982  - Profiling Data for the US since 1982
        echo slara   - Association Rule Analysis
        echo stats   - Aircraft Accidents in the US since 1982 - limited
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_APPLICATION="Enter the Streamlit application name "
    ) else (
        set IO_AVSTATS_APPLICATION=%2
    )
)

if ["%IO_AVSTATS_TASK%"] EQU ["u_p_d"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo avall   - Data from January 1, 2008 to today
        echo Pre2008 - Data from January 1, 1982 to December 31, 2007
        echo upDDMON - New additions and updates until DD day in the month MON
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_MSACCESS="Enter the stem name of the desired MS Access database file "
    ) else (
        set IO_AVSTATS_MSACCESS=%2
    )
)

echo.
echo Script %0 is now running

if exist logging_io_avstats.log (
    del /f /q logging_io_avstats.log
)

echo =======================================================================
echo Start %0
echo -----------------------------------------------------------------------
echo IO-AVSTATS - Aviation Event Statistics.
echo -----------------------------------------------------------------------
echo PYTHONPATH   : %PYTHONPATH%
echo -----------------------------------------------------------------------
echo TASK         : %IO_AVSTATS_TASK%
echo APPLICATION  : %IO_AVSTATS_APPLICATION%
echo COMPOSE_TASK : %IO_AVSTATS_COMPOSE_TASK%
echo MSACCESS     : %IO_AVSTATS_MSACCESS%
echo MSEXCEL      : %IO_AVSTATS_MSEXCEL%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

rem ----------------------------------------------------------------------------
rem Load aviation occurrence categories into PostgreSQL.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["a_o_c"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Run Docker Compose tasks (Cloud).
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["c_d_c"] (
    call scripts\run_docker_compose_cloud %IO_AVSTATS_COMPOSE_TASK%
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Create or update a Docker image.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["c_d_i"] (
    call scripts\run_create_image %IO_AVSTATS_APPLICATION% yes yes
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Run Docker Compose tasks (Local).
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["c_d_l"] (
    call scripts\run_docker_compose_local %IO_AVSTATS_COMPOSE_TASK%
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Create the PostgreSQL database schema.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["c_d_s"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t "u_d_s"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Zip the files for the cloud.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["c_f_z"] (
    call scripts\run_cloud_files_zip
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Correct decimal US latitudes and longitudes.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["c_l_l"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Cleansing PostgreSQL data.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["c_p_d"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Find the nearest airports.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["f_n_a"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Load airport data into PostgreSQL.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["l_a_p"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Load data from a correction file into PostgreSQL.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["l_c_d"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%" -e "%IO_AVSTATS_MSEXCEL%".xlsx
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Load country and state data into PostgreSQL.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["l_c_s"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Load NTSB MS Access database data into PostgreSQL.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["l_n_a"] (
    pipenv run python src\launcher.py -t d_n_a -m "%IO_AVSTATS_MSACCESS%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t d_n_a -m "%IO_AVSTATS_MSACCESS%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t u_d_s
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%" -m "%IO_AVSTATS_MSACCESS%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Load simplemaps data into PostgreSQL.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["l_s_d"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Load sequence of events data into PostgreSQL.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["l_s_e"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Load ZIP Code Database data into PostgreSQL.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["l_z_d"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Refresh the PostgreSQL database schema.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["r_d_s"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Run a Streamlit application.
rem ----------------------------------------------------------------------------

if ["%IO_AVSTATS_TASK%"] EQU ["r_s_a"] (
    if ["%IO_AVSTATS_APPLICATION%"] EQU ["ae1982"] (
        pipenv run streamlit run src\ioavstats\%IO_AVSTATS_APPLICATION%.py --server.port 8501 -- --mode Std
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
            exit %ERRORLEVEL%
        )

        goto END_OF_SCRIPT
    )

    if ["%IO_AVSTATS_APPLICATION%"] EQU ["members"] (
        pipenv run streamlit run src\ioavstats\%IO_AVSTATS_APPLICATION%.py --server.port 8598
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
            exit %ERRORLEVEL%
        )

        goto END_OF_SCRIPT
    )

    if ["%IO_AVSTATS_APPLICATION%"] EQU ["pd1982"] (
        pipenv run streamlit run src\ioavstats\%IO_AVSTATS_APPLICATION%.py --server.port 8502
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
            exit %ERRORLEVEL%
        )

        goto END_OF_SCRIPT
    )

    if ["%IO_AVSTATS_APPLICATION%"] EQU ["slara"] (
        pipenv run streamlit run src\ioavstats\%IO_AVSTATS_APPLICATION%.py --server.port 8503
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
            exit %ERRORLEVEL%
        )

        goto END_OF_SCRIPT
    )

    if ["%IO_AVSTATS_APPLICATION%"] EQU ["stats"] (
        pipenv run streamlit run src\ioavstats\ae1982.py --server.port 8599
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
            exit %ERRORLEVEL%
        )

        goto END_OF_SCRIPT
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Update the PostgreSQL database schema.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["u_d_s"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Complete processing of a modifying MS Access file.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["u_p_d"] (
    pipenv run python src\launcher.py -t d_n_a -m "%IO_AVSTATS_MSACCESS%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t l_n_a -m "%IO_AVSTATS_MSACCESS%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t c_l_l
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t f_n_a
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t v_n_d
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    pipenv run python src\launcher.py -t r_d_s
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Show the IO-AVSTATS-DB version.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["version"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Verify selected NTSB data.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["v_n_d"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

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
