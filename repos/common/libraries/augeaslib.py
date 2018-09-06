import fnmatch
import os
import subprocess
import xml.etree.ElementTree as ET


from collections import namedtuple, OrderedDict


Lens = namedtuple("Lens", "name included excluded")


def augeas_get_known_files(augeas_tree, lens_name):
    return augeas_tree.match("/augeas/files//path[../lens = \"@{LENS}\" or ../lens = \"{LENS}.lns\"]".format(
        LENS=lens_name))


def augeas_add_file_to_filter(augeas_tree, file_path, lens_name):
    augeas_tree.set("/augeas/load/{LENS}/incl[last()+1]".format(LENS=lens_name), file_path)
    augeas_tree.load()


def augeas_get_directive_argument(augeas_tree, augeas_file_path, directive_name):
    return augeas_tree.match("{AUGEAS_FILE_PATH}/directive[. = \"{DIRECTIVE}\"]/arg".format(
        AUGEAS_FILE_PATH=augeas_file_path, DIRECTIVE=directive_name))


def augeas_get_path_value(augeas_tree, augeas_path):
    return augeas_tree.get(augeas_path)


def get_lens_transformations(lens_config, augeas_tree):
    """Finds config files based on provided lens and directives and returns
    relevant augeas transformations for augtool.

    We can do augeas lens transformation. e.g.:

        Httpd.lns incl /opt/config.conf

    which basically means: add "include /opt/config.conf" to Httpd lens
    filter. This can be later used as:

    > augtool -At "Httpd.lns incl /opt/config.conf"

    So, we find all possible config files based on provided directives and
    output transformations for all of them.

    We return list of transformations that can be glued to the augtool
    command.
    """

    def gather_files_for_resolution(lens_name):
        """What We do here is basically the same thing as running:

        > augtool match /augeas/files//path[../lens = "@lens_name" or ../lens = "lens_name.lns"]

        Which produces list of files that Httpd lens loaded into augeas
        internal structures.
        After that, we put unresolved file paths into the set, so they will
        get eventually resolved.
        """
        for augeas_file_path in augeas_get_known_files(augeas_tree, lens_name):
            path_value = augeas_get_path_value(augeas_tree, augeas_file_path)
            if path_value not in files_already_resolved:
                files_to_resolve.add(path_value)

    # Augeas is case sensitive and people will forget.
    lens_config['lens_name'] = lens_config['lens_name'].capitalize()

    # Basically the same thing as adding file path directly to the lens filter.
    for file_path in lens_config['load_files']:
        augeas_add_file_to_filter(augeas_tree, file_path, lens_config['lens_name'])

    files_to_resolve = set()
    files_already_resolved = set()
    gather_files_for_resolution(lens_config['lens_name'])

    while files_to_resolve and lens_config['directives']:
        augeas_file_path = files_to_resolve.pop()
        files_already_resolved.add(augeas_file_path)

        for directive in lens_config['directives']:
            # Locate all directive keywords in config and get its location in augeas tree.
            directive_arg_paths = augeas_get_directive_argument(augeas_tree, augeas_file_path, directive)

            # Get values for all located directives.
            for path in directive_arg_paths:
                directive_arg = augeas_get_path_value(augeas_tree, path)

                # If there is relative path in config file, we need to prepend
                # supplied prefix.
                if not directive_arg.startswith('/') and lens_config['prefix_for_relative']:
                    directive_arg = lens_config['prefix_for_relative'] + '/' + directive_arg

                augeas_add_file_to_filter(augeas_tree, directive_arg, lens_config['lens_name'])
                gather_files_for_resolution(lens_config['lens_name'])

    transformations = []
    for augeas_file_path in augeas_get_known_files(augeas_tree, lens_config['lens_name']):
        # Need to extract filesystem path from augeas tree.
        fs_file_path = augeas_file_path.split("/augeas/files")[1].split("/path")[0]
        lens_and_file = "{LENS}.lns incl {FS_FILE_PATH}".format(LENS=lens_config['lens_name'], FS_FILE_PATH=fs_file_path)
        transformations.append("-t" + lens_and_file)

    return transformations


def get_all_transformations(lenses_config, augeas_tree):
    """Get transformations for all provided lenses."""
    transformations = []
    for config in lenses_config:
        transformations.extend(get_lens_transformations(config, augeas_tree))
    return transformations


def get_augtool_data(augeas_config, xml_path, augeas_tree):
    # TODO: is it needed to get new transformations on every run of augtool?
    trans = get_all_transformations(augeas_config['lens_transforms'], augeas_tree)

    include_arg = []
    if augeas_config['use_custom_lenses']:
        include_arg = ["--include=" + augeas_config['custom_lenses_folder']]

    data = subprocess.check_output(["augtool"] + trans + include_arg + ["dump-xml", xml_path])
    return data


def get_lenses(augeas_config, augeas_tree):
    """Load information about lenses from Augease's `/augeas` sub-key

        This information represents:
        1) Lens name
        2) Included paths
           We use these to find which path corresponds to whichh lens
        3) Excluded paths
           Currently unused
    """

    augtool_data = get_augtool_data(augeas_config, "/augeas", augeas_tree)

    root = ET.fromstring(augtool_data)
    loaded = []

    # Auges/Node stores information about all supported lenses
    for ld in root.findall("./node[@label='augeas']/node[@label='load']/*"):
        name, incl, excl = ld.attrib['label'], [], []

        if not augeas_config['required_lenses'] or name in augeas_config['required_lenses']:
            for ie in ld.findall("./node[@label='incl']/value"):
                incl.append(ie.text)
            for ee in ld.findall("./node[@label='excl']/value"):
                excl.append(ee.text)

            loaded.append(Lens(name, incl, excl))

    return loaded


def find_lens(path, lens_data):
    """Find lens for given `path` in `lens_data`."""
    # TODO: Optimize - this function is very slow
    for ld in lens_data:
        for ip in ld.included:
            if fnmatch.fnmatch(path, ip):
                return ld

    return None


def process_augeas_data(augeas_config, augeas_tree):
    """The function starts by iterating first level of data nodes, but
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
                since we need to call `fnmatch` NxM times per each file path
         2.a.b) Property elements are recursively descended using `_rec_props()` function
                which returns the whole property tree
         2.b) Non-File Path
              Intermediary component of the path i.e. directory - recurse using `_rec` until we hit 2.a)
        3) All data are accumulated in `data` variable
    """
    augtool_data = get_augtool_data(augeas_config, "/files", augeas_tree)
    lens_data = get_lenses(augeas_config, augeas_tree)

    root = ET.fromstring(augtool_data)

    def walk_nodes(root):
        """Performs recursive pre-order depth-first traversal of tree from `root` node
            first using `_rec` function to drill down to a valid path and then
            `_rec_props` to obtain whole property sub-tree.

            The original XML preserves order of declaration so we do as well and hence use
            `OrderedDict` for dictionaries here. Preserving order of declarations is important
            because we want to see configuration directives in the same order they were declared in
            to figure out which one is valid.
        """

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
            """Recursive file path function"""
            if 'label' in n.attrib:
                curpath += '/' + n.attrib['label']

            if os.path.isfile(curpath):
                lens = find_lens(curpath, lens_data)
                if lens:
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
