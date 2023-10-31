#!/bin/zsh

set -e

# ------------------------------------------------------------------------------
#
# run_create_image.zsh: Create a Docker image.
#
# ------------------------------------------------------------------------------

export APPLICATION_DEFAULT=ae1982
export DOCKER_CLEAR_CACHE_DEFAULT=yes
export DOCKER_HUB_PUSH_DEFAULT=yes
export IO_AERO_STREAMLIT_SERVER_PORT=8501
export MODE=n/a

if [[ -z "$1" ]]; then
    print "\n========================================================="
    print "\nall      - All Streamlit applications"
    print "\n---------------------------------------------------------"
    print "\nae1982  - Aircraft Accidents in the US since 1982"
    print "\npd1982  - Profiling Data for the US since 1982"
    print "\nslara   - Association Rule Analysis"
    print "\n---------------------------------------------------------"
    read "APPLICATION?Enter the desired application name [default: ${APPLICATION_DEFAULT}] "
    APPLICATION="${APPLICATION:-$APPLICATION_DEFAULT}"
    export APPLICATION
else
    export APPLICATION=$1
fi

if [[ -z "$2" ]]; then
    read "DOCKER_HUB_PUSH?Push image to Docker Hub (yes / no) [default: ${DOCKER_HUB_PUSH_DEFAULT}] "
    DOCKER_HUB_PUSH="${DOCKER_HUB_PUSH:-$DOCKER_HUB_PUSH_DEFAULT}"
    export DOCKER_HUB_PUSH
else
    export DOCKER_HUB_PUSH=$2
fi

if [[ -z "$3" ]]; then
    read "DOCKER_CLEAR_CACHE?Clear Docker cache (yes / no) [default: ${DOCKER_CLEAR_CACHE_DEFAULT}] "
    DOCKER_CLEAR_CACHE="${DOCKER_CLEAR_CACHE:-$DOCKER_CLEAR_CACHE_DEFAULT}"
    export DOCKER_CLEAR_CACHE
else
    export DOCKER_CLEAR_CACHE=$3
fi

print "\n"
print "\nScript $0 is now running - Application: ${APPLICATION}"

export LOG_FILE=run_create_image.log

print "\n"
print "\nYou can find the run log in the file ${LOG_FILE}"
print "\n"
print "\nPlease wait ..."
print "\n"

exec &> >(tee -i "${LOG_FILE}") 2>&1
sleep .1

print "\n================================================================================"
print "\nStart $0"
print "\n--------------------------------------------------------------------------------"

print "\nCreate a Docker image for application ${APPLICATION}"

print "\n--------------------------------------------------------------------------------"
print "\nDOCKER_CLEAR_CACHE       : ${DOCKER_CLEAR_CACHE}"
print "\nDOCKER_HUB_PUSH          : ${DOCKER_HUB_PUSH}"
print "\nSTREAMLIT_SERVER_PORT    : ${IO_AERO_STREAMLIT_SERVER_PORT}"
print "\n--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n================================================================================"

if [[ "${APPLICATION}" = "all" ]]; then
    ( ./scripts/run_create_image.sh ae1982  "${DOCKER_HUB_PUSH}" "${DOCKER_CLEAR_CACHE}" )
    ( ./scripts/run_create_image.sh pd1982  "${DOCKER_HUB_PUSH}" "${DOCKER_CLEAR_CACHE}" )
    ( ./scripts/run_create_image.sh slara   "${DOCKER_HUB_PUSH}" "${DOCKER_CLEAR_CACHE}" )
    return
fi

rm -rf tmp/upload
mkdir -p tmp/upload

rm -rf tmp/docs/img
mkdir -p tmp/docs/img

if [[ "${DOCKER_CLEAR_CACHE}" = "yes" ]]; then
    docker builder prune --all --force
fi

print "\nDocker stop/rm ${APPLICATION} ................................ before containers:"
docker ps -a
docker ps    | grep "${APPLICATION}" && docker stop       "${APPLICATION}"
docker ps -a | grep "${APPLICATION}" && docker rm --force "${APPLICATION}"
print "\n............................................................. after containers:"
docker ps -a
print "\n............................................................. before images:"
docker image ls
docker image ls | grep "${APPLICATION}" && docker rmi --force ioaero/"${APPLICATION}"
print "\n............................................................. after images:"
docker image ls

if [[ "${APPLICATION}" = "ae1982" ]]; then
    export MODE=Std
fi

docker build --build-arg APP="${APPLICATION}" \
             --build-arg MODE=${MODE} \
             --build-arg SERVER_PORT=${IO_AERO_STREAMLIT_SERVER_PORT} \
             -t ioaero/"${APPLICATION}" .

docker tag ioaero/"${APPLICATION}" ioaero/"${APPLICATION}"

if [[ "${DOCKER_HUB_PUSH}" = "yes" ]]; then
    docker push ioaero/"${APPLICATION}"
fi

docker images -q -f "dangling=true" -f "label=autodelete=true"

for IMAGE in $(docker images -q -f "dangling=true" -f "label=autodelete=true")
do
    docker rmi -f "${IMAGE}"
done

rm -rf tmp/upload
rm -rf tmp/docs/img

print "\n"
print "\n--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
print "\n--------------------------------------------------------------------------------"
print "\nEnd   $0"
print "\n================================================================================"
