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

#mp3_player = '/opt/local/bin/mpg321 -q '
mp3_player = '/opt/local/bin/mpg123 -q '
somafm_url = 'http://somafm.com/'
stations_info = (
    ('Bassdrive', 'http://www.bassdrive.com/v2/streams/BassDrive.pls', 'Drum n Bass Radio',),
)

class InternetRadioStation:
    """
    A simple representation of an internet radio station
    """
    def __init__(self, name=None, pls_url=None, desc=None):
        self.name = name
        self.pls_url = pls_url
        self.desc = desc
        
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

    def pad_description(self, width, padding):
        wrapped_desc = wrap(self.desc, width)
        lines = wrapped_desc.split('\n')
        padfu = lambda s: ' ' * padding + s + '\n'        
        new_desc = map(padfu, lines)
        return ''.join(new_desc).rstrip()

    def __str__(self):
        return "%s" % (self.name)

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    Found at :: http://code.activestate.com/recipes/148061/
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )


def ioctl_GWINSZ(fd):
    """
    Tabulation functions for discovering terminal width
    Found at :: http://pdos.csail.mit.edu/~cblake/cls/cls.py
    """
    try:
        import fcntl, termios, struct, os
        cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    except:
        return None
    return cr

def term_width():
    cr = ioctl_GWINSZ(0)
    if not cr:
        return 80
    else:
        return cr[1]

def crank_the_radio():
    # Initialize list with soma.fm
    station_list = scrape_somafm_info(somafm_url)
    
    # include additional pls files
    for station in stations_info:
        station_obj = make_station(station)
        station_list.append(station_obj)
        
    print "Stations:"
    for key, station in enumerate(station_list):
        print "  %2d. %s :: %s\n%s" % (key,
                                       station.name,
                                       station.pls_url,
                                       station.pad_description((term_width()-6), 6))
    choice = input("Choice ?: ")
    station = station_list[choice]
    return station.play()

def make_station(station_tuple):
    name = station_tuple[0]
    pls = station_tuple[1]
    desc = station_tuple[2]
    return InternetRadioStation(name, pls, desc)

def format_station_description(description):
    description = description.replace("\n", "")
    description = description.replace("  ", " ")
    description = description.replace("  ", " ")
    description = description.strip()
    return description
    
def scrape_somafm_info(url):
    station_list = []
    page = urllib2.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html)
    for station in soup.fetch('li'):
        station_name = station.h3.contents[0]
        station_desc = ' '.join(station('p', {'class':'descr'})[0].contents)
        station_desc = format_station_description(station_desc)
        station_url = station.a['href']
        pls_name_info = station_url.rsplit('/')
        pls_url = '%s%s%s' % (url, pls_name_info[2], '.pls')
        irs = InternetRadioStation(name=station_name,
                                   pls_url=pls_url,
                                   desc=station_desc)
        station_list.append(irs)
    return station_list
        
if __name__ == "__main__":
    print crank_the_radio()

