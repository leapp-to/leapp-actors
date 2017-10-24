import json
import sys

data = json.load(sys.stdin)

targetinfo = {'docker': None, 'rsync': None, 'containers': None}

targetinfo['docker'] = ('OK', None)
for check in data['dockerinfo'].keys():
    retcode, msg = data['dockerinfo'][check]
    if retcode:
        targetinfo['docker'] = ('ERROR', msg)
        break

targetinfo['rsync'] = ('OK', None)
for check in data['rsyncinfo'].keys():
    retcode, msg = data['rsyncinfo'][check]
    if retcode:
        targetinfo['rsync'] = ('ERROR', msg)
        break

if data['containerslist']['retcode']:
    targetinfo['containers'] = ('ERROR', data['containerslist']['containers'])
else:
    targetinfo['containers'] = ('OK', data['containerslist']['containers'])

sys.stdout.write(json.dumps({"targetinfo": targetinfo}) + '\n')
