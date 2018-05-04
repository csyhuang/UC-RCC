#!/usr/bin/env python
# coding: utf-8
# from __future__ import print_function

__source__ = 'extract_annotations.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

'''
Extract transcriber annotations from  transcript document

Input: document string object

Output: document string with annotations removed and list object containing annotations

Expanded annotation vector to include missing values

'''

from preprocess import create_annotation_vector


if __name__ == "__main__":

    infile = '../CC_TRANSCRIPTS2/Copy of 611 GEN MC 611 edited.srt.txt'
    ulist, annotation_vector = create_annotation_vector(infile)
    print (len(ulist), len(annotation_vector))
    print (annotation_vector)






