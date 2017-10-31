import sys
import os
import json

DEFAULT_SERVICES = '''
cloud-config
cloud-final
cloud-init
cloud-init-local
ip6tables
iptables
lvm2-monitor
network'''.strip().split()

data = json.load(sys.stdin)
container_dir = data["container_directory"][0]["value"]
blacklist = data.get("upstart_service_blacklist",
                     [{"value": DEFAULT_SERVICES}])[0]["value"]

for level in range(0, 7):
    p = os.path.join(container_dir, 'etc', 'rc{}.d'.format(level))
    for entry in os.listdir(p):
        link = os.path.join(p, entry)
        name = os.path.basename(os.readlink(link))
        if name in blacklist:
            os.unlink(link)
    with open(os.path.join(container_dir, 'etc', 'init', 'rcS-emergency.conf'), 'w') as f:
        f.write('exit 0\n')
