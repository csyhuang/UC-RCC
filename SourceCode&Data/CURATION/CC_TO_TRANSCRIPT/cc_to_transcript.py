#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = 'cc_to_transcript.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = "Frank J. Greco"
__email__ = ""
__status__ = "Development"

#
# Convert close caption files to transcript files
#

import os

def create_transcript(infile,outfile):
    fi = open(infile, 'r')
    fo = open(outfile, 'w')

    text=fi.read()
    combined=''
    for x in text.splitlines():
        if not x[:2].isdigit() and x:
            if x[0] == '-':
                if combined.startswith('-'):
                    print (combined[1:])
                    fo.write(combined[1:]+'\n')
                combined=x
            else:
                combined += ' '+ x
    print (combined[1:])
    fo.write(combined[1:]+'\n')
    fo.close()
    fi.close()

def main():
    # Loop thru directory containing cc files
    print (indir, outdir)

    for filename in os.listdir(indir):
        if filename.endswith(".srt"):
            infile = indir + '/' + filename
            outfile = outdir + '/' + filename + '.txt'
            create_transcript(infile,outfile)


if __name__ == "__main__":
    indir = '../CC_SRT_FILES'
    outdir = '../CC_TRANSCRIPTS2'
    main()