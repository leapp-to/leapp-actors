import json
import os
import re
import sys
import ast


def is_tornado_package(main_path):
    with open(main_path, 'r') as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for elem in node.names:
                    if 'tornado' in elem.name:
                        return True
    return False


tornado_apps = []
# TODO: replace that with sys.stdin
params = {}
with open("output", "r") as f:
    params = json.load(f)


for val in params.get('list_processes', {}).values():
    app_metadata = {
        "project_path": None,
        "virtual_env_path": None if 'VIRTUAL_ENV' not in val['environ'] else val['environ']['VIRTUAL_ENV'],
        "main_file_name": None,
        "python_version": None
    }

    main_file = re.search("[a-zA-Z0-9\/]*\.py", val['cmdline'])
    if main_file is None:
        continue
    main_file = main_file.group()

    mfile_full_path = os.path.join(val['cwd'], main_file)
    app_metadata['project_path'], app_metadata['main_file_name'] = mfile_full_path.rsplit('/', 1)

    # check requirements files
    if app_metadata['virtual_env_path'] is None and \
       not os.path.exists(os.path.join(app_metadata['project_path'], 'requirements.txt')):
       continue

    # check if main file contains tornado import
    if is_tornado_package(mfile_full_path):
        tornado_apps.append(app_metadata)

sys.stdout.write(json.dumps(tornado_apps))
