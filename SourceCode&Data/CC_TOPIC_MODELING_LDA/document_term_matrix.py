#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from __future__ import print_function

__source__ = "document_term_matrix,py"
__author__ = "Frank J. Greco"
__copyright__ = ""
__credits__ = "https://pypi.python.org/pypi/lda#downloads"
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = "Frank J. Greco"
__email__ = ""
__status__ = "Development"

#create and manage document term matrix; generate lda model

import numpy as np
import textmining
import lda.datasets

class DocumentTermMatrix():
    # Initialize class to create term-document matrix


    def __init__(self):
        self.tdm = textmining.TermDocumentMatrix()
        self.docs = []
        self.titles = []

    def reset(self):
        self.docs = []
        self.titles = []

    def add_doc(self,title,doc):
        self.titles.append(title)
        self.docs.append(doc)

    # create a  variable with doc-term info
    def create(self):
        for doc in self.docs:
            self.tdm.add_doc(doc)

        self.dtm = list(self.tdm.rows(cutoff=1))
        self.vocab = tuple(self.dtm[0])
        self.X = np.array(self.dtm[1:])
        return self.dtm

    # get document-term matrix from remaining rows
    def get_dtm(self):
        return self.dtm

    def get_X(self):
        return self.X

    def get_vocabulary(self):
        return self.vocab

    def print_input(self):
        print("\nDocuments:")
        for n, doc in enumerate(self.docs):
            print("document {}: {}".format(n + 1, doc))

        print("\nTitles:")
        for n, title in enumerate(self.titles):
            print("title {}: {}".format(n + 1, title))

        print("\nCombined Titles and Documents:")
        for n, item in enumerate(list(zip(self.titles, self.docs))):
            print("Item {}: {}".format(n + 1, item))

    def print_DTM(self):
        # Document-term matrix
        print("\nDocument-term Matrix:\n")
        print("\ntype(X): {}".format(type(self.X)))
        print("\nshape: {}".format(self.X.shape))
        print("X:", self.X, sep="\n" )
        print("\nNumber of rows = number of documents, number of columns = number of word in the vocabulary")

        # Vocabulary
        print("\nVocabulary:")
        print("\ntype(vocab): {}".format(type(self.vocab)))
        print("\nlen(vocab): {}".format(len(self.vocab)))
        print("\nWords:", self.vocab, sep="\n")


    def lda(self, n_topics=2, random_state=0, n_iter=100):

        self.model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=random_state)

        self.model.fit(self.X)  # model.fit_transform(X) is also available

        print('Model Fit: ', self.model.fit(self.X))
        print
        print('Model components: ', self.model.components_)
        print
        print('Log likelihood: ', self.model.loglikelihood())
        print


    def topic(self, mod='', v=''):
        topic_word = self.model.topic_word_  # model.components_ also works
        n_top_words = 8
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(self.vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
            print("Topic {}: {}".format(i, ' '.join(topic_words)))


