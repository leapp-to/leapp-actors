#!/usr/bin/env python

"""
tmeszaro@redhat.com

This file gets called from the Makefile test target.

It takes care of checking for correct inputs and calls pytest with correct
cmd line arguments.

Particularly, solves the following situation:
- when running:

  $ make test ACTOR=foobar

  - and foobar actor has no tests, we report it back to the user and run no tests.
  - and foobar actor/test file does not even exist, we also report this with error.
"""

import os
import sys
import subprocess


def find_actor_tests(actor):
    """ Checks if the actors exists and has tests. Reports errors otherwise.
    """
    for root, subdirs, _ in os.walk("./src"):
        if actor in subdirs:
            tests_dir = os.path.join(root, actor, 'tests')
            if os.path.isdir(tests_dir):
                for some_file in os.listdir(tests_dir):
                    if 'test' in some_file:
                        return (True, "{ACTOR_NAME} tests found!".format(ACTOR_NAME=actor))
            return (False, "Error: actor \"{ACTOR_NAME}\" is missing tests in the: {TESTS_DIR}".format(
                ACTOR_NAME=actor, TESTS_DIR=tests_dir))
    return (False, "Error: cannot find actor \"{ACTOR_NAME}\"!".format(ACTOR_NAME=actor))


def print_pretty(msg):
    """ Prints msg in a pretty way.
    """
    print("+{STUFF}+\n| {MSG} |\n+{STUFF}+".format(STUFF="-"*(len(msg)+2), MSG=msg))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Need ACTOR= and REPORT= values! This should not happen!")
        sys.exit(1)

    pytest_cmd = ["pytest", "-v"]
    actor_value = sys.argv[1].split('=')[1]
    report_value = sys.argv[2].split('=')[1]

    print('ACTOR=', actor_value)
    print('REPORT=', report_value)

    if actor_value != '':
        passed, status = find_actor_tests(actor_value)
        print_pretty(status)
        if not passed:
            sys.exit(1)
        pytest_cmd += ["-k", "test_schema or {ACTOR}".format(ACTOR=actor_value)]

    if report_value != '':
        pytest_cmd += ["--junit-xml={REPORT}".format(REPORT=report_value)]

    print(pytest_cmd)
    subprocess.call(pytest_cmd)
