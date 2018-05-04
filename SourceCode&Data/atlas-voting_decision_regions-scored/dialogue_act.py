#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "dialogue_act.py"
__author__ = "Frank J. Greco"
__copyright__ = ""
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "Development"

#
# Identify speech acts across a moving set of sentence/utterance frames.
#
# input: transcript file(s)
#
# output: Speech act component vector normalized by total speech act count for a transcripts
#
# See the read_text function for the template of possible speech acts
#
#
import nltk

import datetime
import json
import re
import nltk
import sys
import frame_stack as fs

from collections import Counter


#print (posts[0:10])

def dialogue_act_features(post):
     features = {}
     for word in nltk.word_tokenize(post):
         features['contains({})'.format(word.lower())] = True
     return features

print ("Create Speech Act Classifier")
posts = nltk.corpus.nps_chat.xml_posts()[:10000]
featuresets = [(dialogue_act_features(post.text), post.get('class'))
                for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print ("Accuracy")
print(nltk.classify.accuracy(classifier, test_set))

#reload(sys)
#sys.setdefaultencoding('utf8')

def split_into_sentences(text):

    sent_text = nltk.sent_tokenize(text)  # this yields a list of sentences
    return sent_text

def read_text(text, frame_size):
    speech_acts = []

    speech_acts_template={
        "nAnswer": 0.0,
        "ynQuestion": 0.0,
        "yAnswer": 0.0,
        "whQuestion": 0.0,
        "System": 0.0,
        "Accept": 0.0,
        "Clarify": 0.0,
        "Emphasis": 0.0,
        "Other": 0.0,
        "Statement": 0.0,
        "Reject": 0.0,
        "Continuer":0.0,
        "Bye":0.0,
        "Greet":0.0,
        "Emotion":0.0
        }

    count = 0
    ucount = 0

    speech_act_count=0

    speech_acts_dict=speech_acts_template

    sx = fs.FrameStack(frame_size)


    ulist = [line for line in text.split('\n')]

    fulllist = []

    for utterance in ulist:
        slist=[]
        slist = slist + split_into_sentences(utterance)

        ucount += 1
        ###print ("\n##### Utterance Number {} #####".format(ucount))

        exceptions = []

        for item in slist:

            sx.limit_push(item)
            group = sx.long_peek(frame_size)

            try:
                count += 1
                act=classifier.classify(dialogue_act_features(group))
                ###print()
                ###print(count, ":", group)

            except Exception as e:

                sx.undo_limit_push()

                if hasattr(e, 'message'):
                    exceptions.append(e.message)
                else:
                    exceptions.append(e)
                pass

            else:
                fulllist.append(group)
                #print("speech act:", act)
                if act in speech_acts_dict.keys():
                    speech_acts_dict[act] += 1
                    speech_act_count += 1
                else:
                    print ("Ignoring:{}".format(act))

        if len(exceptions) > 0 :print("Exceptions:",exceptions)

    return speech_acts_dict,speech_act_count,ucount,fulllist



def speech_act_vector(text):
    speech_act_dict,total_speech_act_count, ucount, fulllist = read_text(text, 1)

    for key in speech_act_dict:
        if total_speech_act_count > 0:
            speech_act_dict[key]= float(speech_act_dict[key])/total_speech_act_count

    return speech_act_dict


if __name__ == '__main__':

    print ('Start processing: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    text_dict_file = 'text_dict5.json'

    with open(text_dict_file) as data_file:
        text_dict = json.load(data_file)

    for key in text_dict.keys()[0:5]:

        sac = speech_act_vector(text_dict[key]['text'])


        x=[sac[key] for key in sac.keys()]

        print (x)


    print ('End  processing: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

