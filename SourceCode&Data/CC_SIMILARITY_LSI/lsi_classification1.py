#!/usr/bin/python
# coding: utf-8
from __future__ import print_function

__source__ = "lsi_classification1,py"
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

#
# Buiild an LSI model on a set of transcript testfiles
# Perform a similarity query  of a testfile against the model
# <provide outside reference here>
#


import logging
import sys
import os
import re
from gensim import corpora, models, similarities
from collections import defaultdict
from preprocess import create_doc_index
from preprocess import TagWorksheet


def main(transcript_dir,testfile,xls_pathname):
    reload(sys)
    sys.setdefaultencoding('utf8')

    print ('\ntranscript_dir:', transcript_dir)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARNING)

    documents, doc_index= create_doc_index(transcript_dir)

    # Remove common words and tokenize
    stoplist = set('for a of the and to in'.split())

    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    # Remove words that appear only once

    frequency = defaultdict(int)

    for text in texts:
                 for token in text:
                     frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    print("\nCreate and save dictionary:")
    dictionary = corpora.Dictionary(texts)
    dictionary.save('./tmp/TopicClassifier.dict') # store the dictionary, for future reference

    #print(dictionary)
    #print(dictionary.token2id)

    print ('\nOpen testfile:', testfile)

    tf = open(testfile, 'r')
    new_doc=(str.decode(tf.read(), "UTF-8", "ignore"))
    tf.close()

    print ("\nQuery document:\n")
    print(new_doc)

    print ("\nVector representation of query document:\n")
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    print(new_vec)

    print("\nCreate and save corpus:")
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('./tmp/TopicClassifier.mm', corpus)

    print("\nCorpus:")
    print(corpus)

    print("\nBuild LSI Model:")
    lsi = models.LdaModel(corpus, id2word=dictionary, num_topics=10)

    # Transform testfile document (question) to bag of words
    vec_bow = new_vec
    vec_lsi = lsi[vec_bow] # convert the query to LSI space
    print(vec_lsi)

    # Transform corpus to LSI space and index it
    index = similarities.MatrixSimilarity(lsi[corpus])
    #index = similarities.MatrixSimilarity.load(save_index)

    print("Creating sims...")
    sims = index[vec_lsi] # perform a similarity query against the corpus
    print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples

    print("Sorting sims...")
    sims_sorted = sorted(enumerate(sims), key=lambda item: -item[1])
    print(sims_sorted) # print sorted (document number, similarity score) 2-tuples

    print("Doc Index...")
    print(doc_index)

    print("Combined Results...")
    #[ print ('Seq: {} CaseID: {} File: {} Similarity: {}'.format(item[0][0], item[0][1], item[0][2], item[1])) for item in zip(doc_index,sims)]

    print ("Len(sims): {}  Len(Index): {}".format(len(sims), len(doc_index)))

    combined=[]
    for item in zip(doc_index, sims):
        combined.append((item[0][1], item[0][2], item[1]))

    combined_sorted=sorted(combined, key=lambda x: -x[-1])

    for item in combined_sorted:
        print(item)

    tw=TagWorksheet(xls_pathname)

    s = []

    #print ("tw.get.tags(825):", tw.get_tags(825))


    for item in combined_sorted[0:4]:
        tl=tw.get_tags(int(item[0]))
        print(item,'\t',tl)
        s.append(set(tl))

    print("\ntag sets:",s)

    y = set.intersection(*s)

    print ("\ntag set intersection:",y)


if __name__ == "__main__":
    testfile1='../CC_TRANSCRIPTS/Copy of 825 SCI EA 825 edited.srt.txt'
    testfile2='../CC_TRANSCRIPTS/Copy of 001 ENLEAYA001.srt.txt'
    main(transcript_dir='../CC_TRANSCRIPTS3',
         testfile=testfile1,
         xls_pathname='../CC_FILES_TAGLIST/TW Case List.xlsx')