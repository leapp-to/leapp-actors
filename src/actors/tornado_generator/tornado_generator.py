import os
import sys
import json
import re
import subprocess


def _execute(cmd, **kwds):
    try:
        return subprocess.check_output(cmd, shell=True, **kwds)
    except OSError as exc:
        sys.stderr.write(str(exc) + '\n')
        return None


def extract_tornado_apps(params):
    try:
        return params['tornado_apps'][0]['apps']
    except LookupError:
        sys.stderr.write("Invalid tornado_apps structure, could not find inside params")
        return None


def get_img_path(python_exec):
    res = re.search("\d\.?\d?$", tornado_app['python_exec'])
    py_version = 2 if res is None else int(res.group())

    if py_version < 3:
        py_img = 'python-27-rhel7'
    else:
        py_img = 'python-36-rhel7'

    return os.path.join('registry.access.redhat.com/rhscl', py_img)


def create_requirements_file(virtual_env_path, project_path):
    activate_path = os.path.join(virtual_env_path, 'bin/activate')
    req_path = os.path.join(project_path, 'requirements.txt')
    return _execute('source {} && pip freeze > {}'.format(activate_path, req_path), executable='/bin/bash')


def build_img(project_path, base_img):
    # build img requires s2i from OpenShift
    # https://docs.openshift.com/enterprise/3.0/creating_images/s2i.html
    out_img = base_img + '-tornado-app'
    res =_execute(
        's2i build -c {path} {img} {out_img}'.format(
            path=project_path,
            img=base_img,
            out_img=out_img
        )
    )
    return out_img if res is not None else None


def run_container(img, entry_point):
    # run tornado container and expose random port
    return _execute(
        'docker run -e APP_FILE={entry} -p 8080 -itd {img}'.format(
            entry=entry_point,
            img=img
        )
    )


if __name__ == '__main__':
    params = {} if os.isatty(sys.stdin.fileno()) else json.load(sys.stdin)
    tornado_apps = extract_tornado_apps(params)
    if tornado_apps is None:
        sys.exit(1)

    for tornado_app in tornado_apps:
        py_img = get_img_path(tornado_app['python_exec'])

        # if there is virtual env then prepare requirements.txt file (if exists - replace)
        if tornado_app['virtual_env_path'] is not None:
            if create_requirements_file(tornado_app['virtual_env_path'], tornado_app['project_path']) is None:
                continue

        # build docker image with tornado application
        img = build_img(tornado_app['project_path'], py_img)
        if img is None:
            continue

        # start docker container with tornado application
        run_container(img, tornado_app['main_file'])
