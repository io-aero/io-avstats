#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_create_image.sh: Create a Docker image.
#
# ------------------------------------------------------------------------------

export APPLICATION_DEFAULT=faaus2008

export DOCKER_CLEAR_CACHE_DEFAULT=yes
export DOCKER_HUB_PUSH_DEFAULT=no

if [ -z "$1" ]; then
    echo "========================================================="
    echo "faaus2008 - Fatal Aircraft Accidents in the US since 2008"
    echo "pdus2008  - Profiling Data for the US since 2008"

    echo "---------------------------------------------------------"
    read -p "Enter the desired application name [default: ${APPLICATION_DEFAULT}] " APPLICATION
    export APPLICATION=${APPLICATION}

    if [ -z "${APPLICATION}" ]; then
        export APPLICATION=${APPLICATION_DEFAULT}
    fi
else
    export APPLICATION=$1
fi

if [ -z "$2" ]; then
    read -p "Push image to Docker Hub (yes / no) [default: ${DOCKER_HUB_PUSH_DEFAULT}] " DOCKER_HUB_PUSH
    export DOCKER_HUB_PUSH=${DOCKER_HUB_PUSH}
else
    export DOCKER_HUB_PUSH=$2
fi

if [ -z "$3" ]; then
    read -p "Clear Docker cache (yes / no) [default: ${DOCKER_CLEAR_CACHE_DEFAULT}] " DOCKER_CLEAR_CACHE
    export DOCKER_CLEAR_CACHE=${DOCKER_CLEAR_CACHE}
else
    export DOCKER_CLEAR_CACHE=$3
fi

echo ""
echo "Script $0 is now running - Application: ${APPLICATION}"

export LOG_FILE=run_create_image.log

echo ""
echo "You can find the run log in the file ${LOG_FILE}"
echo ""
echo "Please wait ..."
echo ""

exec &> >(tee -i "${LOG_FILE}") 2>&1
sleep .1

echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"

echo "Create a Docker image for application ${APPLICATION}"

echo "--------------------------------------------------------------------------------"
echo "DOCKER_CLEAR_CACHE : ${DOCKER_CLEAR_CACHE}"
echo "DOCKER_HUB_PUSH    : ${DOCKER_HUB_PUSH}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

if [ "${DOCKER_CLEAR_CACHE}" = "yes" ]; then
    docker builder prune --all --force
fi

echo "Docker stop/rm !APPLICATION! ........................................... before:"
docker ps -a
docker ps    | find "!APPLICATION!" && docker stop !APPLICATION!
docker ps -a | find "!APPLICATION!" && docker rm --force !APPLICATION!
echo "......................................................................... after:"
docker ps -a

docker build --build-arg APP=!APPLICATION! -t ioaero/${APPLICATION} .

docker tag ioaero/${APPLICATION} ioaero/${APPLICATION}

if [ "${DOCKER_HUB_PUSH}" = "yes" ]; then
    docker push ioaero/${APPLICATION}
fi

docker images -q -f "dangling=true" -f "label=autodelete=true"

for IMAGE in $(docker images -q -f "dangling=true" -f "label=autodelete=true")
do
    docker rmi -f ${IMAGE}
done

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"