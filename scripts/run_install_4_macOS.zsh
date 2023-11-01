#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_install_4_macOS.zsh: Install a io-avstats environment for macOS
#
# Step 1.
#
# ------------------------------------------------------------------------------

export VERSION_PYTHON3=3.10.11

export PWD_PREVIOUS="${PWD}"
cd ${HOME}

# Setting Environment Variables ----------------------------------------------------
PATH_ADD_ON=${HOME}/.local/bin
PATH_ORIG=${PATH_ORIG:-${PATH}}

echo '' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc
echo '# Environment io-avstats for macOS - Start' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc

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

print "\n------------------------------------------------------------------------------"
print "\nStep: Install Python3 - Version ${VERSION_PYTHON3}"
print "\n------------------------------------------------------------------------------"
rm -rf ${HOME}/.asdf/downloads/python
rm -rf ${HOME}/.asdf/installs/python
rm -rf ${HOME}/.asdf/plugins/python

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
