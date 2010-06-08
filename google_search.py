#!/usr/bin/env python
import urllib
import simplejson

query = urllib.urlencode({'q' : 'David Christian',
                          'rsz': 'small'})
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' \
      % (query)
print url
search_results = urllib.urlopen(url)
json = simplejson.loads(search_results.read())
results = json['responseData']['results']
for i in results:
    print "ITEM ::\n  " + i['titleNoFormatting'] + "\n  " + i['url']
