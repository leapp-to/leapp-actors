import os
import errno
import sys
import json

data = json.load(sys.stdin)
container_dir = data["container_directory"][0]["value"]
try:
    os.makedirs(container_dir)
except OSError as exc:
    if exc.errno != errno.EEXIST:  # raise exception if it's different than FileExists
        raise
