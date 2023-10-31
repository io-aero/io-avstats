#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_cloud_setup_instance.zsh: Set up the cloud environment.
#
# ------------------------------------------------------------------------------

# Setting Environment Variables ----------------------------------------------------
export DEBIAN_FRONTEND=noninteractive
export HOST_ENVIRONMENT=vm
export LOG_FILE=run_cloud_setup_instance.log

exec &> >(tee -i ${LOG_FILE}) 2>&1
sleep .1

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="
echo "Uninstall existing software"
echo "------------------------------------------------------------------------------"

sudo apt-get purge -qy containerd.io \
                       docker-buildx-plugin \
                       docker-compose-plugin \
                       docker-ce \
                       docker-ce-cli

sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd

sudo apt-get clean -qy

echo "=============================================================================="
echo "Supplement necessary system software"
echo "------------------------------------------------------------------------------"

sudo apt-get update -qy

sudo apt-get install -qy ca-certificates \
                         curl \
                         gnupg \
                         lsb-release

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(source /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -qy

sudo apt-get install -qy containerd.io \
                         docker-buildx-plugin \
                         docker-ce \
                         docker-ce-cli \
                         docker-compose-plugin \
                         dos2unix \
                         software-properties-common \
                         unzip \
                         zip

sudo apt autoremove -qy

getent group docker || groupadd docker

sudo usermod -aG docker $USER

newgrp docker <<EONG
echo "hello from within newgrp"
id
EONG

sudo systemctl enable docker.service
sudo systemctl enable containerd.service

echo " "
echo "=============================================================================> Version Docker Compose: "
echo " "
echo "Current version of Docker Compose: $(docker compose version)"
echo " "
echo "=============================================================================="

echo " "
echo "=============================================================================> Version Docker Desktop: "
echo " "
echo "Current version of Docker Desktop: $(docker version)"
echo " "
echo "=============================================================================="

echo " "
echo "=============================================================================> Version dos2unix: "
echo " "
echo "Current version of dos2unix: $(dos2unix -V)"
echo " "
echo "=============================================================================="

echo " "
echo "=============================================================================> Version unzip: "
echo " "
echo "Current version of unzip: $(unzip -v)"
echo " "
echo "=============================================================================="

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
