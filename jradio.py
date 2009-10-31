#!/usr/bin/env python

#############################################################
# jradio ::: http://j2d2.tumblr.com/post/73499186/jradio-py #
#############################################################

import urllib2
import sys
import os
import re
import time
from BeautifulSoup import BeautifulSoup

mp3_player = '/opt/local/bin/mpg321 -q '
somafm_url = 'http://somafm.com/'
stations_info = {
    'Bassdrive': 'http://www.bassdrive.com/v2/streams/BassDrive.pls',
}

class InternetRadioStation:
    """
    A simple representation of an internet radio station
    """
    def __init__(self, name=None, pls_url=None, url=None):
        self.name = name
        self.pls_url = pls_url
        
    def play(self):
        urls_available = self.urls_from_pls(self.pls_url)
        for url in urls_available:
            print '\nTrying url ::: %s' % (url)
            val = os.system(mp3_player + url)
            if val == 2:
                return '\nFinished playing'
        return "No usable urls found"

    def urls_from_pls(self, pls_url):
        playlist = urllib2.urlopen(pls_url)
        urls = []
        for line in playlist:
            p = re.compile('File\d+=(.*)')
            m = p.match(line)
            if m:
                url_line = m.group(1)
                if not url_line.endswith('/'):
                    url_line += '/'
                urls.append(url_line)
        return urls

    def __str__(self):
        return "%s ::: %s" % (self.name, self.pls_url)

def crank_the_radio():
    # Initialize list with soma.fm
    station_list = scrape_somafm_info(somafm_url)
    
    # include additional pls files
    for name in stations_info:
        pls_url = stations_info[name]
        station_list.append(make_stations(name,pls_url))
        
    print "Stations:"
    for key, station in enumerate(station_list):
        print "  %2d. %s" % (key, station)
    choice = input("Choice ?: ")
    station = station_list[choice]
    return station.play()

def make_stations(name, pls):
    return InternetRadioStation(name, pls)

def scrape_somafm_info(url):
    station_list = []
    page = urllib2.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html)
    for station in soup.fetch('li'):
        station_name = station.h3.contents[0]
        station_url = station.a['href']
        pls_name_info = station_url.rsplit('/')
        pls_url = '%s%s%s' % (url, pls_name_info[2], '.pls')
        irs = InternetRadioStation(name=station_name,
                                   pls_url=pls_url)
        station_list.append(irs)
    return station_list
        
if __name__ == "__main__":
    print crank_the_radio()

