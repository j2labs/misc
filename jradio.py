#!/usr/bin/env python

#############################################################
# jradio ::: http://j2d2.tumblr.com/post/73499186/jradio-py #
#############################################################

import urllib2
import sys
import os
import re
import time

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
    station_name = None
    station_url = None
    list_found = False
    regex_station = re.compile('<!-- (.*) -->')
    regex_url = re.compile('<a href="(.*)" >.*')
    for line in page:
        if not list_found:
            if '<!-- updated ' in line:
                list_found = True
        else:
            m = regex_station.match(line)
            if m and not station_name:
                station_name = m.group(1)
                m = None
            m = regex_url.match(line)
            if m and station_name:
                station_url = m.group(1)
                pls_name_info = station_url.rsplit('/')
                pls_url = url + pls_name_info[2] + '.pls'
                irs = InternetRadioStation(name=station_name,
                                           pls_url=pls_url)
                station_list.append(irs)
                station_name = None
    return station_list
        
if __name__ == "__main__":
    print crank_the_radio()

