#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "cc_utterance_analyzer.py"
__author__ = "Frank J. Greco"
__copyright__ = "Copyriight 2015-2018, Frank J Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "Development"

#
# Plot heat map of cosine similarities between pairs of intra-transcript utterances.
#

import datetime


import nltk
import sys
import frame_stack as fs

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer


import pandas as pd

reload(sys)
sys.setdefaultencoding('utf8')

def read_file2(indir, testfile,frame_size):

    sx = fs.FrameStack(frame_size)

    fullpath=indir+'/'+testfile

    print ("\nFullpath: "+fullpath+"\n")

    ulist = [line.rstrip('\n') for line in open(fullpath)]

    print (ulist)

    return ulist


def vectorize(train_set):

    print("Vectorize...")

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

    # for item in zip(doc_ids, doc_names,cosine_scores[0]):
    #    print item

    len_train_set=len(train_set)

    print ("len_train_set:", len_train_set)

    cs3=pd.DataFrame(cosine_scores3)

    print (type(cs3))

    print (cs3)

    return cs3

def heatmap3(cs3):
    from bkcharts import HeatMap, show, output_file
    from bokeh.palettes import RdGy11 as palette  # @UnresolvedImport
    from bokeh.models import HoverTool
    from bokeh.models import CrosshairTool

    crosshair = CrosshairTool()


    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("(x,y)", "(@x,@y)"),
        ("score", "@values")
    ])

    print (type(cs3))

    score = []
    for x in c3.apply(tuple):
        score.extend(x)

    data = {
        'utterance1': list(cs3.index) * len(cs3.columns),
        'utterance2': [item for item in list(cs3.columns) for i in range(len(c3.index))],
        'score': score,
    }


    output_file('utterance_heatmap.html')
    hm = HeatMap(data, x='utterance1', y='utterance2', values='score', title='Cosine Similarity', tools=[hover,crosshair], stat=None, palette=palette)
    #show(hm)
    return hm

def sidebyside(hm,ulist,transcript,html_fn):
    from bokeh.embed import components
    script, div = components(hm)

    tl = ' '
    for i in range(0, len(ulist)):
        tl = tl + '<p style="text-align:left">{}:{}'.format(str(i),ulist[i])



    d = {'transcript': transcript, 'script': script, 'div': div, 'text': tl}

    html_template = """
     <!DOCTYPE html>
     <html lang="en">
         <head>

             <meta charset="utf-8">
             <title>Heat Map %(transcript)s </title>

             <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.6.min.css" type="text/css" />
             <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.6.min.js"></script>

             %(script)s

         </head>
         <body>
         
         <h2>Heat Map %(transcript)s</h2>
        
          <table style="width:100">
           <tr>
             <th> %(div)s </th>
             <th>  
                 <div style="overflow: auto; align:left; width:600px; height:200px;">
                 %(text)s.
                 </div
             </th>
            <tr>
             <th>  
                 <div style="overflow: auto; align:left; width:600px; height:200px;">
                 %(text)s.
                 </div
             </th>
           </table> 
         </body>
     </html>
     """

    html_source = html_template % d

    fd = open(html_fn+'.html', 'w')

    fd.write(html_source)



def split_into_sentences(text):
    sent_text = nltk.sent_tokenize(text)  # this yields a list of sentences
    return sent_text

if __name__ == '__main__':

    print ('Start processing: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    indir = '../CC_TRANSCRIPTS3'

    testfile1 = 'Copy of 001 ENLEAYA001.srt.txt'
    testfile2 = 'Copy of 021 SSH EA 021edited.srt.txt'
    testfile3 = 'Copy of 1062 SCI AYA 1062edited.srt.txt'

    testfile4 = 'gba.txt'

    testfile=testfile3

    ulist = read_file2(indir, testfile, 3)

    c3 = vectorize(ulist)

    hm = heatmap3(c3)

    sidebyside(hm,ulist,testfile,'1062_SCI_AYA')

    print ('\nEnd  processing: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

