#!/usr/bin/env python

import json

keys = {
    'out': 'path',
    'ctx': 'context'
}

path = ["/usr/lib*/python*/site-packages/*"]
context = 'Python'

print(json.dumps({keys['out']: [{'value': path}],
                  keys['ctx']: [{'value': context}]}))
