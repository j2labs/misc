#!/usr/bin/env python

import glob
import urllib
import sys

if len(sys.argv) < 2:
    directory_pattern = '*/*/*'
else:
    directory_pattern = sys.argv[1]

files = glob.glob(directory_pattern)
index = open('index.html', 'w')
index.write('<html>\n  <body>\n')

for f in files:
    file_url = urllib.pathname2url(f)
    print file_url
    index.write('    <a href="%s">%s</a><br/>\n' % (file_url, f))
index.write('  </body>\n</html>\n')
