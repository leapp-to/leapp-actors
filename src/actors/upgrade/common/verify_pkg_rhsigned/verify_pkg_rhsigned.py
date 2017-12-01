#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

keys = {
    'in_ctx': 'context',
    'in_pkg': 'pkg',
    'check_out': 'check_output',
    'check_ctx': 'context',
    'check_value': 'value'
}

rhsign = ["199e2f91fd431d51",
          "5326810137017186",
          "938a80caf21541eb",
          "fd372689897da07a",
          "45689c882fa658e0"]

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

tmpl = "rpm -q --qf '%{{SIGPGP:pgpsig}}\n' {pkg}"

error = []
if keys['in_pkg'] in inputs:
    for pkgs in inputs[keys['in_pkg']]:
        for pkg in pkgs['value']:
            if not pkg:
                continue

            cmd = tmpl.format(pkg=pkg)
            p = Popen(cmd, shell=True, stdout=PIPE)
            out, _ = p.communicate()

            for sign in rhsign:
                if sign in out:
                    break
            else:
                error.append({keys['check_ctx']: context,
                              keys['check_value']: "{} is not signed by Red Hat".format(pkg)})

out = {}
if error:
    out.update({keys['check_out']: [{'value': error}]})

print(json.dumps(out))
