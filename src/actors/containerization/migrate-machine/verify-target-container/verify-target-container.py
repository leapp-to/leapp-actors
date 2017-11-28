#!/usr/bin/python

import sys
import json

'''- name: force_create
type: BaseTypeBool
- name: containerslist
type: ContainersList
- name: container_name
type: BaseTypeString'''

inputs = json.load(sys.stdin)

if not inputs['force_create'][0]['value']:
    if inputs['container_name'][0]['value'] in inputs['containerslist'][0]['containers']:
        sys.stderr.write("ERROR: container {} already runs on target".format(
            inputs['container_name'][0]['value']) + "\n")
        sys.exit(1)
