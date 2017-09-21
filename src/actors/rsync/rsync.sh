SOURCE_HOST=$1
SOURCE_USER=$2
TARGET_HOST=$3
TARGET_USER=$4
STORAGE_PATH=$5
EXCLUDED_PATHS=$6

# Check path
if [ -z $STORAGE_PATH ]; then
    >&2 echo "Storage path must be set"
    exit 1
fi

set -f
EXCLUDED_PATHS=$(echo $EXCLUDED_PATHS | tr ',' "\n" | sed -e 's/^\s*\(.*\)\s*$/\1/')
EXCLUDE_OPTIONS=""

for path in $EXCLUDED_PATHS; do
    EXCLUDE_OPTIONS="--exclude=$path $EXCLUDE_OPTIONS"
done

# Setting up the SSH options parameter
if [ ! -z $SSH_OPTIONS ]; then
    SSH_OPTIONS=" -o $SSH_OPTIONS" 
fi

rsync -aAX -r $EXCLUDE_OPTIONS ${SOURCE_USER}@${SOURCE_HOST}:/ $STORAGE_PATH

# In case of a remote target
if [ "localhost" != $TARGET_HOST ] && [ "127.0.0.1" != $TARGET_HOST ]; then
  rsync -aAX -r ${STORAGE_PATH}/ ${TARGET_USER}@${TARGET_HOST}:${STORAGE_PATH}/
fi
exit 0;
