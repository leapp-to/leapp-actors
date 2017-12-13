#!/usr/bin/env python

from subprocess import Popen, PIPE
import json

cmd = "perl -MConfig -e '$,=q{ }; print @Config{installarchlib,installprivlib,installvendorarch,installvendorlib}'"
p = Popen(cmd, shell=True, stdout=PIPE)
out, _ = p.communicate()
path = out.rstrip().split(' ')
context = 'Perl'

print(json.dumps({'path': [{'value': path}],
                  'context': [{'value': context}]}))
