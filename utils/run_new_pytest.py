#!/usr/bin/env python

"""
tmeszaro@redhat.com

This file gets called from the Makefile test_new target.

It takes care of checking for correct inputs and calls pytest with correct
cmd line arguments.

Particularly, solves the following situation:
- when running:

  $ make test ACTOR=foobar

  - foobar actor does not even exist, we also report this with error.
  - foobar actor has no tests, we report it back to the user and run no tests.
"""

import argparse
import os
import subprocess
import sys

from leapp.repository.scan import scan_repo

BASE_REPO = "repos"
REPOS = ["common", "containerization", "upgrade"]

def get_actor_tests(actor_name):
    """ Checks if the actors exists and has tests. Reports errors otherwise.

    Returns (list of actor test directories | None, status message)
    """
    for repo in REPOS:
        repository = scan_repo(BASE_REPO + "/" + repo)
        repository.load()
        actor = repository.lookup_actor(actor_name)
        if not actor:
            return (None, "Error: cannot find actor \"{ACTOR_NAME}\"!".format(ACTOR_NAME=actor_name))
        if not actor.tests:
            return (None, "Error: actor \"{ACTOR_NAME}\" is missing tests!".format(ACTOR_NAME=actor_name))
        testdirs = []
        for testdir in actor.tests:
            testdirs.append(os.path.join(BASE_REPO, repo, actor.directory, testdir))
        return (testdirs, "{ACTOR_NAME} tests found!".format(ACTOR_NAME=actor_name))
    return (None, "Error: WAT?!")

def print_pretty(msg):
    """ Prints msg in a pretty way.
    """
    print("+{STUFF}+\n| {MSG} |\n+{STUFF}+".format(STUFF="-"*(len(msg)+2), MSG=msg))

if __name__ == "__main__":
    pytest_cmd = ["pytest", "-v", BASE_REPO]

    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", help="name of the actor for which to run tests")
    parser.add_argument("--report", help="filepath where to save report")
    args = parser.parse_args()

    if args.actor:
        testdirs, status = get_actor_tests(args.actor)
        print_pretty(status)
        if not testdirs:
            sys.exit(1)
        formatted_testdirs = " ".join(testdirs)
        pytest_cmd += ["{TESTDIRS}".format(TESTDIRS=formatted_testdirs)]

    if args.report:
        pytest_cmd += ["--junit-xml={REPORT}".format(REPORT=args.report)]

    print(pytest_cmd)
    exit(subprocess.call(pytest_cmd))
