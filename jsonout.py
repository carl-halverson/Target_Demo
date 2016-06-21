#!/usr/bin/env python

import os, sys, json

def get_dir_size(base_dir):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(base_dir):
        if '/.' in dirpath:
            continue
        for f in filenames:
            if '/.' in f:
                continue
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_files_by_file_size(path):
    items = []
    for basename in os.listdir(path):
        filename = os.path.join(path, basename)
        if '/.' in filename:
            continue
        if os.path.isfile(filename):
            items.append({'name': filename, 'size': os.path.getsize(filename)})
        elif os.listdir(filename) != []:
            items.append({'name': filename, 'size': get_dir_size(filename),
                          'children': get_files_by_file_size(filename)})
    return items

Files = {'name': sys.argv[1], 
         'size': get_dir_size(sys.argv[1]),
         'children': get_files_by_file_size(sys.argv[1])}

print json.dumps(Files, indent=4, sort_keys=True)