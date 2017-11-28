import json
import os
import re


def get_version(root_dir):
    pattern = '\d.\d.\d'
    version = ''

    with open (os.path.join(root_dir, 'wp-includes/version.php')) as f:
        for line in f:
            if line.startswith('$wp_version'):
                version = re.search(pattern, line).group(0)

    return version


def get_db_host(root_dir):
    pattern = '(?<=DB_HOST\',)\s*[\w.\'()]+(?=\))'
    with open(os.path.join(root_dir, "wp-config.php")) as f:
        config = f.read()

    match = re.search(pattern, config)

    if match is None:
        raise Exception("Unable to find address of database host")

    host = match.group(0)
    db_host = re.search('(?<=\')[\w.]+(?=\')', host).group(0)

    if 'getenv' in host:
        db_host = os.getenv(db_host, "")

    if not db_host:
        raise Exception("Unable to find address of database host")
    else:
        if db_host == 'localhost':
            db_host = '127.0.0.1'
        return db_host


def get_root_dir():
    root_dir = ''
    for root, dirs, files in os.walk('/'):
        for name in dirs:
            if name == 'wp-includes':
                root_dir = os.path.abspath(root)
                break

    if not root_dir:
        raise Exception("Unable to locate wordpress root directory")

    return root_dir


if __name__ == "__main__":
    root_directory = get_root_dir()
    database_host = get_db_host(root_directory)
    version = get_version(root_directory)

    print(json.dumps({
        'wordpress_root_directory': [{
            'value': root_directory
        }],
        'database_host': [{
            'value': database_host
        }],
        'wordpress_version': [{
            'value': version
        }]
    }))
