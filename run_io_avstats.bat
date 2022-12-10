@echo off

rem ----------------------------------------------------------------------------
rem
rem run_io_avstats.bat: Process IO-AVSTATS tasks.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set ENV_FOR_DYNACONF=dev
set ERRORLEVEL=

set IO_AVSTATS_NTSB_WORK_DIR=data\download
set IO_AVSTATS_POSTGRES_CONNECTION_PORT=5432
set IO_AVSTATS_POSTGRES_CONTAINER_NAME=io_avstats_container
set IO_AVSTATS_POSTGRES_CONTAINER_PORT=5432
set IO_AVSTATS_POSTGRES_DBNAME_ADMIN=postgres
set IO_AVSTATS_POSTGRES_NET=io_avstats_net
set IO_AVSTATS_POSTGRES_PASSWORD_ADMIN=postgresql
set IO_AVSTATS_POSTGRES_PGDATA=data\postgres
set IO_AVSTATS_POSTGRES_USER_ADMIN=postgres
set IO_AVSTATS_POSTGRES_VERSION=latest

set IO_AVSTATS_CORRECTION=
set IO_AVSTATS_MSACCESS=
set IO_AVSTATS_TASK=
set IO_AVSTATS_TASK_DEFAULT=faaus2008

set PYTHONPATH=

if ["%1"] EQU [""] (
    echo =========================================================
    echo faaus2008 - Fatal Aircraft Accidents in the US since 2008
    echo pdus2008  - Profiling Data for the US since 2008
    echo ---------------------------------------------------------
    echo d_n_a     - Download a NTSB MS Access database file
    echo l_n_a     - Load NTSB MS Access database data into PostgreSQL
    echo c_l_l     - Correct decimal US latitudes and longitudes
    echo v_n_d     - Verify selected NTSB data
    echo ---------------------------------------------------------
    echo c_p_d     - Cleansing PostgreSQL data
    echo d_s_f     - Download basic simplemaps files
rem echo d_z_f     - Download the ZIP Code Database file
    echo l_c_d     - Load data from a correction file into PostgreSQL
    echo l_c_s     - Load country and state data into PostgreSQL
    echo l_s_d     - Load simplemaps data into PostgreSQL
    echo l_z_d     - Load ZIP Code Database data into PostgreSQL
    echo ---------------------------------------------------------
    echo c_d_s     - Create the PostgreSQL database schema
    echo d_d_f     - Delete the PostgreSQL database files
    echo d_d_s     - Drop the PostgreSQL database schema
    echo s_d_c     - Set up the PostgreSQL database container
    echo u_d_s     - Update the PostgreSQL database schema
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

if ["%IO_AVSTATS_TASK%"] EQU ["d_n_a"] (
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

if ["%IO_AVSTATS_TASK%"] EQU ["l_c_d"] (
    if ["%2"] EQU [""] (
        echo =========================================================
        dir /A:-D /B data\correction\*.xlsx
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_CORRECTION="Enter the stem name of the desired correction file "
    ) else (
        set IO_AVSTATS_CORRECTION=%2
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

echo.
echo Script %0 is now running

if exist logging_io_avstats.log (
    del /f /q logging_io_avstats.log
)

echo =======================================================================
echo Start %0
echo -----------------------------------------------------------------------
echo IO-AVSTATS - Aviation Accident Statistics.
echo -----------------------------------------------------------------------
echo PYTHONPATH : %PYTHONPATH%
echo -----------------------------------------------------------------------
echo TASK       : %IO_AVSTATS_TASK%
echo CORRECTION : %IO_AVSTATS_CORRECTION%
echo MSACCESS   : %IO_AVSTATS_MSACCESS%
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

rem ----------------------------------------------------------------------------
rem Create the PostgreSQL database schema.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["c_d_s"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
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
rem Delete the PostgreSQL database files.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["d_d_f"] (
    if  exist "%IO_AVSTATS_POSTGRES_PGDATA%" (
        echo "%IO_AVSTATS_POSTGRES_PGDATA%"
        dir /a "%IO_AVSTATS_POSTGRES_PGDATA%"
        runas /user:Administrator "rd /s /q '%IO_AVSTATS_POSTGRES_PGDATA%'"
    )
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Drop the PostgreSQL database schema.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["d_d_s"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Download a NTSB MS Access database file.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["d_n_a"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%" -m "%IO_AVSTATS_MSACCESS%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Download basic simplemaps files.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["d_s_f"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Download the ZIP Code Database file.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["d_z_f"] (
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Show the IO-AVSTATS faaus2008 application.
rem ----------------------------------------------------------------------------

if ["%IO_AVSTATS_TASK%"] EQU ["faaus2008"] (
    pipenv run streamlit run src\faaus2008_app\faaus2008.py
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
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%" -c "%IO_AVSTATS_CORRECTION%"
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
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%" -m "%IO_AVSTATS_MSACCESS%"
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
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%" -m "%IO_AVSTATS_MSACCESS%"
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
    pipenv run python src\launcher.py -t "%IO_AVSTATS_TASK%" -m "%IO_AVSTATS_MSACCESS%"
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Show the IO-AVSTATS pdus2008 application.
rem ----------------------------------------------------------------------------

if ["%IO_AVSTATS_TASK%"] EQU ["pdus2008"] (
    pipenv run streamlit run src\pdus2008_app\pdus2008.py
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)

rem ----------------------------------------------------------------------------
rem Setup the database container.
rem ----------------------------------------------------------------------------
if ["%IO_AVSTATS_TASK%"] EQU ["s_d_c"] (
    call scripts\run_setup_postgresql
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
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
