#!/usr/bin/python
__author__ = 'Carl Halverson'

import os
import sys
import json

rootdir = sys.argv[1]

print "Carl's Script to Show Target Files Size to Bytes"
print "---------------"
from os.path import join, getsize
for root, dirs, files in os.walk(rootdir):
    print root,
    print sum([getsize(join(root, name)) for name in files]),
    print "bytes"

Files = {root: sum([getsize(join(root, name)) for name in files]),
		}

print json.dumps(Files)
