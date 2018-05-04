#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "lda_transcripts,py"
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

#
# Create and manage document term matrix; generate lda model
# Marshall full set of transcript documents for LDA analysis
#
from document_term_matrix import DocumentTermMatrix

import os,re,json

from preprocess import create_title_list

dtm=DocumentTermMatrix()

titles, docs = create_title_list('../CC_TRANSCRIPTS3/')
print (len(titles),len(docs))

for title, doc in zip(titles, docs):
    dtm.add_doc(title,doc)

#dtm.print_input()

dtm.create()

dtm.print_DTM()

dtm.lda(n_topics=10)

dtm.topic()