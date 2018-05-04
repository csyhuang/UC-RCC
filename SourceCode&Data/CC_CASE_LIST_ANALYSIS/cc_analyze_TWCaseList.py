#!/usr/bin/env python
# coding: utf-8
# from __future__ import print_function

__source__ = 'cc_analyze_TWCaseList.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

#
# Read TW Case list, treat tag labels as documents, create tfidf matrix, plot cosine similarities
# comparing first doc to the remaining docs.
#

import xlrd
import collections
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def main(xls_pathname,outdir,outfile):
    print
    print "outdir",outdir
    print "xls_pathname",xls_pathname
    print "outputfile",outfile

    wb = xlrd.open_workbook( xls_pathname)
    print
    print wb.sheet_names()

    # Read sheet

    sheet = wb.sheet_by_index(2)

    # first column (CaseID) :
    first_column = sheet.col_values(0)

    #fourth column (Tag labels):
    fourth_column = sheet.col_values(3)

    tag_dict=collections.OrderedDict()

    for x,y in zip(first_column,fourth_column):
        try:
            if int(x) in tag_dict.keys():
                tag_dict[int(x)].append(y)
            else:
                tag_dict[int(x)]=[y]
        except:
            print "error",x
            pass


    #print tag_dict

    print
    for x in tag_dict.keys():
        print x, ','.join(tag_dict[x])


    train_set=[]
    doc_names=[]
    name_tokens=[]
    doc_ids=[]

    for x in tag_dict.keys():

        try:
            doc_ids.append(x)
            #doc = str.decode(fi.read(), "UTF-8", "ignore")
            doc_names.append(x)
            train_set.append(','.join(tag_dict[x]))
        except:
            pass
    #
    # Adapted from skilearn examples...
    #
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)  #finds the tfidf score with normalization
    cosine_scores = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)
    # [n:m] controls what document[s] are  compared to. Comparison values are stored as lists in a list.
    # [0:1] causes he first element of tfidf_matrix_train to me compared to the remaining elemements.

    print
    for item in zip(doc_ids, doc_names,cosine_scores[0]):
        print item

    from bokeh.plotting import figure, output_file, show


    x=doc_ids
    y=cosine_scores[0]

    # Output to HTML file
    output_file(outdir + '/' + outfile)

    # Plot results
    p = figure(title="cosine vs doc id", x_axis_label='Case ID', y_axis_label='Cosine(angle between Doc 1 & all others')

    p.circle(x, y, color="red", legend="tags.")

    # Display plot
    show(p)

if __name__ == "__main__":
    main(xls_pathname='../CC_FILES_TAGLIST/TW Case List.xlsx',outdir='.',outfile="cc_tags.html")
