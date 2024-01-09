@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

set PYTHON_VERSION=3.10

echo ==========================================================================
echo Install Python 3 on Windows.
echo -------------------------------------------------------------------------
echo Downloading Python Installer
curl -o python-installer.exe https://www.python.org/ftp/python/%PYTHON_VERSION%.0/python-%PYTHON_VERSION%.0-amd64.exe

echo Installing Python
start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

echo Verifying Python Installation
python --version

echo ==========================================================================
echo Install pip for Python 3
echo -------------------------------------------------------------------------
echo Python 3 and pip3 are installed with Python %PYTHON_VERSION%

echo ==========================================================================
echo Install pipenv with pip
echo -------------------------------------------------------------------------
pip3 install --user pipenv
pipenv --version

echo -------------------------------------------------------------------------
echo DATE TIME : %date% %time%
echo -------------------------------------------------------------------------
echo End
echo ==========================================================================
