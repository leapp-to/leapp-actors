#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

inputs = {}
if not sys.stdin.isatty():
    input_data = sys.stdin.read()
    if input_data:
        inputs = json.loads(input_data)

tmpl = "find -P {path} -maxdepth 0 -type d 2> /dev/null"

path_list = [x['value'] for x in inputs.get('path', [])]

contents = []
for paths in path_list:
    for path in paths:
        cmd = tmpl.format(path=path)
        out, _ = Popen(cmd, shell=True, stdout=PIPE).communicate()
        for content in out.rstrip().split('\n'):
            if content not in contents:
                contents.append(content)

print(json.dumps({'content': [{'value': contents}]}))
