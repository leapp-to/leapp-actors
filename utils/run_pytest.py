#!/usr/bin/env python

"""
tmeszaro@redhat.com

This script is called by the make test target.


There can be two arguments:

 1. ACTOR=myactor

    NOTE: This is currently disabled, we will enable this when the CI will
          support "one actor, one container" testing.

 2. REPORT=myreport.xml

    Outputs xml report for the JUnit.


What is happening

 1. Checks cmd line arguments. There can be ACTOR and REPORT.

 2. Copies BASE_REPO to TMP_BASE_REPO. Renames all tests in TMP_BASE_REPO
    so they have unique names (by appending IDs). This is needed in order
    to avoid name mismatch for pytest. For more info, see pytest documentation:
    https://docs.pytest.org/en/latest/goodpractices.html#tests-outside-application-code

 3. Finds and registers all leapp repos in the TMP_BASE_REPO path.

 4. Checks if there are actor tests present.

 5. Runs pytest on the TMP_BASE_REPO.

 6. Removes TMP_BASE_REPO.
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys

from leapp.exceptions import LeappError
from leapp.repository.scan import find_and_scan_repositories

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("run_pytest.py")

BASE_REPO = "repos"
TMP_BASE_REPO = "tmp_" + BASE_REPO


def snactor_register(path):
    """ Snactor registers all repos in @path.
    """
    cmd = "snactor repo find --path {PATH}".format(PATH=path)
    try:
        logger.info(" Registering leapp repositories. This may take a while.")
        return subprocess.check_output(cmd, shell=True)
    except OSError as exc:
        sys.stderr.write(str(exc) + '\n')
        return None

if __name__ == "__main__":
    pytest_cmd = ["pytest", "-v"]
    pytest_cmd.append(TMP_BASE_REPO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", help="name of the actor for which to run tests")
    parser.add_argument("--report", help="filepath where to save report")
    args = parser.parse_args()

    # User wants to test single actor specified in the args.actor.
    if args.actor:
        # NOTE: ACTOR flag is disabled. Check module docstring for more info.
        logger.critical(" ACTOR flag is currently disabled!")
        sys.exit(1)

    # User wants to output xml report for junit.
    if args.report:
        pytest_cmd += ["--junit-xml={REPORT}".format(REPORT=args.report)]

    # Copy repository to tmp directory & make sure there is no conflict between
    # test names. NOTE: from now on, we are working with TMP_BASE_REPO.
    shutil.rmtree(TMP_BASE_REPO, ignore_errors=True)
    shutil.copytree(BASE_REPO, TMP_BASE_REPO)
    actor_id = 0
    for root, dirs, files in os.walk(TMP_BASE_REPO):
        if "tests" in root and "tests/" not in root:
            for item in files:
                if item.endswith(".py"):
                    old_item = os.path.join(root, item)
                    new_item = old_item.replace(".", "_" + str(actor_id) + ".")
                    shutil.move(old_item, new_item)
                    actor_id += 1

    # Register repos. This may take a while.
    snactor_register(TMP_BASE_REPO)

    # Find and collect leapp repositories.
    repos = {}
    for root, dirs, files in os.walk(BASE_REPO):
        if ".leapp" in dirs:
            repository = find_and_scan_repositories(root, include_locals=True)
            try:
                repository.load()
            except LeappError as exc:
                sys.stderr.write(exc.message)
                sys.exit(2)
            repos[repository] = root

    # Scan repositories for tests and print status.
    logger.info(" = Scanning Leapp repositories for tests")
    for repo, repo_path in repos.items():
        for actor in repo.actors:
            if not actor.tests:
                status = " Tests MISSING: {ACTOR} | class={CLASS}"
                status = status.format(ACTOR=actor.name, CLASS=actor.class_name)
                logger.critical(status)

    # Run pytest.
    logger.info(" Running pytest with: {PYTEST_CMD}".format(PYTEST_CMD=pytest_cmd))
    pytest_status = subprocess.call(pytest_cmd)

    # Cleanup.
    shutil.rmtree(TMP_BASE_REPO)
    sys.exit(pytest_status)
