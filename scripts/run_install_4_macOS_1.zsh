#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_install_4_macOS_1.zsh: Install a io-avstats environment for macOS
#
# Step 1.
#
# ------------------------------------------------------------------------------

export VERSION_PYTHON3=3.10.11

export PWD_PREVIOUS="${PWD}"
cd ${HOME}

# Setting Environment Variables ----------------------------------------------------
export LOCALE=en_US.UTF-8

PATH_ADD_ON=${HOME}/.local/bin
PATH_ORIG=${PATH_ORIG:-${PATH}}

export TIMEZONE=America/Chicago

echo '' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc
echo '# Environment io-avstats for macOS - Start' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc
print "\n "
print "\nScript $0 is now running"

export LOG_FILE=run_install_4_macOS_1.log

print "\n"
print "\nYou can find the run log in the file ${LOG_FILE}"
print "\n"

exec &> >(tee -i ${LOG_FILE}) 2>&1
sleep .1

print "\n=============================================================================="
print "\nStart $0"
print "\n------------------------------------------------------------------------------"
print "\nInstall a io-avstats_dev environment for macOS - Step 1."
print "\n------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n=============================================================================="
print "\nSupplement necessary system software"
print "\n------------------------------------------------------------------------------"
# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    print "\nHomebrew is not installed. Installing now..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew cleanup

brew update
brew upgrade

brew install asdf \
             autoconf \
             automake \
             awscli \
             dbeaver-community \
             dos2unix \
             findutils \
             gcc \
             arm-none-eabi-gdb \
             git \
             grep \
             libpq \
             llvm \
             make \
             openjdk \
             openssl \
             p7zip \
             pkg-config \
             tcl-tk \
             wget \
             xz

print "\n------------------------------------------------------------------------------"
print "\nStep: Setting up the environment: 1. Setting the environment variables"
print "\n------------------------------------------------------------------------------"

# from Python 3 ----------------------------------------------------------------------
PATH_ADD_ON=${HOME}/.asdf/installs/python/${VERSION_PYTHON3}/bin:${PATH_ADD_ON}

echo '' >> ${HOME}/.zshrc
echo 'export VERSION_PYTHON3='${VERSION_PYTHON3} >> ${HOME}/.zshrc

print "\n------------------------------------------------------------------------------"
print "\nStep: Setting up the environment: 2. Initializing the interactive shell session"
print "\n------------------------------------------------------------------------------"
echo '' >> ${HOME}/.zshrc
echo 'alias python=python3' >> ${HOME}/.zshrc
echo 'alias vi=vim' >> ${HOME}/.zshrc

eval echo 'export PATH=${PATH_ORIG}:${PATH_ADD_ON}' >> ${HOME}/.zshrc
eval echo 'export PATH_ORIG=${PATH_ORIG}' >> ${HOME}/.zshrc

echo '' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc
echo '# Environment io-avstats for macOS - End' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc

print "\n------------------------------------------------------------------------------"
print "\nStep: Install AWS CLI"
print "\n------------------------------------------------------------------------------"
aws --version
aws configure
print "\n=============================================================================="

# Initializing the interactive shell session ---------------------------------------
source ${HOME}/.zshrc

pwd
cd "${PWD_PREVIOUS}"
pwd
print "\n "
print "\n------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n------------------------------------------------------------------------------"
print "\nEnd   $0"
print "\n=============================================================================="

exit 0
