#!/usr/bin/env python

"""
Author: tmeszaro@redhat.com


Apache generator actor. Uses data from apache_scanner, creates image with
buildah and pushes this image into the specified registrty.


Running the container:

- after pulling image from registry, run:

$ docker run -dt -p HOST_PORT:CONTAINER_PORT IMAGE_ID


Possible improvements:

- build from this? registry.access.redhat.com/rhscl/httpd-24-rhel7
- parse httpd -S or httpd -V to get main config location, so we can run httpd
   with non-standard config location
- copy also other things (like logs, etc.)
- move image pushing into separate actor

"""


import json
import os
import sys
import subprocess
import shlex
from distutils.spawn import find_executable


def find_buildah():
    def _is_valid(path):
        return path and os.path.isfile(path) and os.access(path, os.X_OK)
    path = os.path.abspath('buildah')
    if not _is_valid(path):
        path = find_executable('buildah')
    if not _is_valid(path):
        raise Exception('Could not find a valid buildah binary: %s' % path)
    return path


BUILDAH = find_buildah()


def execute(cmd):
   try:
       return subprocess.check_output(shlex.split(cmd))
   except subprocess.CalledProcessError as e:
       sys.stderr.write(str(e) + '\n')
       return None


def create_httpd_container(image):
    cname = execute('%s from %s' % (BUILDAH, image))
    if not cname:
        raise Exception('Error creating container')
    return cname


def copy_to_container(cname, src, dst):
    if cname and src and dst:
        execute('%s copy %s %s %s' % (BUILDAH, cname, src, dst))


if __name__ == "__main__":
    INPUT = json.load(sys.stdin)
    APACHE_SCANNER = INPUT['apache_scanner'][0]

    registry = INPUT['registry'][0]
    user = registry['user']
    password = registry['password']

    cname = create_httpd_container(image="registry.fedoraproject.org/fedora:26")
    image_uri = registry['address'] + "/" + user + "/" + cname

    execute('%s run %s -- yum update -y' % (BUILDAH, cname))
    execute('%s run %s -- yum install -y httpd' % (BUILDAH, cname))

    ## Install missing modules.
    for module_path in APACHE_SCANNER["LoadModule"]:
        pkg_name = module_path.split('/')[-1].split('.so')[0]
        execute("%s run %s -- yum install -y %s" % (BUILDAH, cname, pkg_name))

    ## Copy configs & data to image.
    for config in APACHE_SCANNER["absolute_path"]:
        copy_to_container(cname, config, config)
    for item in APACHE_SCANNER["DocumentRoot"]:
        copy_to_container(cname, item, item)

    ## Right now, we only run httpd with default httpd.conf location.
    execute('%s config %s --cmd "httpd -DFOREGROUND"' % (BUILDAH, cname))

    port = APACHE_SCANNER['Listen'][0]
    execute('%s config %s --port %s' % (BUILDAH, cname, port))
    execute('%s commit %s %s' % (BUILDAH, cname, image_uri))
    execute('%s push --creds=%s:%s %s %s' % (BUILDAH, user, password, image_uri, image_uri))

    print(json.dumps({'apache_generator': [{'image': cname, 'uri': image_uri, 'port': port}]}))
