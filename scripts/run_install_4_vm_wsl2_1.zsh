#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_install_4_vm_wsl2_1.zsh: Install a io-avstats environment for Ubuntu 22.04
#
# Step 1.
#
# ------------------------------------------------------------------------------

sudo rm -rf /tmp/*

export HOST_ENVIRONMENT_DEFAULT=vm

export VERSION_IO_AVSTATS_DB=1.7.8

export VERSION_DBEAVER=23.2.3
export VERSION_PYTHON3=3.10.11

sudo rm -rf ${HOME}/.asdf/downloads/python
sudo rm -rf ${HOME}/.asdf/installs/python
sudo rm -rf ${HOME}/.asdf/plugins/python

if [[ -z "$1" ]]; then
    echo "=============================================================================="
    echo "vm   - Virtual Machine"
    echo "wsl2 - Windows Subsystem for Linux Version 2"
    echo "------------------------------------------------------------------------------"
    read -q "HOST_ENVIRONMENT?Enter the underlying host environment type [default: ${HOST_ENVIRONMENT_DEFAULT}] "
    export HOST_ENVIRONMENT=${HOST_ENVIRONMENT:-${HOST_ENVIRONMENT_DEFAULT}}
else
    export HOST_ENVIRONMENT=$1
fi

export PWD_PREVIOUS="${PWD}"
cd ${HOME}

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
sudo apt-get clean -qy

sudo apt-get update -qy
sudo apt-get upgrade -qy

sudo apt-get install -qy autoconf \
                         automake \
                         awscli \
                         build-essential \
                         curl \
                         default-jre \
                         dos2unix \
                         git \
                         libbz2-dev \
                         libffi-dev \
                         liblzma-dev \
                         libncursesw5-dev \
                         libreadline-dev \
                         libsqlite3-dev \
                         libssl-dev \
                         libxml2-dev \
                         libxmlsec1-dev \
                         llvm \
                         make \
                         p7zip-full \
                         postgresql-client \
                         software-properties-common \
                         tk-dev \
                         vim \
                         wget \
                         xz-utils \
                         zlib1g-dev

echo "------------------------------------------------------------------------------"
echo "Step: Setting Locale & Timezone"
echo "------------------------------------------------------------------------------"
sudo ln -fs /usr/share/zoneinfo/${TIMEZONE} /etc/localtime
sudo dpkg-reconfigure --frontend noninteractive tzdata
sudo locale-gen "${LOCALE}"
sudo update-locale "LANG=${LOCALE}"
sudo locale-gen --purge "${LOCALE}"
sudo dpkg-reconfigure --frontend noninteractive locales

echo "------------------------------------------------------------------------------"
echo "Step: Setting up the environment: 1. Setting the environment variables"
echo "------------------------------------------------------------------------------"

# from asdf ------------------------------------------------------------------------
PATH_ADD_ON=${HOME}/.asdf/bin:${HOME}/.asdf/shims:${PATH_ADD_ON}

# from DBeaver ----------------------------------------------------------------------
if [[ "${HOST_ENVIRONMENT}" == "vm" ]]; then
    export HOME_DBEAVER=/opt/dbeaver
    PATH_ADD_ON=${HOME_DBEAVER}:${PATH_ADD_ON}
    echo "if [[ $(id -gn) != 'docker' ]]; then ( newgrp docker ) fi" >> ${HOME}/.zshrc
fi

# from Python 3 ----------------------------------------------------------------------
PATH_ADD_ON=${HOME}/.asdf/installs/python/${VERSION_PYTHON3}/bin:${PATH_ADD_ON}

# from Locale & Timezone -----------------------------------------------------------
echo '' >> ${HOME}/.zshrc
echo 'export DEBIAN_FRONTEND='${DEBIAN_FRONTEND} >> ${HOME}/.zshrc
echo 'export HOST_ENVIRONMENT='${HOST_ENVIRONMENT} >> ${HOME}/.zshrc
echo 'export LANG='${LOCALE} >> ${HOME}/.zshrc
echo 'export LANGUAGE='${LOCALE} >> ${HOME}/.zshrc
echo 'export LC_ALL='${LOCALE} >> ${HOME}/.zshrc
echo 'export LOCALE='${LOCALE} >> ${HOME}/.zshrc

echo '' >> ${HOME}/.zshrc
echo 'export VERSION_IO_AVSTATS_DB='${VERSION_IO_AVSTATS_DB} >> ${HOME}/.zshrc

echo '' >> ${HOME}/.zshrc
if [[ "${HOST_ENVIRONMENT}" = "vm" ]]; then
    echo 'export VERSION_DBEAVER='${VERSION_DBEAVER} >> ${HOME}/.zshrc
fi
echo 'export VERSION_PYTHON3='${VERSION_PYTHON3} >> ${HOME}/.zshrc

echo "------------------------------------------------------------------------------"
echo "Step: Setting up the environment: 2. Initializing the interactive shell session"
echo "------------------------------------------------------------------------------"
echo '' >> ${HOME}/.zshrc
echo 'alias python=python3' >> ${HOME}/.zshrc
echo 'alias vi=vim' >> ${HOME}/.zshrc

# PATH variable --------------------------------------------------------------------
echo '' >> ${HOME}/.zshrc
if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    # from DBeaver ---------------------------------------------------------------------
    eval echo 'export HOME_DBEAVER=${HOME_DBEAVER}' >> ${HOME}/.zshrc
fi

eval echo 'export PATH=${PATH_ORIG}:${PATH_ADD_ON}' >> ${HOME}/.zshrc
eval echo 'export PATH_ORIG=${PATH_ORIG}' >> ${HOME}/.zshrc

# from asdf ------------------------------------------------------------------------
echo '' >> ${HOME}/.zshrc
eval echo '. ${HOME}/.asdf/asdf.sh' >> ${HOME}/.zshrc
eval echo '. ${HOME}/.asdf/completions/asdf.bash' >> ${HOME}/.zshrc
# Note: Zsh completions might be different from Bash and may require separate files.

# from Docker Desktop --------------------------------------------------------------
if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    echo '' >> ${HOME}/.zshrc
    echo "if [ '$(id -gn)' != 'docker' ]; then ( newgrp docker ) fi" >> ${HOME}/.zshrc
fi

echo '' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc
echo '# Environment io-avstats for Ubuntu 22.04 - End' >> ${HOME}/.zshrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.zshrc

# Initializing the interactive shell session ---------------------------------------
source ${HOME}/.zshrc

echo "------------------------------------------------------------------------------"
echo "Step: Install AWS CLI"
echo "------------------------------------------------------------------------------"
aws --version
aws configure
echo "=============================================================================="

echo "------------------------------------------------------------------------------"
echo "Step: Install asdf - part 1"
echo "------------------------------------------------------------------------------"
sudo rm -rf ${HOME}/.asdf
git clone https://github.com/asdf-vm/asdf.git ${HOME}/.asdf
echo "=============================================================================="

if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    echo "------------------------------------------------------------------------------"
    echo "Step: Install DBeaver - Version ${VERSION_DBEAVER}"
    echo "------------------------------------------------------------------------------"
    wget --quiet https://github.com/dbeaver/dbeaver/releases/download/${VERSION_DBEAVER}/dbeaver-ce-${VERSION_DBEAVER}-linux.gtk.x86_64.tar.gz
    sudo tar -xf dbeaver-ce-${VERSION_DBEAVER}-linux.gtk.x86_64.tar.gz
    sudo rm -rf ${HOME_DBEAVER}
    sudo cp -r dbeaver ${HOME_DBEAVER}
    sudo rm -rf dbeaver
    sudo rm -f dbeaver-ce-*.tar.gz
    echo " "
    echo "=============================================================================> Version  DBeaver: "
    echo " "
    echo "Current version of DBeaver: $(${HOME_DBEAVER}/dbeaver -help)"
    echo " "
    echo "=============================================================================="
    echo "------------------------------------------------------------------------------"
    echo "Step: Install Docker Desktop"
    echo "------------------------------------------------------------------------------"
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" --yes
    sudo apt-key fingerprint 0EBFCD88
    sudo apt-get install -qy docker-ce \
                             docker-ce-cli \
                             containerd.io
    sudo chmod 666 /var/run/docker.sock
    if ! [ $(getent group docker | grep -q "\b$USER\b") ]; then
        sudo usermod -aG docker $USER
    fi
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
