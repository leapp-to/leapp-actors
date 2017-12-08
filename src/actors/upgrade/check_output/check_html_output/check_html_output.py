#!/usr/bin/env python

import json
import sys
from jinja2 import Template

HTML_TMPL = """
<!DOCTYPE html>
<html>
<body>
  <table style="width:100%">
    {% for checks in check_output %}
      {% for check in checks['checks'] %}
        {% for param in check['params'] %}
          <tr>
            <td>{{ check['check_id'] }}</td>
            <td><font color="red"><b>{{ check['status'] }}</b></font></td>
            <td>{{ check['summary'] }}: {{ param  }}</td>
          </tr>
        {% endfor %}
      {% endfor %}
    {% endfor %}
  </table>
</body>
</html>
"""

keys = {
    'in': 'check_output',
    'out': 'html_output'
}

template = Template(HTML_TMPL)

inputs = {}
if not sys.stdin.isatty():
    input_data = sys.stdin.read()
    if input_data:
        inputs = json.loads(input_data)

check_output = []
if keys['in'] in inputs:
    check_output = inputs[keys['in']]

html = template.render(check_output=check_output)
print(json.dumps({keys['out']: [{'value': html}]}))
