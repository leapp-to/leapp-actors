import os
import sys
import json


def readlink(path, filename):
    return os.readlink(os.path.join(path, filename))


def get_environ(pid):
    output = {}
    with open(os.path.join(pid, 'environ'), 'rb') as f:
        environ = f.read().split("\x00")
        for env in environ:
            if env:
                name, val = env.split('=', 1)
                output[name] = val
    return output


def get_cmdline(pid):
    cmdline = None
    with open(os.path.join(pid, 'cmdline'), 'rb') as f:
        cmdline = f.read().replace("\x00", " ").strip()
    return cmdline


if __name__ == '__main__':
    params = {} if sys.stdin.isatty() else json.load(sys.stdin)

    actor_output = {'process_list': [
        {'processes': []}
    ]}

    root = '/proc'
    cpid = str(os.getpid())

    for directory in os.listdir(root):

        if not directory.isdigit():
            continue
        if directory == cpid:
            continue

        pid = os.path.join(root, directory)
        try:
            cmdline = get_cmdline(pid)
            environ = get_environ(pid)
        except (OSError, IOError) as exc:
            sys.stderr.write(str(exc) + "\n")
            continue

        if params is not None and not str(params.get('filter', '')) in cmdline:
            continue

        actor_output['process_list'][0]['processes'].append({
            "cwd": readlink(pid, "cwd"),
            "exe": readlink(pid, "exe"),
            "environ": environ,
            "cmdline": cmdline
        })

    sys.stdout.write(json.dumps(actor_output))
