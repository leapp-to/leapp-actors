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

if not inputs['force_create']['value']:
    if inputs['container_name']['value'] in inputs['containerslist']['containers']:
        sys.stderr.write("ERROR: container {} already runs on target".format(inputs['container_name']['value']) + "\n")
        sys.exit(1)
