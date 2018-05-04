#!/usr/bin/env python
# coding: utf-8
# from __future__ import print_function

__source__ = 'cc_create_traing.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Preliminary Development"

#
# Creates for a given caseID, a dictionary that associates a complete utterance with a tag label set.
#
import xlrd

import collections

import re


def parseTag(x):
    r = re.sub('\\\\', '', x)
    s = r.split(':')
    sl = []
    sl.append('00:' + ':'.join(s[1:3]) + ',000')
    sl.append('00:' + ':'.join(s[3:5]) + ',000')
    return sl

def parseIndex(y):
    yl = y.split(' --> ')

    return yl

def parseSegments(left,right):
    leftl = left.split(' --> ')
    rightl = right.split(' --> ')
    segmentl=[leftl[0],rightl[1]]
    return segmentl


def isIntersect(x,y):
    print
    print "Comparing:", x, y
    if x[0] <= y[1] and x[1]  >= y[0]:
        return True
    else:
        return False


def searchTags(tag_dict,caseId, segment):
    tag_list=[]
    print
    print "searchTags: ", "caseId: ", caseId, "segment: ", segment
    for t in tag_dict[caseId]:
        print
        print "caseID: ",caseId, "tagSegment: ",t[0], "tag: ", t[1]
        if isIntersect(t[0],segment):
            print "Positive intersection: ",t[1]
            tag_list.append(t[1])
        else:
            print "No intersection"

    return tag_list

#Read TAG spreadsheet#####################

def readTagXLS(xls_pathname):

    wb = xlrd.open_workbook(xls_pathname)

    print wb.sheet_names()

    # Get a sheet either by index or by name
    sh = wb.sheet_by_index(2)

    # Case ID (first column):
    first_column = sh.col_values(0)

    # VideoSegment (second column):
    second_column = sh.col_values(1)

    #Tag (fourth column):
    fourth_column = sh.col_values(3)

    tag_dict=collections.OrderedDict()

    for x,y,z in zip(first_column,second_column, fourth_column):
        try:
            if not y:
                y="Blank:00\\:00:00\\:00:False"

            if not int(x) in tag_dict.keys():
                tag_dict[int(x)] = []
            tag_dict[int(x)].append([parseTag(y.encode()), z])

        except:
            print "error",x
            pass

    print
    for x in tag_dict.keys():
        print
        for y in tag_dict[x]:
            print x, y[0],y[1]
    return tag_dict


#Read CC File#############################

def processCCFile(tag_dict, caseId, cc_pathname):

    fi = open(cc_pathname, 'r')
    text=fi.read()

    combined=''
    dashflag=1
    segmentStarted=0
    startSegment='init'
    #endSegment='init'
    videoSegment='00:00:00,000 --> 00:00:00,000'
    segmentId='0'
    pre_videoSegment = ''
    pre_segmentId = ''
    training_list=[]

    # Loop  thru cc file
    for x in text.splitlines():
        if not x:
            continue
        if x[:2].isdigit():
            dashflag=0
            if ':' in x:
                pre_videoSegment=videoSegment

                if segmentStarted==0:
                    startSegment=pre_videoSegment
                    segmentStarted=1

                videoSegment=x
                print "VideoSegment: ", pre_videoSegment

            else:
                pre_segmentId=segmentId
                segmentId=x
                print "Segment Id:", pre_segmentId


        if not x[:2].isdigit() and x:

            if x[0] == '-':

                if dashflag==1:
                    combined += ' ' + x
                else:
                    dashflag = 1
                    print
                    print combined
                    endSegment=pre_videoSegment
                    segmentStarted=0
                    print
                    sl=parseSegments(startSegment, endSegment)
                    tl=searchTags(tag_dict, caseId, sl)
                    training_list.append([pre_segmentId,combined,tl])
                    print
                    print "=================="
                    print
                    combined = x

            else:
                dashflag = 0
                combined += ' '+ x
    print
    print combined
    print
    endSegment = pre_videoSegment
    sl=parseSegments(startSegment,endSegment)
    tl=searchTags(tag_dict, caseId, sl)
    training_list.append([segmentId, combined, tl])
    print
    print "=================="
    print

    fi.close()
    return training_list

#########################################################

def main(indir,outfile,xls_pathname,sourcefile):

    print
    print 'indir:',indir
    print 'outfile:',outfile
    print 'xls_pathname',xls_pathname
    print 'sourcefile:',sourcefile
    print

    import json

    tag_dict=readTagXLS(xls_pathname)

    fo = open(outfile, 'w')


    #fileList=["Copy of 001 ENLEAYA001.srt","Copy of 002 MATH AYA 002 edited.srt"]
    #caseIdList=[1,2]


    #########################################################
    with open(sourcefile) as json_file:
        source = json.load(json_file)


    #for infile, caseId in zip(fileList,caseIdList):
    for data_item in source['data']:
        #print data_item['infile'], data_item['caseID']

        cc_pathname=indir+'/'+ data_item['infile']

        training_list=processCCFile(tag_dict, data_item['caseID'], cc_pathname)

        for item in training_list:
            s = '{};{};{}\n'.format(item[0], item[1][2:], item[2]) # strip out leading dash
            print (s)

            fo.write(s)


if __name__ == "__main__":
    main(indir='../CC_FILES',
         outfile="cc_training_set.txt",
         xls_pathname='../CC_FILES_TAGLIST/TW Case List.xlsx',
         sourcefile='cc_training_source.json')


