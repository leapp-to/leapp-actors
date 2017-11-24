import json
import os
from subprocess import Popen, PIPE


def run_cmd(cmd):
    proc = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return (proc.returncode, out, err)


containerslist = {'retcode': None,
                  'containers': []}

retcode, out, err = run_cmd('docker ps -a --format {{.Names}}')

containerslist['retcode'] = retcode
if retcode == 0:
    containerslist['containers'] = out.splitlines()

macrocontainers = '/var/lib/leapp/macrocontainers/'
if os.path.isdir(macrocontainers):
    _, directories, _ = os.walk(macrocontainers).next()
    containerslist['containers'].extend(directories)

containerslist['containers'] = list(set(containerslist['containers']))
print(json.dumps({'containerslist': [containerslist]}))
