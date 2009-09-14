#!/usr/bin/env python
import urllib
import simplejson

query = urllib.urlencode({'q' : 'apple tablet site:engadget.com',
                          'rsz': 'large'})
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' \
      % (query)
search_results = urllib.urlopen(url)
json = simplejson.loads(search_results.read())
results = json['responseData']['results']
for i in results:
    print "ITEM ::\n  " + i['titleNoFormatting'] + "\n  " + i['url']
