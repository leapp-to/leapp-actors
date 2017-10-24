#!/usr/bin/python

from subprocess import Popen, PIPE
import shlex
import sys
import json

keys = {
    'user': 'user',
    'host': 'host',
    'output': 'output'}

for arg in sys.argv:
    try:
        key, value = arg.split('=')
        if key in keys:
            keys[key] = value
    except ValueError:
        pass

inputs = {}
if not sys.stdin.isatty():
    inputs = json.load(sys.stdin)


host = 'localhost'
if keys['host'] in inputs:
    host = inputs[keys['host']]['value'] or host

user = 'root'
if keys['user'] in inputs:
    user = inputs[keys['user']]['value'] or user

mode = 'local' if host in ('127.0.0.1', 'localhost') else 'ssh'

tmpl = '''
    ansible -m setup -i {host}, -u {user} -c{mode} all
        -a gather_subset=!hardware,!virtual,!ohai,!facter'''

cmd = tmpl.format(user=user, host=host, mode=mode)
p = Popen(shlex.split(cmd), stdout=PIPE)
out, err = p.communicate()

if not p.returncode:
    sys.stdout.write(json.dumps({
        keys['output']: json.loads(out.split("=>")[1])}))
sys.exit(p.returncode)
