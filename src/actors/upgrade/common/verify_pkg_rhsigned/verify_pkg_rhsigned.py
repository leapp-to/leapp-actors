#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

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

tmpl = "rpm -q --qf '%{{SIGPGP:pgpsig}}\n' {pkg}"

context = ','.join(x['value'] for x in inputs.get('context', []))
pkgs_list = [x['value'] for x in inputs.get('pkg', [])]

not_signed = []
for pkgs in pkgs_list:
    for pkg in pkgs:
        cmd = tmpl.format(pkg=pkg)
        out, _ = Popen(cmd, shell=True, stdout=PIPE).communicate()

        for sign in rhsign:
            if sign in out:
                break
        else:
            not_signed.append(pkg)

if not_signed:
    check_result = [{
        'check_actor': 'verify_pkg_rhsigned',
        'check_action': context,
        'status': 'FAIL',
        'summary': 'Package is not signed by Red Hat',
        'params': not_signed
    }]
    print(json.dumps({'check_output': [{'checks': check_result}]}))

else:
    print(json.dumps({}))
