#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_install_dbeaver.sh: Install DBeaver on Ubuntu.
#
# ------------------------------------------------------------------------------

echo "=========================================================================="
echo "Checking for Java..."
echo "--------------------------------------------------------------------------"
java -version || sudo apt update && sudo apt -y install default-jdk

echo "=========================================================================="
echo "Installing DBeaver."
echo "--------------------------------------------------------------------------"
curl -fsSL https://dbeaver.io/debs/dbeaver.gpg.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/dbeaver.gpg

echo "=========================================================================="
echo "Adding DBeaver repository..."
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
echo "Updating package lists and installing DBeaver..."
echo "--------------------------------------------------------------------------"
sudo apt update && sudo apt install dbeaver-ce

echo "=========================================================================="
echo "Checking DBeaver installation..."
echo "--------------------------------------------------------------------------"
apt policy dbeaver-ce

date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------"
echo "End   $0"
echo "=========================================================================="
