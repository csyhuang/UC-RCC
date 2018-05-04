#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = 'cc_metrics.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "Development"

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from jaccard import jaccard_similarityp

def calculate_similarities(train_set):

    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)  # finds the tfidf score with normalization

    cs = cosine_similarity(tfidf_matrix_train,tfidf_matrix_train)

    #print ("\ncosine_scores:\n", cs)

    js=jaccard_similarityp(train_set)

    #jaccard_scores = array(js)

    #print("\njaccard_scores:\n", js)

    return cs, js



