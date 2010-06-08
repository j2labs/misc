#!/usr/bin/env python

import csv
import sys
import re
import os
from optparse import OptionParser

def DoReshapeProcess(Input, Output='default'):
    """Determine whether to process the input as a file or list of files contained in an input directory.
    Create an output directory to write output files if the input is a directory.
    
    @Input - csv file or directory containing csv files
    @Output - if specified, ouput files will be written to this directory
    
    """
    
    if os.path.isdir(Input):
        FileList = os.listdir(Input)
        if Output == 'default':
            os.mkdir('out')
        for EachFile in FileList:
            ReshapeAMTCSV(os.path.join(Input, EachFile), os.path.join(os.getcwd(), 'out'))
    elif os.path.isfile(Input):
        ReshapeAMTCSV(Input)
    else:
        print 'Input is not supported'
        
def ReshapeAMTCSV(InputFile, Output='default'):
    """Parse an input file containing data exported from ATM and write out simplified file in an out directory.
    
    @Input - Input csv file
    """
    
    f = open(InputFile)
    file_data = f.readlines()
    handler = csv.reader(file_data)
    headers = handler.next()
    
    # find header info and prepare data structures
    info_lines = []
    for i,h in enumerate(headers):
        if h == 'AssignmentStatus':
            ass_status = int(i)
        #29/01/2010 Johann added info about starting time for the task
        if h == 'AcceptTime':
            ass_start = int(i)
        #29/01/2010 Johann added info about submit time for the task
        if h == 'SubmitTime':
            ass_submit = int(i)
        #29/01/2010 Johann added info about location of worker
        if h == 'Answer.where_live':
            worker_location = int(i)
        #29/01/2010 Johann added info about period of time during which worker has been speaking language
        if h == 'Answer.how_long':
            english_long = int(i)
        if h == 'WorkerId':
            worker_id = int(i)
        if h == 'Input.numSegs':
            input_segments = int(i)
            info_group = [None] * 3
            
            # number of segments is on line below headers
            next_line = handler.next()
            num_segs = int(next_line[i])
            print num_segs
            #info_lines = [[None, None, None] for i in xrange(int(num_segs) + 1)]
            info_lines = [[None, None] for i in xrange(int(num_segs) + 1)]
            print info_lines
            handler = csv.reader(file_data)
            handler.next()
    
    
    #    m = re.findall('Input.seg(\d+)', h)
    #    if len(m) == 1:
    #        print 'Here'
    #        seg_id = int(m[0])
    #        try:
    #            info_lines[seg_id][0] = int(i)
    #        except IndexError:
    #            pass
            
        m = re.findall('Answer.seg(\d+)', h)
        if len(m) == 1:
            seg_id = int(m[0])
            #info_lines[int(seg_id)][1] = int(i)
            info_lines[int(seg_id)][0] = int(i)
    
        m = re.findall('Answer.translation(\d+)', h)
        if len(m) == 1:
            seg_id = int(m[0])
            #info_lines[int(seg_id)][2] = int(i)
            info_lines[int(seg_id)][1] = int(i)
    
    #29/01/2010: Johann added tab as delimiter instead of comma
    if Output == 'default':
        #writer = csv.writer(sys.stdout, delimiter='\t')
        writer = csv.writer(sys.stdout)
    else:
        #writer = csv.writer(open(os.path.join(Output, 'mod_' + os.path.basename(InputFile)), 'wb'), delimiter='\t')
        writer = csv.writer(open(os.path.join(Output, 'mod_' + os.path.basename(InputFile)), 'wb'))
            
    # Print a line for 
    for l in handler:
        # seg id's start with 1. thus, so do we
        for seg_id in xrange(1, int(num_segs)+1):
            line = (l[ass_status],
                    l[worker_id],
                    l[ass_start],
                    l[ass_submit],
                    l[input_segments],
                    l[english_long],
                    l[worker_location],
                    l[ info_lines[seg_id][0] ],
                    l[ info_lines[seg_id][1] ],
#                    l[ info_lines[seg_id][2] ]
                                    )
            writer.writerow(line)

if __name__ == "__main__":
    parser = OptionParser(usage="%prog -i input <-o=outputdir>")
    parser.add_option('-i', '--input', dest='input', action='store',
                      help='Input to parse (file or directory)')
    parser.add_option('-o', '--outputdir', dest='output', action='store', help='Optional output directory to write output files')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    (options, args) = parser.parse_args()
    DoReshapeProcess(options.input, options.output)
