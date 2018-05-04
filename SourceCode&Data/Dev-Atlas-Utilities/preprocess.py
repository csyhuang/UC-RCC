#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "preprocess.py"
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

import xlrd
import collections
import os
import re
import json
import pickle

#
# create_tag_dict
#
#def preprocess_worksheet(xls_pathname,s=True,v=True):
def create_tag_dict(xls_pathname,s=True,v=True):

    print("\n*** Begin process_worksheet ***\n")

    wb = xlrd.open_workbook(xls_pathname)

    print (wb.sheet_names())

    # sheet index
    sh = wb.sheet_by_index(2)

    # case id (first) column:
    first_column = sh.col_values(0)

    # tags (fourth) column:
    fourth_column = sh.col_values(3)

    tag_dict=collections.OrderedDict()

    tag_dict[0]=['NaN']

    for x, y in zip(first_column, fourth_column)[1:]: # [1:] skips past the header

        try:
            if int(x) in tag_dict.keys():
                tag_dict[int(x)].append(y)
            else:
                tag_dict[int(x)]=[y]
        except:
            print ("error: create_tag_dict:",x)
            pass

    if (s):
        print("Sort Tag Dictionary")
        for x in tag_dict.keys():
            print(x, sorted(set(tag_dict[x])))
            tag_dict[x] = sorted(set(tag_dict[x]))

    if (v):

        print("\ncreate_tag_dict: len(tag_dict.keys()):{}".format(len(tag_dict.keys())))

        for x in tag_dict.keys():
            print (x, ','.join(tag_dict[x]))


    print("\n*** End process_worksheet ***\n")

    return tag_dict

#
# create_tag_sub_dict
#
#def analyze_tags(tag_dict, target_tag):
def create_tag_sub_dict(tag_dict, target_tag):

    tag_sub_dict=collections.OrderedDict()

    for x in tag_dict.keys():

        if target_tag =='all':

            try:
                tag_sub_dict[x]=' '.join(tag_dict[x])

            except:
                print ("error: create_tag_sub_dict:",target_tag)
                pass

        elif target_tag in tag_dict[x]:

            try:
                tag_sub_dict[x]=' '.join(tag_dict[x])

            except:
                print ("error: create_tag_sub_dict:",target_tag)
                pass

    print ("create_tag_sub_dict: len(tag_sub_dict)",len(tag_sub_dict))

    print(tag_sub_dict.keys())

    return tag_sub_dict

#
# create_text_dict
#
#def analyze_text(transcript_dir, tag_sub_dict=''):
def create_text_dict_l(transcript_dir, tag_sub_dict=''):

    def addtodict(key, d, t1, t2):

        if key in d.keys():

            d[key][0] = d[key][0] + ',' + t1
        else:
            d[key] = [t1, t2]

    unsorted_text_dict=dict()

    for filename in os.listdir(transcript_dir):

        if filename.endswith(".txt"):

            name_tokens=filename.split()

            s = re.sub('[^0-9]+', ' ', name_tokens[2])

            infile = transcript_dir + '/' + filename
            fi = open(infile, 'r')
            doc = str.decode(fi.read(), "UTF-8", "ignore")
            fi.close()

            if int(s) in tag_sub_dict.keys():
                #train_dict[int(s)] = [doc,tag_sub_dict[int(s)]]
                addtodict(int(s),unsorted_text_dict,doc,tag_sub_dict[int(s)])

    print("create_text_dict_l: #keys:", len(unsorted_train_dict.keys()))

    text_sub_dict1 = collections.OrderedDict(sorted(unsorted_text_dict.items()))

    text_sub_dict = collections.OrderedDict()

    for key in text_sub_dict1.keys():
        text_sub_dict[str(key)]=text_sub_dict1[key]

    print (text_sub_dict.keys())

    return text_sub_dict


#
# create_text_dict_j
# Called by cc_extract_features_v2.py
#
def create_text_dict_j(transcript_dir, tag_dict):

    print ("\n*** Begin process_textfiles ***\n")

    #def addtodict(key, d, t1, t2, t3):
    #    if key in d.keys():
    #        d[key][0] = d[key][0] + ',' + t1
    #    else:
    #        d[key] = [t1, t2, t3]

    def addtodict(key, d, t1, t2, t3,fn):
        if key in d.keys():
            d[key]['text'] = d[key]['text'] + ',' + t1
            d[key]['filename'].append(filename)
        else:
            d[key] = {'text':t1, 'tags': t2,'annotations' : t3, 'filename':[fn]}

    text_dict = dict()

    num_doc = 0
    no_annotation = 0
    yes_annotation = 0

    print("\ncreate_text_dict_j: Create text_dict from transcipt files\n")

    for filename in os.listdir(transcript_dir):

        if filename.endswith(".txt"):

            name_tokens = filename.split()

            s = re.sub('[^0-9]+', ' ', name_tokens[2])

            infile = transcript_dir + '/' + filename

            fi = open(infile, 'r')
            doc = str.decode(fi.read(), "UTF-8", "ignore")
            fi.close()

            clean_doc, fa = extract(doc)
            num_doc += 1

            ulist = doc.split('\n')
            fa2 = []
            annotation_vector = []
            for line in ulist:
                clean_doc2, fa2 = extract(line)
                if len(fa2) == 0:
                    fa2 = ['none']
                #print(line)
                #print(fa2)
                annotation_vector.append(fa2)
            print(annotation_vector)
            print(len(ulist), len(annotation_vector))


            if len(fa) == 0:
                no_annotation += 1
            else:
                yes_annotation += 1

            print ("filename:", filename, "adding caseID: ", s)

            addtodict(s, text_dict, clean_doc, tag_dict[int(s)], annotation_vector, filename) #saving s as string instead of int(s)

    print ("\ncreate_text_dict_j: Created text_dict from transcipt files\n")

    print ('no_annotation: {0}, yes_annotation: {1}, num_doc: {2}'.format(no_annotation, yes_annotation, num_doc))

    print ("\n*** End create_text_dict_j ***\n")

    return text_dict


#
# create_doc_index
#
def create_doc_index(transcript_dir):

    documents = []

    doc_index = []

    index = 0

    for filename in os.listdir(transcript_dir):

        try:

            if filename.endswith(".txt"):
                name_tokens = filename.split()

                s = re.sub('[^0-9]+', ' ', name_tokens[2])

                infile = transcript_dir + '/' + filename
                fi = open(infile, 'r')
                documents.append(str.decode(fi.read(), "UTF-8", "ignore"))
                doc_index.append((index, s, filename))
                index += 1
                fi.close()
        except:
            print("Error: preprocess: create_doc_index: filename: {}".format(filename))

    return documents, doc_index

#
# create_train_set
# Called by DictionaryVectorization.ipynb
#
def create_train_set(transcript_dir):
    ordered_train_set=[]
    doc_names=[]
    name_tokens=[]
    doc_ids=[]

    unordered_train_dict=dict()


    for filename in os.listdir(transcript_dir):
        if filename.endswith(".txt"):

            try:
                name_tokens=filename.split()

                infile = transcript_dir + '/' + filename
                fi = open(infile, 'r')
                doc = str.decode(fi.read(), "UTF-8", "ignore")

                #doc_ids.append(int(name_tokens[2]))
                #print "===>", filename
                #doc_names.append(name_tokens[3:])
                #train_set.append(doc)

                unordered_train_dict[int(name_tokens[2])]=doc

            except:
                pass

    ordered_train_dict = collections.OrderedDict(sorted(train_dict.items()))
    for x in ordered_train_dict.keys():
        train_set.append(ordered_train_dict[x])
    return ordered_train_set, ordered_train_dict


#
# create_title_list
#
def create_title_list(transcript_dir):
    titles= []
    docs = []
    for filename in os.listdir(transcript_dir):

        if filename.endswith(".txt"):

            name_tokens = filename.split()

            s = re.sub('[^0-9]+', ' ', name_tokens[2])

            fi = open(transcript_dir+filename, 'r')

            doc = str.decode(fi.read(), "UTF-8", "ignore")

            titles.append(filename)

            docs.append(doc)

    return titles,docs

#
# find_case
#
def find_case(caseID,transcript_dir='.'):
    transcripts=[]
    for filename in os.listdir(transcript_dir):

        if filename.endswith(".txt"):

            name_tokens = filename.split()

            s = re.sub('[^0-9]+', ' ', name_tokens[2])
            #print (s)

            if caseID in s:
                transcripts.append(filename)
    return transcripts

#
# process transcriber annotation
#
def find_annotations(s):
    return re.findall(r"\[([A-Za-z0-9_]+)\]", s)


def find_annotations2(s):
    return re.findall(r"\((\w+)\)", s)


def del_annotations(s):
    return re.sub("[\(\[].*?[\)\]]", "", s)

def extract(doc):

    fa = find_annotations(doc)
    clean_doc = del_annotations(doc)

    return clean_doc, fa

#
# create_annotation_vector
# Called by extract_annotations.py
#

def create_annotation_vector(infile):
    fi = open(infile, 'r')
    doc = str.decode(fi.read(), "UTF-8", "ignore")
    fi.close()

    # clean_doc, fa = extract(doc)
    # print (fa)

    # ulist = [line.rstrip('\n') for line in open(infile)]
    ulist = doc.split('\n')
    fa2 = []
    annotation_vector = []
    for line in ulist:
        clean_doc, fa2 = extract(line)
        if len(fa2) == 0:
            fa2 = ['NaN']
        print (line)
        print (fa2)
        annotation_vector.append(fa2)
    print (annotation_vector)
    return ulist, annotation_vector



#
# create_text_dict_annotation
# Called by cc_find_annotations.ipynb
#
def create_text_dict_annotation(transcript_dir, tag_dict):
    print("\n*** Begin process_textfiles ***\n")

    def addtodict(key, d, t1, t2):
        if key in d.keys():
            d[key][0] = d[key][0] + ',' + t1
        else:
            d[key] = [t1, t2]

    text_dict = dict()

    num_doc = 0
    no_annotation = 0
    yes_annotation = 0

    for filename in os.listdir(transcript_dir):

        if filename.endswith(".txt"):

            name_tokens = filename.split()

            s = re.sub('[^0-9]+', ' ', name_tokens[2])

            infile = transcript_dir + '/' + filename
            fi = open(infile, 'r')
            doc = str.decode(fi.read(), "UTF-8", "ignore")

            fa = find_annotations(doc)

            clean_doc = del_annotations(doc)

            num_doc += 1

            if len(fa) == 0:
                no_annotation += 1
            else:
                yes_annotation += 1

            # print ("\n\n",filename,"\n",fa)

            fi.close()

            # text_dict[int(s)] = [doc,tag_sub_dict[int(s)]]
            addtodict(int(s), text_dict, clean_doc, tag_dict[int(s)])

    print("\nCreated text_dict from transcript files\n")

    print('no_annotation: {0}, yes_annotation: {1}, num_doc: {2}'.format(no_annotation, yes_annotation, num_doc))

    print("\n*** End process_textfiles ***\n")

    return text_dict


#
# Tag_Worksheet
# Called by topicClassificatinLSIv1.py; lsi001.ipynb
#
class TagWorksheet:
    tag_dict = collections.OrderedDict()
    xls_pathname=''
    wb=''
    def __init__(self,xls_pathname):
        self.xls_pathname = xls_pathname
        self.tag_dict=create_tag_dict(self.xls_pathname)
    def get_tags(self,key):
        return self.tag_dict[key]

#
# Called by create_indices.py in Vectorization&WordEmbedding
#
class TranscriptIndex:
    index_dict = dict()
    transcript_dir=' '
    num_doc = 0

    def __init__(self,transcript_dir = '../CC_TRANSCRIPTS3'):
        self.transcript_dir=transcript_dir

    def create_index(self):

        def addtodict(key, d, t1):
            if key in d.keys():
                d[key][0] = d[key][0] + ',' + t1
            else:
                d[key] = [t1]

        print("\nTranscriptIndex: create_index: Create filename index from transcript ...\n")

        for filename in os.listdir(self.transcript_dir):

            if filename.endswith(".txt"):

                name_tokens = filename.split()

                s = re.sub('[^0-9]+', ' ', name_tokens[2])

                self.num_doc += 1

                print (filename)

                addtodict(int(s), self.index_dict, filename)


        print ('num_doc: {}'.format(self.num_doc))

        print("\nCreated index of transcript files\n")

        return self.index_dict

    def get_filename(self,key):
        return self.index_dict[key]

    def get_keys(self,filename):
        key_list=[]
        for key in self.index_dict.keys():
            if filename in self.index_dict[key]:
                key_list.append(key)
        return key_list

    def make_pickle(self,filename="index_dict3.p"):
        pickle.dump(self.index_dict, open(filename, "wb"))
        return pickle

    def use_pickle(self,filename="index_dict3.p"):
        self.index_dict = pickle.load(open(filename, "rb"))
        return

#
# Called by test_transcript_parser in ParseTranscript
# Called by wordembedding-Atlas2.ipynb in WordEmedding
#
#
class ParsedTranscript:

    indir=''

    filename = ''

    fullpath = indir + '/' + filename

    raw_transcript=[]

    words=[]

    word2int = {}

    int2word = {}

    vocab_size=0

    raw_sentences=[]

    sentences = []
    tokenized_sentences=[]

    def __init__(self,filename,indir='.'):
        self.indir=indir
        self.filename=filename
        return

    def read_file(self):

        self.fullpath=self.indir+'/'+self.filename

        self.raw_transcript = [line.rstrip('\n').lower() for line in open(self.fullpath)]

        for utterance in self.raw_transcript:
            for word in utterance.split():
                if word != '.':        # because we don't want to treat . as a word
                    word=word.replace(",", "")
                    word=word.replace(".", "")
                    word=word.replace("?", "")
                    word=word.replace("!", "")
                    self.words.append(word)

        self.words = set(self.words) # so that all duplicate words are removed

        self.vocab_size = len(self.words) # gives the total number of unique words


        for i,word in enumerate(self.words):
            self.word2int[word] = i
            self.int2word[i] = word


        # raw sentences is a list of sentences.
        for utterance in self.raw_transcript:
            self.raw_sentences.append(re.split('[,.!?]', utterance))

            for sentence in self.raw_sentences[-1]:
                if len(sentence) > 0:
                    self.sentences.append(sentence)
                    self.tokenized_sentences.append(sentence.split())

    def get_raw_transcript(self):
        return self.raw_transcript

    def get_raw_sentences(self):
        return self.raw_sentences

    def get_sentences(self):
        return self.sentences

    def get_tokenized_sentences(self):
        return self.tokenized_sentences

    def get_words(self):
        return self.words

    def get_filename(self):
        return self.filename

    def get_word2int(self,word):
        return self.word2int[word]

    def get_int2word(self,value):
        return self.word2int[value]


    def print_parms(self):

        print ('fullpath:',self.fullpath)
        print('len raw_transcript:', len(self.raw_transcript))
        print ("vocab_size:", self.vocab_size)
        print("word2int['us']:",self.word2int['us'])
        print("int2word[2]:",self.int2word[2])
        print ('len(sentences:',len(self.sentences))
        print('sentences[0:20]:',self.sentences[0:20])
