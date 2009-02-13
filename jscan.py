#!/usr/bin/env python

import socket
import sys

def usage():
    print "jscan host:port host:po-rt host:p,o,r,t"
    print "jscan 127.0.0.1:631,21,80"

class Scanner():
    def __init__(self, description):
        try:
            self.host,port_desc = description.split(':')
            
            if port_desc.find('-') > 0:
                start, end = port_desc.split('-')
                istart = int(start)
                iend = int(end)
                self.ports = range(istart, iend)
            elif port_desc.find(','):
                ports = port_desc.split(',')
                self.ports = map(int, ports)
            else:
                self.ports = [int(port_desc)]

        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        
    def scan(self):
        print "Scanning %s" % (self.host)
        for port in self.ports:
            try:
                sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sd.connect((self.host, port))
            except socket.error:
                pass
            else:
                print "  open: %d" % (port)
                sd.close()

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        usage()
    for arg in sys.argv[1:]:
        s = Scanner(arg)
        s.scan()

