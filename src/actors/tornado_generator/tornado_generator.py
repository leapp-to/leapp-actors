import os
import sys
import json
import re
import subprocess


params = {} if os.isatty(sys.stdin.fileno()) else json.load(sys.stdin)
tornado_apps = params['tornado_apps'][0]['apps']

for tornado_app in tornado_apps:

    res = re.search("\d\.?\d?$", tornado_app['python_exec'])
    py_version = 2 if res is None else int(res.group())
    py_img = 'registry.access.redhat.com/rhscl/'

    if py_version < 3:
        py_img += 'python-27-rhel7'
    else:
        py_img += 'python-36-rhel7'

    if tornado_app['virtual_env_path'] is not None:
        activate_path = os.path.join(tornado_app['virtual_env_path'], 'bin/activate')
        req_path = os.path.join(tornado_app['project_path'], 'requirements.txt')
        subprocess.call(
            'source {} && pip freeze > {}'.format(activate_path, req_path),
            shell=True,
            executable='/bin/bash'
        )

    # get the project name from end
    ex_code = subprocess.call('s2i build -c {} {} py-{}-tornado-app'.format(tornado_app['project_path'], py_img, py_version), shell=True)
    if ex_code == 0:
        subprocess.call('docker run -e APP_FILE={} -p 8080 -itd py-{}-tornado-app'.format(tornado_app['main_file_name'], py_version), shell=True)

