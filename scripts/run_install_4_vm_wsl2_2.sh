#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_install_4_vm_wsl2_2.sh: Install a io-avstats environment for Ubuntu 22.04
#
# Step 2.
#
# ------------------------------------------------------------------------------

export PWD_PREVIOUS="${PWD}"
cd ${HOME}

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
echo "Install a io-avstats_dev environment for Ubuntu 22.04 - Step 2."
echo "------------------------------------------------------------------------------"
echo "HOST_ENVIRONMENT                  : ${HOST_ENVIRONMENT}"
echo "USER                              : ${USER}"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="
echo "Step: Install asdf - part 2"
echo "------------------------------------------------------------------------------"
echo " "
echo "Current version of asdf is: $(asdf --version)"
echo " "
echo "=============================================================================="

echo "------------------------------------------------------------------------------"
echo "Step: Install Python3 - Version ${VERSION_PYTHON3}"
echo "------------------------------------------------------------------------------"
sudo rm -rf ${HOME}/.asdf/downloads/python
sudo rm -rf ${HOME}/.asdf/installs/python
sudo rm -rf ${HOME}/.asdf/plugins/python

asdf plugin add python
asdf install python ${VERSION_PYTHON3}
asdf global python ${VERSION_PYTHON3}
echo "------------------------------------------------------------------------------"
echo "Step: Install pip"
echo "------------------------------------------------------------------------------"
sudo apt-get install -qy python3-pip
echo " "
echo "=============================================================================> Version  Python3: "
echo " "
echo "Current version of Python3: $(python3 --version)"
echo " "
echo "Current version of pip:     $(pip --version)"
echo " "
echo "=============================================================================="

echo "------------------------------------------------------------------------------"
echo "Step: Cleanup"
echo "------------------------------------------------------------------------------"
sudo apt-get -qy autoremove
sudo rm -rf /tmp/*

echo "=============================================================================> Current Date: "
echo " "
date
echo " "
# Show Environment Variables -------------------------------------------------------
echo "=============================================================================> Environment variable LANG: "
echo " "
echo "${LANG}"
echo " "
echo "=============================================================================> Environment variable LANGUAGE: "
echo " "
echo "${LANGUAGE}"
echo " "
echo "=============================================================================> Environment variable LC_ALL: "
echo " "
echo "${LC_ALL}"
echo " "
echo "=============================================================================> Environment variable PATH: "
echo " "
echo "${PATH}"
echo " "
# Show component versions ----------------------------------------------------------
echo "=============================================================================> Components"
pwd
cd "${PWD_PREVIOUS}"
pwd
( ./run_version_check.sh )
echo " "
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="

exit 0
