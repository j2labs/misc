#!/usr/bin/env python

###############################################################
# jresize ::: http://j2d2.tumblr.com/post/73821449/jresize-py #
###############################################################

from PIL import Image
from os import listdir, mkdir
from os.path import exists as direxists
from shutil import rmtree

compatible_extensions = ['jpg','png','gif','bmp']
def check_extension(file_name):    
    for ext in compatible_extensions:
        if file_name.lower().endswith('.'+ext):
            return True
    return False

def downsize_img_proportionally(file, width):
    img = Image.open(file)
    wpercent = (width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    shrunk = img.resize((width,hsize),Image.ANTIALIAS)
    return shrunk

shrunk_dir_default = "/shrunk"
def downsize_directory(dir, width, shrunk_dir=None):
    if not shrunk_dir:
        shrunk_dir = dir+shrunk_dir_default
    if not shrunk_dir.endswith('/'):
        shrunk_dir += '/'
    if not dir.endswith('/'):
        dir += '/'
    if direxists(shrunk_dir):
        rmtree(shrunk_dir)
    mkdir(shrunk_dir)
    for f in listdir(dir):
        if check_extension(f):
            print f
            shrunk = downsize_img_proportionally(dir+f, width)
            shrunk.save(shrunk_dir+f)

if __name__ == '__main__':
    import sys
    width = None
    img_dir = None
    if len(sys.argv) == 3:
        width = int(sys.argv[1])
        img_dir = sys.argv[2]
        downsize_directory(img_dir, width)
    else:
        print "Error: try %s width img_dir" % (sys.argv[0])
