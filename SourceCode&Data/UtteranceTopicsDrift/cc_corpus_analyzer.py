#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "cc_corpus_analyzer.py"
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

#
# Plot heatmap of cosine similarities between all pairs of transcripts.
#

import datetime
import sys
import os, re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer


import pandas as pd

reload(sys)
sys.setdefaultencoding('utf8')

def read_file3(text_dict):

    dlist=[]

    for key in text_dict.keys():
        dlist.append(text_dict[key]['text'].strip('\n'))


    return dlist

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



    cs3=pd.DataFrame(cosine_scores2)

    print (cs3)

    return cs3


def heatmap3(nba):
    from bkcharts import HeatMap, show, output_file
    from bokeh.palettes import RdGy11 as palette  # @UnresolvedImport
    from bokeh.models import HoverTool
    from bokeh.models import CrosshairTool

    crosshair = CrosshairTool()

    def test_hover(x):
        return ["This is {}".format(x)]


    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("(x,y)", "(@x,@y)"),
        ("score", "@values")
    ])


    score = []

    for x in nba.apply(tuple):
        score.extend(x)


    data = {
        'transcript1': list(nba.index) * len(nba.columns),
        'transcript2': [item for item in list(nba.columns) for i in range(len(nba.index))],
        'score': score
    }


    output_file('utterance_heatmap.html')
    hm = HeatMap(data, x='transcript1', y='transcript2', values='score', title='Cosine Similarity', stat=None, tools=[hover,crosshair], palette=palette)

    #show(hm)
    return hm


def find_transcripts(caseID, transcript_dir):
    transcripts = []
    for filename in os.listdir(transcript_dir):

        if filename.endswith(".txt"):

            name_tokens = filename.split()

            s = re.sub('[^0-9]+', ' ', name_tokens[2])

            if caseID == s:

                transcripts.append(filename)
    return transcripts

def sidebyside(hm,tl, transcript_dir):
    from bokeh.embed import components
    script, div = components(hm)
    text=''
    for i in range(0, len(tl)):
        text = text + '<p style="text-align:left">{}:{}'.format(str(i), find_transcripts(tl[i],transcript_dir))

    d = {'script': script, 'div': div, 'text': text}

    html_template = """
     <!DOCTYPE html>
     <html lang="en">
         <head>
    
             <meta charset="utf-8">
             <title>Heat Map-Full Corpus</title>
    
             <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.6.min.css" type="text/css" />
             <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.6.min.js"></script>
    
             %(script)s
    
         </head>
         <body>
         <h2>Heat Map-Full Corpus </h2>
          <table style="width:100">
           <tr>
             <th> %(div)s </th>
             
             <th>  
                 <div style="overflow: auto; align:left; width:800px; height:200px;">
                 %(text)s.
                 </div
             </th>

           </table> 
         </body>
     </html>
     """

    html_source= html_template % d

    fd = open('corpus_analysis.html', 'w')
    fd.write(html_source)


if __name__ == '__main__':

    print ('Start processing: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    import pickle

    text_dict = pickle.load(open('text_dict5.p', "rb"))

    tl=[]
    for item in text_dict.keys():
        tl.append(item)

    dlist = read_file3(text_dict)

    cs3 = vectorize(dlist)

    hm=heatmap3(cs3)

    sidebyside(hm,tl,'../CC_TRANSCRIPTS3')

    print ('\nEnd  processing: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

