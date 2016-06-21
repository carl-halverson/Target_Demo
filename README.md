# Target_Demo

Key challenges to the case study is 
1. I have to do some programming
2. If you can’t SSH in then how would the user even run the command remotely.  Is that assumed?  Would I be parsing a data collection tool for this information and if so would this be an API call, DB query or client on the instance?
3. I need to figure out how to pass an argument 
4. I need to write code that will parse a mount point by file and size
5. I need to output this file to JSON format 

I have never coded in python from scratch before but I know it is widely used and is something I want to learn.  I choose to start my research utilizing python 2.7 as my coding language.

I have python installed and use shims as a python version manager.

I am going to assume this command is allowed to be run by the user locally on the server by means of an ssh call, service account or monitoring client.  This will focus my attention on getting this working locally on my MAC.

I look up passing arguments with python and find information on sys.argv module which will take any command line arguments and put then in sys.argv as a list.

I think I can simply use sys.argv in the command in place of a state variable that way the argument gets passes with whatever the user types to parse.

So I will write up a simple script to see if my argument is passing correctly.  I need an easy way to write and test.  I need a python IDE that will run my code from the screen as I write it.

http://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/

#!/usr/bin/python __author__ = 'Carl Halverson'  import sys  MountPoint = ("First argument: %s" % str(sys.argv[1])) print ("Mount Point Name: %s" % str(MountPoint))

OUTPUT: 
Mount Point Name: First argument: mountpoint

Test complete

My argument was successfully passed.  I’m moving on to parsing a mount point and outputting the files by size in bytes

I found an article on os.stat and st_size that seems to fit my needs

os.walk looks to be another option.  I think I need to define my own method now that I am reading more on how to do this.

I got os.walk to list files in a directory using the argument.

It’s not pretty but it is now outputting the directory file names with the bytes

#!/usr/bin/python
__author__ = 'Carl Halverson'

import os
import sys

rootdir = sys.argv[1]

print "Carl's Script to Show Target Files Size to Bytes"
print "---------------"
from os.path import join, getsize
for root, dirs, files in os.walk(rootdir):
    print root, "consumes",
    print sum([getsize(join(root, name)) for name in files]),
    print "bytes in", len(files), "non-directory files"

OUTPUT:
f45c89ad2817:repo vcx554$ python final.py /tmp
Carl's Script to Show Target Files Size to Bytes
---------------
/tmp consumes 6 bytes in 4 non-directory files
/tmp/com.apple.launchd.cYXhSmLXTw consumes 0 bytes in 1 non-directory files
/tmp/com.apple.launchd.o8b652lTYk consumes 0 bytes in 1 non-directory files
/tmp/CylanceDesktopRemoteFile consumes 0 bytes in 0 non-directory files
/tmp/KSOutOfProcessFetcher.1786965270.ppfIhqX0vjaTSb8AJYobDV7Cu68= consumes 165040 bytes in 1 non-directory files

Now to see about this JSON output

I found json.dumps and added the json module.  Now is the tricky part.  How to get my outputs to key pairs then output to json.

At this point I’ve been on a google search frenzy.  Python is awesome.  I’m really getting side tracked just learning more about it.  I have installed Shims and now have my own version running 2.7.11 so I’m not running on top of the OS version and took a online training course late into the night.

I found some interesting articles on outputting JSON with a python script in pretty format.  I am still having issues pulling all the functions together.  I have a script that will output the CWD but won’t take a custom argument and it’s not pretty like the example in the case study but I’m getting closer.

I have two code bases I’m working with.  

1. /code 
2. #!/usr/bin/python
3. __author__ = 'Carl Halverson'
4. 
5. import os
6. import sys
7. import json
8. 
9. rootdir = sys.argv[1]
10. 
11. print "Carl's Script to Show Target Files Size to Bytes"
12. print "---------------"
13. from os.path import join, getsize
14. for root, dirs, files in os.walk(rootdir):
15.     print root,
16.     print sum([getsize(join(root, name)) for name in files]),
17.     print "bytes"
18. 
19. Files = {root: sum([getsize(join(root, name)) for name in files]),
20. 		}
21. 
22. print json.dumps(Files)

/code 
1. #!/usr/bin/env python
2. 
3. import os, sys, json
4. 
5. def get_dir_size(base_dir):
6.     total_size = 0
7.     for dirpath, dirnames, filenames in os.walk(base_dir):
8.         if '/.' in dirpath:
9.             continue
10.         for f in filenames:
11.             if '/.' in f:
12.                 continue
13.             fp = os.path.join(dirpath, f)
14.             total_size += os.path.getsize(fp)
15.     return total_size
16. 
17. def get_files_by_file_size(path):
18.     items = []
19.     for basename in os.listdir(path):
20.         filename = os.path.join(path, basename)
21.         if '/.' in filename:
22.             continue
23.         if os.path.isfile(filename):
24.             items.append({'name': filename, 'size': os.path.getsize(filename)})
25.         elif os.listdir(filename) != []:
26.             items.append({'name': filename, 'size': get_dir_size(filename),
27.                           'children': get_files_by_file_size(filename)})
28.     return items
29. 
30. files = {'name': sys.argv[1], 
31.          'size': get_dir_size(sys.argv[1]),
32.          'children': get_files_by_file_size(sys.argv[1])}
33. 
34. print json.dumps(files)

I’m have to admit I’m stumped at this point and am not afraid to ask for help.  Time to call in the big guns.  I have a lot of great contacts that know Python very well.  Time to use a life line.

Wow, after a good half hour with two of my most trusted python resources they had to admit they had never attempted this before and want me to report back to them if I get it working.  The poked around at the code for a few and I’m sure they could figure it out if they had time to dedicate to this effort but, seems I’m on my own.

Well I figured out how to make the json pretty by adding 
/code
print json.dumps (Files, indent=4, sort_keys=True)

It’s still not exactly like the case study but, at least you can get an idea of my thought process tackling this challenge and how I go about solving problems.  If I didn’t have a full time job right now I would spend some more time on this and figure it out for sure.
