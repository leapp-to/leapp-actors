import os
import sys
import json


DEFAULT_MACROCONTAINERS_PATH = '/var/lib/leapp/macrocontainers'


if __name__ == "__main__":
    inputs = json.load(sys.stdin)

    print(json.dumps({
        'container_directory': {
            'value': os.path.join(DEFAULT_MACROCONTAINERS_PATH,
                                  inputs['container_name']['value'])
        }
    }))
