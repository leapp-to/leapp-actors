#!/usr/bin/env python

import json

path = ["/usr/lib*/python*/site-packages/*"]
context = 'Python'

print(json.dumps({'path': [{'value': path}],
                  'context': [{'value': context}]}))
