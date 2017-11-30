#!/usr/bin/python
import json
from subprocess import Popen, PIPE

info = {}
checks = {'path': 'which rsync',
          'version': 'rsync --version'}

for check, cmd in checks.items():
    info.update({check: None})
    proc = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    if proc.returncode:
        info[check] = (proc.returncode, err.strip())
    else:
        info[check] = (proc.returncode, out.strip())

print(json.dumps({'rsyncinfo': [info]}))
