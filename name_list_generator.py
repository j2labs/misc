#!/usr/bin/env python

import urllib
import re

print 'Fetching names from the Census...'
names_list_url = 'http://www.census.gov/genealogy/names/dist.all.last'
names_data = urllib.urlopen(names_list_url).readlines()

print 'Processing Census data'
previous_name = 'John'
for line in names_data:
    m = re.findall('(\w+).*', line)
    if len(m) == 1:
        name = m[0]
        print '%s, %s' % (name.capitalize(), previous_name.capitalize())
        previous_name = name
