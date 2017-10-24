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
    inputs = json.load(sys.stdin)

    cmd = _build_cmd(inputs['container_directory']['value'],
                     inputs['container_name']['value'],
                     inputs['osversion']["version"].split(".")[0],
                     inputs['force_create']['value'],
                     inputs['exposed_ports']['ports'])

    out, err, return_code = _execute(cmd)
    outputs = {
        'container_id': {'value': out},
        'error': {'value': err}
    }
    print(json.dumps(outputs))
    sys.exit(return_code)
