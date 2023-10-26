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

set IO_AERO_AVIATION_EVENT_STATISTICS=data\AviationAccidentStatistics
set IO_AERO_CORRECTION_WORK_DIR=data\correction

set IO_AERO_NTSB_WORK_DIR=data\download

if ["!IO_AERO_POSTGRES_CONNECTION_PORT!"] EQU [""] (
    set IO_AERO_POSTGRES_CONNECTION_PORT=5432
)

set IO_AERO_POSTGRES_CONTAINER_NAME=io_avstats_db
set IO_AERO_POSTGRES_DBNAME_ADMIN=postgres
set IO_AERO_POSTGRES_PASSWORD_ADMIN=V3s8m4x*MYbHrX*UuU6X
set IO_AERO_POSTGRES_PGDATA=data\postgres
set IO_AERO_POSTGRES_USER_ADMIN=postgres
set IO_AERO_POSTGRES_VERSION=16.0

set IO_AERO_APPLICATION=
set IO_AERO_COMPOSE_TASK=
set IO_AERO_COMPOSE_TASK_DEFAULT=logs
set IO_AERO_CONTAINER=
set IO_AERO_CONTAINER_DEFAULT=*
set IO_AERO_MSACCESS=
set IO_AERO_MSEXCEL=
set IO_AERO_TASK=
set IO_AERO_TASK_DEFAULT=r_s_a

set PYTHONPATH=.

if ["%1"] EQU [""] (
    echo =========================================================
    echo r_s_a   - Run the IO-AVSTATS application
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
    echo c_d_s   - Create the IO-AVSTATS-DB PostgreSQL database schema
    echo c_p_d   - Cleansing PostgreSQL data
    echo f_n_a   - Find the nearest airports
    echo l_a_p   - Load airport data into PostgreSQL
    echo l_c_s   - Load country and state data into PostgreSQL
    echo l_s_e   - Load sequence of events data into PostgreSQL
    echo s_d_c   - Set up the IO-AVSTATS-DB PostgreSQL database container
    echo u_d_s   - Update the IO-AVSTATS-DB PostgreSQL database schema
    echo ---------------------------------------------------------
    echo c_d_i   - Create or update an application Docker image
    echo c_d_c   - Run Docker Compose tasks - Cloud
    echo c_f_z   - Zip the files for the cloud
    echo ---------------------------------------------------------
    set /P IO_AERO_TASK="Enter the desired task [default: %IO_AERO_TASK_DEFAULT%] "

    if ["!IO_AERO_TASK!"] EQU [""] (
        set IO_AERO_TASK=%IO_AERO_TASK_DEFAULT%
    )
) else (
    set IO_AERO_TASK=%1
)

if ["%IO_AERO_TASK%"] EQU ["c_d_c"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo clean - Remove all containers and images
        echo down  - Stop  Docker Compose
        echo logs  - Fetch the logs of a container
        echo up    - Start Docker Compose
        echo ---------------------------------------------------------
        set /P IO_AERO_COMPOSE_TASK="Enter the desired Docker Compose task [default: %IO_AERO_COMPOSE_TASK_DEFAULT%] "

        if ["!IO_AERO_COMPOSE_TASK!"] EQU [""] (
            set IO_AERO_COMPOSE_TASK=%IO_AERO_COMPOSE_TASK_DEFAULT%
        )
    ) else (
        set IO_AERO_COMPOSE_TASK=%2
    )
)

if ["%IO_AERO_TASK%"] EQU ["c_d_i"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo all     - All Streamlit applications
        echo ---------------------------------------------------------
        echo ae1982  - Aircraft Accidents in the US since 1982
        echo pd1982  - Profiling Data for the US since 1982
        echo slara   - Association Rule Analysis
        echo ---------------------------------------------------------
        set /P IO_AERO_APPLICATION="Enter the Streamlit application name "
    ) else (
        set IO_AERO_APPLICATION=%2
    )
)

if ["%IO_AERO_TASK%"] EQU ["l_c_d"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        dir /A:-D /B %IO_AERO_CORRECTION_WORK_DIR%\*.xlsx
        echo ---------------------------------------------------------
        set /P IO_AERO_MSEXCEL="Enter the stem name of the desired correction file "
    ) else (
        set IO_AERO_MSEXCEL=%2
    )
)

if ["%IO_AERO_TASK%"] EQU ["l_n_a"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo avall   - Data from January 1, 2008 to today
        echo Pre2008 - Data from January 1, 1982 to December 31, 2007
        echo upDDMON - New additions and updates until DD day in the month MON
        echo ---------------------------------------------------------
        set /P IO_AERO_MSACCESS="Enter the stem name of the desired MS Access database file "
    ) else (
        set IO_AERO_MSACCESS=%2
    )
)

if ["%IO_AERO_TASK%"] EQU ["u_p_d"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        echo avall   - Data from January 1, 2008 to today
        echo Pre2008 - Data from January 1, 1982 to December 31, 2007
        echo upDDMON - New additions and updates until DD day in the month MON
        echo ---------------------------------------------------------
        set /P IO_AERO_MSACCESS="Enter the stem name of the desired MS Access database file "
    ) else (
        set IO_AERO_MSACCESS=%2
    )
)

echo.
echo Script %0 is now running
echo.

if exist logging_io_aero.log (
    del /f /q logging_io_aero.log
)

if ["%IO_AERO_TASK%"] EQU ["r_s_a"] (
    set IO_AERO_AVSTATS_LOG=run_io_avstats_db_%IO_AERO_TASK%_%IO_AERO_APPLICATION%.log
) else (
    set IO_AERO_AVSTATS_LOG=run_io_avstats_db_%IO_AERO_TASK%.log
)

echo You can find the run log in the file %IO_AERO_AVSTATS_LOG%
echo.
echo Please wait ...
echo.

if exist %IO_AERO_AVSTATS_LOG% (
    del /f /q %IO_AERO_AVSTATS_LOG%
)

> %IO_AERO_AVSTATS_LOG% 2>&1 (

    echo =======================================================================
    echo Start %0
    echo -----------------------------------------------------------------------
    echo IO-AVSTATS - Aviation Event Statistics.
    echo -----------------------------------------------------------------------
    echo PYTHONPATH   : %PYTHONPATH%
    echo -----------------------------------------------------------------------
    echo TASK         : %IO_AERO_TASK%
    echo APPLICATION  : %IO_AERO_APPLICATION%
    echo COMPOSE_TASK : %IO_AERO_COMPOSE_TASK%
    echo MSACCESS     : %IO_AERO_MSACCESS%
    echo MSEXCEL      : %IO_AERO_MSEXCEL%
    echo -----------------------------------------------------------------------
    echo:| TIME
    echo =======================================================================

    rem ----------------------------------------------------------------------------
    rem Load aviation occurrence categories into PostgreSQL.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["a_o_c"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Run Docker Compose tasks (Cloud).
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["c_d_c"] (
        call scripts\run_docker_compose_cloud %IO_AERO_COMPOSE_TASK%
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Create or update an application Docker image.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["c_d_i"] (
        call scripts\run_create_image %IO_AERO_APPLICATION% yes yes
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Create the IO-AVSTATS-DB PostgreSQL database schema.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["c_d_s"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t "u_d_s"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Zip the files for the cloud.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["c_f_z"] (
        call scripts\run_cloud_files_zip
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Correct decimal US latitudes and longitudes.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["c_l_l"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Cleansing PostgreSQL data.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["c_p_d"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Find the nearest airports.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["f_n_a"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Load airport data into PostgreSQL.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["l_a_p"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Load data from a correction file into PostgreSQL.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["l_c_d"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%" -e "%IO_AERO_MSEXCEL%".xlsx
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Load country and state data into PostgreSQL.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["l_c_s"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Load NTSB MS Access database data into PostgreSQL.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["l_n_a"] (
        pipenv run python scripts\launcher.py -t d_n_a -m "%IO_AERO_MSACCESS%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t d_n_a -m "%IO_AERO_MSACCESS%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t u_d_s
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%" -m "%IO_AERO_MSACCESS%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Load simplemaps data into PostgreSQL.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["l_s_d"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Load sequence of events data into PostgreSQL.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["l_s_e"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Load ZIP Code Database data into PostgreSQL.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["l_z_d"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Refresh the PostgreSQL database schema.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["r_d_s"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Run a Streamlit application.
    rem ----------------------------------------------------------------------------

    if ["%IO_AERO_TASK%"] EQU ["r_s_a"] (
        pipenv run streamlit run ioavstats\Menu.py --server.port 8501
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Set up the IO-AVSTATS-DB PostgreSQL database container.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["s_d_c"] (
        call scripts\run_setup_postgresql
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Update the IO-AVSTATS-DB PostgreSQL database schema.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["u_d_s"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Complete processing of a modifying MS Access file.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["u_p_d"] (
        pipenv run python scripts\launcher.py -t d_n_a -m "%IO_AERO_MSACCESS%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t l_n_a -m "%IO_AERO_MSACCESS%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t c_l_l
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t f_n_a
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t v_n_d
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        pipenv run python scripts\launcher.py -t r_d_s
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )

    rem ----------------------------------------------------------------------------
    rem Verify selected NTSB data.
    rem ----------------------------------------------------------------------------
    if ["%IO_AERO_TASK%"] EQU ["v_n_d"] (
        pipenv run python scripts\launcher.py -t "%IO_AERO_TASK%"
        if ERRORLEVEL 1 (
            echo Processing of the script run_io_avstats was aborted
            exit 1
        )

        goto END_OF_SCRIPT
    )
)

rem ----------------------------------------------------------------------------
rem Program abort due to wrong input.
rem ----------------------------------------------------------------------------

echo Processing of the script run_io_avstats is aborted: unknown task='%IO_AERO_TASK%'
exit 1

:END_OF_SCRIPT
echo.
echo -----------------------------------------------------------------------
echo:| TIME
echo -----------------------------------------------------------------------
echo End   %0
echo =======================================================================
