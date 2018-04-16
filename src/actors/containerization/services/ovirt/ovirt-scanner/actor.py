#!/usr/bin/python

import json
import subprocess

from leapp.actor import actorize
from leapp.actor.filesystem import FSRegistry


def run_process(*args, **kwargs):
    proc = subprocess.Popen(*args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        **kwargs)
    stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode


@actorize(
    name='ovirt-scanner',
    description='Scan for oVirt and related services',
    outputs={'ovirt_scan_result': 'OVirtScanResult'},
    tags=('containerization',)
)
def ovirt_scanner(channels):
    stdout, _, rcode = run_process(["./scan.sh"])
    if not rcode:
        fsnode = FSRegistry(channels).create_node('ovirt')
        fsnode.add_directory('/etc/ovirt-engine')
        fsnode.add_directory('/etc/ovirt-engine-dwh')
        fsnode.add_directory('/etc/ovirt-engine-metrics')
        fsnode.add_directory('/etc/ovirt-engine-setup.conf.d')
        fsnode.add_directory('/etc/ovirt-host-deploy.conf.d')
        fsnode.add_directory('/etc/ovirt-imageio-proxy')
        fsnode.add_directory('/etc/ovirt-vmconsole')
        fsnode.add_directory('/etc/ovirt-web-ui')

        services = [json.loads(line) for line in stdout.strip().split('\n') if line.strip()]
        unit_names = set([svc['service'] for svc in services])
        channels.ovirt_scan_result.push({
            'services': services,
            'engine': 'ovirt-engine.service' in unit_names,
            'dwh': 'ovirt-engine-dwhd.service' in unit_names,
            'imageio': 'ovirt-imageio-proxy.service' in unit_names,
            'websocket': 'ovirt-websocket-proxy.service' in unit_names,
            'vmconsole': 'ovirt-vmconsole-proxy-sshd.service' in unit_names
        })
