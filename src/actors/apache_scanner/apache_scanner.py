#!/usr/bin/env python2

"""
Author: tmeszaro@redhat.com

Actor that extracts selected data from the Augeas actor output.
If you want to extract additional data from the augeas aug_httpd lens,
specify them in the 'SEARCHES' tuple.


Possible improvements:
- include information from: httpd -V
- include information from: httpd -S
- possibly identify if some testing configuration files have nested/recursive
   Includes and write code to extract those files as well
"""

import sys
import json

SEARCHES = (
    ("IncludeOptional",),
    ("User",),
    ("Group",),
    ("Mutex",),
    ("PidFile",),
    ("Listen",),
    ("TypesConfig",),
    ("CacheRoot",),
    ("MIMEMagicFile",),
    ("ScriptSock",),
    ("SSLCertificateKeyFile",),
    ("SSLCertificateFile",),
    ("CustomLog",),
    ("ErrorLog",),
    ("Include",),
    ("VirtualHost",),
    ("Directory",),
    ("DocumentRoot",),
    ("absolute_path",),
    ("LoadModule", 1),
)


def extract(augeas_output):
    # Sometimes augeas gives us list of dicts and sometimes only dict.
    # We want to always have the data in the list.
    if isinstance(augeas_output, dict):
        augeas_output = [augeas_output]

    def search(augeas_data, item, propindex=0):
        for table in augeas_data:
            for key in table:
                if item == key:
                    yield (item, table[key])
                if item == table[key] and 'properties' in table:
                    if 'value' in table['properties'][propindex]:
                        yield (item, table['properties'][propindex]['value'])
            if 'properties' in table:
                for generator in search(table['properties'], item, propindex):
                    yield generator
    out = {}
    for args in SEARCHES:
        for result in search(augeas_output, *args):
            out.setdefault(result[0], []).append(result[1])
    return {"apache_scanner": [out]}


if __name__ == "__main__":
    AUGEAS_OUTPUT = json.load(sys.stdin)
    try:
        # We are interested only in the aug_httpd lens from the augeas actor
        # output. We can drop every other augeas lens.
        AUG_HTTPD = AUGEAS_OUTPUT['aug_httpd']
    except KeyError as error:
        error.args = ("Could not get lens 'aug_httpd' from the augeas actor "
                      + "output. Make sure augeas actor is producing data in "
                      + "the aug_httpd lens.",)
        raise
    print(json.dumps(extract(AUG_HTTPD)))
