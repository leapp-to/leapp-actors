import json
import sys

data = json.load(sys.stdin)

targetinfo = {'docker': None, 'rsync': None, 'containers': None}

targetinfo['docker'] = ('OK', None)
for check in data['dockerinfo'][0].keys():
    retcode, msg = data['dockerinfo'][0][check]
    if retcode:
        targetinfo['docker'] = ('ERROR', msg)
        break

targetinfo['rsync'] = ('OK', None)
for check in data['rsyncinfo'][0].keys():
    retcode, msg = data['rsyncinfo'][0][check]
    if retcode:
        targetinfo['rsync'] = ('ERROR', msg)
        break

if data['containerslist'][0]['retcode']:
    targetinfo['containers'] = ('ERROR', data['containerslist'][0]['containers'])
else:
    targetinfo['containers'] = ('OK', data['containerslist'][0]['containers'])

sys.stdout.write(json.dumps({"targetinfo": [targetinfo]}) + '\n')
