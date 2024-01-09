#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_install_docker.sh: Install Docker Engine on Ubuntu.
#
# ------------------------------------------------------------------------------

echo "=========================================================================="
echo "Installing Docker Engine."
echo "--------------------------------------------------------------------------"

echo "=========================================================================="
echo "Setting up the Docker repository."
echo "--------------------------------------------------------------------------"
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release

echo "=========================================================================="
echo "Adding Docker’s official GPG key."
echo "--------------------------------------------------------------------------"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg

echo "=========================================================================="
echo "Setting up the stable repository."
echo "--------------------------------------------------------------------------"
echo \
  "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "=========================================================================="
echo "Installing Docker Engine."
echo "--------------------------------------------------------------------------"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

echo "=========================================================================="
echo "Verifying Docker Engine installation."
echo "--------------------------------------------------------------------------"
sudo docker --version

echo "=========================================================================="
echo "Docker Engine is installed."
echo "--------------------------------------------------------------------------"
newgrp docker
sudo systemctl restart docker
sudo systemctl start docker

date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------"
echo "End   $0"
echo "=========================================================================="
