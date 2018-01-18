#!/usr/bin/env python

"""
Author: tmeszaro@redhat.com


Apache generator actor. Uses data from apache_scanner, creates image with buildah
and pushes this image into the specified registrty.


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

import dnf


def find_buildah():
    def _is_valid(path):
        return path and os.path.isfile(path) and os.access(path, os.X_OK)
    path = os.path.abspath('buildah')
    if not _is_valid(path):
        path = find_executable('buildah')
    if not _is_valid(path):
        raise Exception('Could not find a valid buildah binary: {0}'.format(path))
    return path

BUILDAH = find_buildah()

def execute(cmd):
    out = subprocess.check_output(shlex.split(cmd))
    return out.strip()

def create_httpd_container():
    cname = execute('{buildah} from fedora'.format(buildah=BUILDAH))
    if not cname:
        raise Exception('Error creating container')
    return cname

def copy_to_container(cname, src, dst):
    if cname and src and dst:
        execute('{buildah} copy {cname} {src} {dst}'.format(
            buildah=BUILDAH,
            cname=cname,
            src=src,
            dst=dst
        ))

def get_container_id(cname):
    cntrs = json.loads(execute('{buildah} containers --json'.format(buildah=BUILDAH)))
    ids = [x['id'].strip() for x in cntrs if x['containername'] == cname]
    if len(ids) != 1:
        raise Exception('Incorrect number of containers with name {0}'.format(cname))
    return ids[0]

if __name__ == "__main__":
    INPUT = json.load(sys.stdin)

    APACHE_SCANNER = INPUT['apache_scanner'][0]
    REGISTRY = INPUT['registry'][0]
    USER = REGISTRY['user']
    PW = REGISTRY['password']
    SOURCE_IMG_NAME = "registry.fedoraproject.org/fedora:26"
    TARGET_REGISTRY = REGISTRY['address']

    cname = execute('%s from %s' % (BUILDAH, SOURCE_IMG_NAME))

    FINAL = TARGET_REGISTRY + "/" + USER + "/" + cname

    execute('%s run %s -- dnf update -y' % (BUILDAH, cname))
    execute('%s run %s -- dnf install -y httpd' % (BUILDAH, cname))

    ## Install missing modules.
    base = dnf.Base()
    base.fill_sack()
    QUERY = base.sack.query()
    for module_path in APACHE_SCANNER["LoadModule"]:
        ## Getting httpd module name from the module file name is probably
        ##  not 100% reliable way to get package name (but it seems to work).
        ## Using "rpm provides" is probaby more reliable, but it requires to
        ##  parse the rpm output (which can be messy).
        pkg_name = "*%s*" % module_path.split('/')[1].split('.')[0]
        result = QUERY.filter(name__glob=pkg_name).run()
        for pkg in result:
            if not pkg.installed:
                execute("%s run %s -- dnf install -y %s" % (BUILDAH, cname, pkg.name))

    ## Copy configs & data to image.
    for config in APACHE_SCANNER["absolute_path"]:
        copy_to_container(cname, config, config)
    for item in APACHE_SCANNER["DocumentRoot"]:
        copy_to_container(cname, item, item)

    ## Right now, we only run httpd with default httpd.conf location.
    execute('%s config %s --cmd "httpd -DFOREGROUND"' % (BUILDAH, cname))

    PORT = APACHE_SCANNER['Listen'][0]
    execute('%s config %s --port %s' % (BUILDAH, cname, PORT))
    execute('%s commit %s %s' % (BUILDAH, cname, FINAL))
    execute('%s push --creds=%s:%s %s %s' % (BUILDAH, USER, PW, FINAL, FINAL))

    print(json.dumps({'apache_generator': [{'image': cname,
                                            'uri': FINAL,
                                            'port': PORT}]}))
