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
        {% for param in check.get('params', [""]) %}
          <tr>
            <td>{{ check['check_actor'] }}</td>
            <td>{{ check['check_action'] }}</td>
            <td><font color="red"><b>{{ check['status'] }}</b></font></td>
            {% if param %}
            <td>{{ check['summary'] }}: {{ param }}</td>
            {% else %}
            <td>{{ check['summary'] }}</td>
            {% endif %}
          </tr>
        {% endfor %}
      {% endfor %}
    {% endfor %}
  </table>
</body>
</html>
"""

template = Template(HTML_TMPL)

inputs = {}
if not sys.stdin.isatty():
    input_data = sys.stdin.read()
    if input_data:
        inputs = json.loads(input_data)

check_output = inputs.get('check_output', [])
html = template.render(check_output=check_output)
print(json.dumps({'html_output': [{'value': html}]}))
