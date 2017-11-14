import os
import sys
import json

def readlink(path, filename):
    return os.readlink(os.path.join(path, filename))

output = {'process_list': [
    {'processes': []}
]}

root = '/proc'
pid = str(os.getpid())

params = {}
if not sys.stdin.isatty():
    params = json.load(sys.stdin)

for directory in os.listdir(root):
    if not directory.isdigit():
        continue
    if directory == pid:
        continue

    proc_dir = os.path.join(root, directory)
    try:
        with open(os.path.join(proc_dir, 'cmdline'), 'rb') as f:
            cmdline = f.read().replace("\x00", " ").strip()

        with open(os.path.join(proc_dir, 'environ'), 'rb') as f:
            environ_output = {}
            environ = f.read().split("\x00")
            for env in environ:
                if env:
                    name, val = env.split('=', 1)
                    environ_output[name] = val

        if params is not None and not str(params.get('filter', '')) in cmdline:
            continue

        output['process_list'][0]['processes'].append({
            "cwd": readlink(proc_dir, "cwd"),
            "exe": readlink(proc_dir, "exe"),
            "environ": environ_output,
            "cmdline": cmdline
        })
    except (OSError, IOError) as exc:
        sys.stderr.write(str(exc) + "\n")

sys.stdout.write(json.dumps(output))
