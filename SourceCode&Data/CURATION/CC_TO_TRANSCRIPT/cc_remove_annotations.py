#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = 'cc_remove_annotations.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"
#
# Convert close caption files to transcript files
#

import os

import re

def find_annotations(s):
    return re.findall(r"\[([A-Za-z0-9_]+)\]", s)

def find_annotations2(s):
    return re.findall(r"\((\w+)\)", s)

def del_annotations(s):
    return re.sub("[\(\[].*?[\)\]]", "", s)

def remove_annotations(infile,outfile):
    fi = open(infile, 'r')
    fo = open(outfile, 'w')

    doc_in  = str.decode(fi.read(), "UTF-8", "ignore")

    doc_out =del_annotations(doc_in).encode('utf-8')

    fo.write(doc_out)

    fo.close()
    fi.close()

# Loop thru directory containing transcripts
def main():
    print(indir, outdir)

    for filename in os.listdir(indir):
        if filename.endswith(".txt"):
            infile = indir + '/' + filename
            outfile = outdir + '/' + filename
            remove_annotations(infile,outfile)

if __name__ == "__main__":
    indir = '../CC_TRANSCRIPTS'
    outdir = './CC_TRANSCRIPTS3'
    main()