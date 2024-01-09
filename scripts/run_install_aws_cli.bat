@echo off
SETLOCAL

echo ==========================================================================
echo Installing AWS CLI on Windows.
echo -------------------------------------------------------------------------
echo Please ensure that AWSCLIV2.msi is downloaded in the current directory
start /wait msiexec /i AWSCLIV2.msi /quiet /norestart

echo Verifying AWS CLI installation
aws --version

echo ==========================================================================
echo Configuring AWS CLI
echo -------------------------------------------------------------------------
aws configure

echo -------------------------------------------------------------------------
echo DATE TIME: %DATE% %TIME%
echo -------------------------------------------------------------------------
echo End
echo ==========================================================================
