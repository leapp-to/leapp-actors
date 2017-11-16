#!/usr/bin/env python

import json

keys = {
    'out': 'path',
    'ctx': 'context'
}

path = ["/usr/lib/ruby/site_ruby/*/*",
        "/usr/lib/ruby/gems/*/gems/*"]
context = 'Ruby'

print(json.dumps({keys['out']: [{'value': path}],
                  keys['ctx']: [{'value': context}]}))
