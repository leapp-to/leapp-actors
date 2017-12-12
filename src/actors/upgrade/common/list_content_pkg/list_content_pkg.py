#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

keys = {
    'name': 'list_content_pkg',
    'in_ctx': 'context',
    'in_content': 'content',
    'out': 'pkg',
    'check_out': 'check_output'
}

inputs = {}
if not sys.stdin.isatty():
    input_data = sys.stdin.read()
    if input_data:
        inputs = json.loads(input_data)

ctx_list = []
if keys['in_ctx'] in inputs:
    for ctx in inputs[keys['in_ctx']]:
        ctx_list.append(ctx['value'])
context = ','.join(ctx_list)

tmpl = "rpm -qf {content}"

pkgs = []
not_packaged = []
if keys['in_content'] in inputs:
    for contents in inputs[keys['in_content']]:
        for content in contents['value']:
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
    out.update({keys['out']: [{'value': pkgs}]})

if not_packaged:
    check_result = [{
        'check_actor': keys['name'],
        'check_action': context,
        'status': 'FAIL',
        'summary': 'Path is not owned by any package',
        'params': not_packaged
    }]
    check_out = [{'checks': check_result}]
    out.update({keys['check_out']: check_out})

print(json.dumps(out))
