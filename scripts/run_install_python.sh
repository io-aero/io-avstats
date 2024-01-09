#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_install_python.sh: Install Python via PPA (Personal Package Archive) on Ubuntu.
#
# ------------------------------------------------------------------------------

# Set the Python version
PYTHON_VERSION="3.10"

echo "=========================================================================="
echo "Adding PPA for Python and updating package lists."
echo "--------------------------------------------------------------------------"
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

echo "=========================================================================="
echo "Install Python."
echo "--------------------------------------------------------------------------"
sudo apt install -y python${PYTHON_VERSION}
python3 --version

echo "=========================================================================="
echo "Install pip for Python 3."
echo "--------------------------------------------------------------------------"
sudo apt install python3-pip
pip3 install --user --upgrade pip
pip3 --version

echo "=========================================================================="
echo "Install pipenv with pip."
echo "--------------------------------------------------------------------------"
pip3 install --user pipenv
python3 -m pipenv --version

echo "--------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------"
echo "End   $0"
echo "=========================================================================="
