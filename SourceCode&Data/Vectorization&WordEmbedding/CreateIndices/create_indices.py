#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = 'create_indices.py'
__author__ = ""
__copyright__ = ""
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = ""

import os
import re
from preprocess import TranscriptIndex

def test1():
    tx = TranscriptIndex(transcript_dir = '../../CC_TRANSCRIPTS3')

    idx = tx.create_index()

    fn = tx.get_filename(004)
    print("filename1:", fn)

    #kl = tx.get_keys(fn[0])

    #print("keys:", kl)

    print('idx', idx)

    fn = tx.get_filename(tx.get_keys(fn[0])[0])
    print("filename2:", fn)

def test2():
    tx = TranscriptIndex(transcript_dir = '../../CC_TRANSCRIPTS3')

    idx = tx.create_index()

    # kl = tx.get_keys(fn[0])

    # print("keys:", kl)

    # print('idx', idx)

    tx.make_pickle("index_dict3.p")

def test3():
    tx = TranscriptIndex(transcript_dir = '../../CC_TRANSCRIPTS3')

    tx.use_pickle("index_dict3.p")

    kl = tx.get_keys("xxx")

    print("keys:", kl)

    print('idx', tx.index_dict)

    fn = tx.get_filename(004)
    print("filename:", fn)

if __name__ == "__main__":

    test1()








