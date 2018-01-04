import json
import sys
import os
from subprocess import check_output, CalledProcessError
from jinja2 import Template


def _execute(cmd, **kwargs):
    try:
        return check_output(cmd, shell=True, **kwargs)
    except CalledProcessError as e:
        sys.stderr.write(str(e)+'\n')
        return None


def build_base_image(version):
    path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(path, 'Dockerfile.j2'), 'r') as f:
        template = Template(f.read())

    dockerfile = template.render(version=version)
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(dockerfile)

    cmd = 'docker build -t wp-base ' + path
    _execute(cmd)


def build_container(directory, version):
    name = 'wp-'+version
    cmd = 's2i build {directory} wp-base {name}'.format(directory=directory, name=name)
    ret = _execute(cmd)
    return name if ret else None


def run_container(name):
    cmd = 'docker run -d -p 8080:8080 --name wordpress ' + name
    _execute(cmd)


if __name__ == "__main__":
    inputs = json.load(sys.stdin)
    version = inputs["wordpress_version"][0]["value"]
    root_directory = inputs["wordpress_root_directory"][0]["value"]
    db_host = inputs["database_host"][0]["value"]

    if db_host in ['127.0.0.1', 'localhost']:
        raise Exception('Wordpress with DB on localhost is not supported')

    build_base_image(version)
    container_name = build_container(root_directory, version)
    if container_name:
        run_container(container_name)
    else:
        raise Exception('Failed to create container')