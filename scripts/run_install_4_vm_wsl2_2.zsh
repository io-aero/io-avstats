#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_install_4_vm_wsl2_2.zsh: Install a io-avstats environment for Ubuntu 22.04
#
# Step 2.
#
# ------------------------------------------------------------------------------

export PWD_PREVIOUS="${PWD}"
cd ${HOME}

print "\nScript $0 is now running\n"

export LOG_FILE=run_install_4_vm_wsl2_2.log

print "\nYou can find the run log in the file ${LOG_FILE}\n"

# The following redirection will work in zsh and append both stdout and stderr to the log file
exec > >(tee -i ${LOG_FILE}) 2>&1
sleep .1

print "=============================================================================="
print "Start $0"
print "------------------------------------------------------------------------------"
print "Install a io-avstats_dev environment for Ubuntu 22.04 - Step 2."
print "------------------------------------------------------------------------------"
print "HOST_ENVIRONMENT                  : ${HOST_ENVIRONMENT}"
print "USER                              : ${USER}"
print "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "=============================================================================="
print "Step: Install asdf - part 2"
print "------------------------------------------------------------------------------"
print "\nCurrent version of asdf is: $(asdf --version)\n"
print "=============================================================================="

rm -rf ${HOME}/.asdf/downloads/python
rm -rf ${HOME}/.asdf/downloads/tmux

rm -rf ${HOME}/.asdf/installs/python
rm -rf ${HOME}/.asdf/installs/tmux

rm -rf ${HOME}/.asdf/plugins/python
rm -rf ${HOME}/.asdf/plugins/tmux

print "------------------------------------------------------------------------------"
print "Step: Install Python3 - Version ${VERSION_PYTHON3}"
print "------------------------------------------------------------------------------"
asdf plugin add python
asdf install python ${VERSION_PYTHON3}
asdf global python ${VERSION_PYTHON3}
print "\n=============================================================================> Version  Python3:"
print "\nCurrent version of Python3: $(python3 --version)"
print "\nCurrent version of pip:     $(pip --version)\n"
print "=============================================================================="

print "------------------------------------------------------------------------------"
print "Step: Cleanup"
print "------------------------------------------------------------------------------"
brew autoremove

print "\n=============================================================================> Current Date: \n"
date
print "\n=============================================================================> Environment variable LANG: \n"
print "${LANG}\n"
print "=============================================================================> Environment variable LANGUAGE: \n"
print "${LANGUAGE}\n"
print "=============================================================================> Environment variable LC_ALL: \n"
print "${LC_ALL}\n"
print "=============================================================================> Environment variable PATH: \n"
print "${PATH}\n"

# Show component versions ----------------------------------------------------------
print "=============================================================================> Components"
pwd
cd "${PWD_PREVIOUS}"
pwd
( ./run_version_check.zsh )
print "\n------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "------------------------------------------------------------------------------"
print "End   $0"
print "=============================================================================="

exit 0
