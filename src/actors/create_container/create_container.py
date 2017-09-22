#!/usr/bin/python
import sys
import json
import shlex
from subprocess import Popen, PIPE


def _execute(cmd):
    p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out, err, p.returncode


def _build_cmd(source_path, name, version, force, exposed_ports):
    good_mounts = ['bin', 'etc', 'home', 'lib', 'lib64', 'media',
                   'opt', 'root', 'sbin', 'srv', 'usr', 'var']

    if force:
        _execute('sudo docker rm -f {}'.format(name))

    cmd = 'sudo docker create --restart always -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro'

    for mount in good_mounts:
        cmd += ' -v {d}/{m}:/{m}:Z'.format(d=source_path, m=mount)

    for port in exposed_ports:
        if not port.get('exposed_port'):
            cmd += ' -p {:d}/{p}'.format(port['port'], p=port['protocol'])
        else:
            cmd += ' -p {:d}:{:d}/{p}'.format(port['exposed_port'], port['port'], p=port['protocol'])

    cmd += ' --name ' + name + ' leapp/leapp-scratch:' + version + ' /.leapp/leapp-init'

    return cmd


if __name__ == "__main__":
    cmd = _build_cmd(json.loads(sys.argv[1])['value'],
                     json.loads(sys.argv[2])['value'],
                     json.loads(sys.argv[3])["version"].split(".")[0],
                     json.loads(sys.argv[5])['value'],
                     json.loads(sys.argv[4])['ports'])

    out, err, return_code = _execute(cmd)
    outputs = {
        'container_id': dict(value=out),
        'error': dict(value=err)
    }
    print(json.dumps(outputs))
    sys.exit(return_code)
