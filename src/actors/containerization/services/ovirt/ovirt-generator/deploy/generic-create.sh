#!/bin/bash

CONTAINER_NAME=$LEAPP_OVIRT_GENERATOR_CURRENT_CONTAINER_NAME
CONTAINER_FILESYSTEM_STAGING=$LEAPP_GENERATOR_FILES_BASE_PATH

logmsg() {
    echo "$@" 1>&2;
}

logmsg "-- REMOVING existing $CONTAINER_NAME"
buildah rm $CONTAINER_NAME 2>&1 > /dev/null
logmsg "-- CREATING new container $CONTAINER_NAME"
buildah from --name $CONTAINER_NAME ovirt-engine-base 1>&2

if [ -f ./deploy/$CONTAINER_NAME/install.sh ]; then
    logmsg "-- ADDING install.sh to $CONTAINER_NAME"
    logmsg buildah add $CONTAINER_NAME ./deploy/$CONTAINER_NAME/install.sh /root/install.sh 1>&2
    buildah add $CONTAINER_NAME ./deploy/$CONTAINER_NAME/install.sh /root/install.sh 1>&2
    logmsg "-- RUNNING install.sh in container $CONTAINER_NAME"
    logmsg buildah run --volume $CONTAINER_FILESYSTEM_STAGING:/staging $CONTAINER_NAME /bin/bash /root/install.sh
    buildah run --volume $CONTAINER_FILESYSTEM_STAGING:/staging $CONTAINER_NAME /bin/bash /root/install.sh 1>&2
fi

if [ -f ./deploy/$CONTAINER_NAME/entrypoint.sh ]; then
    logmsg "-- ADDING entrypoint.sh to $CONTAINER_NAME"
    buildah add $CONTAINER_NAME ./deploy/$CONTAINER_NAME/entrypoint.sh /root/entrypoint.sh 1>&2
    logmsg "-- CONFIG Setting ENTRYPOINT to entrypoint.sh for container $CONTAINER_NAME"
    buildah config --entrypoint /root/entrypoint.sh $CONTAINER_NAME 1>&2
fi

exit 0
