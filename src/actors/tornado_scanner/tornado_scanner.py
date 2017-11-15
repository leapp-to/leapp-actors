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


def get_python_exec(proc_cmdline, virtual_env_path=None):
    if virtual_env_path is not None:
        v_python_exec = os.path.join(app_metadata['virtual_env_path'], 'bin/python')
        return os.readlink(v_python_exec) if os.path.islink(v_python_exec) else 'python'

    python_exec = re.search("python([0-9]\.?[0-9]?(d|m|u)?)?", process['cmdline'])
    return python_exec.group() if python_exec is not None else None


def get_main_file_path(cmdline, cwd):
    main_file = re.search("[a-zA-Z0-9\/]*\.py", cmdline)
    return os.path.join(cwd, main_file.group()) if main_file is not None else None


def extract_processes_param(params):
    try:
        return params['process_list'][0]['processes']
    except LookupError:
        sys.stderr.write("Could not find processes to check")


def check_if_files_exist(path, files):
    result = {}
    for f in files:
        result[f] = os.path.exists(os.path.join(path, f))
    return result


if __name__ == '__main__':
    params = {} if os.isatty(sys.stdin.fileno()) else json.load(sys.stdin)
    processes = extract_processes_param(params)
    if processes is None:
        sys.exit(1)

    output = {'tornado_apps': [
        {'apps': []}
    ]}

    for process in processes:
        app_metadata = {
            "project_path": None,
            "virtual_env_path": process['environ'].get('VIRTUAL_ENV'),
            "main_file_name": None,
            "python_exec": None
        }

        # get main file path
        main_file_path = get_main_file_path(process['cmdline'], process['cwd'])
        if main_file_path is None:
            continue
        app_metadata['project_path'], app_metadata['main_file_name'] = main_file_path.rsplit('/', 1)

        # check if main file contains tornado import
        if not is_tornado_package(main_file_path):
            continue

        # get python exec
        app_metadata["python_exec"] = get_python_exec(process['cmdline'], process['virtual_env_path'])
        if app_metadata["python_exec"] is None:
            continue

        # check requirements for the project
        req_files = check_if_files_exist(app_metadata['project_path'], ('requirements.txt', 'setup.py',))
        if app_metadata['virtual_env_path'] is None and \
           not req_files['requirements.txt'] and \
           not req_files['setup.py']:
            continue

        # add tornado app to result list
        output['tornado_apps'][0]['apps'].append(app_metadata)

    sys.stdout.write(json.dumps(output))
