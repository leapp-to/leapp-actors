#!/bin/bash
[[ -f /sbin/leapp-init-prepare ]] && /bin/bash /sbin/leapp-init-prepare
SERVICE_NAME=$1.service
SVCTYPE=$(grep ^Type= `find /etc/systemd/system -name $SERVICE_NAME` | cut -d= -f2-)
SERVICE_USER=$(grep ^User= `find /etc/systemd/system -name $SERVICE_NAME` | cut -d= -f2-)
if [[ ! -z "$SERVICE_USER" ]] && [[ "$SERVICE_USER" != "$USER" ]]; then
        echo $SERVICE_USER;
        sudo -u $SERVICE_USER /sbin/leapp-init $1;
        exit $?;
fi
eval $(grep ^Environment= `find /etc/systemd/system -name $SERVICE_NAME` | cut -d= -f2-)
for EFILE in $(grep ^EnvironmentFile= `find /etc/systemd/system -name $SERVICE_NAME` | cut -d= -f2-); do
        EFILE=$(echo $EFILE | sed "s/^-//");
        if [ -f $EFILE ]; then
                source $EFILE;
        fi
done;
rm -f /tmp/leappd-init.notify;

python -c "import os, socket; s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM); s.bind('/tmp/leappd-init.notify'); os.chmod('/tmp/leappd-init.notify', 0777); s.recv(1024)" &

export NOTIFY_SOCKET=/tmp/leappd-init.notify;
eval $(grep ^ExecStartPre= `find /etc/systemd/system -name $SERVICE_NAME` | cut -d= -f2-);
eval $(grep ^ExecStart= `find /etc/systemd/system -name $SERVICE_NAME` | cut -d= -f2-);
[[ "$SVCTYPE" == "forking" ]] && /usr/bin/sleep infinity;

