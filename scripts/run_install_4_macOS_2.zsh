#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_install_4_macOS_2.zsh: Install a io-avstats environment for macOS
#
# Step 2.
#
# ------------------------------------------------------------------------------

export PWD_PREVIOUS="${PWD}"
cd ${HOME}

print "\nScript $0 is now running\n"

export LOG_FILE=run_install_4_macOS_2.log

print "\nYou can find the run log in the file ${LOG_FILE}\n"

# The following redirection will work in zsh and append both stdout and stderr to the log file
exec > >(tee -i ${LOG_FILE}) 2>&1
sleep .1

print "\n=============================================================================="
print "\nStart $0"
print "\n------------------------------------------------------------------------------"
print "\nInstall a io-avstats_dev environment for macOS - Step 2."
print "\n------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n=============================================================================="
print "\nStep: Install asdf - part 2"
print "\n------------------------------------------------------------------------------"
print "\nCurrent version of asdf is: $(asdf --version)\n"
print "\n=============================================================================="

rm -rf ${HOME}/.asdf/downloads/python

rm -rf ${HOME}/.asdf/installs/python

rm -rf ${HOME}/.asdf/plugins/python

print "\n------------------------------------------------------------------------------"
print "\nStep: Install Python3 - Version ${VERSION_PYTHON3}"
print "\n------------------------------------------------------------------------------"
asdf plugin add python
asdf install python ${VERSION_PYTHON3}
asdf global python ${VERSION_PYTHON3}
print "\n=============================================================================> Version  Python3:"
print "\nCurrent version of Python3: $(python3 --version)"
print "\nCurrent version of pip:     $(pip --version)\n"
print "\n=============================================================================="

print "\n------------------------------------------------------------------------------"
print "\nStep: Cleanup"
print "\n------------------------------------------------------------------------------"
brew autoremove

print "\n=============================================================================> Current Date: \n"
date
print "\n=============================================================================> Environment variable LANG: \n"
print "\n${LANG}\n"
print "\n=============================================================================> Environment variable LANGUAGE: \n"
print "\n${LANGUAGE}\n"
print "\n=============================================================================> Environment variable LC_ALL: \n"
print "\n${LC_ALL}\n"
print "\n=============================================================================> Environment variable PATH: \n"
print "\n${PATH}\n"
pwd
cd "${PWD_PREVIOUS}"
pwd
( ./run_version_check.zsh )
print "\n------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n------------------------------------------------------------------------------"
print "\nEnd   $0"
print "\n=============================================================================="

exit 0
