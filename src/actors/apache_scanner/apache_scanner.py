#!/usr/bin/env python2

"""
Author: tmeszaro@redhat.com

Actor that extracts selected data from the Augeas actor output.
If you want to extract additional data from the augeas aug_httpd lens, check
'searches' tuple in the printall() function.


Possible improvements:
- include information from: httpd -V
- include information from: httpd -S
- possibly identify if some testing configuration files have nested/recursive
   Includes and write code to extract those files as well
"""

import sys
import json


def searchblock(tablelist, mykey, myvalue=None, block=True):
    """ Searches augeas output for specified key or key-value and yields
        corresponding matched data.

        Args:
            tablelist: 'aug_httpd' lens data from the augeas actor output
            mykey: key of the block we want to search for
            myvalue: value of the block we want to search for,
                     if left None then get everything that matches at least mykey
            block: if False, do not yield whole dict but only key-value pair

        Returns:
            Yields the whole matching subdict of the tablelist if block=True
            or only single key-value pair otherwise.
    """
    # Sometimes augeas gives us list of dicts and sometimes only dict.
    # We want to always have the data in the list.
    if isinstance(tablelist, dict):
        tablelist = [tablelist]

    for table in tablelist:
        for key in table:
            if (myvalue is None and key == mykey) or \
               (myvalue is not None and key == mykey and myvalue == table[key]):
                if block is True:
                    yield table
                else:
                    yield key + "=" + table[key]
        if 'properties' in table:
            for generator in searchblock(table['properties'], mykey, myvalue, block):
                yield generator


def getblock(tablelist, mykey, myvalue=None, block=True, propitem=0):
    """ Accumulates matched data and returns them for output.

        Arguments:
            block: if False, will pass block=False to searchblock
            propitem: specify from which index in 'properties' to search

        Returns:
            Extracted data in form of dictionary.
    """
    out = {}
    if block is True:
        for dic in searchblock(tablelist, mykey, myvalue, block):
            if dic[mykey] not in out:
                out[dic[mykey]] = [dic['properties'][propitem]['value']]
            else:
                out[dic[mykey]].append(dic['properties'][propitem]['value'])
    else:
        for line in searchblock(tablelist, mykey, myvalue, block):
            key, value = line.split("=")
            if key not in out:
                out[key] = [value]
            else:
                out[key].append(value)
    return out


def printall(tablelist):
    """ Prints all occurrences of the specified key-value pairs.

    Tuple @searches contains information about what to extract and how it will
    be extracted (see @block and propitem@ arguments to getblock() function.

    Args:
        tablelist: 'aug_httpd' lens data from the augeas actor output

    Returns:
        json formatted extracted data from the augeas aug_httpd lens
    """
    searches = (
        # Arguments for the getblock function.
        # mykey, myvalue=None, block=True, propitem=0
        ("value", "IncludeOptional"),
        ("value", "User"),
        ("value", "Group"),
        ("value", "Mutex"),
        ("value", "PidFile"),
        ("value", "Listen"),
        ("value", "TypesConfig"),
        ("value", "CacheRoot"),
        ("value", "MIMEMagicFile"),
        ("value", "ScriptSock"),
        ("value", "SSLCertificateKeyFile"),
        ("value", "SSLCertificateFile"),
        ("value", "CustomLog"),
        ("value", "ErrorLog"),
        ("value", "Include"),
        ("name", "VirtualHost"),
        ("name", "Directory"),
        ("value", "DocumentRoot"),
        ("absolute_path", None, False),
        ("value", "LoadModule", True, 1),
    )

    out = {}
    for args in searches:
        result_table = getblock(tablelist, *args)
        for key in result_table:
            out[key] = result_table[key]
    return {"apache_scanner": [out]}


if __name__ == "__main__":
    AUGEAS_OUTPUT = json.load(sys.stdin)
    try:
        # We are interested only in the aug_httpd lens from the augeas actor
        #  output. We can drop every other augeas lens.
        TABLELIST = AUGEAS_OUTPUT['aug_httpd']
    except KeyError:
        raise KeyError("Could not get lens 'aug_httpd' from the augeas actor " \
                        "output. Make sure augeas actor is producing data in " \
                        "aug_httpd lens.")
    print(json.dumps(printall(TABLELIST)))
