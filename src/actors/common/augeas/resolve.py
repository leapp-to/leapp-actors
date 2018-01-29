#!/usr/bin/env python

"""
tmeszaro@redhat.com


Possible Improvements:

- Providing prefix for directive argument paths could be automatized by running
  vanilla augeas actor before resolving directives. Then put output of augeas
  actor to relevant scanner and extract root directory.
  After that, run this module.

"""


import sys
import json

import augeas


AUG = augeas.Augeas()


def augeas_get_known_files():
    lens = INPUT["lens"]
    return AUG.match("/augeas/files//path[../lens = \"@%s\" or ../lens = \"%s.lns\"]" % (lens, lens))


def augeas_add_file_to_filter(file_path):
    lens = INPUT["lens"]
    AUG.set("/augeas/load/%s/incl[last()+1]" % lens, file_path)
    AUG.load()


def augeas_get_directive_argument(augeas_file_path, directive_name):
    return AUG.match("%s/directive[. = \"%s\"]/arg" % (augeas_file_path, directive_name))


def augeas_get_path_value(augeas_path):
    return AUG.get(augeas_path)


INPUT = json.load(sys.stdin)["aug_input"][0]

def get_transformations():
    """ Finds config files based on provided lens and directives and returns
    relevant augeas transformations for augtool.

    We can do augeas lens transformation. e.g.:

        Http.lns incl /opt/config.conf

    which basically means: add "include /opt/config.conf" to Httpd lens filter.
    This can be later used as:

    > augtool -At "Http.lns incl /opt/config.conf"

    So, we find all possible config files based on provided directives and output
    transformations for all of them.

    We return list of transformations that can be glued to the augtool command.
    """

    def gather_files_for_resolution():
        """ What We do here is basically the same thing as running:

        > augtool match /augeas/files//path[../lens = "@Httpd" or ../lens = "Httpd.lns"]

        Which produces list of files that Httpd lens loaded into augeas internal
        structures.
        After that, We put unresolved file paths into the set, so they will get
        eventually resolved.
        """
        for augeas_file_path in augeas_get_known_files():
            path_value = augeas_get_path_value(augeas_file_path)
            if path_value not in files_already_resolved:
                files_to_resolve.add(path_value)

    # We need at minimum lens name"
    if "lens" not in INPUT:
        return []

    # Augeas is case sensitive and people will forget.
    INPUT["lens"] = INPUT["lens"].capitalize()

    # Basically the same thing as adding file path directly to the lens filter.
    if "load_files" in INPUT:
        for file_path in INPUT["load_files"]:
            augeas_add_file_to_filter(file_path)

    files_to_resolve = set()
    files_already_resolved = set()
    gather_files_for_resolution()

    while len(files_to_resolve) > 0 and "directives" in INPUT:
        augeas_file_path = files_to_resolve.pop()
        files_already_resolved.add(augeas_file_path)

        for directive in INPUT["directives"]:
            # Locate all directive keywords in config and get its location in augeas tree.
            directive_arg_paths = augeas_get_directive_argument(augeas_file_path, directive)

            # Get values for all located directives.
            for path in directive_arg_paths:
                directive_arg = augeas_get_path_value(path)

                # If there is relative path in config file, We need to prepend
                # supplied prefix.
                if not directive_arg.startswith('/') and "prefix_for_relative" in INPUT:
                    directive_arg = INPUT["prefix_for_relative"] + '/' + directive_arg

                augeas_add_file_to_filter(directive_arg)
                gather_files_for_resolution()

    transformations = []
    for augeas_file_path in augeas_get_known_files():
        # Need to extract filesystem path from augeas tree.
        fs_file_path = augeas_file_path.split("/augeas/files")[1].split("/path")[0]
        lens_and_file = "{LENS}.lns incl {FS_FILE_PATH}".format(LENS=INPUT["lens"], FS_FILE_PATH=fs_file_path)
        transformations.append("-t" + lens_and_file)

    return transformations
