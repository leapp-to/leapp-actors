#!/bin/bash

yum install http://resources.ovirt.org/pub/yum-repo/ovirt-release41.rpm -y
yum update -y
yum install ovirt-engine sudo -y
rm /root/install.sh
