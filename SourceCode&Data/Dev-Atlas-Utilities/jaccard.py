#!/usr/bin/env python
from __future__ import print_function
#
# Computes jaccard metrics.
#
def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)

def jaccard_similarity3(x, y,z):
    intersection_cardinality = len(set.intersection(*[set(x), set(y),set(z)]))
    union_cardinality = len(set.union(*[set(x), set(y), set(z)]))
    return intersection_cardinality / float(union_cardinality)

def jaccard_similarityn(*argv):
    l=[]
    for arg in argv:
        l.append(set(arg))
    intersection_cardinality = len(set.intersection(*l))
    union_cardinality = len(set.union(*l))
    return intersection_cardinality / float(union_cardinality)

def jaccard_similarityp(matrix):

    m=[]

    for doc1 in matrix:
        row=[]

        for doc2 in matrix:
            js=jaccard_similarityn(doc1, doc2)

            row.append(js)
        m.append(row)

    print ("\njaccard: len(m):",len(m))
    return m

