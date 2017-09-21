import json
import sys

data = json.load(sys.stdin)

machineinfo = {'osversion': data['osversion'],
               'hostnameinfo': data['hostnameinfo'],
               'iplist': data['ip_list'],
               'rpm_packages': {"packages": []}}

if 'rpm_packages' in data:
    machineinfo['rpm_packages'] = data['rpm_packages']

print(json.dumps({"machineinfo": machineinfo}))
