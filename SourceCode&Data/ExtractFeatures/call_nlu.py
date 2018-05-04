#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = 'call_nlu.py'
__author__ = "Frank J. Greco"
"""
/**
 * Copyright 2017 IBM Corp. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License'); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
 """
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "Example"

def call_nlu(text_dict):
    import sys
    from watson_developer_cloud import NaturalLanguageUnderstandingV1
    from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions

    credentials = {
    "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
    "username": "supply username",
    "password": "supply password"
    }

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username=credentials["username"],
        password=credentials["password"],
        version="2017-02-27")

    for key in text_dict.keys():
        try:
            response = natural_language_understanding.analyze(
                text=text_dict[key]['text'],
                features=Features(
                    entities=EntitiesOptions(
                        sentiment=True,
                        limit=1),
                    sentiment=SentimentOptions())
            )

            nlu_features = [response['language'], response['sentiment']['document']['label'],
                            response['sentiment']['document']['score']]
            #text_dict[key].append(nlu_features)
            text_dict[key]['nlu']=nlu_features

            if response['language'] != 'en':
                print ("Non-english text:", response['language'])
                if key in text_dict.keys():
                    print ("Deleting Key:", key)
                    del text_dict[key]


        except:
            print ("error: key:", key)
            if key in text_dict:
                print ("Deleting Key:", key)
                del text_dict[key]
            print ("Unexpected error:", sys.exc_info())
            pass

    return text_dict