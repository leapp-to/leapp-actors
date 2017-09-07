import sys
import json
import shlex
from subprocess import Popen, PIPE


def _execute(cmd):
    return Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE).communicate()


def _build_cmd(source_path, name, img, init_bin, exposed_ports):
    good_mounts = ['bin', 'etc', 'home', 'lib', 'lib64', 'media',
                   'opt', 'root', 'sbin', 'srv', 'usr', 'var']

    cmd = 'docker create --restart always -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro'

    for mount in good_mounts:
        cmd += ' -v {d}/{m}:/{m}:Z'.format(d=source_path, m=mount)

    for port in exposed_ports:
        if not port.get('exposed_port'):
            cmd += ' -p {:d}/{p}'.format(port['port'], p=port['protocol'])
        else:
            cmd += ' -p {:d}:{:d}/{p}'.format(port['exposed_port'], port['port'], p=port['protocol'])

    cmd += ' --name ' + name + ' ' + img + ' ' + init_bin

    return cmd


if __name__ == "__main__":
    inputs = json.load(sys.stdin)

    cmd = _build_cmd(inputs['container_directory']['value'],
                     inputs['container_name']['value'],
                     inputs['image']['value'],
                     inputs['init_bin']['value'],
                     inputs['exposed_ports']['ports'])

    out, err = _execute(cmd)
    outputs = {
        'container_id': dict(value=out),
        'error': dict(value=err)
    }
    print(json.dumps(outputs))
