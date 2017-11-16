#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

keys = {
    'in': 'path',
    'out': 'content'
}

inputs = {}
if not sys.stdin.isatty():
    input_data = sys.stdin.read()
    if input_data:
        inputs = json.loads(input_data)

tmpl = "find -P {path} -maxdepth 0 -type d 2> /dev/null"

content = []
if keys['in'] in inputs:
    for paths in inputs[keys['in']]:
        for path in paths['value']:
            cmd = tmpl.format(path=path)
            p = Popen(cmd, shell=True, stdout=PIPE)
            out, _ = p.communicate()
            content.extend(out.rstrip().split('\n'))

print(json.dumps({keys['out']: [{'value': content}]}))
