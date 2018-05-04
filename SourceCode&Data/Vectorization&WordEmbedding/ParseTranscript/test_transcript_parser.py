#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "transcript_parser_v1.py"
__author__ = "Frank J. Greco"
__copyright__ = ""
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "Development"

'''
Parse transcript file into
'''


from preprocess import ParsedTranscript

if __name__ == "__main__":

    rt=ParsedTranscript('Copy of 001 ENLEAYA001.srt.txt', '../../CC_TRANSCRIPTS3')

    rt.read_file()

    rt.print_parms()

    print ()
    print (rt.get_tokenized_sentences())