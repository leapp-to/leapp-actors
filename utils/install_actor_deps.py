#!/usr/bin/python

"""
Script for installing dependencies for specific actor.
It is called from Makefile install-deps target.
If given actor does not exists or does not have Makefile,
this is reported and script exits with return code 1.
If no actor is specified dependencies will be installed for all actors with Makefile.

usage: python install_actor_deps.py [ACTOR]
"""

import argparse
import os
import sys
from subprocess import check_call, CalledProcessError


def error(msg, rc):
    sys.stderr.write(msg)
    sys.exit(rc)


def install(path):
    cmd = "make -f {} install-deps".format(path)
    try:
        check_call(cmd, shell=True)
    except CalledProcessError as e:
        error(str(e)+'\n', e.returncode)


def install_actor_deps(actor, directory):
    for root, dirs, files in os.walk(directory):
        if actor in dirs:
            makefile_path = os.path.join(root, actor, 'Makefile')
            if os.path.isfile(makefile_path):
                install(makefile_path)
                return
            error("Actor '{}' doesn't have Makefile!\n".format(actor), 1)
    error("Actor '{}' doesn't exist!\n".format(actor), 1)


def install_all_deps(directory):
    for root, dirs, files in os.walk(directory):
        if 'Makefile' in files:
            install(os.path.join(root, 'Makefile'))


if __name__ == "__main__":
    ACTORS_DIR = './src/actors'

    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", help="name of the actor for which to install dependencies")
    args = parser.parse_args()

    if args.actor:
        install_actor_deps(args.actor, ACTORS_DIR)
    else:
        install_all_deps(ACTORS_DIR)
