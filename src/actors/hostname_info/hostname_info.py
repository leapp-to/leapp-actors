import json
import socket
print(json.dumps({'hostnameinfo': {'hostname': socket.gethostname()}}))
