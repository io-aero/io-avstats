#!/bin/bash

set -e

# ------------------------------------------------------------------------------
# run_prep_bash_scripts.sh: Configure EOL and execution rights for bash scripts.
# ------------------------------------------------------------------------------

echo "=========================================================================="
echo "Start $0"
echo "--------------------------------------------------------------------------"
echo "Configure EOL and execution rights - Ubuntu."
echo "--------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=========================================================================="

# Check if dos2unix is installed and install it if not
if ! command -v dos2unix &> /dev/null
then
    echo "Installing dos2unix..."
    sudo apt update
    sudo apt install -y dos2unix
else
    echo "dos2unix is already installed."
fi

# Set execute permissions on .sh files
chmod +x *.sh
chmod +x */*.sh

# Convert EOL characters from Windows to Unix style
dos2unix *.sh
dos2unix */*.sh

echo "--------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------"
echo "End   $0"
echo "=========================================================================="
