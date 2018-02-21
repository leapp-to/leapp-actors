#!/usr/bin/env python

import os
import sys

TRUE = 0
FALSE = 1

print(sys.argv)
if len(sys.argv) != 2:
    sys.exit(1)

def tests_present(actor):
    """
    - actor foobar has no tests, there is no feedback to the user, framework
       just silently ends. We want to tell the user that there are missing
       tests
    - when running $ make test ACTOR=foobar, and foobar actor has no tests,
       report this back to user with warning/error
    """
    actor_dir = './src'
    test_sign = 'test'

    for root, subdirs, files in os.walk(actor_dir):
        if actor in subdirs:
            actor_dir = os.path.join(root, actor)
            tests_dir = os.path.join(actor_dir, 'tests')
            print tests_dir

            if os.path.isdir(tests_dir)and len(os.listdir(tests_dir)) > 0:
                for i in os.listdir(tests_dir):
                    if test_sign in i:
                        return TRUE
    return FALSE

sys.exit(tests_present(sys.argv[1]))
