#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "multi_transcript_vectors.py"
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
# K Nearest Neighbor
###########################################################
import collections
import datetime

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

from sklearn.neighbors import KNeighborsClassifier

from sklearn.utils import shuffle

import numpy as np

import json
import pickle


def vectorize(train_dict):

    train_set = []
    key_list=[]

    od = collections.OrderedDict(sorted(train_dict.items()))
    for key in od.keys():
        key_list.append(key)
        train_set.append(od[key]['text'])

    #key_list, train_set = shuffle(key_list, train_set, random_state=0)

    vectorizer1 = HashingVectorizer()
    vectorizer2 = TfidfVectorizer()
    vectorizer3 = CountVectorizer()

    matrix_train1 = vectorizer1.fit_transform(train_set)  # finds the Hashing score with normalization
    matrix_train2 = vectorizer2.fit_transform(train_set)  # finds the tfidf score with normalization
    matrix_train3 = vectorizer3.fit_transform(train_set)  # finds the Count score with normalization
    # [n:m] controls what document[s] are  compared to. Comparison values are stored as lists in a list.
    # [0:1] causes he first element of tfidf_matrix_train to me compared to the remaining elements.

    # for item in zip(doc_ids, doc_names,cosine_scores[0]):
    #    print item
    return matrix_train1, matrix_train2, matrix_train3, od


def vectors_from_dict(text_dict='text_dict5.json', tags=[]):

    v=collections.OrderedDict()

    with open(text_dict) as data_file:
        text_dict = json.load(data_file)

    od = collections.OrderedDict(sorted(text_dict.items()))

    for tag in tags:

        v[tag]=[]

        for key in od.keys():

            if tag in text_dict[key]['tags']:
                v[tag].append(1)

            else:
                v[tag].append(0)

        print ('Tag: {}, Count: {}'.format(tag, len(v[tag])))

    return  v



def create_y_multilabel(tags):

    v = vectors_from_dict(text_dict='text_dict5.json', tags=tags)


    vlist=[]

    for key in v.keys():
        vk=v[key]
        vlist.append(vk)
        #print(key,vk)

    #y_multilabel = np.c_[v['TW04'],v['TW12']]

    tlist=[]
    for tag in tags:
        tlist.append(v[tag])

    y_m = []
    for i in range(len(tlist[0])):
        t = []
        for j in tlist:
            t.append(j[i])
        y_m.append(t)

    y_multilabel= np.array(y_m)

    print('multilabel.shape:', y_multilabel.shape)

    #print("\ny_multilabel:\n",y_multilabel)

    return y_multilabel

def create_x_train(text_dict):

    print ('\nvectorize')
    m1, m2, m3, od= vectorize(text_dict)

    #print ("\ntype(m)", type(m2))
    #print('\nm2:' m2)
    #print ("\nm2",m2.shape)
    #print ("\nm2[0]:",m2[0])
    #print("\nm2[0].shape:", m2[0].shape)
    #print("\nm2[216].shape:", m2[216].shape)

    m2a=m2.toarray()

    #print ('\nm2a',m2a)
    #print ('len(m2a)',len(m2a))
    #print('len(m2a[0])', len(m2a[0]))
    return m2a

def main(args):

    import json

    with open('text_dict5.json') as fp:
        text_dict = json.load(fp)

    print("\n# retained documents:", len(text_dict))

    X=create_x_train(text_dict)

    y = create_y_multilabel(tags)

    split = 200

    n_shuffles=5

    total_test_successes=0
    total_test_failures=0

    total_train_successes = 0
    total_train_failures = 0

    print('Tags:', tags)

    for j in range(n_shuffles):
        print("Run:{}".format(j))
        #print('\nCall KNeighborsClassifier:')
        knn_clf = KNeighborsClassifier()

        #print('\nCall knn_clf.fit')
        knn_clf.fit(X[:split], y[:split])

        test_successes=0
        test_failures=0

        for i in range(len(X[split:])):

            key=i+split

            target = [X[key]]

            pred=knn_clf.predict(target)

            if (pred[0] == y[key]).all():
                test_successes += 1
            else:
                test_failures += 1


        total_test_successes += test_successes
        total_test_failures += test_failures


        #####################################
        train_successes = 0
        train_failures = 0

        for key in range(len(X[:split])):



            target = [X[key]]

            pred = knn_clf.predict(target)

            if (pred[0] == y[key]).all():
                train_successes += 1
            else:
                train_failures += 1

        total_train_successes += train_successes
        total_train_failures += train_failures


        #####################################

        X, y = shuffle(X, y, random_state=0)


    print ("Total Test Successes: {} Total Test Failures: {}".format(total_test_successes, total_test_failures))

    test_success_ratio=float(total_test_successes)/(total_test_successes + total_test_failures)

    print ("test_success_ratio: {}".format(test_success_ratio))


    print("\nTotal Train Successes: {} Total Train Failures: {}".format(total_train_successes, total_train_failures))

    train_success_ratio = float(total_train_successes) / (total_train_successes + total_train_failures)

    print("train_success_ratio: {}".format(train_success_ratio))


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--xls_dir", type=str, default='../', help="Worksheet directory")
    argparser.add_argument("--xls_name", type=str, default='TW Case List.xlsx', help="Case List worksheet")
    argparser.add_argument("--transcript_dir", type=str, default='../CC_TRANSCRIPTS2', help="Transcript dir")
    parsed_args = argparser.parse_args()

    # tags = ['TW04','TW05', 'TW07', 'TW08','TW09']
    # tags = ['TW01', 'TW02', 'TW03', 'TW04', 'TW05', 'TW06', 'TW07', 'TW08', 'TW09', 'TW10', 'TW11', 'TW12',
    # 'TW13', 'TW14', 'TW15', 'TW16', 'TW17', 'TW18', 'TW19', 'TW20', 'TW21', 'TW22', 'TW23', 'TW24']

    tags = ['TW04', 'TW12']

    main(parsed_args)


