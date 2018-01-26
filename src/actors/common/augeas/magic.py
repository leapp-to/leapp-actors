#!/usr/bin/env python2

import os
import shlex
import subprocess
import uuid

from pprint import pprint as pp

import augeas

## FIXME: this is tmp, make this as optional actor input
INPUT = {"load": ["/opt/test_httpd.conf"],
         "directives": ["Include", "IncludeOptional"],
         "lens": "Httpd"}

AUG = augeas.Augeas()

def augeas_get_known_files():
    lens = INPUT["lens"]
    return AUG.match("/augeas/files//path[../lens = \"@%s\" or ../lens = \"%s.lns\"]" % (lens, lens))

def augeas_add_file_to_filter(file_path):
    lens = INPUT["lens"]
    AUG.set("/augeas/load/%s/incl[last()+1]" % lens, file_path)
    augeas_load_into_tree()

def augeas_get_directive_argument(augeas_file_path, directive_name):
    return AUG.match("%s/directive[. = \"%s\"]/arg" % (augeas_file_path, directive_name))

def augeas_get_path_value(augeas_path):
    return AUG.get(augeas_path)

def augeas_load_into_tree():
    """ load files into tree, so lenses can use them
    """
    AUG.load()

## Load files from input.
for file_path in INPUT["load"]:
    augeas_add_file_to_filter(file_path)

def do_magic():
    ## Load additional files that we've found from directives.
    #for _, augeas_file_path in included_files.iteritems():

    def gather_files_for_resolution():
        for augeas_file_path in augeas_get_known_files():
            path_value = augeas_get_path_value(augeas_file_path)
            if path_value not in files_already_resolved:
                files_to_resolve.add(path_value)
    files_to_resolve = set()
    files_already_resolved = set()
    gather_files_for_resolution()

    while len(files_to_resolve) > 0:
        ## FIXME: rm this
        """
        print('--')
        pp(files_already_resolved)
        pp(files_to_resolve)
        pp(augeas_get_known_files())
        """

        augeas_file_path = files_to_resolve.pop()
        files_already_resolved.add(augeas_file_path)

        #print("RESOLVING:", augeas_file_path)
        for directive in INPUT["directives"]:
            ## Locate all DIRECTIVE keywords in config and get its location in augeas tree.
            directive_arg_paths = augeas_get_directive_argument(augeas_file_path, directive)

            ## Get values for all located directives/
            for path in directive_arg_paths:
                directive_arg = augeas_get_path_value(path)
                #print("FOUND!:", augeas_file_path, directive, directive_arg)
                if not directive_arg.startswith('/'):
                    ## FIXME: get root from non-hardcoded stuff
                    directive_arg = "/etc/httpd/" + directive_arg
                augeas_add_file_to_filter(directive_arg)
                gather_files_for_resolution()


    transformations = []
    for augeas_file_path in augeas_get_known_files():
        fs_file_path = augeas_file_path.split("/augeas/files")[1].split("/path")[0]
        t = "%s.lns incl %s" % (INPUT["lens"], fs_file_path)
        transformations.append("-t")
        transformations.append(t)

    pp(transformations)
    return transformations
