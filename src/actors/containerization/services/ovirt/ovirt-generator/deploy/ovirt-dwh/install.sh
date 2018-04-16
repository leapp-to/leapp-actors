#!/usr/bin/bash


rm -rf /etc/ovirt-engine
rm -rf /etc/pki/ovirt-engine
rm -rf /etc/ovirt-engine-dwh/
cp -a /staging/etc/ovirt-engine /etc
cp -a /staging/etc/pki/ovirt-engine /etc/pki/ovirt-engine
cp -a /staging/etc/ovirt-engine-dwh/ /etc/ovirt-engine-dwh/
