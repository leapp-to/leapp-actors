#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

inputs = {}
if not sys.stdin.isatty():
    input_data = sys.stdin.read()
    if input_data:
        inputs = json.loads(input_data)

tmpl = "rpm -qf {content}"

context = ','.join(x['value'] for x in inputs.get('context', []))
content_list = [x['value'] for x in inputs.get('content', [])]

pkgs = []
not_packaged = []
for contents in content_list:
    for content in contents:
        if not content:
            continue

        cmd = tmpl.format(content=content)
        p = Popen(cmd, shell=True, stdout=PIPE)
        out, _ = p.communicate()
        if p.returncode == 0:
            pkg = out.rstrip()
            if pkg not in pkgs:
                pkgs.append(pkg)
        else:
            not_packaged.append(content)

out = {}
if pkgs:
    out.update({'pkg': [{'value': pkgs}]})

if not_packaged:
    check_result = [{
        'check_actor': 'list_content_pkg',
        'check_action': context,
        'status': 'FAIL',
        'summary': 'Path is not owned by any package',
        'params': not_packaged
    }]
    out.update({'check_output': [{'checks': check_result}]})

print(json.dumps(out))
