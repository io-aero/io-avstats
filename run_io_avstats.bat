@echo off

rem ----------------------------------------------------------------------------
rem
rem run_io_avstats.bat: Process IO-AVSTATS tasks.
rem
rem ----------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set ENV_FOR_DYNACONF=dev
set ERRORLEVEL=

set IO_AVSTATS_TASK=
set IO_AVSTATS_TASK_DEFAULT=demo

set PYTHONPATH=

if ["%1"] EQU [""] (
    echo =========================================================
    echo demo    - Show the IO-AVSTATS demo
    echo version - Show the IO-AVSTATS version
    echo ---------------------------------------------------------
    set /P IO_AVSTATS_TASK="Enter the desired task [default: %IO_AVSTATS_TASK_DEFAULT%] "

    if ["!IO_AVSTATS_TASK!"] EQU [""] (
        set IO_AVSTATS_TASK=%IO_AVSTATS_TASK_DEFAULT%
    )
) else (
    set IO_AVSTATS_TASK=%1
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
echo -----------------------------------------------------------------------
echo:| TIME
echo =======================================================================

rem ----------------------------------------------------------------------------
rem Show the IO-AVSTATS demo.
rem ----------------------------------------------------------------------------

if ["%IO_AVSTATS_TASK%"] EQU ["demo"] (
    pipenv run streamlit run src\demo.py
    if ERRORLEVEL 1 (
        echo Processing of the script run_io_avstats was aborted, error code=%ERRORLEVEL%
        exit %ERRORLEVEL%
    )

    goto END_OF_SCRIPT
)


rem ----------------------------------------------------------------------------
rem Show the IO-AVSTATS version.
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
