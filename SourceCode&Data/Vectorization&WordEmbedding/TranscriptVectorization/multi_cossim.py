#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "multi-cossim.py"
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "Development"

# Author: Frank Greco
###########################################################
# Preprocess text files
# Returns  dictionary text_dict
# key is case ID
# values is file text
###########################################################
import collections
import datetime

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer


def cossim(train_dict):

    print ("# retained documents:", len(train_dict))

    train_set = []

    od = collections.OrderedDict(sorted(train_dict.items()))
    for x in od.keys():
        train_set.append(od[x]['text'])

    vectorizer1 = HashingVectorizer()
    vectorizer2 = TfidfVectorizer()
    vectorizer3 = CountVectorizer()

    matrix_train1 = vectorizer1.fit_transform(train_set)  # finds the Hashing score with normalization
    cosine_scores1 = cosine_similarity(matrix_train1, matrix_train1)
    matrix_train2 = vectorizer2.fit_transform(train_set)  # finds the tfidf score with normalization
    cosine_scores2 = cosine_similarity(matrix_train2, matrix_train2)
    matrix_train3 = vectorizer3.fit_transform(train_set)  # finds the Count score with normalization
    cosine_scores3 = cosine_similarity(matrix_train3, matrix_train3)
    # [n:m] controls what document[s] are  compared to. Comparison values are stored as lists in a list.
    # [0:1] causes he first element of tfidf_matrix_train to me compared to the remaining elements.

    #for item in zip(doc_ids, doc_names,cosine_scores[0]):
    #   print (item)
    return cosine_scores1, cosine_scores2, cosine_scores3, od

def plot_vectors(doc_no, cosine_scores1, cosine_scores2, cosine_scores3, od):
    doc_no = doc_no  # 0-203

    for item in zip(od.keys(), cosine_scores1[doc_no], cosine_scores2[doc_no], cosine_scores3[doc_no]):
        print (item)

    from bokeh.plotting import figure, output_file, show

    x = od.keys()
    y = cosine_scores3[doc_no]

    # output to HTML file
    output_file("cc_text.html")

    # create a new plot with a title and axis labels
    p = figure(title="cosine vs doc id:{}".format(doc_no), x_axis_label='x', y_axis_label='y')

    p.circle(x, y, color="blue", legend="text")

    # Display plot
    show(p)


def main(args):
    import json

    print ('Start time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    with open('text_dict5.json') as fp:
        text_dict = json.load(fp)

    print()
    print ('vectorize')
    cosine_scores1, cosine_scores2, cosine_scores3, od= cossim(text_dict)

    #plot_vectors(doc_no, cosine_scores1, cosine_scores2, cosine_scores3, od)
    print ('End time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--xls_dir", type=str, default='../', help="Worksheet directory")
    argparser.add_argument("--xls_name", type=str, default='TW Case List.xlsx', help="Case List worksheet")
    argparser.add_argument("--transcript_dir", type=str, default='../CC_TRANSCRIPTS2', help="Transcript dir")
    parsed_args = argparser.parse_args()

    doc_no=111
    main(parsed_args)