#!/usr/bin/env python

import simplejson
import urllib
import re

# requires formatting
search_api_url = 'http://search.twitter.com/search.json%s&rpp=100'

# each search string is searched individually
# be mindful of api limitations (150 queries per hour, last i checked)
vote_strings = (
    'jdennis_robinhood13347',
    'sgreenwood_robinhood41608',
    'mperry_sexmoneyanati18868',
    'tbiel_gayforgood18263',
    'emccombs_bigbrothers68923',
    'skennedy_solvingkids19117',
    'jbonnet_healinghaiti14631',
    'jlowry_arton16718',
    'ahood_avivafamilyand20129',
)

paper_trail = {}
for vote_string in vote_strings:
    # Loop through sliding window of tweet stream
    tweets = []
    done_sliding = False

    query_url = '?since_id=0&q=%s' % vote_string
    
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
                if vote_string not in paper_trail:
                    paper_trail[vote_string] = 0
                paper_trail[vote_string] += 1

for vote_string in paper_trail:
    print '%s :: %s' % (vote_string, paper_trail[vote_string])

    
