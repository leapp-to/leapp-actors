#!/usr/bin/python
import os
import subprocess
import shutil
import sys

if len(sys.argv) == 3:
    container_directory, container_name = sys.argv[1:3]
    subprocess.call(["docker", "rm", "-f", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.isdir(container_directory):
        shutil.rmtree(container_directory)
