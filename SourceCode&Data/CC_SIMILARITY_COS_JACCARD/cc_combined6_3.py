#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__doc__="""
Added jaccard similarity function
Settable list of tags and list of document numbers
doc0 set to 0 set to a given input file
Compute cosine similarity between all pairs of documents that share a given tag or is doc 0, and cos_sim of corresponding (tag set pairs)
Graph cos_sim(target doc, doc_no) vs doc no  and  cos_sim(tag label set(target doc), tagset(doc_no)) vs doc_no for each target tag / target doc graph pair
Graph corresponding cos(doc(x)) vs cos(tagset(x))
Output directory set to ..SIMILARITY_PLOTS/CC_PLOTS6_2
Computes mean and variance of cosine similarity for each target document/target tag graph pair.
Produces cc_statlog6_2_{start time}.csv & console log
"""

print(__doc__)

__source__ = 'cc_combined6_3.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"


import os
import sys
import collections

import re

import logging
import datetime

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row
from bokeh.io import save
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label

import statistics

from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr

import numpy as numpy

import pandas as pd

from cc_metrics import calculate_similarities

from preprocess import create_tag_dict
from preprocess import create_tag_sub_dict
from preprocess import create_text_dict_l

from bkcharts import HeatMap, show, output_file
from bokeh.palettes import RdGy11 as palette  # @UnresolvedImport
from bokeh.models import HoverTool
from bokeh.models import CrosshairTool

#
# Plot Results
#
def heatmap3(c3,title="Cosine Similarity",output_filename='cossim_heatmap.html'):


    crosshair = CrosshairTool()

    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("(x,y)", "(@x,@y)"),
        ("score", "@values")
    ])

    score = []

    nba = pd.DataFrame(c3)

    for x in nba.apply(tuple):
        score.extend(x)

    #print("\nscore({}):{}".format(title,score))

    data = {
        'transcript-x': list(nba.index) * len(nba.columns),
        'transcript-y': [item for item in list(nba.columns) for i in range(len(nba.index))],
        'score': score
    }

    output_file(output_filename)

    hm = HeatMap(data, x='transcript-x', y='transcript-y', values='score', title=title, stat=None, tools=[hover,crosshair], palette=palette)

    #show(hm)
    return hm

def heatmap4(title="Test pattern",output_filename='test_heatmap2.html'):

    crosshair = CrosshairTool()

    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("(x,y)", "(@x,@y)"),
        ("score", "@values")
    ])

    score = []

    c3=[[1,0,0],[0,1,0],[0,0,1]]

    nba = pd.DataFrame(c3)

    for x in nba.apply(tuple):
        score.extend(x)

    #print("\nscore({}):{}".format(title,score))

    data = {
        'Index': list(nba.index) * len(nba.columns),
        'Cosine': [item for item in list(nba.columns) for i in range(len(nba.index))],
        'score': score
    }

    output_file(output_filename)
    hm = HeatMap(data, x='Index', y='Cosine', values='score', title=title, stat=None, tools=[hover,crosshair], palette=palette)

    #show(hm)
    return hm

#
# Stat Results
#
def stat_results(doc_ids,
                 doc_no,
                 target_tag,
                 cosine_scores_text,
                 cosine_scores_tags,
                 jaccard_scores_text,
                 jaccard_scores_tags,
                 statlog,
                 cos_means,
                 jaccard_means):


    print("doc_no:", doc_no)
    doc_key = doc_ids[doc_no]
    print("doc_key:", doc_key)

    # Plot p1
    x1 = range(len(doc_ids))
    y1 = cosine_scores_text[doc_no]

    x2 = range(len(doc_ids))
    # y2 = cosine_scores_tags[doc_no]
    y2 = jaccard_scores_tags[doc_no]

    # Plot p2
    x3 = cosine_scores_text[doc_no]
    y3 = jaccard_scores_text[doc_no]

    # Plot p3
    x4 = doc_ids
    y4 = jaccard_scores_text[doc_no]

    a = []

    index = 0

    for item in y1:
        index += 1
        if index != doc_no + 1:
            a.append(item)

    statlog.write(','.join(['doc-' + str(doc_key), target_tag, str(statistics.mean(a)), str(statistics.variance(a))]))

    cos_means[target_tag].append(statistics.mean(a))

    a2 = []
    index = 0

    for item in y4:
        index += 1
        if index != doc_no + 1:
            a2.append(item)

    statlog.write(',')

    statlog.write(','.join([str(statistics.mean(a2)), str(statistics.variance(a2))]))

    jaccard_means[target_tag].append(statistics.mean(a2))

    try:
        pearson=pearsonr(x3, y2)
        spearman=spearmanr(x3, y2)
        print("Pearsonr Result: ", pearson)
        print(spearman)
        statlog.write(','.join(["pearson:", str(pearson[0]), str(pearson[1]), str(spearmanr(x3, y2))]))

    except:
        print("Error Summary Stats(1)", sys.exc_info())
        pass

    try:
        print("Correlation Coefficients:\n", numpy.corrcoef(x3, y3))
    except:
        print("Error: correlation coefficients:", sys.exc_info())
        pass

    statlog.write('\n')

    return

#
# Plot Results
#
def plot_results(doc_ids,
                 doc_no,
                 target_tag,
                 cosine_scores_text,
                 cosine_scores_tags,
                 jaccard_scores_text,
                 jaccard_scores_tags,
                 plot_dir):

    print("doc_no:",doc_no)
    doc_key=doc_ids[doc_no]
    print("doc_key:",doc_key)

    # Plot p1
    x1 = range(len(doc_ids)) #doc_ids
    y1 = cosine_scores_text[doc_no]

    x2 = range(len(doc_ids)) #doc_ids
    #y2 = cosine_scores_tags[doc_no]
    y2 = jaccard_scores_tags[doc_no]

    # Plot p2
    x3 = cosine_scores_text[doc_no]
    y3 = jaccard_scores_text[doc_no]

    # Plot p3
    x4 = range(len(doc_ids)) #doc_ids
    y4 = jaccard_scores_tags[doc_no]

    #########################################
    # create  plot 1
    #########################################
    a=[]

    index=0

    for item in y1:
        index += 1
        if index != doc_no+1:
            a.append(item)

    stats= "n: " + str(len(a)) + " mean: " + str(statistics.mean(a)) +  ' variance: ' + str(statistics.variance(a))

    citation = Label(x=100, y=400, x_units='screen', y_units='screen',
                     text=stats, render_mode='css',
                     border_line_color='black', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0)

    p1 = figure(title="Cosine Similarity between Doc Index: " + str(doc_no)+' CaseId: '+ str(doc_key) + " and each case tagged with:" + target_tag,
                x_axis_label='Doc Index', y_axis_label='Cosine(Blue)/Jaccard(Red)')

    p1.add_layout(citation)

    p1.circle(x1, y1, color="blue", size=5, legend="text")

    p1.circle(x2, y2, color="red", size=2, legend="tags")

    #########################################
    # create  plot 2
    #########################################

    p2 = figure(title="COS similarity vs Jaccard similarity; CaseId " + str(doc_key), x_axis_label='COS metric', y_axis_label='Jaccard metric')

    p2.circle(x3, y3, color="green")

    #########################################
    # create  plot 3
    #########################################

    a3=[]
    index=0

    for item in y4:
        index += 1
        if index != doc_no+1:
            a3.append(item)

    stats3= "n: " + str(len(a3)) + " mean: " + str(statistics.mean(a3)) +  ' variance: ' + str(statistics.variance(a3))

    citation = Label(x=100, y=400, x_units='screen', y_units='screen',
                     text=stats3, render_mode='css',
                     border_line_color='black', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0)


    p3 = figure(title="Jaccard similarity between Doc Index: " + str(doc_no)+' CaseId: '+ str(doc_key) + " and each case tagged with:" + target_tag,
                x_axis_label='Case ID', y_axis_label='Jaccard Metric')
    p3.add_layout(citation)

    p3.circle(x4, y4, color="blue")

    ##########################################################################
    # output to HTML file
    ##########################################################################
    output_file(plot_dir+"/cc_cluster_"+target_tag+"_doc_"+str(doc_key)+".html")

    save(row(p1,p2,p3))

    return

def main():

    global transcript_dir

    cos_means = dict()

    jaccard_means = dict()

    statlog = open(statlog_filename, 'w')
    statlog.write(','.join(
        ['doc_key', 'target_tag', 'cs-mean', 'cs-variance', "js_mean", "js_variance"]))
    statlog.write('\n')

    tag_dict=create_tag_dict(xls_pathname,s=True,v=True)


    #
    # Analyze tags and text
    #

    for target_tag in target_tags:

        cos_means[target_tag]=[]

        jaccard_means[target_tag]=[]

        tag_sub_dict = create_tag_sub_dict(tag_dict, target_tag)

        train_sub_dict= create_text_dict_l(transcript_dir, tag_sub_dict=tag_sub_dict)

        tag_train_set=[]

        text_train_set=[]

        for x in train_sub_dict.keys():
            tag_train_set.append(train_sub_dict[x][1])
            text_train_set.append(train_sub_dict[x][0])

        #print ('\ntag_train_set',tag_train_set)
        #print('\ntext_train_set', text_train_set)

        print ("\nCalculate tag_train_set similarities:")
        cosine_scores_tags, jaccard_scores_tags = calculate_similarities(tag_train_set)

        print("\nCalculate text_train_set similarities:")
        cosine_scores_text, jaccard_scores_text = calculate_similarities(text_train_set)


        heatmap_fn='heatmap_'+target_tag+'.html'

        h1=heatmap3(cosine_scores_text,title='cosine_scores_text: '+ target_tag)

        h2=heatmap3(jaccard_scores_tags,title='jaccard_scores_tags: '+ target_tag)

        #h3=heatmap4()

        save(row(h1,h2))

        #save(row(h3))

        print("\ndoc_ids:",train_sub_dict.keys())

        for doc_no in range(len(train_sub_dict.keys())):

            print('\nmain: doc_no:', doc_no, 'target_tag', target_tag)

            try:

                stat_results(train_sub_dict.keys(),
                             doc_no,
                             target_tag,
                             cosine_scores_text,
                             cosine_scores_tags,
                             jaccard_scores_text,
                             jaccard_scores_tags,
                             statlog,
                             cos_means,
                             jaccard_means)

            except:
                print("main: stat_results error:", "target_tag", target_tag, "doc_no", doc_no,sys.exc_info())
                pass


            try:

                plot_results(train_sub_dict.keys(),
                             doc_no,
                             target_tag,
                             cosine_scores_text,
                             cosine_scores_tags,
                             jaccard_scores_text,
                             jaccard_scores_tags,
                             plot_dir)

            except:
                print("main: plot_results error:", "target_tag", target_tag, "doc_no", doc_no,sys.exc_info())
                pass

    #
    # Test for correlation
    #
    sim_js=[]

    sim_cs=[]

    for item in sorted(cos_means.keys()):
        try:
            statlog.write(','.join(["Target tag:",item, "n:",str(len(cos_means[item]))]))
            statlog.write(',')
            mean_cos_means=statistics.mean(cos_means[item])
            statlog.write(
                ','.join(["Mean of Cosine Similarity means:  ", str(mean_cos_means), ' variance: ',
                             str(statistics.variance(cos_means[item]))]))
            statlog.write(',')
            mean_jaccard_means=statistics.mean(jaccard_means[item])
            statlog.write(
                ','.join(["Mean of Jaccard Similarity means: ", str(mean_jaccard_means), ' variance: ',
                          str(statistics.variance(jaccard_means[item]))]))

            statlog.write('\n')
            sim_cs.append(mean_cos_means)
            sim_js.append(mean_jaccard_means)

        except:
            print ("main:", "error printing summary stats", "item:", item, sys.exc_info())
            statlog.write('\n')
            pass

    #
    # Print Correlation Statistics for full run
    #
    if (len(sim_cs)>1):

        print ("\nsim_cs:",sim_cs)
        statlog.write(','.join(["sim_cs:",str(sim_cs)]))
        statlog.write('\n')

        print("\nsim_js",sim_js)
        statlog.write(','.join(["sim_js:", str(sim_js)]))
        statlog.write('\n')

        print  ("\nPearsonr RESULT: ", pearsonr(sim_cs, sim_js))
        statlog.write(','.join(["Pearsonr RESULT:", str(pearsonr(sim_cs, sim_js))]))
        statlog.write('\n')

        print ("\nSpearmanr RESULT:",spearmanr(sim_cs, sim_js))
        statlog.write(','.join(["Spearmanr RESULT:",str(spearmanr(sim_cs, sim_js))]))
        statlog.write('\n')

        print ("\nCorrelation Coefficients\n",numpy.corrcoef(sim_cs, sim_js))


    et = 'End time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    print (et)

    statlog.close()

if __name__ == "__main__":

    st = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    print("cc_combined6_3: Start time:", st)

    statlog_filename = "../SIMILARITY_PLOTS/cc_combined6_3_statlog_" + st + '.csv'
    print ('statlog:',statlog_filename)

    xls_pathname = '../CC_FILES_TAGLIST/TW Case List.xlsx'
    print ('Case List',xls_pathname)

    transcript_dir = '../CC_TRANSCRIPTS3'
    print ('transcript_dir',transcript_dir)

    #target_tags = ['TW01', 'TW02', 'TW03', 'TW04', 'TW05', 'TW06', 'TW07', 'TW08', 'TW09', 'TW10', 'TW11', 'TW12',
    # 'TW13', 'TW14', 'TW15', 'TW16', 'TW17', 'TW18', 'TW19', 'TW20', 'TW21', 'TW22', 'TW23', 'TW24']
    #target_tags = ['all']
    target_tags = ['TW04']
    print ("target tags:", target_tags)

    plot_dir = '../SIMILARITY_PLOTS/CC_PLOTS6_3_'+st
    print ("plot_dir",plot_dir)

    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    main()
