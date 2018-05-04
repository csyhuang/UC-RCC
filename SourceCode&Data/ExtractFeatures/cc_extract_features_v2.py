#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = 'cc_extract_features_v2.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

###########################################################
# Preprocess text files
# Returns  dictionary text_dict
# key is case ID
# values is file text
###########################################################

import os
import re
import json
import datetime


###########################################################
# Process worksheet
# Return dictionary tag_dict
# Key is case ID
# Value is tag set
###########################################################

#from process_worksheet_v1 import preprocess_worksheet
from preprocess import create_tag_dict
from preprocess import create_text_dict_j
from preprocess import create_text_dict_l

################################################################################

def main():

    from call_nlu import call_nlu

    print ( )
    print ('Start process_workseet: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    tag_dict = create_tag_dict(xls_pathname,v=True)
    print ('End process_worksheet: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    print( )
    print ('Start process_textfiles: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    text_dict = create_text_dict_j(transcript_dir, tag_dict)
    print ('End process_textfiles: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    print ( )
    print ('Start NLU processing: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    call_nlu(text_dict)
    print ('End NLU processing: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    with open(text_dict_filename, 'w') as outfile:
        json.dump(text_dict, outfile)

    import pickle

    pickle.dump(text_dict, open(picklejar_filename, "wb"))


if __name__ == "__main__":

    xls_pathname = '../TW Case List.xlsx'

    transcript_dir = '../CC_TRANSCRIPTS2'

    text_dict_filename = 'text_dict5.json'

    picklejar_filename = "text_dict5.p"

    st = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    main()