import json
import platform
fields = platform.linux_distribution()[:2]
print json.dumps({'osversion': {'name': fields[0], 'version': fields[1]}})
