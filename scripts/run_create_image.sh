#!/bin/bash

set -e

# ------------------------------------------------------------------------------
#
# run_create_image.sh: Create a Docker image.
#
# ------------------------------------------------------------------------------

export APPLICATION_DEFAULT=stats
export DOCKER_CLEAR_CACHE_DEFAULT=yes
export DOCKER_HUB_PUSH_DEFAULT=yes
export IO_AVSTATS_STREAMLIT_SERVER_PORT=8501
export MODE=n/a

if [ -z "$1" ]; then
    echo "========================================================="
    echo "all      - All Streamlit applications"
    echo "---------------------------------------------------------"
    echo "ae1982 - Aircraft Accidents in the US since 1982"
    echo "pd1982 - Profiling Data for the US since 1982"
    echo "stats  - Aircraft Accidents in the US since 1982 - limited"
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
echo "DOCKER_CLEAR_CACHE       : ${DOCKER_CLEAR_CACHE}"
echo "DOCKER_HUB_PUSH          : ${DOCKER_HUB_PUSH}"
echo "STREAMLIT_SERVER_PORT    : ${IO_AVSTATS_STREAMLIT_SERVER_PORT}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

if [ "${APPLICATION}" = "all" ]; then
    ( ./scripts/run_create_image.sh ae1982 ${DOCKER_HUB_PUSH} ${DOCKER_CLEAR_CACHE} )
    ( ./scripts/run_create_image.sh pd1982 ${DOCKER_HUB_PUSH} ${DOCKER_CLEAR_CACHE} )
    ( ./scripts/run_create_image.sh slara  ${DOCKER_HUB_PUSH} ${DOCKER_CLEAR_CACHE} )
    ( ./scripts/run_create_image.sh stats  ${DOCKER_HUB_PUSH} ${DOCKER_CLEAR_CACHE} )
    goto END_OF_SCRIPT
else
    if [ "${APPLICATION}" = "stats" ]; then
        export MODE=Ltd
        copy -i src/ioavstats/ae1982.py src/ioavstats/stats.py
    fi
    if [ "${DOCKER_CLEAR_CACHE}" = "yes" ]; then
        docker builder prune --all --force
    fi
fi

echo "Docker stop/rm ${APPLICATION} ................................ before containers:"
docker ps -a
docker ps    | find "${APPLICATION}" && docker stop ${APPLICATION}
docker ps -a | find "${APPLICATION}" && docker rm --force ${APPLICATION}
echo "............................................................. after containers:"
docker ps -a
echo "............................................................. before images:"
docker image ls
docker image ls | find "${APPLICATION}" && docker rmi --force ioaero/${APPLICATION}
echo "............................................................. after images:"
docker image ls

if [ "${APPLICATION}" = "ae1982" ]; then
    export MODE=Std
fi

docker build --build-arg APP=${APPLICATION} \
             --build-arg MODE=${MODE} \
             --build-arg SERVER_PORT=${IO_AVSTATS_STREAMLIT_SERVER_PORT} \
             -t ioaero/${APPLICATION} .

docker tag ioaero/${APPLICATION} ioaero/${APPLICATION}

if [ "${DOCKER_HUB_PUSH}" = "yes" ]; then
    docker push ioaero/${APPLICATION}
fi

docker images -q -f "dangling=true" -f "label=autodelete=true"

for IMAGE in $(docker images -q -f "dangling=true" -f "label=autodelete=true")
do
    docker rmi -f ${IMAGE}
done

if [ "${APPLICATION}" = "stats" ]; then
    rm -f src/ioavstats/stats.py
fi

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
