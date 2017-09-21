import json
import socket
import sys
import os
data = json.load(sys.stdin)
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(os.environ['LEAPP_ACTOR_STDOUT_SOCK'])
containers = [container.strip('"') for container in data['containerslist']['containers']]
if data['check_target_service_status']['value']:
    rsync_status = 'error'
    docker_status = 'error'
    if all([value[0] == 0 for value in data['rsyncinfo'].values()]):
        rsync_status = 'ok'
    if all([value[0] == 0 for value in data['dockerinfo'].values()]):
        docker_status = 'ok'
    output = json.dumps({'docker': docker_status, 'rsync': rsync_status, 'containers': containers})
else:
    output = '\n'.join(containers) + '\n'
s.sendall(output)
s.close()
