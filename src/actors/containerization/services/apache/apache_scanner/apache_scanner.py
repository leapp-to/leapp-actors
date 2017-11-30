#!/usr/bin/env python

"""
Author: tmeszaro@redhat.com

Actor that extracts selected data from the Augeas actor output.
If you want to extract additional data from the augeas aug_httpd lens,
refer to the 'SEARCHES' tuple.


Possible improvements:
- include information from: httpd -V
- include information from: httpd -S
- possibly identify if some testing configuration files have nested/recursive
   Includes and write code to extract those files as well
"""

import sys
import json


# This tuple specifies what kind of data we want to extract from the augeas
# actor output.
#
# Search elements are usually apache config directives, but search function
# will also try to search non-directives.
#
# Tuple elements are then unpacked as function arguments to the search
# function inside extract function.
# Check extract/search function for more info.
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
    """ Extracts useful information from the augeas output.

    Args:
        augeas_output: aug_httpd lens data from the augeas actor.

    Returns:
        A dictionary containing relevant information extracted from the augeas
        output. It may look something like this:

        {
            "apache_scanner": [{
                    "MIMEMagicFile": ["conf/magic"],
                    "Group": ["apache"],
                    "IncludeOptional": ["conf.d/*.conf"],
                    "absolute_path": [
                        "/etc/httpd/conf/httpd.conf",
                        "/etc/httpd/conf.d/userdir.conf",
                        "/etc/httpd/conf.d/welcome.conf",
                        "/etc/httpd/conf.d/autoindex.conf",
                        "/etc/httpd/conf.d/mod_dnssd.conf"],
                    ...
            }]
        }
    """

    # Sometimes, augeas gives us list of dicts and sometimes only dict.
    # We want to always have the data in the list.
    if isinstance(augeas_output, dict):
        augeas_output = [augeas_output]

    def search(augeas_data, item, propindex=0):
        """ Searches for the specific item in the augeas output data.

        Args:
            augeas_data: This will be augeas aug_httpd lens data in the first
                iteration. In subsequent iterations, it may contain subsets of
                the aug_httpd lens data.
            item: String that we want to base our search around.
            propindex: Index in the "properties" value. Sometimes, we want to
                extract from different index than the default 0.
                e.g. the following example of augeas_data shows, that for
                item="LoadModule", we would like to extract properties[1],
                because it contains interesting value, and not properties[0].

                {
                    ...
                    "value": "LoadModule",
                    "properties": [
                        {
                            ...
                            "value": "request_module"
                        },
                        {
                            ...
                            "value": "/usr/lib/apache2/modules/mod_request.so"
                        }]
                }

        Yields:
            Tuple of the form (item, item value). For example, when searching
            for "Directory", we may get the following:

            ("Directory"/", "\"/var/www/html\"")
        """

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
        error.args += ("Could not get lens 'aug_httpd' from the augeas " +
                       "actor output. Make sure augeas actor is producing " +
                       "data in the aug_httpd lens.",)
        raise
    print(json.dumps(extract(AUG_HTTPD)))
