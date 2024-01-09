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

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
echo "Install a io-avstats_dev environment for macOS - Step 1."
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="
echo "Supplement necessary system software"
echo "------------------------------------------------------------------------------"
# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Installing now..."
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

echo "------------------------------------------------------------------------------"
echo "Step: Setting up the environment: 1. Setting the environment variables"
echo "------------------------------------------------------------------------------"

# from Python 3 ----------------------------------------------------------------------
PATH_ADD_ON=${HOME}/.asdf/installs/python/${VERSION_PYTHON3}/bin:${PATH_ADD_ON}

echo '' >> ${HOME}/.zshrc
echo 'export VERSION_PYTHON3='${VERSION_PYTHON3} >> ${HOME}/.zshrc

echo "------------------------------------------------------------------------------"
echo "Step: Setting up the environment: 2. Initializing the interactive shell session"
echo "------------------------------------------------------------------------------"
echo '' >> ${HOME}/.zshrc
echo 'alias python=python3' >> ${HOME}/.zshrc
echo 'alias vi=vim' >> ${HOME}/.zshrc

eval echo 'export PATH=${PATH_ORIG}:${PATH_ADD_ON}' >> ${HOME}/.zshrc
eval echo 'export PATH_ORIG=${PATH_ORIG}' >> ${HOME}/.zshrc

echo '' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc
echo '# Environment io-avstats for macOS - End' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc

echo "------------------------------------------------------------------------------"
echo "Step: Install AWS CLI"
echo "------------------------------------------------------------------------------"
aws --version
aws configure
echo "=============================================================================="

# Initializing the interactive shell session ---------------------------------------
source ${HOME}/.zshrc

echo "------------------------------------------------------------------------------"
echo "Step: Install Python3 - Version ${VERSION_PYTHON3}"
echo "------------------------------------------------------------------------------"
rm -rf ${HOME}/.asdf/downloads/python
rm -rf ${HOME}/.asdf/installs/python
rm -rf ${HOME}/.asdf/plugins/python

asdf plugin add python
asdf install python ${VERSION_PYTHON3}
asdf global python ${VERSION_PYTHON3}
echo "=============================================================================> Version  Python3:"
echo "Current version of Python3: $(python3 --version)"
echo "Current version of pip:     $(pip --version)\n"
echo "=============================================================================="

echo "------------------------------------------------------------------------------"
echo "Step: Cleanup"
echo "------------------------------------------------------------------------------"
brew autoremove
pwd
cd "${PWD_PREVIOUS}"
pwd

( ./run_version_check.zsh )

echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="

exit 0
