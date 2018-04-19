#!/bin/bash

exec su -m -s /bin/bash ovirt-vmconsole /usr/libexec/ovirt-vmconsole-proxy-sshd -f /usr/share/ovirt-vmconsole/ovirt-vmconsole-proxy/ovirt-vmconsole-proxy-sshd/sshd_config
