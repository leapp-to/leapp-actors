#!/bin/bash

ENABLED_UNITS=$(systemctl list-unit-files | grep enabled | cut -f1 -d\  | grep -e ovirt -e postgres -e httpd)
for UNIT in $ENABLED_UNITS; do
    UNIT_PATH=$(systemctl show -p FragmentPath $UNIT  | cut -d= -f2)
    RPM=$(rpm -qf $UNIT_PATH --queryformat="\"name\": \"%{name}\", \"version\": \"%{version}\"")
    echo "{\"service\": \"$UNIT\", \"rpm\": {$RPM}}"
done;


