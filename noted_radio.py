#!/usr/bin/env python

import json
import urllib
import os

noted_url = 'http://api.extension.fm/v1.1/user/noted.get?owner=%s'
mp3_player = '/opt/local/bin/mpg123 -q'

username = raw_input("Who's noted? ")
noted_json = urllib.urlopen(noted_url % (username)).read()
noted_list = json.loads(noted_json)

for songvo in noted_list['data']['songs']:
    song_data = songvo['songvo']
    if song_data.has_key('artist') and song_data.has_key('songtitle'):
        print "%s - %s" % (song_data['artist'], song_data['songtitle'])
        os.system('%s %s' % (mp3_player, song_data['url']))
