import json
import sys

data = json.load(sys.stdin)

machineinfo = {'osversion': data['osversion'][0],
               'hostnameinfo': data['hostnameinfo'][0],
               'iplist': data['ip_list'][0],
               'rpm_packages': {"packages": []}}

if 'rpm_packages' in data:
    machineinfo['rpm_packages'] = data['rpm_packages'][0]

print(json.dumps({"machineinfo": [machineinfo]}))
