#!/usr/bin/python

import os
import subprocess
import sys

from leapp.actor import actorize
from leapp.actor.filesystem import FSRegistry


def run_process(*args, **kwargs):
    proc = subprocess.Popen(*args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        **kwargs)
    stdout, stderr = proc.communicate()
    if '--debug' in sys.argv:
        sys.stderr.write(stderr + '\n')
    return stdout, stderr, proc.returncode


def get_container_id(container_name):
    container_id, _, _ = run_process(['buildah', 'inspect', '-f', '{{.ContainerID}}', container_name])
    return container_id or ''



def create_service_container(container_name):
    os.environ['LEAPP_OVIRT_GENERATOR_CURRENT_CONTAINER_NAME'] = container_name
    out, err, code = run_process(['/bin/bash', 'deploy/{}/create.sh'.format(container_name)])
    if code:
        return {
            'container_name': container_name,
            'errors': [{
                "message": err}]}
    return {
        'container_name': container_name,
        'container_id': get_container_id(container_name)}


@actorize(
    name='ovirt-generator',
    description='Generates an orchestrated set of oVirt engine service containers',
    inputs={'ovirt_scan_result': 'OVirtScanResult'},
    outputs={'ovirt_container': 'OVirtContainer'},
    tags=('containerization',)
)
def ovirt_actor(channels):
    fsreg = FSRegistry(channels)
    fsnode = fsreg.fetch_node('ovirt')
    base_path = fsnode.get_base_path()
    os.environ['LEAPP_GENERATOR_FILES_BASE_PATH'] = base_path
    run_process(['/bin/bash', './deploy/create-base-image.sh'])

    scan_result = channels.ovirt_scan_result.pop()
    container_names = {
        'engine': 'ovirt-engine',
        'imageio': 'ovirt-imageio-proxy',
        'websocket': 'ovirt-websocket-proxy',
        'vmconsole': 'ovirt-vmconsole-proxy',
        'dwh': 'ovirt-dwh'
    }
    for service, container_name in container_names.items():
        if scan_result.get(service):
            message = create_service_container(container_name)
            channels.ovirt_container.push(message)
