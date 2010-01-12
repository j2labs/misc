#!/usr/bin/env python

import simplejson
import urllib
import re

# requires formatting
search_api_url = 'http://search.twitter.com/search.json%s&rpp=100'

# each search string is search individually
# be mindful of api limitations (150 queries per hour, last i checked)
search_strings = (
    #'%23polarisdms',
    '%23j2labs',    
)

paper_trail = {}
for search_string in search_strings:
    # Loop through sliding window of tweet stream
    tweets = []
    done_sliding = False

    query_url = '?since_id=0&q=%s' % search_string
    while not done_sliding:
        search_url = search_api_url % (query_url)
        twitter = urllib.urlopen(search_url)
        json = twitter.read()
        data = simplejson.loads(json)
        if len(data['results']) == 0:
            done_sliding = True
        else:
            query_url = data['refresh_url']
            
            for tweet in data['results']:
                unesc_text = tweet['text']
                text = unesc_text.replace('\'', '\\\'')
                m = re.findall('(#\w+) and I vote for the (#\w+) topic', text)
                if len(m) == 1:
                    group = m[0][0]
                    ballot = m[0][1]
                    if ballot not in paper_trail:
                        paper_trail[ballot] = 0
                    paper_trail[ballot] += 1

for topic in paper_trail:
    print '%s :: %s' % (topic, paper_trail[topic])

    
