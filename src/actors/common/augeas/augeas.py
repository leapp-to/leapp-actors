# coding: utf-8


import json
import os
import subprocess
import xml.etree.ElementTree as ET
import fnmatch
from collections import namedtuple, OrderedDict

"""
Note: We include additional non-default lenses from the "lenses" directory
      using the --include directive.
      These lenses may override the default augeas lenses.
"""

Lens = namedtuple("Lens", "name included excluded")


def get_lenses():
    ''' Load information about lenses from Augease's `/augeas` sub-key

        This information represents:
        1) Lens name
        2) Included paths
           We use these to find which path corresponds to whichh lens
        3) Excluded paths
           Currently unused
    '''
    augeas = subprocess.check_output(["augtool", "--include=lenses", "dump-xml", "/augeas"])
    root = ET.fromstring(augeas)
    loaded = []

    # Auges/Node stores information about all supported lenses
    for ld in root.findall("./node[@label='augeas']/node[@label='load']/*"):
        name, incl, excl = ld.attrib['label'], [], []

        for ie in ld.findall("./node[@label='incl']/value"):
            incl.append(ie.text)
        for ee in ld.findall("./node[@label='excl']/value"):
            excl.append(ie.text)

        loaded.append(Lens(name, incl, excl))

    return loaded


def find_lens(path, lens_data):
    ''' Find lens for given `path` in `lens_data` '''
    #TODO: Optimize - this function is very slow
    for ld in lens_data:
        for ip in ld.included:
            if fnmatch.fnmatch(path, ip):
                return ld

    return None


def process_augeas_data(lens_data):
    ''' The function starts by iterating first level of data nodes, but
        it's important to first understand how Augeas representes information
        about files.

        Augeas Output
        -------------

         The output XML is nested collection of key-values based on file system
         structure:

             /etc/httpd.conf/DocumentRoot/Value
             /etc/httpd.conf/IfModule/mime_type/
             ...

         So until a certain depth, the chain of key-values represents a file path,
         and the remaining key-values represent parsed elements from the file.

        So based on this layout, the general algorithm is as follows:

        1) Iterate first level of nodes
        2) Check if the current node represents a real file-system path to a file
         2.a) File Path
              Children nodes of the current node are recursively converted to dictionaries
              holding nodes properties
         2.a.a) Lens for the pathh is found, in worst case scenario we need to iterate over
                all lenses (N) and all their `inclusive` paths (M), so this operation is very expensive
                since we need to call `fnmatch` N×M times per each file path
         2.a.b) Property elements are recursively descended using `_rec_props()` function
                which returns the whole property tree
         2.b) Non-File Path
              Intermediary component of the path i.e. directory - recurse using `_rec` until we hit 2.a)
        3) All data are accumulated in `data` variable
    '''
    data = subprocess.check_output(["augtool", "--include=lenses", "dump-xml", "/files"])
    root = ET.fromstring(data)

    def walk_nodes(root):
        ''' Performs recursive pre-order depth-first traversal of tree from `root` node
            first using `_rec` function to drill down to a valid path and then
            `_rec_props` to obtain whole property sub-tree.

            The original XML preserves order of declaration so we do as well and hence use
            `OrderedDict` for dictionaries here. Preserving order of declarations is important
            because we want to see configuration directives in the same order they were declared in
            to figure out which one is valid.
        '''

        data = OrderedDict()

        def _rec_props(n):
            ''' Recursive property function '''
            label = n.attrib['label']

            # Skip comments for now
            if label == '#comment':
                return

            props = OrderedDict()
            props['name'] = label

            value = n.find('value')
            if value is not None:
                props['value'] = value.text


            sub = [v for v in (_rec_props(node) for node in n.findall('node')) if v]

            if sub:
                # Do not output empty properties to save space
                props['properties'] = sub

            return props

        def _rec(n, curpath=''):
            ''' Recursive file path function  '''
            if 'label' in n.attrib:
                curpath += '/' + n.attrib['label']

            is_file = os.path.isfile(curpath)

            if is_file:
                lens = find_lens(curpath, lens_data)
                name = 'aug_' + lens.name.lower()
                if name in data:
                    data[name].append(_rec_props(n))
                else:
                    data[name] = [_rec_props(n)]
                data[name][-1]['absolute_path'] = curpath

            else:
                for c in n:
                    _rec(c, curpath)


        for node in root.findall("./node[@path='/files']/node"):
            _rec(node)

        return data

    return walk_nodes(root)


metadata = process_augeas_data(get_lenses())
print(json.dumps(metadata))
