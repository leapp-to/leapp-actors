#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

keys = {
    'in_ctx': 'context',
    'in_content': 'content',
    'out': 'pkg',
    'err_out': 'error',
    'err_ctx': 'context',
    'err_value': 'value'
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

pkg = []
error = []
if keys['in_content'] in inputs:
    for contents in inputs[keys['in_content']]:
        for content in contents['value']:
            if not content:
                continue

            cmd = tmpl.format(content=content)
            p = Popen(cmd, shell=True, stdout=PIPE)
            out, _ = p.communicate()
            if p.returncode == 0:
                pkg.append(out.rstrip())
            else:
                error.append({keys['err_ctx']: context,
                              keys['err_value']: out.rstrip()})

out = {}
if pkg:
    out.update({keys['out']: [{'value': pkg}]})
if error:
    out.update({keys['err_out']: [{'value': error}]})

print(json.dumps(out))
