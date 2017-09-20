#!/usr/bin/python

import json
import os
import sys
from subprocess import Popen, PIPE

LEAPP_CONTAINER_DIRECTORY = '/var/lib/leapp/macrocontainers'


info = {}
checks = {'dockerinfo': {'path': 'which docker',
                         'systemd_state': 'systemctl show --property ActiveState docker',
                         'info': 'docker info'},
          'rsyncinfo': {'path': 'which rsync', 'version': 'rsync --version'}}

for group in checks.keys():
    info[group] = {}
    for check, cmd in checks[group].items():
        proc = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        if proc.returncode:
            info[group][check] = (proc.returncode, err.strip())
        else:
            info[group][check] = (proc.returncode, out.strip())

proc = Popen(["docker", "ps", "-a", "--format", "{{.Names}}"], stdout=PIPE, stderr=PIPE)
out, _ = proc.communicate()
containers = out.split()
if os.path.isdir(LEAPP_CONTAINER_DIRECTORY):
    _, directories, _ = os.walk(LEAPP_CONTAINER_DIRECTORY).next()
    containers += directories

containers = list(set(containers))
containers.sort()

info["containerslist"] = {"containers": containers}
sys.stdout.write(json.dumps(info))
