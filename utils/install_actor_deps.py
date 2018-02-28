#!/usr/bin/python

"""
Script for installing dependencies for specific actor.
It is called from Makefile install-deps target if actor is specified.
If given actor does not exists or does not have Makefile,
this is reported and script exits with return code 1.

usage: python install_actor_deps.py ACTOR
"""

import sys
import os
from subprocess import check_call, CalledProcessError


def error(msg, rc):
    sys.stderr.write(msg)
    sys.exit(rc)


def install_deps(path):
    cmd = "make -f {} install-deps".format(path)
    try:
        check_call(cmd, shell=True)
    except CalledProcessError as e:
        error(str(e)+'\n', e.returncode)


def find_actor_makefile(actor):
    for root, dirs, files in os.walk('./src/actors'):
        if actor in dirs:
            makefile_path = os.path.join(root, actor, 'Makefile')
            if os.path.isfile(makefile_path):
                return True, "Found Makefile for actor '{}'.".format(actor), makefile_path
            return False, "Actor '{}' doesn't have Makefile!\n".format(actor), None
    return False, "Actor '{}' doesn't exist!\n".format(actor), None


if __name__ == "__main__":
    try:
        actor = sys.argv[1]
    except IndexError:
        error("Missing actor name!\nusage: python install_actor_deps.py ACTOR\n", 1)

    passed, status, path = find_actor_makefile(actor)
    if not passed:
        error(status, 1)

    print(status)
    install_deps(path)
