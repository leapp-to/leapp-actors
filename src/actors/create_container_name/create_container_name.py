import sys
import json

if __name__ == "__main__":
    data = json.load(sys.stdin)
    container_name = data.get('user_container_name', {}).get('value')
    hostname = data['hostnameinfo']['hostname']
    container_name = container_name if container_name else "container_" + hostname

    print(json.dumps({'container_name': {'value': container_name}}))
