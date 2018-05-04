#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "cc_n_gram_v2.py"
__author__ = "Frank J. Greco"
__copyright__ = ""
__credits__ = []
__license__ = "Apache"
__version__ = "2"
__email__ = ""
__status__ = "Development"

import json

from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import HashingVectorizer

import datetime

###########################################################
# extract X array of documents y array of labels
# Returns  X and y
###########################################################

def extractXy(text_dict):
    print("\n*** Begin extractXy ***\n")
    y = []
    X = []

    print("\n[Begin text_dict (key, doc[0:10], taglist)]\n")
    for k in text_dict.keys():
        y.append(text_dict[k]['tags'])
        X.append(text_dict[k]['text'])
        print(k, text_dict[k]['text'][0:10], text_dict[k]['tags'])

    print("\n[End of text_dict]")

    print("\nReturning X,y (Here are first 10 characters of the first 3 X records and the assoicated y values:)\n")
    for a, b in zip(X, y)[0:3]:
        print(a[0:10], b)
    print("\n*** End extractXy ***\n")
    return X, y



###########################################################
# encode_documents
# Returns encoded matrix using count_vectorizer
###########################################################

def encode_documents(X, n_gram_lower=1, n_gram_upper=1):
    print("\n*** Begin encode_documents ***\n")

    # vectorizer = CountVectorizer()
    vectorizer = CountVectorizer(ngram_range=(n_gram_lower, n_gram_upper), token_pattern=r'\b\w+\b', min_df=1)

    print(type(vectorizer))

    encoded_matrix = vectorizer.fit_transform(X)

    word_index = dict()
    for key in vectorizer.vocabulary_.keys():
        word_index[vectorizer.vocabulary_[key]] = key

    print("\n*** End encode_documents ***\n")

    return encoded_matrix, word_index


def print_encoded_matrix(encoded_matrix, word_index):
    print("\n*** Begin print_encoded_matrix ***\n")

    print(type(encoded_matrix))

    print("\nlength encoded_matrix:", len(encoded_matrix.toarray()))

    print("\nsparce encoded_matrix[0]:\n")

    print(encoded_matrix[0])

    print("\nsparce encoded_matrix.toarray()[][82600:82610]\n")

    #for item in encoded_matrix.toarray():
    #    print(item[82600:82610])

    #for x in range(82600, 82610):
    #    if x in word_index.keys():
    #        print(x, word_index[x])

    total = 0
    for item0 in encoded_matrix.toarray():
        for item1 in item0:
            total += item1

    print('total n_grams:', total)

############ n_gram_extractor ##############

def n_gram_extractor(text_dict, n_gram_lower=1, n_gram_upper=1):
    print("\n*** Begin n_gram_extractor ***")

    vectorizer = CountVectorizer(ngram_range=(n_gram_lower, n_gram_upper), token_pattern=r'\b\w+\b', min_df=1)

    analyze = vectorizer.build_analyzer()

    ng_list = []

    count = 0

    ng_total = 0

    reverse_index=[]

    for k in text_dict.keys():
        Z = text_dict[k]['text']

        ng = analyze(Z)

        ng_list.append(ng)

        print("Excerpt:", Z[0:20])

        print("Count: {} Doc Key: {}, n-gram len: {}, n-gram excerpt: {}\n".format(count, k, len(ng), ng[0:10]))

        ng_total += len(ng)

        reverse_index.append(k)

        count += 1

    print("ng_total: ", ng_total)

    print("\n*** End n_gram_extractor ***\n")

    return ng_list,reverse_index


###########################################################
# K-Mean
# Performs K-Mean cluster analysis on encoded matrix
###########################################################

def KM(encoded_matrix, labels, n_clusters=3):
    from sklearn import metrics

    print("\nBegin KM\n")

    from sklearn.cluster import KMeans

    print("K-means calculation...")
    km = KMeans(n_clusters=n_clusters)


    print("fit")
    print(km.fit(encoded_matrix))

    print("centers")
    print(km.cluster_centers_)

    print("len m", len(km.labels_))

    print("predict")
    prediction=km.predict(encoded_matrix)
    print (prediction)

    print("labels")
    print(km.labels_)

    print()

    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
    print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
    print("Adjusted Rand-Index: %.3f"
          % metrics.adjusted_rand_score(labels, km.labels_))
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(encoded_matrix, km.labels_))

    print()




    print("\nEnd KM\n")



    return prediction

def main():
    print('Start time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    #with open('text_dict4s.txt') as data_file: #4s keeps multiple occurances of a tag
    with open('text_dict5.json') as data_file:
        text_dict = json.load(data_file)

    X, y = extractXy(text_dict)

    ng_list, reverse_index = n_gram_extractor(text_dict, n_gram_lower=2, n_gram_upper=2)

    print("\nreverse_index\n")
    print (reverse_index)

    encoded_matrix, word_index = encode_documents(X, n_gram_lower=2, n_gram_upper=2)

    #print_encoded_matrix(encoded_matrix, word_index)

    prediction=KM(encoded_matrix, y, n_clusters=2)

    for i in range(0,len(prediction)):
        print (i, reverse_index[i], prediction[i])

    s0 = set()
    s1 = set()
    s2 = set()
    d0 = []
    d1 = []
    d2 = []
    for i, l in enumerate(zip(text_dict.keys(), prediction)):
        print(i, l)
        if l[1] == 0:
            s0.add(l[0])
            d0.append(text_dict[l[0]]['filename'])

        elif l[1] == 1:
            s1.add(l[0])
            d1.append(text_dict[l[0]]['filename'])
        else:
            s2.add(l[0])
            d2.append(text_dict[l[0]]['filename'])

    print()
    print('s0:', s0)
    print('d0:', d0)

    print()
    print('s1:', s1)
    print('d1:', d1)

    print()
    print('s2:', s2)
    print('d2:', d2)

    print('End time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))


if __name__ == "__main__":

    main( )