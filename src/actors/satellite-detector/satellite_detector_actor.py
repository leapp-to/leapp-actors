#!/usr/bin/env python
import sys

import json

from subprocess import Popen, PIPE
import shlex

# Defaults inputs
inputs = {
    "user": "root",
    "host": "localhost"
}

# Output fields
output_fields = {"satellite_detected": False,
                 "satellite_version_major": None,
                 "satellite_version_minor": None,
                 "satellite_version_bugfix": None,
                 "satellite_services": []}

if not sys.stdin.isatty():
    input_data = sys.stdin.read()
    if input_data:
        loaded_inputs = json.loads(input_data)
else:
    loaded_inputs = {}

# Load inputs
for key in inputs.keys():
    if key in loaded_inputs.keys():
        inputs[key] = loaded_inputs[key][0].get("value", inputs[key])


mode = "local" if inputs["host"] in ("localhost", "127.0.0.1") else "ssh"
cmd = "ansible -m satellite_detector -M . -i {host}, -c {mode} -u {user} {host}".format(host=inputs["host"],
                                                                                        user=inputs["user"],
                                                                                        mode=mode)

ansible = Popen(shlex.split(cmd), stdout=PIPE)
ansible_stdout, _ = ansible.communicate()

if not ansible.returncode:
    ansible_json = json.loads(ansible_stdout.split("=>")[1])
    output = {}

    if not ansible_json.get("satellite_detected", False):
        output["satellite_detected"] = False
    else:
        for key in output_fields.keys():
            output[key] = ansible_json.get(key, output_fields[key])

    print(json.dumps({"app_satellite_detection": [output]}))


sys.exit(ansible.returncode)
