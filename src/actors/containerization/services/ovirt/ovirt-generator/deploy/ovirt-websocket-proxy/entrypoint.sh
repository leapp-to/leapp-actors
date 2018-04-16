#!/bin/bash

exec su -m -s /usr/bin/python ovirt /usr/share/ovirt-engine/services/ovirt-websocket-proxy/ovirt-websocket-proxy.py start
