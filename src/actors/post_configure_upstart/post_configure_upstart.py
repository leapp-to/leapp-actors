import sys
import os
import json

data = json.load(sys.stdin)
container_dir = data["container_directory"]["value"]
blacklist = data["upstart_service_blacklist"]["value"]

for level in range(0, 7):
    p = os.path.join(container_dir, 'etc', 'rc{}'.format(level))
    for entry in os.listdir(p):
        link = os.path.join(p, entry)
        name = os.path.basename(os.readlink(link))
        if name in blacklist:
            os.unlink(link)
    with open(os.path.join(container_dir, 'etc', 'init', 'rcS-emergency.conf'), 'w') as f:
        f.write('exit 0\n')
