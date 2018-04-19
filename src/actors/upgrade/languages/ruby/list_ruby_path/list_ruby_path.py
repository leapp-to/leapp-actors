#!/usr/bin/env python

import json

path = ["/usr/lib/ruby/site_ruby/*/*",
        "/usr/lib/ruby/gems/*/gems/*"]
context = 'Ruby'

print(json.dumps({'path': [{'value': path}],
                  'context': [{'value': context}]}))
