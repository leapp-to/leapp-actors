#!/bin/bash

logmsg() {
    echo "$@" 1>&2;
}

CONTAINER_NAME="ovirt-engine-base"

exit 0

logmsg "# CLEANING base image creation reminants"
buildah rmi --force $CONTAINER_NAME 2>&1 > /dev/null ||:
buildah rm $CONTAINER_NAME 2>&1 > /dev/null ||:
logmsg "# CREATING container $CONTAINER_NAME for the base image"
buildah from --pull --name $CONTAINER_NAME centos:7 1>&2
logmsg "# ADDING install.sh to $CONTAINER_NAME"
buildah add $CONTAINER_NAME deploy/install.sh /root/install.sh 1>&2
logmsg "# RUNNING install.sh in $CONTAINER_NAME"
buildah run $CONTAINER_NAME /root/install.sh 1>&2

logmsg "# COMMITTING $CONTAINER_NAME to $CONTAINER_NAME"
buildah commit --rm $CONTAINER_NAME $CONTAINER_NAME 1>&2
