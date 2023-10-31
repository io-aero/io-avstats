#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_install_4_vm_wsl2_1.zsh: Install a io-avstats environment for Ubuntu 22.04
#
# Step 1.
#
# ------------------------------------------------------------------------------

export HOST_ENVIRONMENT_DEFAULT=vm

export VERSION_PYTHON3=3.10.11

rm -rf ${HOME}/.asdf/downloads/python
rm -rf ${HOME}/.asdf/installs/python
rm -rf ${HOME}/.asdf/plugins/python

if [[ -z "$1" ]]; then
    echo "=============================================================================="
    echo "vm   - Virtual Machine"
    echo "wsl2 - Windows Subsystem for Linux Version 2"
    echo "------------------------------------------------------------------------------"
    read "HOST_ENVIRONMENT?Enter the underlying host environment type [default: ${HOST_ENVIRONMENT_DEFAULT}]: "
HOST_ENVIRONMENT=${HOST_ENVIRONMENT:-$HOST_ENVIRONMENT_DEFAULT}
    export HOST_ENVIRONMENT=${HOST_ENVIRONMENT:-${HOST_ENVIRONMENT_DEFAULT}}
else
    export HOST_ENVIRONMENT=$1
fi

echo 090

export PWD_PREVIOUS="${PWD}"
cd ${HOME}

echo 100

# Setting Environment Variables ----------------------------------------------------
export DEBIAN_FRONTEND=noninteractive
export LOCALE=en_US.UTF-8

PATH_ADD_ON=${HOME}/.local/bin
PATH_ORIG=${PATH_ORIG:-${PATH}}

export TIMEZONE=America/Chicago

echo '' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc
echo '# Environment io-avstats for Ubuntu 22.04 - Start' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc
echo " "
echo "Script $0 is now running"

export LOG_FILE=run_install_4_vm_wsl2_1.log

echo ""
echo "You can find the run log in the file ${LOG_FILE}"
echo ""

exec &> >(tee -i ${LOG_FILE}) 2>&1
sleep .1

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
echo "Install a io-avstats_dev environment for Ubuntu 22.04 - Step 1."
echo "------------------------------------------------------------------------------"
echo "HOST_ENVIRONMENT                  : ${HOST_ENVIRONMENT}"
echo "USER                              : ${USER}"
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

# from Locale & Timezone -----------------------------------------------------------
echo '' >> ${HOME}/.zshrc
echo 'export HOST_ENVIRONMENT='${HOST_ENVIRONMENT} >> ${HOME}/.zshrc

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
echo '# Environment io-avstats for Ubuntu 22.04 - End' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc

echo "------------------------------------------------------------------------------"
echo "Step: Install AWS CLI"
echo "------------------------------------------------------------------------------"
aws --version
aws configure
echo "=============================================================================="

# Initializing the interactive shell session ---------------------------------------
source ${HOME}/.zshrc

if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    echo "------------------------------------------------------------------------------"
    echo "Step: Install Docker Desktop"
    echo "------------------------------------------------------------------------------"
    echo "Updating Homebrew..."
    brew update

    echo "Installing Docker CLI..."
    brew install docker

    echo "Docker CLI installation complete."
    echo "To get full Docker functionality, you'll need to install Docker Desktop manually from: https://www.docker.com/products/docker-desktop"
    echo " "
    echo "=============================================================================> Version  Docker Desktop: "
    echo " "
    echo "Current version of Docker Desktop: $(docker version)"
    echo " "
    echo "=============================================================================="
fi

pwd
cd "${PWD_PREVIOUS}"
pwd
echo " "
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="

exit 0
