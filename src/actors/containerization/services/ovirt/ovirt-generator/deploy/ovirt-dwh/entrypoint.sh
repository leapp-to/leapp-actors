#!/bin/bash

exec su -m -s /usr/bin/python ovirt /usr/share/ovirt-engine-dwh/services/ovirt-engine-dwhd/ovirt-engine-dwhd.py --redirect-output start
