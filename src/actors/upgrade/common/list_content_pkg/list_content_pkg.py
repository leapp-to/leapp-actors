#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

keys = {
    'in_ctx': 'context',
    'in_content': 'content',
    'out': 'pkg',
    'check_out': 'check_output',
    'check_ctx': 'context',
    'check_value': 'value'
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
report = []
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
                report.append({keys['check_ctx']: context,
                               keys['check_value']: out.rstrip()})

out = {}
if pkgs:
    out.update({keys['out']: [{'value': pkgs}]})
if report:
    out.update({keys['check_out']: [{'value': report}]})

print(json.dumps(out))
