import os
import sys
import json


def readlink(path, filename):
    return os.readlink(os.path.join(path, filename))


def get_environ(pid):
    try:
        with open(os.path.join(pid, 'environ'), 'rb') as f:
            environ = f.read().split("\x00")
    except EnvironmentError as exc:
        sys.stderr.write(str(exc) + "\n")
        return None

    output = {}
    for env in environ:
        if env:
            name, val = env.split('=', 1)
            output[name] = val
    return output


def get_cmdline(pid):
    try:
        with open(os.path.join(pid, 'cmdline'), 'rb') as f:
            return f.read().replace("\x00", " ").strip()
    except EnvironmentError as exc:
        sys.stderr.write(str(exc) + "\n")
        return None


if __name__ == '__main__':
    actor_output = {'process_list': [
        {'processes': []}
    ]}

    root = '/proc'
    cpid = str(os.getpid())

    for directory in os.listdir(root):

        if not directory.isdigit() or directory == cpid:
            continue

        pid = os.path.join(root, directory)
        cmdline = get_cmdline(pid)
        environ = get_environ(pid)

        if cmdline is None or environ is None:
            continue

        actor_output['process_list'][0]['processes'].append({
            "cwd": readlink(pid, "cwd"),
            "exe": readlink(pid, "exe"),
            "environ": environ,
            "cmdline": cmdline
        })

    sys.stdout.write(json.dumps(actor_output))
