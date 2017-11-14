import json
import os
import re
import sys
import ast


def is_tornado_package(main_file_path):
    with open(main_file_path, 'r') as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for elem in node.names:
                    if 'tornado' in elem.name:
                        return True
    return False

output = {'tornado_apps': [
    {'apps': []}
]}

params = {}
if not os.isatty(sys.stdin.fileno()):
    params = json.load(sys.stdin)

try:
    processes = params['process_list'][0]['processes']
except LookupError as exc:
    exit(1)

for process in processes:
    app_metadata = {
        "project_path": None,
        "virtual_env_path": None if 'VIRTUAL_ENV' not in process['environ'] else process['environ']['VIRTUAL_ENV'],
        "main_file_name": None,
        "python_exec": None
    }

    # get python exec
    if app_metadata['virtual_env_path'] is not None:
        v_python_exec = os.path.join(app_metadata['virtual_env_path'], 'bin/python')
        if os.path.islink(v_python_exec):
            app_metadata['python_exec'] = os.readlink(v_python_exec)
        else:
            app_metadata['python_exec'] = 'python'
    else:
        python_exec = re.search("python([0-9]\.?[0-9]?(d|m|u)?)?", process['cmdline'])
        if python_exec is None:
            continue
        app_metadata['python_exec'] = python_exec.group()

    # get python main file
    main_file = re.search("[a-zA-Z0-9\/]*\.py", process['cmdline'])
    if main_file is None:
        continue
    main_file = main_file.group()

    mfile_full_path = os.path.join(process['cwd'], main_file)
    app_metadata['project_path'], app_metadata['main_file_name'] = mfile_full_path.rsplit('/', 1)

    # check requirements and setup files
    if app_metadata['virtual_env_path'] is None and \
       not os.path.exists(os.path.join(app_metadata['project_path'], 'requirements.txt')) and \
       not os.path.exists(os.path.join(app_metadata['project_path'], 'setup.py')):
       continue

    # check if main file contains tornado import
    if is_tornado_package(mfile_full_path):
        output['tornado_apps'][0]['apps'].append(app_metadata)

sys.stdout.write(json.dumps(output))
