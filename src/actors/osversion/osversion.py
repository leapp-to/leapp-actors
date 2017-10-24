import json
import platform
import sys


fields = platform.linux_distribution()[:2]
sys.stdout.write(json.dumps({
    'osversion': {'name': fields[0], 'version': fields[1]}}) + '\n')
